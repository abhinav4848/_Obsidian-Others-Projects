from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from urllib.parse import urlsplit
import sys,re,json,hashlib,zipfile,os,yaml
W=Path(__file__).resolve().parent;R=W.parent
sys.path.insert(0,str(W));from heading_spacing import trim
from andy_cleanup import shorten,trail,clean_url,source_line,remove_empty_source_headings
EXCLUDED={'.git','.obsidian','.trash','__pycache__'}
IMPORT=re.compile(r'^(Type of Link|Completion Status|Last edited time):[^\n]*(?:\n|$)|^Author:[ \t]*Andy Matuschak[ \t]*(?:\n|$)',re.M)
URL=re.compile(r'https?://[^\s<>\)\]"\}]+')
def front(t):
 m=re.match(r'\A---[ \t]*\n(.*?)\n(?:---|\.\.\.)[ \t]*(?:\n|$)',t,re.S)
 return (m[1],t[m.end():]) if m else (None,t)
def property_blocks(fm):
 if fm is None:return []
 starts=list(re.finditer(r'^(?:[A-Za-z_][\w -]*|"[^"\n]+"|\x27[^\x27\n]+\x27):',fm,re.M));out=[]
 for i,m in enumerate(starts):
  end=starts[i+1].start() if i+1<len(starts) else len(fm)
  out.append((m[0][:-1].strip('"\x27'),m.start(),end,fm[m.start():end]))
 return out
def set_prop(fm,key,value):
 fm='' if fm is None else fm
 block=key+': '+json.dumps(value,ensure_ascii=False)+'\n'
 matching=[b for b in property_blocks(fm) if b[0].casefold()==key.casefold()]
 if matching:
  first=matching[0][1]
  for _,a,b,_ in reversed(matching):fm=fm[:a]+fm[b:]
  fm=fm[:first]+block+fm[first:]
 else:fm=fm.rstrip('\n')+('\n' if fm else '')+block
 return fm.rstrip('\n')
def outside_lines(body):
 fence=None
 for i,line in enumerate(body.splitlines(keepends=True)):
  mark=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)',line)
  if fence:
   if mark and mark[1][0]==fence[0] and len(mark[1])>=fence[1] and not mark[2].strip():fence=None
   yield i,line,False;continue
  if mark:fence=(mark[1][0],len(mark[1]));yield i,line,False;continue
  yield i,line,True
def source_cleanup(p,fm,body):
 removed=[];sources=[];newlines=[];section=None
 for _,line,safe in outside_lines(body):
  if not safe:newlines.append(line);continue
  h=re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$',line.strip())
  if h:
   if section and len(h[1])<=section:section=None
   if h[2].casefold() in {'source','sources','original source','source url'}:section=len(h[1])
   newlines.append(line);continue
  urls=URL.findall(line)
  explicit=bool(section or re.match(r'^\s*[-*]?\s*Source for this file:',line,re.I) or source_line(line))
  # Named self-links in a source footer are another import format.
  self_link=re.match(r'^\s*(?:[-*]|\d+\.)?\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*$',line)
  if self_link and self_link[1].casefold()==p.stem.casefold():explicit=True
  if explicit and urls:
   sources+=urls;removed.append(line.rstrip());continue
  newlines.append(line)
 body=remove_empty_source_headings(''.join(newlines))
 existing=[]
 for key,_,_,block in property_blocks(fm):
  if key in {'URL','URLs','url','urls','source','Source'}:existing+=URL.findall(block)
 if not sources:return fm,body,{'source_lines_moved':0}
 candidates=[shorten(clean_url(u)) for u in existing+sources]
 groups={}
 for u in candidates:
  key=('andy',trail(u)[-1]) if urlsplit(u).hostname=='notes.andymatuschak.org' else u
  if key not in groups or len(trail(u))>len(trail(groups[key])):groups[key]=u
 chosen=list(groups.values())
 # Consolidate recognized URL/source fields while retaining other metadata verbatim.
 for key,a,b,_ in reversed(property_blocks(fm)):
  if key in {'URL','URLs','url','urls','source','Source'}:fm=fm[:a]+fm[b:]
 fm=set_prop(fm,'URL',chosen[0] if len(chosen)==1 else chosen)
 return fm,body,{'source_lines_moved':len(removed),'moved_sources':sources,'final_URL':chosen,'source_identities':len(chosen)}
