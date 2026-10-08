from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote, quote
from datetime import datetime, timezone
import concurrent.futures, hashlib, json, re, urllib.request

ROOT=Path(__file__).resolve().parent.parent
TASK=ROOT/'_Codex/letters-integration'; CACHE=TASK/'cache'; CACHE.mkdir(exist_ok=True)
ATT=ROOT/'Andy Matuschak/Attachments'
inv=json.loads((TASK/'inventory.json').read_text(encoding='utf-8'))

def canonical(url):
 p=urlsplit(url); return urlunsplit(('https',p.netloc.lower(),quote(unquote(p.path),safe="/,:@'()-"),p.query,''))

known={}
for a in json.loads((ROOT/'_Codex/august-letter-integration/applied.json').read_text(encoding='utf-8'))['assets']:
 known[canonical(a['source_URL'])]=a['destination']
items={}; numbers={}
for url,letters in inv['assets'].items():
 key=canonical(url)
 if key in items:
  items[key]['source_URLs'].append(url); continue
 filename=unquote(urlsplit(url).path.rsplit('/',1)[-1])
 image=not re.search(r'\.pdf$',filename,re.I)
 record={'URL':key,'source_URLs':[url],'letters':letters,'kind':'image' if image else 'PDF'}
 if key in known and (ROOT/known[key]).is_file():
  record.update({'status':'reused','destination':known[key]})
 elif not image and (ATT/filename).is_file():
  record.update({'status':'reused','destination':(ATT/filename).relative_to(ROOT).as_posix()})
 else:
  if image:
   owner=letters[0];numbers[owner]=numbers.get(owner,0)+1
   subject=owner.split(' Patreon letter - ',1)[1]
   subject=re.sub(r'[<>:"/\\|?*]','-',subject).strip().rstrip('.')
   extension=Path(filename).suffix.lower()
   filename='Andy- '+subject+' '+str(numbers[owner])+extension
  else:
   filename=filename.replace('processes2.pdf','processes.pdf')
   if filename=='ipfs.draft3.pdf': filename='Benet - 2014 - IPFS - Content Addressed, Versioned, P2P File System.pdf'
   if filename.startswith('Butler - 2010 - '):filename='Butler - 2010 - Repeated Testing Produces Superior Transfer of Learning Relative to Repeated Studying.pdf'
   filename=re.sub(r'[<>:"/\\|?*]','-',filename)
  record['filename']=filename
 items[key]=record

def fetch(record):
 if record.get('status')=='reused':
  record['sha256']=hashlib.sha256((ROOT/record['destination']).read_bytes()).hexdigest();return record
 cache=CACHE/(hashlib.sha256(record['URL'].encode()).hexdigest()+'.bin')
 try:
  if cache.exists():data=cache.read_bytes()
  else:
   address=record['URL']
   if address.startswith('https://ipfs.io/ipfs/'):
    address='https://research.protocol.ai/publications/ipfs-content-addressed-versioned-p2p-file-system/benet2014.pdf'
    record['alternate_source_URL']=address
   req=urllib.request.Request(address,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=45) as response:
    data=response.read(200000001);assert len(data)<=200000000
    record.update({'resolved_URL':response.url,'HTTP_status':response.status})
   cache.write_bytes(data)
  if record['kind']=='PDF':assert data.lstrip().startswith(b'%PDF-') and b'%%EOF' in data[-4096:]
  else:assert data.startswith((b'\x89PNG',b'GIF87a',b'GIF89a',b'\xff\xd8\xff')) or (data.startswith(b'RIFF') and data[8:12]==b'WEBP')
  record.update({'status':'downloaded','cache':cache.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 except Exception as e:record.update({'status':'unavailable','error':str(e)})
 return record

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(fetch,items.values()))
out={'checked_at':datetime.now(timezone.utc).isoformat(),'assets':results}
(TASK/'downloads.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for status in ['reused','downloaded','unavailable']:
 print(status,sum(a['status']==status for a in results))
for a in results:
 if a['status']=='unavailable':print(a['URL'],a['error'])
