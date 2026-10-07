from pathlib import Path
from urllib.parse import quote,urlsplit
from datetime import datetime,timezone
import urllib.request,urllib.error,json,re,hashlib,concurrent.futures,unicodedata,html,yaml
W=Path(__file__).resolve().parent;R=W.parent;S=W/'andy-online';S.mkdir(exist_ok=True);C=S/'pages';C.mkdir(exist_ok=True)
def norm(s):return re.sub(r'[^\w]+',' ',unicodedata.normalize('NFKC',s)).strip().casefold()
def front(t):
 m=re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n',t,re.S)
 return (yaml.safe_load(m[1]) or {},t[m.end():]) if m else ({},t)
def get(u):
 key=hashlib.sha256(u.encode()).hexdigest();p=C/(key+'.json')
 if p.exists():return json.loads(p.read_text(encoding='utf-8'))
 result={'requested_URL':u,'checked_at':datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as response:
   text=response.read(5000000).decode('utf-8');result['resolved_URL']=response.url;result['HTTP_status']=response.status
  match=re.search(r'<script id="notetower-initial-data"[^>]*>(.*?)</script>',text,re.S)
  if match:
   data=json.loads(match[1]);result['site_data']=data
   result['notes']=[entry['data'] for entry in data.get('noteCache',{}).values() if 'data' in entry and entry['data']]
  else:
   title=re.search(r'<title>(.*?)</title>',text,re.S);result['HTML_title']=html.unescape(title[1]) if title else None
 except Exception as e:result['error']=str(e)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def check(item):
 p,body=item;name=p.stem; titles=[name]
 for line in body.splitlines():
  m=re.match(r'^#\s+(.+?)\s*$',line)
  if m and m[1] not in titles and len(m[1])>10 and m[1].casefold() not in {'references','key design properties','implementations','andy matuschak'}:titles.append(m[1])
 titles=titles[:3];results=[]
 for title in titles:
  u='https://notes.andymatuschak.org/'+quote(title.replace(' ','_'),safe='')
  result=get(u);results.append({k:v for k,v in result.items() if k not in {'site_data','notes'}})
  for note in result.get('notes',[]):
   if norm(note.get('title',''))==norm(title):
    slug=note.get('slug');public=note.get('contentMarkdown','');
    localwords=set(norm(re.sub(r'\[\[([^]|]*)(?:\|([^]]*))?\]\]',lambda m:m[2] or m[1].rsplit('/',1)[-1],body)).split())
    publicwords=set(norm(re.sub(r'\[\[.*?:::(.*?)\]\]',r'\1',public)).split());overlap=len(localwords&publicwords)/max(1,len(localwords))
    if title!=name and overlap<0.45:continue
    if slug:return {'note':p.relative_to(R).as_posix(),'status':'verified','URL':'https://notes.andymatuschak.org/'+quote(slug,safe=''),'online_title':note['title'],'requested_URL':u,'title_used':title,'body_word_overlap':round(overlap,3),'cache':str((C/(hashlib.sha256(u.encode()).hexdigest()+'.json')).relative_to(W))}
 return {'note':p.relative_to(R).as_posix(),'status':'needs_search','titles_tried':titles,'attempts':results}
items=[]
for p in sorted((R/'Andy Matuschak').rglob('*.md')):
 props,body=front(p.read_text(encoding='utf-8-sig'))
 if not props.get('URL'):items.append((p,body))
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for result in pool.map(check,items):
  out.append(result)
  if len(out)%10==0:print('Checked',len(out),'of',len(items),'notes;',sum(x['status']=='verified' for x in out),'verified',flush=True)
(S/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verified',sum(x['status']=='verified' for x in out),'of',len(out),flush=True)
print('Needs search:',[x['note'].split('/')[-1] for x in out if x['status']!='verified'],flush=True)