def transform(p,data):
 raw=data.decode('utf-8-sig');nl='\r\n' if '\r\n' in raw else '\n';t=raw.replace('\r\n','\n');fm,body=front(t);record={'path':p.relative_to(R).as_posix()}
 if p.is_relative_to(R/'Andy Matuschak'):
  count=0;lines=[]
  for _,line,safe in outside_lines(body):
   if safe and IMPORT.fullmatch(line):count+=1
   else:lines.append(line)
  body=''.join(lines);record['import_lines_removed']=count
  # These literal imported fields can also occur as YAML properties.
  for key,a,b,block in reversed(property_blocks(fm)):
   if key in {'Type of Link','Completion Status','Last edited time'} or (key=='Author' and re.search(r'Author:\s*["\x27]?Andy Matuschak["\x27]?\s*$',block.strip())):
    fm=fm[:a]+fm[b:];record['import_lines_removed']+=1
  fm,body,src=source_cleanup(p,fm,body);record.update(src)
 fm=set_prop(fm,'title',p.stem)
 headings=[(i,line,re.match(r'^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$',line.rstrip())) for i,line,safe in outside_lines(body) if safe and re.match(r'^ {0,3}#{1,6}\s+',line)]
 first=headings[0] if headings else None
 if first and first[2][2]==p.stem:
  if len(first[2][1])!=1:
   ls=body.splitlines(keepends=True);ls[first[0]]='# '+p.stem+'\n';body=''.join(ls);record['heading_action']='promoted_matching_heading'
  else:record['heading_action']='already_matches'
 else:
  body='# '+p.stem+'\n'+body.lstrip('\n');record['heading_action']='added_filename_heading'
 output='---\n'+fm.rstrip('\n')+'\n---\n'+body.lstrip('\n');output=output.replace('\n',nl).encode('utf-8')
 if data.startswith(b'\xef\xbb\xbf'):output=b'\xef\xbb\xbf'+output
 output=trim(output)[0]
 return output,record
files=[p for p in sorted(R.rglob('*.md')) if not any(x in EXCLUDED for x in p.relative_to(R).parts[:-1])]
original={p:p.read_bytes() for p in files};updates={};records=[]
for p,data in original.items():
 out,record=transform(p,data);records.append(record)
 if out!=data:updates[p]=out
stats={'notes_scanned':len(files),'notes_updated':len(updates),'andy_import_lines_removed':sum(x.get('import_lines_removed',0) for x in records),'andy_source_lines_moved':sum(x.get('source_lines_moved',0) for x in records),'andy_notes_with_sources_moved':sum(x.get('source_lines_moved',0)>0 for x in records),'heading_actions':dict(Counter(x['heading_action'] for x in records))}
plan={'stats':stats,'notes':records};(W/'note-titles-and-sources-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))
if '--apply' in sys.argv:
 assert not (W/'note-titles-and-sources-applied.json').exists(),'Already applied'
 backup=W/'backups'/('note-titles-and-sources-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
 with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
  for p in updates:z.writestr(p.relative_to(R).as_posix(),original[p])
 with zipfile.ZipFile(backup) as z:assert z.testzip() is None
 for p,out in updates.items():
  assert p.resolve().is_relative_to(R.resolve()) and p.read_bytes()==original[p]
  temp=W/'note-update.tmp';temp.write_bytes(out);os.replace(temp,p)
 for p in files:
  b=p.read_bytes();fm,body=front(b.decode('utf-8-sig').replace('\r\n','\n'));pr=yaml.safe_load(fm) if 'x/Templates' not in p.relative_to(R).as_posix() else None
  if pr is not None:assert pr.get('title')==p.stem,p
  # Literal JSON string remains valid YAML even in templates with unexpanded placeholders.
  tb=next(block for key,_,_,block in property_blocks(fm) if key=='title');assert json.loads(tb.split(':',1)[1].strip())==p.stem,p
  headings=[re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$',line.rstrip()) for _,line,safe in outside_lines(body) if safe and re.match(r'^ {0,3}#{1,6}\s+',line)]
  assert headings[0][1]==p.stem,p
  assert trim(b)==(b,0),p
  if p in updates:assert b==updates[p],p
 plan['backup']=backup.relative_to(R).as_posix();plan['hashes']={p.relative_to(R).as_posix():{'before':hashlib.sha256(original[p]).hexdigest(),'after':hashlib.sha256(out).hexdigest()} for p,out in updates.items()}
 (W/'note-titles-and-sources-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Applied and verified',len(updates),'notes')
