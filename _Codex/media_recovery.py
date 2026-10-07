"""Recover media-sync references from local assets and exact historical source URLs."""
from pathlib import Path
from collections import defaultdict, Counter
from urllib.parse import unquote, urlsplit
from datetime import datetime, timezone
import hashlib, json, re, subprocess, sys

WORK=Path(__file__).resolve().parent
ROOT=WORK.parent
STATE=WORK/'media-recovery'
STATE.mkdir(exist_ok=True)
EXCLUDED={'.git','.obsidian','.trash','_Codex'}
MEDIA=re.compile(r'_media-sync_resources/[^\s<>"\'\]\)|?#]+?\.(?:jpe?g|png|gif|webp|svg|pdf|mp3|mp4|wav|m4a|ogg)(?:\.md)?',re.I)
SOURCE_URL=re.compile(r'https?://[^\s<>"\]\)]+')
EXTS={'.jpg','.jpeg','.png','.gif','.webp','.svg','.pdf','.mp3','.mp4','.wav','.m4a','.ogg'}

def git(*args):
    return subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)

def old_text(revision,path):
    r=git('show',revision[:8]+':'+path)
    if r.returncode:
        rows=git('ls-tree','-r','-z',revision).stdout.split(b'\0')
        for row in rows:
            if b'\t' in row:
                head,name=row.split(b'\t',1)
                if name.decode('utf-8')==path:
                    r=git('cat-file','blob',head.decode().split()[-1]); break
    return r.stdout.decode('utf-8-sig') if r.returncode==0 else None

def source_for_line(line,historical):
    # Exact property roles and image labels identify the former URL, not a fuzzy title.
    prop=re.match(r'^([A-Za-z_][\w-]*):',line)
    if prop:
        for old in historical.splitlines():
            if old.startswith(prop[1]+':'):
                urls=SOURCE_URL.findall(old)
                if len(urls)==1: return urls[0].rstrip('\\')
    image=re.search(r'!\[([^\]]*)\]\(',line)
    if image:
        candidates=[]
        for old in historical.splitlines():
            if '!['+image[1]+'](' in old:
                m=re.search(r'!\['+re.escape(image[1])+r'\]\((https?://.*)\)',old)
                if m: candidates.append(m[1])
        if len(set(candidates))==1: return candidates[0]
    return None

def inventory():
    notes=[]; local=defaultdict(list); refs=defaultdict(list)
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(x in EXCLUDED for x in p.relative_to(ROOT).parts[:-1]): continue
        if p.suffix.lower() in EXTS: local[p.name.casefold()].append(p)
        if p.suffix.lower() not in {'.md','.canvas','.base'}: continue
        text=p.read_bytes().decode('utf-8-sig')
        if '_media-sync_resources' not in text: continue
        rel=p.relative_to(ROOT).as_posix(); notes.append(rel)
        for number,line in enumerate(text.splitlines(),1):
            for m in MEDIA.finditer(line): refs[m[0]].append({'note':rel,'line':number,'text':line})
    versions={}; records=[]
    for target,usages in sorted(refs.items()):
        exact=ROOT/unquote(target)
        matches=[exact] if exact.is_file() else local.get(Path(target).name.casefold(),[])
        by_hash={hashlib.sha256(p.read_bytes()).hexdigest():p for p in matches}
        record={'original_path':target,'references':usages,'local_candidates':[p.relative_to(ROOT).as_posix() for p in matches],'source_candidates':[]}
        if len(by_hash)==1: record['local_match']=next(iter(by_hash.values())).relative_to(ROOT).as_posix()
        elif len(by_hash)>1: record['status']='ambiguous_local_filename'
        if 'local_match' not in record:
            for use in usages:
                note=use['note']
                if note not in versions:
                    history=git('log','--all','--format=%H','--',note).stdout.decode().splitlines()
                    versions[note]=[]
                    for rev in history:
                        text=old_text(rev,note)
                        if text and 'https://' in text:
                            versions[note].append((rev,text))
                for rev,text in versions[note]:
                    url=source_for_line(use['text'],text)
                    if url:
                        candidate={'URL':url,'revision':rev,'note':note,'evidence':'same property or image label before media-sync rewrite'}
                        if candidate not in record['source_candidates']: record['source_candidates'].append(candidate)
                        break
        urls=list(dict.fromkeys(c['URL'] for c in record['source_candidates']))
        if len(urls)==1: record['source_URL']=urls[0]
        elif len(urls)>1: record['status']='conflicting_historical_sources'
        records.append(record)
    plan={'notes':notes,'assets':records,'stats':{'notes_affected':len(notes),'asset_paths':len(records),'reference_occurrences':sum(len(r['references']) for r in records),'local_matches':sum('local_match' in r for r in records),'recoverable_source_urls':sum('source_URL' in r for r in records),'unknown_source_paths':sum('source_URL' not in r and 'local_match' not in r for r in records),'unique_source_urls':len({r['source_URL'] for r in records if 'source_URL' in r})}}
    (STATE/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(plan['stats'],indent=2))
    print(json.dumps([{'path':r['original_path'],'local':r.get('local_match'),'URL':r.get('source_URL')} for r in records if '88455' in r['original_path']],indent=2))

if __name__=='__main__': inventory()
