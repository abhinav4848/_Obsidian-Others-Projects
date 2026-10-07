from audit import *
from lyt_cleanup import build as lyt_build, fm_body, fields, body_key
from andy_cleanup import build as andy_build, transform, trail, source_line
import sys, yaml, difflib

def hashes(base):
    return {p.relative_to(base).as_posix():digest(p) for p in files(base)}

def preservation():
    data={'references':{k:hashes(Path(v)) for k,v in CFG['reference_vaults'].items()},'other_files':{p.relative_to(ROOT).as_posix():digest(p) for p in files(ROOT) if p.relative_to(ROOT).parts[0] not in {CFG['lyt_folder'],'_Codex'} and not (p.relative_to(ROOT).parts[0]==CFG['andy_folder'] and p.suffix=='.md')}}
    (WORK/'preservation-baseline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def norm(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).strip().casefold()

def markdown_links(text):
    for m in re.finditer(r'(?<!!)\[([^\]\n]+)\]\(',text):
        start=m.end(); i=start; depth=1; angle=False
        while i<len(text) and depth:
            c=text[i]
            if c=='\\': i+=2; continue
            if c=='\n': break
            if c=='<': angle=True
            elif c=='>': angle=False
            elif not angle and c=='(': depth+=1
            elif not angle and c==')': depth-=1
            i+=1
        if depth: continue
        raw=text[start:i-1].strip()
        if raw.startswith('<') and '>' in raw: raw=raw[1:raw.index('>')]
        yield m.start(),raw

def links(state,scope):
    lookup={k.casefold():k for k in state}
    names=defaultdict(set)
    aliases=defaultdict(set)
    for rel,data in state.items():
        p=Path(rel); names[p.name.casefold()].add(rel)
        if p.suffix=='.md':
            names[p.stem.casefold()].add(rel)
            try:
                fm=fm_body(data.decode('utf-8-sig'))[0]
                props=fields(fm)
                if 'aliases' in props:
                    a=yaml.safe_load(props['aliases'])['aliases']
                    for name in a if isinstance(a,list) else [a]:
                        if name: aliases[str(name).casefold()].add(rel)
            except (yaml.YAMLError,UnicodeError,TypeError): pass
    def resolve(target,source):
        key=unquote(target).strip().replace('\\','/')
        if not key: return source
        if '://' in key or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',key): return None
        for c in [key,str(Path(source).parent / key).replace('\\','/')]:
            for ext in ['','.md']:
                if (c+ext).casefold() in lookup: return lookup[(c+ext).casefold()]
        # Path-qualified wiki links must match a real root or relative path.
        if '/' in key: return None
        matches=names.get(key.casefold(),set()) or aliases.get(key.casefold(),set())
        return next(iter(matches)) if len(matches)==1 else None
    records=[]
    for rel,data in state.items():
        if not rel.startswith(scope+'/') or Path(rel).suffix not in TEXT_EXT: continue
        text=data.decode('utf-8-sig')
        for m in re.finditer(r'\[\[([^\]\n]+)\]\]',text):
            raw=m[1].split('|')[0]; target,sep,anchor=raw.partition('#')
            if not raw or '{{' in raw or '://' in raw: continue
            actual=resolve(target,rel)
            status='resolved' if actual else 'missing_file'
            if actual and anchor and Path(actual).suffix=='.md':
                content=state[actual].decode('utf-8-sig')
                if anchor.startswith('^'):
                    if not re.search(r'(?:^|\s)\^'+re.escape(anchor[1:])+r'(?:\s|$)',content): status='missing_block'
                else:
                    heads=re.findall(r'(?m)^\s*(?:>\s*)*(?:\[![^\]]+\][-+]?\s*)?#{1,6}\s+(.+?)\s*$',content)
                    if norm(anchor) not in {norm(h) for h in heads}: status='missing_heading'
            records.append({'source':rel,'target':raw,'resolved_to':actual,'status':status,'line':text.count('\n',0,m.start())+1,'kind':'wiki'})
        for offset,raw in markdown_links(text):
            target,sep,anchor=raw.partition('#')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',raw) or raw.startswith('#'): continue
            # Ignore empty Markdown placeholders and plugin templating syntax.
            if not target or '{{' in raw: continue
            actual=resolve(target,rel)
            records.append({'source':rel,'target':raw,'resolved_to':actual,'status':'resolved' if actual else 'missing_file','line':text.count('\n',0,offset)+1,'kind':'markdown'})
    return records

def validate(preview):
    disk={p.relative_to(ROOT).as_posix():p.read_bytes() for p in files(ROOT) if p.relative_to(ROOT).parts[0]!='_Codex'}
    if preview:
        li,lo,lp=lyt_build(); ai,ao,ap=andy_build()
        before=disk.copy()
        after={k:v for k,v in disk.items() if not k.startswith(CFG['lyt_folder']+'/')}
        after.update({CFG['lyt_folder']+'/'+k:v for k,v in lo.items()}); after.update(ao)
    else:
        lp=json.loads((WORK/'lyt-plan.json').read_text(encoding='utf-8'))
        ap=json.loads((WORK/'andy-plan.json').read_text(encoding='utf-8'))
        after=disk; before={}
        for rel,expected in lp['final_sha256'].items(): assert digest(LYT/rel)==expected,rel
        assert {p.relative_to(LYT).as_posix() for p in files(LYT)}==set(lp['final_sha256'])
        for rel,expected in ap['final_sha256'].items(): assert digest(ROOT/rel)==expected,rel
        saved=json.loads((WORK/'preservation-baseline.json').read_text(encoding='utf-8'))
        for k,data in saved['references'].items(): assert hashes(Path(CFG['reference_vaults'][k]))==data,'Reference changed: '+k
        for rel,expected in saved['other_files'].items(): assert digest(ROOT/rel)==expected,'Unrelated file changed: '+rel
    lyt_files={k:v for k,v in after.items() if k.startswith(CFG['lyt_folder']+'/')}
    names=defaultdict(list); exact=defaultdict(list)
    for rel,data in lyt_files.items():
        if rel.endswith('.md'):
            names[normalized_name(Path(rel))].append(rel)
            exact[hashlib.sha256(data).hexdigest()].append(rel)
    duplicate_names=[g for g in names.values() if len(g)>1]
    duplicate_bytes=[g for g in exact.values() if len(g)>1]
    assert not duplicate_names,duplicate_names
    assert not duplicate_bytes,duplicate_bytes
    errors=[]; urls=0; idem_errors=[]
    for d in ap['decisions']:
        if 'URL' not in d: continue
        rel=d['path']; data=after[rel]; t=data.decode('utf-8-sig'); fm,body=fm_body(t)
        props=yaml.safe_load(fm)
        assert 'URL' in props and 'URLs' not in props,rel
        actual=props['URL']; actual=[actual] if isinstance(actual,str) else actual
        assert actual==d['URL'],(rel,actual,d['URL'])
        for u in actual:
            if 'notes.andymatuschak.org' in u: assert len(trail(u))<=3,(rel,u)
            urls+=1
        assert not any(source_line(line) for line in body.splitlines()),rel
        again,decision=transform(rel,data)
        if again!=data: idem_errors.append(rel)
    assert not idem_errors,idem_errors
    from andy_cleanup import URL_RE
    for rel,data in after.items():
        if rel.startswith(CFG['andy_folder']+'/') and rel.endswith('.md'):
            for u in URL_RE.findall(data.decode('utf-8-sig')):
                if 'notes.andymatuschak.org' in u: assert len(trail(u))<=3,(rel,u)
    for rel,data in lyt_files.items():
        if not rel.endswith('.md'): continue
        text=data.decode('utf-8-sig'); fm=fm_body(text)[0]
        if fm and '{{' not in fm:
            try: yaml.safe_load(fm)
            except yaml.YAMLError as e: errors.append({'path':rel,'error':str(e)})
    scopes={}
    for scope in [CFG['lyt_folder'],CFG['andy_folder'],CFG['lizards_folder']]:
        records=links(after,scope)
        scopes[scope]={'counts':dict(Counter(r['status'] for r in records)),'unresolved':[r for r in records if r['status']!='resolved']}
    result={'mode':'preview' if preview else 'applied','lyt_duplicate_titles':duplicate_names,'lyt_exact_duplicate_notes':duplicate_bytes,'andy_properties_validated':urls,'andy_transform_idempotent':not idem_errors,'yaml_errors':errors,'links':scopes}
    if preview:
        old=links(before,CFG['lyt_folder']); new=links(after,CFG['lyt_folder'])
        result['lyt_links_before']=dict(Counter(r['status'] for r in old))
        # Every previously valid target still has a canonical file after consolidation.
        regressions=[]
        for r in old:
            if r['status']!='resolved': continue
            target=r['resolved_to']
            if target.startswith(CFG['lyt_folder']+'/'):
                suffix=target[len(CFG['lyt_folder'])+1:]
                canonical=lp['destination_map'].get(suffix,suffix)
                if CFG['lyt_folder']+'/'+canonical not in after: regressions.append(r)
        result['removed_valid_targets']=regressions
        assert not regressions,regressions
    (WORK/('verification-preview.json' if preview else 'verification-final.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False,indent=2))
    print(json.dumps({k:v['counts'] for k,v in scopes.items()},ensure_ascii=False,indent=2))
    assert not errors,errors

if __name__=='__main__':
    if '--baseline' in sys.argv: preservation(); print('Preservation baseline recorded.')
    else: validate('--preview' in sys.argv)
