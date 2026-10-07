"""Remove blank lines after Markdown headings, preserving all other bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, sys, zipfile

WORK=Path(__file__).resolve().parent
ROOT=WORK.parent
EXCLUDED={'.git','.obsidian','.trash','__pycache__'}

def trim(data):
    lines=data.decode('utf-8').splitlines(keepends=True)
    result=[]; removed=0; after_heading=False; fence=None; frontmatter=False
    for i,line in enumerate(lines):
        raw=line.rstrip('\r\n')
        clean=raw.lstrip('\ufeff') if i==0 else raw
        if i==0 and clean.strip()=='---': frontmatter=True; result.append(line); continue
        if frontmatter:
            result.append(line)
            if clean.strip() in {'---','...'}: frontmatter=False
            continue
        quoted=re.sub(r'^ {0,3}(?:> ?)+','',clean)
        blank=not quoted.strip()
        if after_heading and blank:
            removed+=1
            continue
        after_heading=False
        mark=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',quoted)
        if fence:
            result.append(line)
            if mark and mark[1][0]==fence[0] and len(mark[1])>=fence[1] and not mark[2].strip(): fence=None
            continue
        if mark:
            fence=(mark[1][0],len(mark[1])); result.append(line); continue
        heading=bool(re.match(r'^ {0,3}(?:\[![^\]]+\][-+]?\s*)?#{1,6}(?:[ \t]+|$)',quoted))
        # Setext headings have a nonempty text line followed by an underline.
        if re.match(r'^ {0,3}(?:=+|-+)[ \t]*$',quoted) and result:
            previous=re.sub(r'^ {0,3}(?:> ?)+','',result[-1].rstrip('\r\n'))
            if previous.strip() and not re.match(r'^\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|[-=]{3,}\s*$)',previous): heading=True
        result.append(line)
        after_heading=heading
    out=''.join(result).encode('utf-8')
    return out,removed

def main():
    originals={}; updates={}; records=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix.casefold()!='.md' or any(x in EXCLUDED for x in p.relative_to(ROOT).parts[:-1]): continue
        data=p.read_bytes(); out,count=trim(data)
        if not count: continue
        rel=p.relative_to(ROOT).as_posix()
        originals[rel]=data; updates[rel]=out
        assert trim(out)==(out,0),rel
        # Only complete blank lines were removed, never other content.
        assert [x for x in data.decode('utf-8').splitlines() if re.sub(r'^ {0,3}(?:> ?)+','',x).strip()]==[x for x in out.decode('utf-8').splitlines() if re.sub(r'^ {0,3}(?:> ?)+','',x).strip()],rel
        records.append({'path':rel,'blank_lines_removed':count,'before_sha256':hashlib.sha256(data).hexdigest(),'after_sha256':hashlib.sha256(out).hexdigest()})
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup=WORK/'backups'/('heading-spacing-before-'+stamp+'.zip')
    if updates:
        backup.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
            for rel,data in originals.items(): z.writestr(rel,data)
        with zipfile.ZipFile(backup) as z:
            assert z.testzip() is None
            for rel,data in originals.items(): assert z.read(rel)==data
        temporary=WORK/'heading-spacing-update.tmp'
        for rel,out in updates.items():
            p=(ROOT/rel).resolve(); assert p.is_relative_to(ROOT.resolve())
            assert p.read_bytes()==originals[rel], 'Concurrent edit: '+rel
            temporary.write_bytes(out); os.replace(temporary,p)
        for rel,out in updates.items(): assert (ROOT/rel).read_bytes()==out
    report={'files_changed':len(updates),'blank_lines_removed':sum(x['blank_lines_removed'] for x in records),'backup':str(backup) if updates else None,'files':records}
    (WORK/'heading-spacing-changes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))

if __name__=='__main__': main()
