from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, unquote, quote, urlunsplit
from datetime import datetime, timezone
import hashlib,json,os,re,sys,unicodedata,zipfile
import yaml
from heading_spacing import trim

ROOT=Path(__file__).resolve().parent.parent.resolve();WORK=ROOT/'_Codex';TASK=WORK/'letters-integration';ANDY=ROOT/'Andy Matuschak'
sources=json.loads((WORK/'patreon-import/sources.json').read_text(encoding='utf-8'))['sources']
letters=[ANDY/(s['title']+'.md') for s in sources if s['date']!='2023-08-01']
assets=json.loads((TASK/'assets-ready.json').read_text(encoding='utf-8'))['assets']
INDEX='Patron letters on memory system experiments'
LINK=re.compile(r'(?<!!)\[([^]\r\n]+)\]\((https?://[^\s)]+)\)')
URL_BLOCK=re.compile(r'^URL:[^\r\n]*(?:\r?\n(?:[ \t]+[^\r\n]*|))*(?=\r?\n[^ \t\r\n]|\Z)',re.M)
def norm(s):return re.sub(r'[^\w]+',' ',unicodedata.normalize('NFKC',s)).strip().casefold()
def front(text):
 m=re.match(r'\A(\ufeff?---\r?\n)(.*?)(\r?\n---\r?\n)',text,re.S);assert m
 return m,yaml.safe_load(m[2]) or {},text[m.end():]
def canonical(url):
 p=urlsplit(url);return urlunsplit(('https',p.netloc.lower(),quote(unquote(p.path),safe="/,:@'()-"),p.query,''))
def identity(url):
 p=urlsplit(url)
 if p.netloc.lower()=='notes.andymatuschak.org':
  return ('andy',([unquote(p.path).strip('/')]+[v for k,v in parse_qsl(p.query) if k=='stackedNotes'])[-1])
 if p.netloc.lower() in {'patreon.com','www.patreon.com'} and '/posts/' in p.path:
  m=re.search(r'(?:/|-)(\d+)/?$',p.path)
  if m:return ('patreon',m[1])
 return ('URL',canonical(url))
def wiki(target,label):return '[[Andy Matuschak/'+target+'|'+label+']]'
note_map={};title_map={};pdf_notes={}
for p in ANDY.glob('*.md'):
 _,props,body=front(p.read_text(encoding='utf-8-sig'))
 for url in props.get('URL',[]):
  note_map.setdefault(identity(url),set()).add(p.stem)
  if '.pdf' in url:pdf_notes[canonical(url)]=p.stem
 for title in [p.stem,*([props.get('aliases')] if isinstance(props.get('aliases'),str) else props.get('aliases',[]) or [])]:title_map.setdefault(norm(title),set()).add(p.stem)
for s in sources:
 for key in ['Andy_URL','Patreon_URL']:note_map[identity(s[key])]={s['title']}
note_map[('andy','zY3RYK9gJ6eDnq27vSwBDQh')]={INDEX}
asset_map={canonical(a['URL']):a for a in assets}
def resolve(url,label):
 candidates=note_map.get(identity(url),set())
 if len(candidates)==1:return next(iter(candidates))
 exact=candidates&title_map.get(norm(label),set())
 return next(iter(exact)) if len(exact)==1 else None

def footnote_parts(body):
 heading=re.search(r'^#{1,6}\s+Footnotes\s*\r?$',body,re.M)
 if heading:
  end=body.find('\n',heading.end());end=len(body) if end<0 else end+1
  prefix,tail=body[:heading.start()],body[end:]
 else:
  starts=list(re.finditer(r'^\[\^?\d+\](?::| )',body,re.M))
  if not starts:return body,'',None,[]
  assert starts[0].start()>len(body)*.6, 'Uncertain footnote region'
  prefix,tail=body[:starts[0].start()],body[starts[0].start():]
  heading=None
 lines=tail.splitlines(keepends=True);defs=[]
 for i,line in enumerate(lines):
  m=re.match(r'^(?:\[\^?(\d+)\](?::)?[ \t]+|(\d+)\.[ \t]+|(\d+)[\u00a0 \t]+)(.*?)(\r?\n)?$',line)
  if m:defs.append({'number':int(m[1] or m[2] or m[3]),'line':i,'content':m[4],'newline':m[5] or ''})
 if not defs:return body,'',None,[]
 nums=[d['number'] for d in defs];assert nums==list(range(1,len(nums)+1)),nums
 return prefix,tail,heading,defs

