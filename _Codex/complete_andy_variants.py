"""Complete recognized alternate footer formats from the existing recovery snapshot."""
from audit import *
from andy_cleanup import transform
import zipfile, os

previous=json.loads((WORK/'andy-plan.json').read_text(encoding='utf-8'))
initial={}
with zipfile.ZipFile(WORK/'backups'/'andy-before-2026-10-07.zip') as z:
    assert z.testzip() is None
    for rel,h in previous['original_sha256'].items():
        data=z.read(rel); assert hashlib.sha256(data).hexdigest()==h
        initial[rel]=data
output={}; decisions=[]
for rel,data in initial.items():
    out,d=transform(rel,data); output[rel]=out; decisions.append(d)
for rel,data in output.items():
    assert digest(ROOT/rel) in {previous['final_sha256'][rel],hashlib.sha256(data).hexdigest()},rel
stats={'notes_scanned':len(initial),'notes_updated':sum(output[k]!=v for k,v in initial.items()),'source_properties_standardized':sum('URL' in d for d in decisions),'without_explicit_source':sum('URL' not in d for d in decisions),'source_lines_moved':sum(d.get('source_lines_removed',0) for d in decisions),'distinct_long_chains_shortened':sum(d.get('navigation_chains_shortened',0) for d in decisions),'notes_with_corrected_source_conflicts':sum(bool(d.get('source_conflicts_corrected')) for d in decisions),'notes_with_format_repairs':sum(bool(d.get('format_repairs')) for d in decisions),'other_navigation_links_shortened':sum(d.get('navigation_links_shortened',0) for d in decisions)}
plan={'stats':stats,'decisions':decisions,'original_sha256':previous['original_sha256'],'final_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in output.items()}}
(WORK/'andy-plan-first-pass.json').write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding='utf-8')
for rel,data in output.items():
    p=(ROOT/rel).resolve(); assert p.is_relative_to((ROOT/CFG['andy_folder']).resolve())
    if digest(p)!=hashlib.sha256(data).hexdigest():
        temporary=WORK/'andy-source-update.tmp'
        temporary.write_bytes(data)
        os.replace(temporary,p)
for rel,data in output.items(): assert (ROOT/rel).read_bytes()==data
(WORK/'andy-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(WORK/'andy-applied.json').write_text(json.dumps({'backup':str(WORK/'backups'/'andy-before-2026-10-07.zip'),'stats':stats},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
