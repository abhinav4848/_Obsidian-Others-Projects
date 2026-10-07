from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
import json,hashlib,os,re,zipfile
W=Path(__file__).resolve().parent;R=W.parent;S=W/'media-recovery'
p=json.loads((S/'plan.json').read_text(encoding='utf-8')); d={x['URL']:x for x in json.loads((S/'downloads.json').read_text(encoding='utf-8'))};A=R/'Attachments';A.mkdir(exist_ok=True)
assert not (S/'applied.json').exists(),'Already applied'
byhash={};mapping={};missing=[]; assets=[]
for item in p['assets']:
 result=d.get(item.get('source_URL'))
 if not result or result['status']!='recovered':missing.append(item);continue
 sha=result['sha256']
 if sha not in byhash:
  name=Path(item['original_path']).stem+result['extension'];dest=A/name
  if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()!=sha:dest=A/(Path(name).stem+'-'+sha[:12]+result['extension'])
  content=(W/result['cache']).read_bytes();assert hashlib.sha256(content).hexdigest()==sha
  dest.write_bytes(content);byhash[sha]=dest.relative_to(R).as_posix()
 mapping[item['original_path']]=byhash[sha]
 assets.append({'original_path':item['original_path'],'attachment':byhash[sha],**result,'evidence':item['source_candidates']})
changes={}
for note in p['notes']:
 path=R/note; before=path.read_bytes();text=before.decode('utf-8-sig'); lines=[]
 for line in text.splitlines(keepends=True):
  for old,new in mapping.items():
   if old in line:
    target=new
    if re.search(r'!?\[[^\]]*\]\([^\n]*'+re.escape(old),line):target=os.path.relpath(R/new,path.parent).replace('\\','/')
    line=line.replace(old,target)
  lines.append(line)
 after=''.join(lines).encode('utf-8');after=(b'\xef\xbb\xbf'+after) if before.startswith(b'\xef\xbb\xbf') else after
 if after!=before:changes[note]=(before,after)
backup=W/'backups'/('media-recovery-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
 for note,(before,after) in changes.items():z.writestr(note,before)
for note,(before,after) in changes.items():
 temp=S/'write.tmp';temp.write_bytes(after);os.replace(temp,R/note)
for a in assets:assert hashlib.sha256((R/a['attachment']).read_bytes()).hexdigest()==a['sha256']
for note,(before,after) in changes.items():assert (R/note).read_bytes()==after
stats={'repaired_references':len(mapping),'unique_attachments':len(byhash),'notes_updated':len(changes),'unresolved_references':len(missing)}
record={'stats':stats,'assets':assets,'missing':missing,'backup':backup.relative_to(R).as_posix(),'notes':{n:{'before_sha256':hashlib.sha256(b).hexdigest(),'after_sha256':hashlib.sha256(a).hexdigest()} for n,(b,a) in changes.items()}}
(S/'applied.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Media recovery','Recovered '+str(len(mapping))+' media-sync references in '+str(len(changes))+' notes into '+str(len(byhash))+' unique files in the root `Attachments` folder.','', '## Recovery method','The plugin media folder was empty. Exact original addresses were recovered from the same properties and image labels in saved note history. Repeated images share one attachment. Downloads were checked for a valid media signature; saved file hashes and rewritten note contents were verified.','', '## Unresolved media']
report.extend(['- `'+x['original_path']+'` in `'+x['references'][0]['note']+'`' for x in missing] or ['None.'])
report+=['','## Recovery records','Original note snapshot: `'+record['backup']+'`. Detailed source addresses, history evidence and hashes are in `media-recovery/applied.json`.']
(W/'Media recovery.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
c=json.loads((W/'config.json').read_text());c['attachments_folder']='Attachments';(W/'config.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
print(json.dumps(stats,indent=2))
