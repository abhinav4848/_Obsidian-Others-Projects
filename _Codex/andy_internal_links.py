from pathlib import Path
from collections import defaultdict,Counter
from urllib.parse import urlsplit,parse_qsl,unquote
from datetime import datetime,timezone
import re,json,unicodedata,hashlib,zipfile,os,yaml,sys
W=Path(__file__).resolve().parent;R=W.parent;F=R/'Andy Matuschak'
sys.path.insert(0,str(W));from andy_cleanup import shorten
from heading_spacing import trim
URL=re.compile(r'https?://[^\s<>\)\]"\}]+')
LINK=re.compile(r'(?<!!)\[((?:\\.|[^\]\\])*)\]\((https?://(?:[^\s()]|\([^()]*\))+)(?:\s+"[^"]*")?\)')
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('_',' ').replace('’',"'").replace('“','"').replace('”','"').replace('–','-').replace('—','-')
 return re.sub(r'\s+',' ',s).strip().casefold()
def identity(u):
 s=urlsplit(u.replace('&amp;','&'))
 if s.hostname=='notes.andymatuschak.org':return ('andy-note',([unquote(s.path).strip('/')]+[v for k,v in parse_qsl(s.query) if k=='stackedNotes'])[-1])
 return ((s.hostname or '').casefold().removeprefix('www.'),unquote(s.path).rstrip('/'),s.query)
def front(t):
 if t.startswith('---\n') or t.startswith('---\r\n'):
  m=re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n',t,re.S)
  if m:return m[0],t[m.end():]
 return '',t
def props(t):
 fm,_=front(t)
 try:return yaml.safe_load(fm.strip('-\r\n')) or {}
 except Exception:return {}
files=sorted(F.rglob('*.md')); before={p:p.read_bytes() for p in files};texts={p:b.decode('utf-8-sig') for p,b in before.items()};names=defaultdict(set);ids=defaultdict(set);sourceurls={}
for p,t in texts.items():
 fm,body=front(t);pr=props(t); ns=[p.stem]+re.findall(r'^#\s+(.+?)\s*$',body,re.M)[:1]
 aliases=pr.get('aliases',[]);ns+=aliases if isinstance(aliases,list) else [aliases] if isinstance(aliases,str) else []
 for n in ns:names[norm(n)].add(p)
 source=[]
 for k in ['URL','URLs','url','urls','source','Source']:
  v=pr.get(k,[]);source+=URL.findall(str(v))
 for line in body.splitlines():
  if re.match(r'^\s*[-*]?\s*Source for this file:',line):source+=URL.findall(line)
 sourceurls[p]=source
 for u in source:ids[identity(u)].add(p)
changes=[];skipped=[];additions=defaultdict(dict);after={};new_id_targets=defaultdict(set)
for p,t in texts.items():
 fm,body=front(t);lines=[];fence=None
 for ln,line in enumerate(body.splitlines(keepends=True),1):
  fmch=re.match(r'^\s*(`{3,}|~{3,})',line)
  if fmch:
   if fence is None:fence=fmch[1][0]
   elif fmch[1][0]==fence:fence=None
   lines.append(line);continue
  if fence or re.match(r'^\s*[-*]?\s*Source for this file:',line):lines.append(line);continue
  inline=[m.span() for m in re.finditer(r'(`+).*?\1',line)]
  def convert(m):
   if any(a<=m.start()<b for a,b in inline):return m[0]
   label=m[1];u=m[2]; ident=identity(u); byurl=ids.get(ident,set());byname=names.get(norm(label),set())
   byslug=set()
   if ident[0]=='andy-note' and not re.match(r'^z[A-Za-z0-9]+$',ident[1]):byslug=names.get(norm(ident[1]),set())
   candidates=byurl or byname or byslug
   if len(candidates)>1:
    narrowed=candidates & (byname or byslug)
    if len(narrowed)==1:candidates=narrowed
   if len(candidates)!=1:
    if candidates:skipped.append({'note':p.relative_to(R).as_posix(),'label':label,'URL':u,'reason':'ambiguous destination','candidates':[x.name for x in candidates]})
    return m[0]
   dest=next(iter(candidates))
   if dest==p:return m[0]
   if not byurl and ident[0]!='andy-note':
    skipped.append({'note':p.relative_to(R).as_posix(),'label':label,'URL':u,'reason':'topic name matches, but a different website does not establish the same captured article'});return m[0]
   # A known URL identity contradicting an exact label is not resolved by guesswork.
   if byurl and byname and not byurl & byname:
    skipped.append({'note':p.relative_to(R).as_posix(),'label':label,'URL':u,'reason':'URL identity and link title disagree'});return m[0]
   new_id_targets[ident].add(dest)
   if ident not in {identity(x) for x in URL.findall(texts[dest])}:additions[dest][ident]=shorten(u)
   changes.append({'note':p.relative_to(R).as_posix(),'destination':dest.relative_to(R).as_posix(),'label':label,'URL':u,'match':'source URL identity' if byurl else 'exact title' if byname else 'exact URL title'})
   cleanlabel=label.replace('|','\\|').replace('\\[','[').replace('\\]',']')
   target=dest.relative_to(R).with_suffix('').as_posix()
   return '[['+target+'|'+cleanlabel+']]'
  lines.append(LINK.sub(convert,line))
 after[p]=fm+''.join(lines)