def footnotes(body,title):
 prefix,tail,heading,defs=footnote_parts(body)
 if not defs:return body,0
 for d in defs:
  n=str(d['number'])
  prefix=re.sub(r'\[\[(?:Andy Matuschak/)?('+re.escape(title)+'|'+re.escape(INDEX)+r')\|'+n+r'\]\]', '[^'+n+']',prefix)
  prefix=re.sub(r'\['+n+r'\. See Footnotes\]', '[^'+n+']',prefix)
  prefix=re.sub(r'(?<!\[)\['+n+r'\](?![\](])', '[^'+n+']',prefix)
 lines=tail.splitlines(keepends=True)
 for d in defs:lines[d['line']]='[^'+str(d['number'])+']: '+d['content']+d['newline']
 nl='\r\n' if '\r\n' in body else '\n'
 result=prefix+'## Footnotes'+nl+''.join(lines)
 for d in defs:assert re.search(r'\[\^'+str(d['number'])+r'\](?!:)',prefix), (title,d['number'])
 return result,len(defs)

def concept_links(body):
 added=[]
 for phrase,target in [('reading comprehension','Reading comprehension'),('self-explanation','Self-explanation'),('retrieval practice','Retrieval practice'),('mnemonic medium','Mnemonic medium'),('spaced repetition memory systems','Spaced repetition memory systems')]:
  if not (ANDY/(target+'.md')).exists() or re.search(r'\[\[(?:Andy Matuschak/)?'+re.escape(target)+r'(?:\||\]\])',body):continue
  blocked=[(m.start(),m.end()) for m in re.finditer(r'\[\[.*?\]\]|!?\[[^]\n]*\]\([^\n]*?\)|https?://[^\s]+|`[^`\n]*`|```[\s\S]*?```|~~~[\s\S]*?~~~',body)]
  boundary=body.find('## Footnotes');boundary=len(body) if boundary<0 else boundary
  for m in re.finditer(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',body,re.I):
   start=body.rfind('\n',0,m.start())+1
   if m.start()>=boundary or body[start:m.start()].lstrip().startswith('#') or any(a<=m.start()<b for a,b in blocked):continue
   body=body[:m.start()]+wiki(target,m[0])+body[m.end():];added.append(target);break
 return body,added

def display_plain(body,title):
 prefix,tail,_,defs=footnote_parts(body)
 if defs:
  lines=tail.splitlines(keepends=True)
  for d in defs:lines[d['line']]='[fn:'+str(d['number'])+']: '+d['content']+d['newline']
  for d in defs:
   n=str(d['number'])
   prefix=re.sub(r'\[\[(?:Andy Matuschak/)?(?:'+re.escape(title)+'|'+re.escape(INDEX)+r')\|'+n+r'\]\]', '[fn:'+n+']',prefix)
   prefix=re.sub(r'\['+n+r'\. See Footnotes\]', '[fn:'+n+']',prefix)
   prefix=re.sub(r'\[\^'+n+r'\]|(?<!\[)\['+n+r'\](?![\](])', '[fn:'+n+']',prefix)
  body=prefix+''.join(lines)
 body=re.sub(r' \(PDF: \[\[Andy Matuschak/Attachments/[^]]+\]\]\)','',body)
 body=re.sub(r'!\[\[Andy Matuschak/Attachments/[^]]+\]\]|!\[[^]]*\]\(https?://[^)]+\)','<image>',body)
 body=LINK.sub(lambda m:m[1],body)
 body=re.sub(r'\[\[([^]|]+)(?:\|([^]]+))?\]\]',lambda m:m[2] or m[1],body)
 return [l for l in body.splitlines() if l.strip()]

def build():
 originals={};updates={};rows=[];introduced=[]
 for p in letters:
  relative=p.relative_to(ROOT).as_posix();original=p.read_bytes();text=original.decode('utf-8');fm,props,body=front(text);before=body;stats={'note':relative,'links':[]}
  body,count=footnotes(body,p.stem);stats['footnotes']=count
  def image_replace(m):
   asset=asset_map.get(canonical(m[2]));assert asset,(p.stem,m[2])
   target=asset['destination'];introduced.append(target);return '![['+target+']]'
  body=re.sub(r'!\[([^]\r\n]*)\]\((https?://[^)]+)\)',image_replace,body)
  def replace(m):
   url,label=m[2],m[1];asset=asset_map.get(canonical(url))
   if asset and asset['kind']=='PDF':
    fragment=urlsplit(url).fragment
    target=asset['destination']+('#'+fragment if fragment.startswith('page=') else '')
    after=body[m.end():m.end()+260]
    if asset['destination'] in after and re.match(r'^\s*(?:\(?PDF:\s*)?\[\[',after):return m[0]
    reference=pdf_notes.get(canonical(url));main=wiki(reference,label) if reference else m[0]
    if reference:stats['links'].append({'URL':url,'target':reference,'label':label});introduced.append('Andy Matuschak/'+reference+'.md')
    introduced.append(target);return main+' (PDF: [['+target+']])'
   target=resolve(url,label)
   if target:
    stats['links'].append({'URL':url,'target':target,'label':label});introduced.append('Andy Matuschak/'+target+'.md')
    return wiki(target,label)
   return m[0]
  body=LINK.sub(replace,body)
  body,concepts=concept_links(body);stats['concepts']=concepts
  assert display_plain(before,p.stem)==display_plain(body,p.stem), 'Prose changed: '+p.stem
  out,blanks=trim((text[:fm.end()]+body).encode('utf-8'));stats['heading_blank_lines_removed']=blanks
  _,new_props,new_body=front(out.decode('utf-8'))
  assert new_props==props and props['title']==p.stem and isinstance(props['URL'],list)
  assert re.findall(r'^# (.+)$',new_body,re.M)==[p.stem]
  assert not re.search(r'!\[[^]]*\]\(https?://',new_body)
  if out!=original:originals[relative]=original;updates[relative]=out
  rows.append(stats)
 return originals,updates,rows,introduced

def main():
 assert not (TASK/'applied.json').exists(),'Already applied'
 originals,updates,rows,introduced=build()
 new={a['destination']:a for a in assets if a.get('install')}
 for target in introduced:
  path=target.split('#',1)[0];assert (ROOT/path).is_file() or path in new,target
 plan={'scope':'18 remaining indexed Patreon letters','letters':rows,'introduced_targets':introduced,'assets':assets,'hashes':[{'path':p,'before':hashlib.sha256(originals[p]).hexdigest(),'after':hashlib.sha256(b).hexdigest()} for p,b in updates.items()]}
 (TASK/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'letters_updated':len(updates),'external_links_converted':sum(len(r['links']) for r in rows),'concept_links_added':sum(len(r['concepts']) for r in rows),'footnotes':sum(r['footnotes'] for r in rows),'heading_blank_lines_removed':sum(r['heading_blank_lines_removed'] for r in rows),'new_assets':len(new)},indent=2))
 if '--apply' not in sys.argv:return
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');backup=WORK/'backups'/('remaining-letters-before-'+stamp+'.zip')
 with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
  for p,b in originals.items():z.writestr(p,b)
  z.writestr('_Codex/letters-integration/new-assets.json',json.dumps(list(new),ensure_ascii=False,indent=2))
 with zipfile.ZipFile(backup) as z:
  assert z.testzip() is None
  for p,b in originals.items():assert z.read(p)==b
 for p,b in originals.items():assert (ROOT/p).read_bytes()==b,'Concurrent edit: '+p
 temp=TASK/'update.tmp'
 for dest,a in new.items():
  path=(ROOT/dest).resolve();assert path.is_relative_to((ANDY/'Attachments').resolve()) and not path.exists()
  b=(ROOT/a['cache']).read_bytes();assert hashlib.sha256(b).hexdigest()==a['sha256'];temp.write_bytes(b);os.replace(temp,path)
 for p,b in updates.items():
  assert (ROOT/p).read_bytes()==originals[p];temp.write_bytes(b);os.replace(temp,ROOT/p)
 plan.update({'backup':backup.relative_to(ROOT).as_posix(),'applied_at':datetime.now(timezone.utc).isoformat()})
 (TASK/'applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print('Applied:',backup.name)
if __name__=='__main__':main()
