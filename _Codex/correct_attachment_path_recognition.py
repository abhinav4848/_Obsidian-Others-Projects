from pathlib import Path
from collections import defaultdict
import zipfile,json,hashlib,os
from urllib.parse import quote
W=Path('_Codex');R=Path.cwd();plan=json.loads((W/'attachment-relocation-applied.json').read_text(encoding='utf-8'))
source=(W/'relocate_attachments.py').read_text(encoding='utf-8-sig');env={'__file__':str((W/'relocate_attachments.py').resolve())};exec(source.split('refs={p:references')[0],env)
oldassets=[R/a['original'] for a in plan['assets']];env['assets']=oldassets;env['hashes']={R/a['original']:a['sha256'] for a in plan['assets']};env['byrel']={a['original'].casefold():R/a['original'] for a in plan['assets']};env['byname']=defaultdict(list)
for p in oldassets:env['byname'][p.name.casefold()].append(p)
destinations={}
for a in plan['assets']:
 for d in a['destinations']:destinations[(R/a['original'],Path(d).parts[0])]=R/d
changes=[];fixed=[]
with zipfile.ZipFile(R/plan['backup']) as backup:
 for n,h in plan['note_hashes'].items():
  p=R/n;current=p.read_bytes();assert hashlib.sha256(current).hexdigest()==h['after'],('Concurrent edit',n)
  original=backup.read(n);text=original.decode('utf-8-sig');rows=env['references'](p,text);owner=Path(n).parts[0];new=text
  for x in reversed(rows):
   dest=destinations[(x['asset'],owner)];target=dest.relative_to(R).as_posix() if x['style']!='markdown' else quote(os.path.relpath(dest,p.parent).replace('\\','/'),safe='/.-_~')
   if target!=x['old']:
    new=new[:x['start']]+target+new[x['end']:];changes.append({'note':n,'source':x['asset'].relative_to(R).as_posix(),'destination':dest.relative_to(R).as_posix(),'before':x['old'],'after':target,'style':x['style']})
  out=new.encode('utf-8');out=b'\xef\xbb\xbf'+out if original.startswith(b'\xef\xbb\xbf') else out
  if out!=current:
   fixed.append(n);temp=W/'relocation-correction.tmp';temp.write_bytes(out);os.replace(temp,p)
  assert p.read_bytes()==out
  h['after']=hashlib.sha256(out).hexdigest()
assert fixed==['Andy Matuschak/2023-09-30 Patreon letter - Highlight-driven practice and comprehension support.md'],fixed
plan['link_changes']=changes;plan['stats']['references_updated']=len(changes);plan['corrections']={'prose_preserved_after_restricting_path_recognition':fixed,'restored_from_original_snapshot':True};plan['verification']['changes_rebuilt_from_original_notes_with_strict_path_recognition']=True
(W/'attachment-relocation-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'attachment-relocation-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Restored prose in',len(fixed),'note; valid attachment references:',len(changes))