conflicts={i for i,targets in new_id_targets.items() if len(targets)>1}
if conflicts:raise RuntimeError('One newly inferred URL points to different notes; review before applying')
source_records=[]
for p,urls in additions.items():
 text=after[p];fm,body=front(text);nl='\r\n' if '\r\n' in text else '\n'
 entries=nl.join('- Source for this file: [Original article]('+u+')' for u in urls.values())+nl
 heading=re.search(r'^#{1,6}\s+References?\s*\r?\n',body,re.M|re.I)
 if heading:body=body[:heading.end()]+entries+body[heading.end():].lstrip('\r\n')
 else:body=body.rstrip()+nl+nl+'## References'+nl+entries
 after[p]=fm+body;source_records.append({'note':p.relative_to(R).as_posix(),'URLs':list(urls.values())})
outputs={}
for p,t in after.items():
 b=t.encode('utf-8');b=(b'\xef\xbb\xbf'+b) if before[p].startswith(b'\xef\xbb\xbf') else b
 if b!=before[p]:outputs[p]=trim(b)[0]
plan={'stats':{'links_to_convert':len(changes),'notes_to_update':len(outputs),'notes_receiving_sources':len(source_records),'ambiguous_links_skipped':len(skipped)},'links':changes,'source_additions':source_records,'skipped':skipped}
(W/'andy-internal-links-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(plan['stats'],indent=2))
if '--apply' in sys.argv:
 assert not (W/'andy-internal-links-applied.json').exists(),'Already applied'
 backup=W/'backups'/('andy-internal-links-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
 with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
  for p in outputs:z.writestr(p.relative_to(R).as_posix(),before[p])
 for p,b in outputs.items():
  assert p.read_bytes()==before[p]
  temp=W/'andy-links-write.tmp';temp.write_bytes(b);os.replace(temp,p);assert p.read_bytes()==b
 for c in changes:assert (R/c['destination']).is_file()
 plan['backup']=backup.relative_to(R).as_posix();plan['hashes']={p.relative_to(R).as_posix():{'before':hashlib.sha256(before[p]).hexdigest(),'after':hashlib.sha256(b).hexdigest()} for p,b in outputs.items()}
 (W/'andy-internal-links-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 report=['# Andy internal links',str(len(changes))+' external links now point to existing Andy notes. '+str(len(source_records))+' destination notes received missing source addresses under References, labelled “Source for this file”.','', '## Matching','Links were matched by existing source identity, exact note title/alias, or exact readable URL title. Original link wording was preserved. Navigation sources retain at most three notes. Self-source links, code and properties were preserved.','', '## Links needing review']
 report += ['- `'+x['note']+'`: ['+x['label']+']('+x['URL']+') — '+x['reason'] for x in skipped] or ['None.']
 report+=['','## Recovery','Original changed notes: `'+plan['backup']+'`. Full decisions and hashes: `andy-internal-links-applied.json`.']
 (W/'Andy internal links.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
