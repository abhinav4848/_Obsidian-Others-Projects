from audit import *
import difflib

d = json.loads((WORK/'audit-initial.json').read_text(encoding='utf-8'))
lines=[]
for g in d['normalized_name_groups']:
    lines.append('\n### ' + ' | '.join(g))
    a=read(LYT/g[0]).splitlines()
    for name in g[1:]:
        b=read(LYT/name).splitlines()
        delta=list(difflib.unified_diff(a,b,fromfile=g[0],tofile=name,n=1))
        lines.extend(delta[:160] if delta else ['IDENTICAL'])
        if len(delta)>160: lines.append(f'... {len(delta)-160} more diff lines')
for k in ['pro','lite']:
    lines.append('\n## '+k+' folder paths')
    inv=d['reference_inventory'][k]
    lines.append(json.dumps(dict(Counter(str(Path(x['path']).parent).replace('\\','/') for x in inv)),ensure_ascii=False,indent=2))
    lines.append('\n## '+k+' special filenames')
    lines.extend(x['path'] for x in inv if Path(x['path']).parent.as_posix() in ['Atlas/Maps','Atlas/Dots/X','Atlas/Notes/X/Meta','Atlas/Notes/Things','Atlas/Notes/Ideas','Atlas/Notes/X/Quotes'])
(WORK/'variant-inspection.txt').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines))
