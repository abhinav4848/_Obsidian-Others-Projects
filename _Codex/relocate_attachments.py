from pathlib import Path
from collections import defaultdict,Counter
from urllib.parse import unquote,quote
from datetime import datetime,timezone
import re,json,hashlib,zipfile,os,sys
W=Path(__file__).resolve().parent;R=W.parent
EXCLUDED={'.git','.obsidian','.trash','_Codex','__pycache__'}
EXTS={'.jpg','.jpeg','.png','.gif','.webp','.svg','.pdf','.mp3','.mp4','.wav','.m4a','.ogg','.mov','.avif','.bmp','.ico'}
assets=[p for p in sorted(R.rglob('*')) if p.is_file() and p.suffix.lower() in EXTS and not any(x in EXCLUDED for x in p.relative_to(R).parts[:-1])]
notes=[p for p in sorted(R.rglob('*')) if p.is_file() and p.suffix.lower() in {'.md','.canvas','.base','.excalidraw'} and not any(x in EXCLUDED for x in p.relative_to(R).parts[:-1])]
original={p:p.read_bytes() for p in notes};hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in assets}
byrel={p.relative_to(R).as_posix().casefold():p for p in assets};byname=defaultdict(list)
for p in assets:byname[p.name.casefold()].append(p)
def resolve(current,ref):
 ref=unquote(ref).replace('\\','/')
 if re.search(r'://',ref) or re.match(r'^(?:[a-z][a-z0-9+.-]*:|//)',ref,re.I):return None
 ref=ref.split('#',1)[0].split('?',1)[0]
 if re.search(r'[<>:"|\r\n]',ref):return None
 for candidate in [(current.parent/ref).resolve(),(R/ref.lstrip('/')).resolve()]:
  if candidate.is_relative_to(R):
   found=byrel.get(candidate.relative_to(R).as_posix().casefold())
   if found:return found
 found=byname.get(Path(ref).name.casefold(),[])
 if len(found)==1:return found[0]
 if found and len({hashes[p] for p in found})==1:return found[0]
 return None

def references(note,text):
 spans=[]
 # Markdown bodies, including code fences: file links inside Excalidraw/file queries must follow moves too.
 for m in re.finditer(r'\[\[([^\]\n]+)\]\]',text):
  value=m[1].split('|',1)[0];path=value.split('#',1)[0]
  asset=resolve(note,path)
  if asset:spans.append({'start':m.start(1),'end':m.start(1)+len(path),'asset':asset,'style':'wiki','old':path})
 # Inline Markdown link targets, with balanced parentheses for PDF filenames.
 for start in re.finditer(r'!?\[[^\]\n]*\]\(',text):
  a=start.end();i=a;depth=1;escaped=False
  while i<len(text) and depth:
   ch=text[i]
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='(':depth+=1
   elif ch==')':depth-=1
   if ch=='\n':break
   if depth:i+=1
  if depth:continue
  inner=text[a:i]
  if inner.startswith('<') and '>' in inner:
   a+=1;path=inner[1:inner.index('>')]
  else:
   path=re.sub(r'\s+["\x27][^\n]*["\x27]\s*$','',inner).strip();a+=len(inner)-len(inner.lstrip())
  path=path.split('#',1)[0].split('?',1)[0]
  asset=resolve(note,path)
  if asset:spans.append({'start':a,'end':a+len(path),'asset':asset,'style':'markdown','old':path})
 # Scalar fields such as image_url, show_image_url, banner, image; plain paths in properties/JSON.
 for m in re.finditer(r'(?m)^[ \t]*(?:[A-Za-z_][\w -]*:[ \t]*|-[ \t]*)("(?:[^"\\]|\\.)*"|\x27[^\x27\n]*\x27|[^\n]+)',text):
  token=m[1].strip();a=m.start(1)
  if token.startswith(('"',"'")):
   path=token[1:-1];a+=1
  else:path=token.rstrip('\r').strip()
  path=path.split('#',1)[0].split('?',1)[0]
  asset=resolve(note,path)
  if asset:spans.append({'start':a,'end':a+len(path),'asset':asset,'style':'property','old':path})
 # Native canvas/base/Excalidraw JSON file fields.
 for m in re.finditer(r'"(?:file|path|image|background|src)"\s*:\s*"([^"\n]+)"',text):
  path=m[1].split('#',1)[0];asset=resolve(note,path)
  if asset:spans.append({'start':m.start(1),'end':m.start(1)+len(path),'asset':asset,'style':'property','old':path})
 # Reference-style Markdown links.
 for m in re.finditer(r'(?m)^\s*\[[^\]\n]+\]:\s*<?([^\s<>]+)>?',text):
  path=m[1].split('#',1)[0];asset=resolve(note,path)
  if asset:spans.append({'start':m.start(1),'end':m.start(1)+len(path),'asset':asset,'style':'markdown','old':path})
 dedup={}
 for x in spans:dedup[(x['start'],x['end'])]=x
 rows=sorted(dedup.values(),key=lambda x:x['start']);assert all(a['end']<=b['start'] for a,b in zip(rows,rows[1:])),note
 return rows
