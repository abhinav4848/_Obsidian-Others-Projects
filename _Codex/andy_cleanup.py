"""Standardize identified source URLs without treating citations as sources."""
from audit import *
from lyt_cleanup import fm_body, fields, write_text_bytes
from urllib.parse import urlunsplit, urlencode, quote
import sys, zipfile, yaml

URL_RE=re.compile(r'https?://[^\s<>\)\]"\}]+')
SOURCE_KEYS={'URL','URLs','url','urls','source','Source'}
KNOWN_SOURCE_CONFLICTS={
    'Elaborative encoding.md':'z9Uq4yzBT1QaBU8twwyvm7P',
    'In the Cells of the Eggplant - Chapman.md':'zAQj4GEE7PWDDcSreCGHTP9',
    'Cloze deletion prompts seem to produce less understanding than question answer pairs in spaced repetition memory systems.md':'Cloze_deletion_prompts_seem_to_produce_less_understanding_than_question/answer_pairs_in_spaced_repetition_memory_systems',
}

def clean_url(u):
    u=u.rstrip('\\').replace('&amp;','&')
    if '?' not in u and '&stackedNotes=' in u: u=u.replace('&stackedNotes=','?stackedNotes=',1)
    return u

def trail(u):
    s=urlsplit(clean_url(u))
    return [unquote(s.path).strip('/')]+[v for k,v in parse_qsl(s.query) if k=='stackedNotes']

def shorten(u):
    s=urlsplit(clean_url(u))
    if s.netloc.lower()!='notes.andymatuschak.org': return u
    keep=trail(u)[-CFG['andy_navigation_notes_to_keep']:]
    extras=[(k,v) for k,v in parse_qsl(s.query) if k!='stackedNotes']
    query=urlencode([('stackedNotes',v) for v in keep[1:]]+extras,quote_via=quote)
    return urlunsplit((s.scheme,s.netloc,'/'+quote(keep[0],safe=''),query,s.fragment))

def source_line(line):
    if re.search(r'\bAndy (?:Link|Matuschak (?:site|notes))\b',line,re.I) and 'notes.andymatuschak.org' in line: return True
    m=re.match(r'^\s*(?:[-*]|\d+\.)?\s*\[([^\]]+)\]\((https?://notes\.andymatuschak\.org/[^)]+)\)\s*$',line)
    if m and (m[1].strip().casefold() in {'link','source','original','original note'} or ('|' in m[1] and 'stackedNotes=' in m[2])): return True
    if re.match(r'^\s*(?:[-*]|\d+\.)?\s*(?:URL|url|Source|source):\s*https?://notes\.andymatuschak\.org/',line): return True
    if re.match(r'^\s*(?:[-*]|\d+\.)?\s*https?://notes\.andymatuschak\.org/\S+\s*$',line): return True
    # An unlabeled URL-to-itself is the other source-footer format present here.
    m=re.match(r'^\s*(?:[-*]|\d+\.)?\s*\[(https?://notes\.andymatuschak\.org/[^\]]+)\]\((https?://notes\.andymatuschak\.org/[^)]+)\)\s*$',line)
    return bool(m and clean_url(m[1])==clean_url(m[2]))

def remove_empty_source_headings(body):
    # Remove empty source headings, retaining sections with literature citations.
    lines=body.splitlines(keepends=True)
    remove=set()
    for i,line in enumerate(lines):
        m=re.match(r'^(#{1,6})\s+(?:References?|Sources?)\s*$',line.strip(),re.I)
        if not m: continue
        level=len(m[1]); j=i+1
        while j<len(lines):
            heading=re.match(r'^(#{1,6})\s+',lines[j])
            if heading and len(heading[1])<=level: break
            j+=1
        if all(not x.strip() or x.strip()=='---' for x in lines[i+1:j]):
            remove.update(range(i,j))
            k=i-1
            while k>=0 and not lines[k].strip(): remove.add(k); k-=1
            if k>=0 and lines[k].strip()=='---': remove.add(k)
    return ''.join(x for i,x in enumerate(lines) if i not in remove)

