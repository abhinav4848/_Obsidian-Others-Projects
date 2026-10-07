from audit import *
import difflib

def split_fm(t):
    m=re.match(r'\A---\s*\n(.*?)\n---[^\n]*\n?',t,re.S)
    return (m.group(1),t[m.end():]) if m else ('',t)

def norm_body(t):
    b=split_fm(t)[1]
    b=re.sub(r'\[\[([^\]|#]+)([^\]]*)\]\]',lambda m:'[['+m[1].split('/')[-1]+m[2]+']]',b)
    return re.sub(r'\s+',' ',b).strip()

lf=[p for p in files(LYT) if p.suffix=='.md']
ref={k:{p.stem.casefold():p.relative_to(Path(v)).as_posix() for p in files(Path(v)) if p.suffix=='.md'} for k,v in CFG['reference_vaults'].items()}
print('INCORRECTLY PLACED STATEMENTS:')
wrong=[]
for p in lf:
    rp=ref['lite'].get(p.stem.casefold()) or ref['pro'].get(p.stem.casefold())
    if rp and p.parent.relative_to(LYT).as_posix()=='Atlas/Dots/Statements' and 'Things/' in rp:
        wrong.append(p.name)
print(len(wrong),'of',sum(p.parent.relative_to(LYT).as_posix()=='Atlas/Dots/Statements' for p in lf))
print('POSSIBLE DIFFERENT-TITLE DUPLICATES:')
norm={p:norm_body(read(p)) for p in lf}
for i,p in enumerate(lf):
    a=norm[p]
    if len(a)<100: continue
    for q in lf[i+1:]:
        if normalized_name(p)==normalized_name(q): continue
        b=norm[q]
        if min(len(a),len(b))/max(len(a),len(b),1)<.7: continue
        matcher=difflib.SequenceMatcher(None,a,b)
        if matcher.quick_ratio()<.86: continue
        sim=matcher.ratio()
        if sim>.86: print(round(sim,3),p.relative_to(LYT).as_posix(),'|',q.relative_to(LYT).as_posix())
print('ANDY PROPERTY VARIETIES:')
props=Counter()
urlre=re.compile(r'https?://[^\s<>\)\]"\}]+')
source_missing=[]
conflicts=[]
for p in files(ROOT/CFG['andy_folder']):
    if p.suffix!='.md': continue
    t=read(p); fm,body=split_fm(t)
    keys=re.findall(r'^([A-Za-z][\w -]*):',fm,re.M)
    props.update(keys)
    prop_urls=[]
    for m in re.finditer(r'^(?:URL|URLs|url|source|Source):.*(?:\n(?:[ \t]+.*|\s*- .*))*',fm,re.M): prop_urls.extend(urlre.findall(m[0]))
    labels=[u for line in body.splitlines() if 'Andy Link' in line for u in urlre.findall(line)]
    tops=[u for line in body.splitlines()[:5] if re.match(r'^\s*(?:https?://|(?:URL|Source|source|url):\s*https?://)',line) for u in urlre.findall(line)]
    own=list(dict.fromkeys(prop_urls+labels+tops))
    if not own: source_missing.append(p.name)
    leafs=set()
    for u in own:
        if 'notes.andymatuschak.org' not in u: continue
        u=u.replace('&stackedNotes=','?stackedNotes=',1) if '?' not in u else u
        s=urlsplit(u); st=[v for k,v in parse_qsl(s.query) if k=='stackedNotes']
        leafs.add(st[-1] if st else unquote(s.path).strip('/'))
    if len(leafs)>1: conflicts.append({'note':p.name,'leafs':list(leafs),'sources':own})
print(json.dumps({'properties':dict(props),'source_missing_count':len(source_missing),'missing':source_missing,'source_conflicts':conflicts},ensure_ascii=False,indent=2))