refs={p:references(p,b.decode('utf-8-sig')) for p,b in original.items()};usage=defaultdict(set)
for p,rows in refs.items():
 owner=p.relative_to(R).parts[0] if len(p.relative_to(R).parts)>1 else None
 for x in rows:
  if owner:usage[x['asset']].add(owner)
  else:raise RuntimeError('Attachment used by a root-level note; no collection to choose: '+str(p))
owners={};unreferenced=[]
for a in assets:
 owner=a.relative_to(R).parts[0]
 owners[a]=usage[a] or ({owner} if owner!='Attachments' else set())
 if not usage[a]:unreferenced.append(a.relative_to(R).as_posix())
 assert owners[a],('Unowned root attachment',a)
# Match equal bytes within a collection; use a collision-safe name for distinct content.
destinations={};pool={};occupied={};copies={}
for a in assets:
 for owner in sorted(owners[a]):
  key=(owner,hashes[a])
  if key not in pool:
   dest=R/owner/'Attachments'/a.name
   if dest.exists() and dest not in assets and hashlib.sha256(dest.read_bytes()).hexdigest()!=hashes[a]:dest=dest.with_name(dest.stem+'-'+hashes[a][:12]+dest.suffix)
   if dest.as_posix().casefold() in occupied and occupied[dest.as_posix().casefold()]!=hashes[a]:dest=dest.with_name(dest.stem+'-'+hashes[a][:12]+dest.suffix)
   assert dest.resolve().is_relative_to(R.resolve())
   occupied[dest.as_posix().casefold()]=hashes[a];pool[key]=dest;copies[dest]=a
  destinations[(a,owner)]=pool[key]
updates={};changes=[]
for p,rows in refs.items():
 text=original[p].decode('utf-8-sig');owner=p.relative_to(R).parts[0];new=text
 for x in reversed(rows):
  dest=destinations[(x['asset'],owner)]
  target=dest.relative_to(R).as_posix() if x['style']!='markdown' else os.path.relpath(dest,p.parent).replace('\\','/')
  if x['style']=='markdown':target=quote(target,safe='/.-_~')
  if target!=x['old']:
   new=new[:x['start']]+target+new[x['end']:]
   changes.append({'note':p.relative_to(R).as_posix(),'source':x['asset'].relative_to(R).as_posix(),'destination':dest.relative_to(R).as_posix(),'before':x['old'],'after':target,'style':x['style']})
 if new!=text:
  out=new.encode('utf-8');updates[p]=b'\xef\xbb\xbf'+out if original[p].startswith(b'\xef\xbb\xbf') else out
