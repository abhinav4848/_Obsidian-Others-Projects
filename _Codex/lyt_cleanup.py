"""Build a reviewed LYT consolidation; applying requires an explicit CLI flag."""
from audit import *
import base64, difflib, sys, zipfile, stat
import yaml

# These equivalences were reviewed against the two supplied reference vaults.
RENAMES = {
    '+ About Ideas': '+ About Dots',
    '+ About Utilities': '+ About x',
    'Meta Map': 'Meta PKM',
    'Sources Map': 'Sources',
    'Concepts Map': 'Concepts',
    'ACE Headspace': 'ACE Folder Framework',
    'ACE honors the 3 headspaces of PKM': 'ACE honors the 3 head spaces of PKM',
    'The ACE Headspace allows for flexible folders': 'The ACE Folder Framework Flexes For You',
    'evaporated in a thousand follies\'\'': 'evaporated in a thousand follies',
    '–evaporated in a thousand follies': 'evaporated in a thousand follies',
    'Base Template w Tags': 'Template, Properties, Base + Tags (Kit)',
    'Efforts Template': 'Template, Properties, Effort (Kit)',
    "Nick Milo's Starting Custom Callouts": "Nick Milo's Custom Callouts",
    '2023-08-w34 1': '2023-08-w34',
    'Do you suffer from note-taking_': 'Do you suffer from note-taking',
    'Nineteen Eighty-Four': '1984 (book)',
    'Between the World and Me': 'Between the World and Me (book)',
    'Atomic Habits': 'Atomic Habits (book)',
    "Ptolemy's Almagest": 'The Almagest',
    'Book': 'Books', 'Course': 'Courses', 'Game': 'Games',
    'Movie': 'Movies', 'Paper': 'Papers', 'Song': 'Songs', 'Speech': 'Speeches',
    "People''s attributes are domain-specific": "People's attributes are domain-specific",
}
for n in ['Bill Russell','Carl Sagan','K. Anders Ericsson','Mary Wollstonecraft','Mihaly Csikszentmihalyi','Nina Simone']:
    RENAMES[n] = n + ' (kit)'

def fm_body(t):
    m = re.match(r'\A---[ \t]*\n(.*?)\n---[^\n]*\n?',t,re.S)
    return (m.group(1),t[m.end():]) if m else ('',t)

def fields(fm):
    blocks = {}
    for m in re.finditer(r'^([\w][\w -]*):[^\n]*(?:\n(?![\w][\w -]*:).*?)*(?=\n[\w][\w -]*:|\Z)',fm,re.M):
        blocks[m[1]] = m[0].rstrip()
    return blocks

def canonical_name(stem, lite_names):
    if stem in RENAMES: return RENAMES[stem]
    # The emoji variants all come from the Lite reference.
    key=normalized_name(Path(stem+'.md'))
    found=lite_names.get(key,stem)
    return RENAMES.get(found,found)

def new_layout(path):
    path=path.replace('Atlas/Utilities/','x/').replace('Atlas/Notes/','Atlas/Dots/')
    path=path.replace('Atlas/Dots/Ideas/','Atlas/Dots/Things/')
    if path.startswith('_attachments/'): path='x/Images/'+path.split('/',1)[1]
    return path

def body_key(s):
    s=re.sub(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]',lambda m:m[1].rsplit('/',1)[-1],s)
    s=re.sub(r'(?m)^\s*>\s?', '',s)
    s=re.sub(r'(?m)^#{1,6}\s*(?:\d+\)\s*)?', '',s)
    s=s.replace('Ideaverse for Obsidian','Ideaverse Lite')
    s=s.replace(' #source/quote/250','')
    s=s.replace('[[','').replace(']]','')
    s=re.sub(r'[\*_]','',s)
    return re.sub(r'\s+',' ',s).strip()

def write_text_bytes(s, original):
    newline='\r\n' if b'\r\n' in original else '\n'
    return s.replace('\r\n','\n').replace('\n',newline).encode('utf-8')

