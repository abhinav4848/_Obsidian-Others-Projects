from pathlib import Path
import json,hashlib,urllib.request,urllib.parse,concurrent.futures
W=Path(__file__).resolve().parent; S=W/'media-recovery'; C=S/'cache';C.mkdir(exist_ok=True)
p=json.loads((S/'plan.json').read_text(encoding='utf-8'))
def ext(b):
 if b.startswith(b'\xff\xd8\xff'):return '.jpeg'
 if b.startswith(b'\x89PNG\r\n\x1a\n'):return '.png'
 if b.startswith((b'GIF87a',b'GIF89a')):return '.gif'
 if b.startswith(b'RIFF') and b[8:12]==b'WEBP':return '.webp'
 if b.startswith(b'%PDF-'):return '.pdf'
 if b'<svg' in b[:1000]:return '.svg'
 raise ValueError('response is not recognized media')
def fetch(u):
 key=hashlib.sha256(u.encode()).hexdigest(); f=C/(key+'.bin');meta=C/(key+'.json')
 if f.exists() and meta.exists():return json.loads(meta.read_text())
 errors=[]; urls=[u]
 parsed=urllib.parse.urlsplit(u)
 if parsed.hostname=='wsrv.nl':
  upstream=urllib.parse.parse_qs(parsed.query).get('url',[])
  if upstream:urls+=upstream
 for address in urls:
  try:
   req=urllib.request.Request(address,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=25) as response:
    b=response.read(20000001)
    if len(b)>20000000:raise ValueError('media exceeds 20 MB')
    extension=ext(b)
   f.write_bytes(b)
   r={'URL':u,'fetched_URL':address,'cache':str(f.relative_to(W)),'sha256':hashlib.sha256(b).hexdigest(),'extension':extension,'bytes':len(b),'status':'recovered'}
   meta.write_text(json.dumps(r,indent=2),encoding='utf-8');return r
  except Exception as e:errors.append(str(e))
 return {'URL':u,'status':'unavailable','errors':errors}
urls=sorted({r['source_URL'] for r in p['assets'] if 'source_URL' in r});out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for r in pool.map(fetch,urls):
  out.append(r)
  if len(out)%10==0:print('Checked',len(out),'of',len(urls),flush=True)
(S/'downloads.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Recovered',sum(r['status']=='recovered' for r in out),'of',len(out),'sources',flush=True)
