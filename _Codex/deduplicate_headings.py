from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,timezone
from urllib.parse import unquote
import re,json,unicodedata,hashlib,zipfile,os,sys
W=Path(__file__).resolve().parent;R=W.parent
sys.path.insert(0,str(W));from heading_spacing import trim
EXCLUDED={'.git','.obsidian','.trash','__pycache__'}
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('_',' ')
 s=re.sub(r'\bw/\s*','with ',s,flags=re.I).replace('&',' and ')
 return re.sub(r'[^\w]+',' ',s).strip().casefold()
def split(data):
 t=data.decode('utf-8-sig');m=re.match(r'\A---\r?\n.*?\r?\n(?:---|\.\.\.)\r?\n',t,re.S)
 return (m[0],t[m.end():]) if m else ('',t)
def headings(body):
 fence=None
 for i,line in enumerate(body.splitlines(keepends=True)):
  mark=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)',line)
  if fence:
   if mark and mark[1][0]==fence[0] and len(mark[1])>=fence[1] and not mark[2].strip():fence=None
   continue
  if mark:fence=(mark[1][0],len(mark[1]));continue
  h=re.match(r'^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$',line.rstrip('\r\n'))
  if h:yield {'line':i,'title':h[2],'level':len(h[1]),'raw':line}
def keys(p,fm):
 out={norm(p.stem)}
 # A note number/date is part of the retained filename but not a second page title.
 short=re.sub(r'^(?:\d{4}-\d{2}-\d{2}|\d{12}|\d{1,4}[a-z]?)\s*[- ]\s*','',p.stem,flags=re.I)
 if short!=p.stem:out.add(norm(short))
 # Snipd's exported episode property retains the full title if the filename was truncated.
 if p.is_relative_to(R/'Snipd'):
  import yaml
  try:
   pr=yaml.safe_load(fm.strip('\r\n-')) or {};full=pr.get('episode_title')
   if isinstance(full,str) and norm(full).startswith(norm(p.stem)):out.add(norm(full))
  except Exception:pass
 return out
files=[p for p in sorted(R.rglob('*.md')) if not any(x in EXCLUDED for x in p.relative_to(R).parts[:-1])]
original={p:p.read_bytes() for p in files};textupdates={};removed={};decisions=[]
for p,data in original.items():
 fm,body=split(data);hs=list(headings(body))
 if not hs:continue
 assert hs[0]['title']==p.stem,('Filename heading changed',p,hs[0]['title'])
 k=keys(p,fm);duplicates=[h for h in hs[1:] if norm(h['title']) in k]
 if not duplicates:continue
 indices={h['line'] for h in duplicates};lines=body.splitlines(keepends=True)
 newbody=''.join(line for i,line in enumerate(lines) if i not in indices)
 # Delete only verified title lines; all prose, media and section headings remain.
 assert [line for i,line in enumerate(lines) if i not in indices]==newbody.splitlines(keepends=True)
 textupdates[p]=fm+newbody;removed[p]=duplicates
 decisions.append({'path':p.relative_to(R).as_posix(),'kept_heading':p.stem,'removed_headings':[{'line_in_body':h['line']+1,'text':h['title']} for h in duplicates]})
byrel={p.relative_to(R).with_suffix('').as_posix().casefold():p for p in files};byname=defaultdict(list)
for p in files:byname[p.stem.casefold()].append(p)
def resolve(current,name):
 if not name:return current
 name=unquote(name).replace('\\','/').removesuffix('.md').strip('/')
 candidates=[name,(current.parent.relative_to(R)/name).as_posix()]
 for c in candidates:
  found=byrel.get(c.casefold())
  if found:return found
 arr=byname.get(name.casefold(),[]) if '/' not in name else []
 return arr[0] if len(arr)==1 else None
repairs=[]
WIKI=re.compile(r'\[\[([^\]#|]*)(?:#([^\]|]+))(?P<alias>\|[^\]]*)?\]\]')
for p,data in original.items():
 text=textupdates.get(p,data.decode('utf-8-sig'));lines=[];fence=None;fm=True if text.startswith('---') else False
 for i,line in enumerate(text.splitlines(keepends=True)):
  if fm:
   if i>0 and line.strip() in {'---','...'}:fm=False
   lines.append(line);continue
  mark=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)',line)
  if fence:
   if mark and mark[1][0]==fence[0] and len(mark[1])>=fence[1] and not mark[2].strip():fence=None
   lines.append(line);continue
  if mark:fence=(mark[1][0],len(mark[1]));lines.append(line);continue
  inline=[m.span() for m in re.finditer(r'(`+).*?\1',line)]
  def repair(m):
   if any(a<=m.start()<b for a,b in inline):return m[0]
   ref,fragment=m[1],m[2];dest=resolve(p,ref)
   if dest not in removed or fragment.startswith('^') or fragment==dest.stem:return m[0]
   if norm(fragment) not in {norm(x['title']) for x in removed[dest]}:return m[0]
   out='[['+ref+'#'+dest.stem+(m['alias'] or '')+']]'
   repairs.append({'note':p.relative_to(R).as_posix(),'destination':dest.relative_to(R).as_posix(),'before':m[0],'after':out});return out
  lines.append(WIKI.sub(repair,line))
 result=''.join(lines)
 if result!=data.decode('utf-8-sig'):textupdates[p]=result
updates={}
for p,t in textupdates.items():
 out=t.encode('utf-8');out=b'\xef\xbb\xbf'+out if original[p].startswith(b'\xef\xbb\xbf') else out
 out=trim(out)[0];updates[p]=out
 assert split(out)[0]==split(original[p])[0],('Properties changed',p)
 assert list(headings(split(out)[1]))[0]['title']==p.stem,p
 assert not any(norm(h['title']) in keys(p,split(out)[0]) for h in list(headings(split(out)[1]))[1:]),p
stats={'notes_scanned':len(files),'notes_with_duplicate_titles':len(removed),'duplicate_headings_removed':sum(len(v) for v in removed.values()),'heading_links_updated':len(repairs),'files_updated':len(updates),'collections':dict(Counter(d['path'].split('/')[0] for d in decisions))}
plan={'stats':stats,'headings':decisions,'heading_link_repairs':repairs}
(W/'duplicate-headings-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))
if '--apply' not in sys.argv:sys.exit()
assert not (W/'duplicate-headings-applied.json').exists(),'Already applied'
backup=W/'backups'/('duplicate-headings-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
 for p in updates:z.writestr(p.relative_to(R).as_posix(),original[p])
with zipfile.ZipFile(backup) as z:assert z.testzip() is None
for p,out in updates.items():
 assert p.resolve().is_relative_to(R.resolve()) and p.read_bytes()==original[p],p
 temp=W/'heading-dedup.tmp';temp.write_bytes(out);os.replace(temp,p)
for p,out in updates.items():assert p.read_bytes()==out,p
plan['backup']=backup.relative_to(R).as_posix();plan['hashes']={p.relative_to(R).as_posix():{'before':hashlib.sha256(original[p]).hexdigest(),'after':hashlib.sha256(out).hexdigest()} for p,out in updates.items()}
plan['verification']={'filename_heading_retained':True,'title_and_URL_properties_unchanged':True,'all_equivalent_duplicate_titles_removed':True,'code_fences_preserved':True,'saved_note_bytes_verified':True}
(W/'duplicate-headings-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
config=json.loads((W/'config.json').read_text(encoding='utf-8'));config['markdown_style']['duplicate_page_title_headings']=False;(W/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Applied and verified.',flush=True)