def transform(path,data):
    text=data.decode('utf-8-sig'); fm,body=fm_body(text)
    props=fields(fm)
    sources=[]
    property_keys=[]
    for k,block in props.items():
        if k in SOURCE_KEYS:
            urls=URL_RE.findall(block)
            if urls:
                sources.extend(urls); property_keys.append(k)
    removed=[]
    remaining=[]
    for line in body.splitlines(keepends=True):
        if source_line(line):
            urls=URL_RE.findall(line)
            if urls:
                sources.extend(urls); removed.append(line); continue
        remaining.append(line)
    if not sources:
        result=URL_RE.sub(lambda m:shorten(m[0]) if 'notes.andymatuschak.org' in m[0] and len(trail(m[0]))>3 else m[0],text)
        out=write_text_bytes(result,data)
        return out,{'path':path,'status':'navigation_links_shortened' if out!=data else 'no_explicit_source','navigation_links_shortened':sum('notes.andymatuschak.org' in u and len(trail(u))>3 for u in URL_RE.findall(text))}
    sources=list(dict.fromkeys(sources))
    by_leaf=defaultdict(list)
    for u in sources:
        by_leaf[trail(u)[-1] if 'notes.andymatuschak.org' in u else u].append(u)
    conflict=[]
    expected=KNOWN_SOURCE_CONFLICTS.get(Path(path).name)
    if expected and expected in by_leaf:
        conflict=[u for leaf,urls in by_leaf.items() if leaf!=expected for u in urls]
        by_leaf={expected:by_leaf[expected]}
    final_urls=[]
    for leaf,urls in by_leaf.items():
        chosen=max(urls,key=lambda u:len(trail(u)))
        final_urls.append(shorten(chosen))
    final_urls=list(dict.fromkeys(final_urls))
    # Keep property aliases and all unrelated property values verbatim.
    props={k:v for k,v in props.items() if k not in property_keys}
    value=final_urls[0] if len(final_urls)==1 else final_urls
    props[CFG['andy_url_property']]=yaml.safe_dump({CFG['andy_url_property']:value},allow_unicode=True,sort_keys=False,width=10000).rstrip()
    rest=''.join(remaining)
    replacements={u:shorten(u) for u in sources if 'notes.andymatuschak.org' in u}
    # Preserve self-referential footnotes, shortening their existing source target.
    def replace_source(m):
        u=m[0]
        return replacements.get(u,shorten(u) if 'notes.andymatuschak.org' in u and len(trail(u))>3 else u)
    rest=URL_RE.sub(replace_source,rest)
    rest=remove_empty_source_headings(rest)
    fm='\n'.join(props.values())
    result='---\n'+fm+'\n---\n'+rest.lstrip('\n')
    result_bytes=write_text_bytes(result,data)
    return result_bytes,{'path':path,'status':'updated' if result_bytes!=data else 'already_standard','original_sources':sources,'URL':final_urls,'source_lines_removed':len(removed),'navigation_chains_shortened':sum(len(trail(u))>3 for u in sources),'source_conflicts_corrected':conflict,'format_repairs':[u for u in sources if clean_url(u)!=u]}

def build():
    initial={p.relative_to(ROOT).as_posix():p.read_bytes() for p in files(ROOT/CFG['andy_folder']) if p.suffix=='.md'}
    output={}; decisions=[]
    for rel,data in initial.items():
        out,decision=transform(rel,data); output[rel]=out; decisions.append(decision)
    stats={'notes_scanned':len(initial),'notes_updated':sum(d['status']=='updated' for d in decisions),'without_explicit_source':sum(d['status']=='no_explicit_source' for d in decisions),'source_lines_moved':sum(d.get('source_lines_removed',0) for d in decisions),'distinct_long_chains_shortened':sum(d.get('navigation_chains_shortened',0) for d in decisions),'notes_with_corrected_source_conflicts':sum(bool(d.get('source_conflicts_corrected')) for d in decisions),'notes_with_format_repairs':sum(bool(d.get('format_repairs')) for d in decisions)}
    plan={'stats':stats,'decisions':decisions,'original_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in initial.items()},'final_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in output.items()}}
    (WORK/'andy-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    return initial,output,plan

def apply(initial,output,plan):
    backup=WORK/'backups'/'andy-before-2026-10-07.zip'
    backup.parent.mkdir(exist_ok=True)
    if backup.exists(): raise RuntimeError('Recovery backup already exists; refusing to reapply.')
    with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
        for rel,data in initial.items(): z.writestr(rel,data)
    with zipfile.ZipFile(backup) as z:
        assert z.testzip() is None
        for rel,data in initial.items(): assert z.read(rel)==data
    for rel,data in initial.items(): assert (ROOT/rel).read_bytes()==data, 'Note changed during planning: '+rel
    for rel,data in output.items():
        if data!=initial[rel]:
            p=(ROOT/rel).resolve()
            assert p.is_relative_to((ROOT/CFG['andy_folder']).resolve())
            p.write_bytes(data)
    for rel,data in output.items(): assert (ROOT/rel).read_bytes()==data
    (WORK/'andy-applied.json').write_text(json.dumps({'backup':str(backup),'stats':plan['stats']},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    if (WORK/'andy-applied.json').exists():
        print('This standardization is already applied. Original plans and backups are preserved.')
        sys.exit(0)
    initial,output,plan=build()
    print(json.dumps(plan['stats'],ensure_ascii=False,indent=2))
    if '--apply' in sys.argv: apply(initial,output,plan); print('Applied and verified; recovery backup saved.')
