"""Validate native downloads and check active media for duplicate content."""
from pathlib import Path
from io import BytesIO
from datetime import datetime, timezone
import hashlib, json, re
from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
TASK = ROOT / '_Codex' / 'august-letter-integration'
downloads = json.loads((TASK / 'downloads.json').read_text(encoding='utf-8'))
excluded = {'_Codex', '.git', '.obsidian', '.trash'}
media = []
for path in ROOT.rglob('*'):
    if not path.is_file() or any(x in excluded for x in path.relative_to(ROOT).parts):
        continue
    if path.suffix.casefold() in {'.pdf', '.png', '.jpeg', '.jpg', '.gif', '.webp'}:
        media.append(path)
digests = {}
pixels = {}
dhashes = []

def image_fingerprint(data):
    with Image.open(BytesIO(data)) as source:
        source.load()
        assert not getattr(source, 'is_animated', False), 'Animated asset'
        picture = source.convert('RGBA')
        digest = hashlib.sha256(str(picture.size).encode() + picture.tobytes()).hexdigest()
        values = list(picture.convert('L').resize((9,8)).getdata())
        d = 0
        for y in range(8):
            for x in range(8):
                d = (d << 1) | int(values[y*9+x] > values[y*9+x+1])
        return {'width': picture.width, 'height': picture.height, 'pixel_sha256': digest, 'dhash': d, 'format': source.format}

for path in media:
    data = path.read_bytes()
    relative = path.relative_to(ROOT).as_posix()
    digests.setdefault(hashlib.sha256(data).hexdigest(), []).append(relative)
    if path.suffix.casefold() != '.pdf':
        try:
            fingerprint = image_fingerprint(data)
            pixels.setdefault(fingerprint['pixel_sha256'], []).append(relative)
            dhashes.append((relative, fingerprint))
        except Exception:
            pass

results = []
for asset in downloads['assets']:
    assert asset['status'] == 'downloaded', asset
    path = ROOT / asset['cache']
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == asset['sha256']
    result = {'filename': asset['filename'], 'source_URL': asset['source_URL'], 'sha256': asset['sha256'],
              'existing_byte_matches': digests.get(asset['sha256'], [])}
    if asset['filename'].endswith('.pdf'):
        reader = PdfReader(BytesIO(data), strict=False)
        assert not reader.is_encrypted
        result.update({'kind': 'PDF', 'pages': len(reader.pages), 'valid_PDF': True})
        assert result['pages'] > 0
        # Extract a small title sample only for identity checks; do not copy paper text.
        title_sample = '\n'.join(reader.pages[i].extract_text() or '' for i in range(min(3, len(reader.pages))))
        expected = 'SERT' if asset['filename'].startswith('McNamara') else 'Understanding' if asset['filename'].startswith('Wiggins') else 'Comprehension' if '1998' in asset['filename'] else 'Text comprehension'
        result['title_found_in_first_pages'] = expected.casefold() in re.sub(r'\s+', ' ', title_sample).casefold()
    else:
        fingerprint = image_fingerprint(data)
        result.update({'kind': 'image', **fingerprint, 'existing_pixel_matches': pixels.get(fingerprint['pixel_sha256'], [])})
        result['similar_local_images'] = [{'path': relative, 'hamming_distance': (fingerprint['dhash'] ^ old['dhash']).bit_count()}
            for relative, old in dhashes if (fingerprint['dhash'] ^ old['dhash']).bit_count() <= 4]
    results.append(result)
record = {'checked_at': datetime.now(timezone.utc).isoformat(), 'active_media_checked': len(media), 'assets': results}
(TASK / 'asset-verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
for item in results:
    print(json.dumps(item, ensure_ascii=False))
