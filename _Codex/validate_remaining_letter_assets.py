from pathlib import Path
from io import BytesIO
import hashlib,json,re
from PIL import Image, ImageSequence
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent.parent;TASK=ROOT/'_Codex/letters-integration';ATT=ROOT/'Andy Matuschak/Attachments'
record=json.loads((TASK/'downloads.json').read_text(encoding='utf-8'))
def pixels(data):
 with Image.open(BytesIO(data)) as im:
  im.load()
  if getattr(im,'is_animated',False):return None
  rgba=im.convert('RGBA');return hashlib.sha256(str(rgba.size).encode()+rgba.tobytes()).hexdigest()
existing_hashes={};existing_pixels={}
for path in ATT.iterdir():
 if not path.is_file():continue
 data=path.read_bytes();relative=path.relative_to(ROOT).as_posix()
 existing_hashes.setdefault(hashlib.sha256(data).hexdigest(),relative)
 if path.suffix.lower() in {'.png','.webp','.gif','.jpeg','.jpg'}:
  try:
   fingerprint=pixels(data)
   if fingerprint:existing_pixels.setdefault(fingerprint,relative)
  except Exception:pass
validation=[]
for item in record['assets']:
 assert item['status']!='unavailable',item
 if item['status']=='reused':validation.append({'destination':item['destination'],'kind':item['kind'],'reused':True});continue
 data=(ROOT/item['cache']).read_bytes();assert hashlib.sha256(data).hexdigest()==item['sha256']
 result={'filename':item['filename'],'kind':item['kind']}
 match=existing_hashes.get(item['sha256'])
 if item['kind']=='PDF':
  reader=PdfReader(BytesIO(data));assert not reader.is_encrypted
  result['pages']=len(reader.pages);assert result['pages']>0
  if item['filename'].startswith('Benet'):
   text=reader.pages[0].extract_text();assert 'DRAFT 3' in text and 'Juan Benet' in text
   result['matching_IPFS_Draft_3']=True
 else:
  with Image.open(BytesIO(data)) as im:
   result.update({'format':im.format,'size':list(im.size),'frames':getattr(im,'n_frames',1)})
   for frame in ImageSequence.Iterator(im):frame.load()
   extension={'PNG':'.png','GIF':'.gif','WEBP':'.webp','JPEG':'.jpeg'}[im.format]
   assert Path(item['filename']).suffix.lower()==extension
  fingerprint=pixels(data)
  if fingerprint and not match:match=existing_pixels.get(fingerprint)
  result['pixel_sha256']=fingerprint
 destination=match or (ATT/item['filename']).relative_to(ROOT).as_posix()
 item['destination']=destination
 item['install']=not bool(match)
 if match:item['status']='reused_download_match';result['reused_match']=match
 else:
  assert not (ROOT/destination).exists()
  existing_hashes[item['sha256']]=destination
  if item['kind']=='image' and fingerprint:existing_pixels[fingerprint]=destination
 validation.append(result)
(TASK/'assets-ready.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(TASK/'asset-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_PDFs':sum(a.get('install',False) and a['kind']=='PDF' for a in record['assets']),'new_images':sum(a.get('install',False) and a['kind']=='image' for a in record['assets']),'reused_assets':sum(not a.get('install',False) for a in record['assets']),'GIFs_preserved':sum(v.get('format')=='GIF' for v in validation)},indent=2))