def build():
    initial={p.relative_to(LYT).as_posix():p.read_bytes() for p in files(LYT)}
    refs={}
    ref_names={}
    lite_names={}
    for kind,root in CFG['reference_vaults'].items():
        for p in files(Path(root)):
            rel=p.relative_to(Path(root)).as_posix()
            refs[(kind,rel)]=p
            ref_names.setdefault(p.name.casefold(),[]).append((kind,rel,p))
            if kind=='lite' and p.suffix=='.md':
                lite_names[normalized_name(p)]=p.stem
    dest={}
    for rel in initial:
        p=Path(rel)
        if p.suffix=='.md':
            name=canonical_name(p.stem,lite_names)
            candidates=ref_names.get((name+'.md').casefold(),[])
            if not candidates:
                candidates=[(k,r,p) for (k,r),p in refs.items() if p.suffix=='.md' and canonical_name(p.stem,lite_names)==name]
            latest=next((r for k,r,p in candidates if k=='lite'),None)
            old=next((r for k,r,p in candidates if k=='pro'),None)
            target=latest or new_layout(old or rel)
            target=str(Path(target).with_name(name+'.md')).replace('\\','/')
            if name=='+ About x': target='x/+ About x.md'
        else: target=new_layout(rel)
        if rel=='+/Untitled 1.base': target='+/Untitled.base'
        # Two zero-byte placeholders contain no knowledge. Keep the calendar slot.
        if rel=='+/New spark, so cool.md' and not initial[rel]: target='Calendar/2024-09.md'
        dest[rel]=target

    groups=defaultdict(list)
    for src,target in dest.items(): groups[target].append(src)
    # Map every historical path and known basename to its canonical destination.
    paths={}
    names=defaultdict(set)
    def register(src,target):
        paths[src.casefold()]=target
        paths[(CFG['lyt_folder']+'/'+src).casefold()]=target
        if Path(src).suffix=='.md':
            paths[str(Path(src).with_suffix('')).replace('\\','/').casefold()]=target
            paths[(CFG['lyt_folder']+'/'+str(Path(src).with_suffix('')).replace('\\','/')).casefold()]=target
            names[Path(src).stem.casefold()].add(target)
        else: names[Path(src).name.casefold()].add(target)
    for src,target in dest.items(): register(src,target)
    for target in groups: register(target,target)
    for name,can in RENAMES.items():
        targets=names.get(can.casefold(),set())
        if len(targets)==1: names[name.casefold()].update(targets)
    # Historical layouts in the reference files identify additional stale paths.
    for (kind,rel),p in refs.items():
        can=canonical_name(p.stem,lite_names) if p.suffix=='.md' else p.name
        matches=names.get(can.casefold(),set())
        if len(matches)==1: register(rel,next(iter(matches)))

    restores={}
    changes=Counter()
    def resolve(target):
        key=unquote(target).replace('\\','/').strip()
        if not key or '://' in key or key.startswith('#'): return None
        found=paths.get(key.casefold())
        if found: return found
        base=key.rsplit('/',1)[-1]
        stem=base[:-3] if base.lower().endswith('.md') else base
        can=canonical_name(stem,lite_names)
        matches=names.get(can.casefold(),set()) or names.get(base.casefold(),set())
        if len(matches)==1: return next(iter(matches))
        return None

    def repair_wiki(t):
        def sub(m):
            inside=m[1]
            first,sep,label=inside.partition('|')
            target,hashmark,anchor=first.partition('#')
            found=resolve(target)
            if not found: return m[0]
            if found.endswith('.md'): found=found[:-3]
            if found.endswith('/LYT Mode Theme') and anchor=='Alternative Checkboxes':
                anchor='Alternative Checkboxes aka Icon Bullets'
            result='[['+CFG['lyt_folder']+'/'+found+(hashmark+anchor if hashmark else '')+(sep+label if sep else '')+']]'
            if result!=m[0]: changes['wiki_links']+=1
            return result
        return re.sub(r'\[\[([^\]\n]+)\]\]',sub,t)

    def repair_markdown(t,source):
        def sub(m):
            link=m[2]; angle=link.startswith('<') and link.endswith('>')
            raw=link[1:-1] if angle else link
            if re.match(r'^[A-Za-z]+:',raw) or raw.startswith('#'): return m[0]
            target,hashmark,anchor=raw.partition('#')
            found=resolve(target)
            if not found: return m[0]
            # Absolute vault-root paths are unambiguous in Obsidian.
            result='['+m[1]+'](<' + CFG['lyt_folder']+'/'+found+(hashmark+anchor if hashmark else '')+'>)'
            if result!=m[0]: changes['markdown_links']+=1
            return result
        return re.sub(r'\[([^\]\n]+)\]\((<[^>\n]+>|[^)\n]+)\)',sub,t)

    query_paths={
        'Atlas/Notes/Vaults/Ideaverse/Atlas/Notes/Things':'Atlas/Dots/Things',
        'Atlas/Notes/Vaults/Ideaverse/Atlas/Notes/Statements':'Atlas/Dots/Statements',
        'Atlas/Notes/Vaults/Ideaverse':'Atlas/Dots',
        'Atlas/Notes/Ideas':'Atlas/Dots/Things',
        'Atlas/Notes':'Atlas/Dots', 'Atlas/Utilities':'x',
        'Atlas/Dots':'Atlas/Dots','Atlas/Maps':'Atlas/Maps',
        'Calendar':'Calendar','Efforts':'Efforts','x':'x','+':'+',
    }
    def repair_queries(t):
        # Only path literals inside code fences and known folder filters are changed.
        def fence(m):
            block=m[0]
            def quoted(q):
                value=q[2]
                if value.startswith(CFG['lyt_folder']+'/'): return q[0]
                for old,new in sorted(query_paths.items(),key=lambda x:-len(x[0])):
                    if value==old or value.startswith(old+'/'):
                        changes['query_paths']+=1
                        return q[1]+CFG['lyt_folder']+'/'+new+value[len(old):]+q[1]
                return q[0]
            return re.sub(r'([\"\'])([^\"\'\n]+)\1',quoted,block)
        return re.sub(r'```[^\n]*\n.*?```',fence,t,flags=re.S)

    def rewrite(t,source): return repair_queries(repair_markdown(repair_wiki(t),source))

    # Recover only missing linked files that actually exist in a supplied reference.
    for _ in range(8):
        added=0
        for rel,data in list(initial.items())+list(restores.items()):
            if Path(rel).suffix not in TEXT_EXT: continue
            t=data.decode('utf-8-sig')
            for inside in re.findall(r'\[\[([^\]\n]+)\]\]',t):
                key=inside.split('|')[0].split('#')[0]
                if resolve(key) or not key or '://' in key: continue
                base=unquote(key).rsplit('/',1)[-1]
                candidates=ref_names.get((base if '.' in Path(base).suffix and Path(base).suffix.lower()!='.md' else base.removesuffix('.md')+'.md').casefold(),[])
                if not candidates: continue
                kind,rp,p=next((x for x in candidates if x[0]=='lite'),candidates[0])
                target=new_layout(rp)
                if target in groups or target in restores: continue
                restores[target]=p.read_bytes()
                register(rp,target); register(target,target)
                added+=1
        if not added: break

    output={}
    decisions=[]
    review=[]
    special_body={
        'Atlas/Dots/Things/ACE Folder Framework.md':'Atlas/Dots/Statements/ACE Headspace.md',
        'Atlas/Dots/Things/The ACE Folder Framework Flexes For You.md':'Atlas/Dots/Statements/The ACE Headspace allows for flexible folders.md',
        'Atlas/Maps/Concepts.md':'Atlas/Maps/Concepts.md',
        'x/+ About x.md':'x/+ About x.md',
        "x/Templates/Nick Milo's Custom Callouts.md":"x/Templates/Nick Milo's Custom Callouts.md",
    }
    for target,members in sorted(groups.items()):
        primary=target if target in members else members[0]
        if Path(target).suffix not in TEXT_EXT:
            assert len({hashlib.sha256(initial[m]).hexdigest() for m in members})==1, ('binary conflict',target)
            output[target]=initial[primary]
            continue
        transformed={m:rewrite(initial[m].decode('utf-8-sig'),m) for m in members}
        if len(members)==1:
            output[target]=write_text_bytes(transformed[primary],initial[primary]); continue
        if target.endswith('.base'):
            assert len(set(transformed.values()))==1
            output[target]=write_text_bytes(transformed[primary],initial[primary]); continue
        fms={m:fm_body(t)[0] for m,t in transformed.items()}
        bodies={m:fm_body(t)[1] for m,t in transformed.items()}
        # Current Lite frontmatter is preferred; richer Pro body material is retained.
        preferred=next((m for m in members if m.startswith('Atlas/Dots/') and Path(m).name==Path(target).name),primary)
        if target.startswith('x/') and target in members: preferred=target
        body_source=special_body.get(target) or max(members,key=lambda m:len(bodies[m]))
        if '/Templates/' in target and target in members: body_source=target
        body=bodies[body_source]
        added_paragraphs=[]
        skipped=[]
        for member in members:
            if member==body_source: continue
            # These full-body equivalences were inspected directly; the differences
            # are naming/formatting, except the toolbox additions retained below.
            if target in {'Atlas/Dots/Statements/ACE honors the 3 head spaces of PKM.md','x/+ About x.md',"x/Templates/Nick Milo's Custom Callouts.md"}:
                skipped.append({'member':member,'reason':'reviewed equivalent body; current wording retained'})
                continue
            paras=re.split(r'\n\s*\n',bodies[member])
            for para in paras:
                key=body_key(para)
                if not key or key in body_key(body): continue
                existing=[body_key(x) for x in re.split(r'\n\s*\n',body)]
                best=max((difflib.SequenceMatcher(None,key,e).ratio() for e in existing),default=0)
                if best>.76:
                    skipped.append({'member':member,'paragraph':para,'reason':'superseded wording of the same paragraph'})
                    continue
                # Template fields are handled in frontmatter, not as body appendices.
                if len(key)<25 or key.startswith('[!') or key.startswith('---'): continue
                added_paragraphs.append(para)
                body=body.rstrip()+'\n\n'+para.strip()+'\n'
        basefields=fields(fms[preferred])
        conflicts=[]
        for member in members:
            if member==preferred: continue
            for k,block in fields(fms[member]).items():
                if k not in basefields:
                    basefields[k]=block; continue
                if basefields[k]==block: continue
                try:
                    a=yaml.safe_load(basefields[k])[k]; b=yaml.safe_load(block)[k]
                    if a in (None,[], '') and b not in (None,[], ''): basefields[k]=block
                    elif isinstance(a,list) and isinstance(b,list):
                        values=a+[x for x in b if x not in a]
                        basefields[k]=yaml.safe_dump({k:values},allow_unicode=True,sort_keys=False).rstrip()
                    elif a!=b and b not in (None,[], ''):
                        conflicts.append({'field':k,'kept':basefields[k],'historical':block,'member':member})
                except (yaml.YAMLError,TypeError):
                    conflicts.append({'field':k,'kept':basefields[k],'historical':block,'member':member})
        aliases=[]
        if 'aliases' in basefields:
            try:
                existing=yaml.safe_load(basefields['aliases'])['aliases']
                aliases=existing if isinstance(existing,list) else [existing] if existing else []
            except yaml.YAMLError: pass
        for member in members:
            old=Path(member).stem
            if old!=Path(target).stem and old not in aliases: aliases.append(old)
        for old,new in RENAMES.items():
            if new==Path(target).stem and old not in aliases: aliases.append(old)
        if aliases: basefields['aliases']=yaml.safe_dump({'aliases':aliases},allow_unicode=True,sort_keys=False).rstrip()
        fm='\n'.join(basefields.values())
        final=('---\n'+fm+'\n---\n' if fm else '')+body.lstrip('\n')
        # Explain the supporting Pro folders in the single current toolbox note.
        if target=='x/+ About x.md':
            final+='\nThe Pro reference also supplies `Prompts` and `Scripts`; these remain in `x/Prompts` and `x/Scripts`.\n'
        if target=='Atlas/Dots/X/+ About these notes.md':
            final=final.replace('`Atlas/Notes`','`Atlas/Dots`')
        output[target]=write_text_bytes(final,initial[preferred])
        decisions.append({'target':target,'members':members,'frontmatter_source':preferred,'body_source':body_source,'metadata_conflicts':conflicts,'additional_paragraphs':added_paragraphs,'superseded_paragraphs':skipped})
        review.append('\n### '+target+'\nMembers: '+str(members)+'\nBody: '+body_source)
        for m in members:
            if m!=body_source:
                review.extend(difflib.unified_diff(bodies[body_source].splitlines(),bodies[m].splitlines(),fromfile=body_source,tofile=m,n=1))
        if added_paragraphs: review.append('APPENDED:\n'+'\n\n'.join(added_paragraphs))
    for target,data in restores.items(): output[target]=write_text_bytes(rewrite(data.decode('utf-8-sig'),target),data) if Path(target).suffix in TEXT_EXT else data

    # Old aliases are meaningful even when a renamed file had no duplicate copy.
    # Cross-vault originals are intentionally not mutated.
    stats={'initial_notes':sum(Path(x).suffix=='.md' for x in initial), 'final_notes':sum(Path(x).suffix=='.md' for x in output),'initial_files':len(initial),'final_files':len(output),'duplicate_note_copies_removed':sum(max(0,len(d['members'])-1) for d in decisions if d['target'].endswith('.md')),'consolidated_groups':len(decisions),'moved_files':sum(src!=target for src,target in dest.items()),'restored_files':list(restores),'rewritten_occurrences_including_merged_copies':dict(changes)}
    plan={'stats':stats,'destination_map':dest,'merge_decisions':decisions,'original_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in initial.items()},'final_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in output.items()}}
    (WORK/'lyt-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    (WORK/'lyt-review.txt').write_text('\n'.join(review),encoding='utf-8')
    return initial,output,plan

def remove_empty_folders():
    for p in sorted((p for p in LYT.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
        if not any(p.iterdir()):
            assert p.resolve().is_relative_to(LYT.resolve())
            try: p.rmdir()
            except PermissionError:
                # Supplied vault folders carry Windows' read-only directory flag.
                # Clear it only on an already verified, empty LYT directory.
                p.chmod(stat.S_IWRITE)
                p.rmdir()

def finish_applied():
    plan=json.loads((WORK/'lyt-plan.json').read_text(encoding='utf-8'))
    backup=WORK/'backups'/'lyt-before-2026-10-07.zip'
    with zipfile.ZipFile(backup) as z:
        assert z.testzip() is None
        for rel,h in plan['original_sha256'].items():
            assert hashlib.sha256(z.read(CFG['lyt_folder']+'/'+rel)).hexdigest()==h
    for rel,h in plan['final_sha256'].items(): assert digest(LYT/rel)==h,rel
    assert {p.relative_to(LYT).as_posix() for p in files(LYT)}==set(plan['final_sha256'])
    remove_empty_folders()
    (WORK/'lyt-applied.json').write_text(json.dumps({'backup':str(backup),'stats':plan['stats']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('Completed folder cleanup; saved files and backup verified.')

def apply(initial,output,plan):
    backup=WORK/'backups'/'lyt-before-2026-10-07.zip'
    backup.parent.mkdir(exist_ok=True)
    if backup.exists(): raise RuntimeError('Recovery backup already exists; refusing to reapply.')
    with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
        for rel,data in initial.items(): z.writestr(CFG['lyt_folder']+'/'+rel,data)
    with zipfile.ZipFile(backup) as z:
        assert z.testzip() is None
        for rel,data in initial.items(): assert z.read(CFG['lyt_folder']+'/'+rel)==data
    for rel,data in initial.items(): assert (LYT/rel).read_bytes()==data, 'Note changed during planning: '+rel
    for rel,data in output.items():
        p=(LYT/rel).resolve()
        assert p.is_relative_to(LYT.resolve())
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)
    for rel in set(initial)-set(output):
        p=(LYT/rel).resolve(); assert p.is_relative_to(LYT.resolve()); p.unlink()
    remove_empty_folders()
    for rel,data in output.items(): assert (LYT/rel).read_bytes()==data
    (WORK/'lyt-applied.json').write_text(json.dumps({'backup':str(backup),'stats':plan['stats']},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--finish-applied' in sys.argv: finish_applied(); sys.exit(0)
    if (WORK/'lyt-applied.json').exists():
        print('This consolidation is already applied. Original plans and backups are preserved.')
        sys.exit(0)
    initial,output,plan=build()
    print(json.dumps(plan['stats'],ensure_ascii=False,indent=2))
    if '--apply' in sys.argv: apply(initial,output,plan); print('Applied and verified; recovery backup saved.')