records=[{'original':a.relative_to(R).as_posix(),'sha256':hashes[a],'destinations':[destinations[(a,o)].relative_to(R).as_posix() for o in sorted(owners[a])],'referencing_collections':sorted(usage[a])} for a in assets]
stats={'original_media_files':len(assets),'collection_attachment_files':len(copies),'notes_updated':len(updates),'references_updated':len(changes),'shared_across_collections':sum(len(usage[a])>1 for a in assets),'unreferenced_files_kept_with_original_collection':len(unreferenced),'attachment_folders':dict(Counter(d.relative_to(R).parts[0] for d in copies))}
plan={'stats':stats,'assets':records,'link_changes':changes,'unreferenced':unreferenced}
(W/'attachment-relocation-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2),flush=True)
if '--apply' not in sys.argv:sys.exit()
assert not (W/'attachment-relocation-applied.json').exists(),'Already applied'
backup=W/'backups'/('collection-attachments-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
 for a in assets:z.write(a,a.relative_to(R).as_posix())
 for p in updates:z.writestr(p.relative_to(R).as_posix(),original[p])
 z.write(W/'config.json','_Codex/config.json')
with zipfile.ZipFile(backup) as z:assert z.testzip() is None
for dest,source in copies.items():
 dest.parent.mkdir(parents=True,exist_ok=True)
 data=source.read_bytes();assert hashlib.sha256(data).hexdigest()==hashes[source]
 if dest.exists():assert hashlib.sha256(dest.read_bytes()).hexdigest()==hashes[source],dest
 else:
  temp=W/'attachment-copy.tmp';temp.write_bytes(data);os.replace(temp,dest)
for p,out in updates.items():
 assert p.read_bytes()==original[p],'Concurrent note edit: '+str(p)
 temp=W/'attachment-note.tmp';temp.write_bytes(out);os.replace(temp,p)
for p,out in updates.items():assert p.read_bytes()==out,p
for dest,source in copies.items():assert hashlib.sha256(dest.read_bytes()).hexdigest()==hashes[source],dest
for change in changes:assert (R/change['destination']).is_file(),change
# Every original reference now identifies its owner's verified destination.
for p,rows in refs.items():
 text=p.read_bytes().decode('utf-8-sig');owner=p.relative_to(R).parts[0]
 for x in rows:
  dest=destinations[(x['asset'],owner)]
  target=dest.relative_to(R).as_posix() if x['style']!='markdown' else quote(os.path.relpath(dest,p.parent).replace('\\','/'),safe='/.-_~')
  assert target in text,(p,target)
kept=set(copies)
for a in assets:
 if a in kept:continue
 assert a.resolve().is_relative_to(R.resolve()) and a.is_file()
 assert hashlib.sha256(a.read_bytes()).hexdigest()==hashes[a]
 a.unlink()
# Remove only the old, now-empty media directories; never recurse/delete parent note folders.
import stat
for directory in sorted({a.parent for a in assets},key=lambda x:len(x.parts),reverse=True):
 if directory.exists() and directory not in {d.parent for d in kept} and not any(directory.iterdir()):
  assert directory.resolve().is_relative_to(R.resolve()) and directory!=R
  try:directory.rmdir()
  except PermissionError:directory.chmod(stat.S_IWRITE);directory.rmdir()
plan['backup']=backup.relative_to(R).as_posix();plan['verification']={'attachment_bytes_preserved':True,'updated_note_bytes_verified':True,'every_original_reference_has_a_verified_destination':True,'original_files_removed_only_after_destination_and_link_verification':True}
plan['note_hashes']={p.relative_to(R).as_posix():{'before':hashlib.sha256(original[p]).hexdigest(),'after':hashlib.sha256(out).hexdigest()} for p,out in updates.items()}
(W/'attachment-relocation-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
c=json.loads((W/'config.json').read_text(encoding='utf-8'));c['attachments_folder']='Attachments';c['attachments_location']='collection root';c['attachment_folders']={owner:owner+'/Attachments' for owner in stats['attachment_folders']};c['shared_attachment_policy']='One file per collection, shared among notes in that collection';(W/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Moved attachments and verified updated references.',flush=True)
