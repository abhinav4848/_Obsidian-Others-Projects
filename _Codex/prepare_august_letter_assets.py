"""Download only the six missing assets referenced by the August 1 letter."""
from pathlib import Path
from urllib.parse import urlsplit
from datetime import datetime, timezone
import concurrent.futures, hashlib, json, re, urllib.request

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent
TASK = WORK / 'august-letter-integration'
TASK.mkdir(exist_ok=True)
CACHE = TASK / 'cache'
CACHE.mkdir(exist_ok=True)
NOTE = ROOT / 'Andy Matuschak' / '2023-08-01 Patreon letter - Initial experiments in self-explanation support.md'
TARGET = ROOT / 'Andy Matuschak' / 'Attachments'
SPECS = [
    ('McNamara%20-%202004%20-%20SERT.pdf', 'McNamara - 2004 - SERT - Self-Explanation Reading Training.pdf'),
    ('Wiggins,%20McTighe%20-%202005%20-%20Understanding%20by%20design.pdf', 'Wiggins, McTighe - 2005 - Understanding by Design.pdf'),
    ('Kintsch%20-%201998%20-%20Comprehension.pdf', 'Kintsch - 1998 - Comprehension - A Paradigm for Cognition.pdf'),
    ('Kintsch%20-%201994%20-%20Text%20comprehension,%20memory,%20and%20learning.pdf', 'Kintsch - 1994 - Text comprehension, memory, and learning.pdf'),
    ('BearImages/DE1145CF-7623-4081-9C1F-FCA234C7B2AB/image.png.webp', 'Andy- Initial experiments in self-explanation support 1.webp'),
    ('BearImages/DE1145CF-7623-4081-9C1F-FCA234C7B2AB/image%202.png', 'Andy- Initial experiments in self-explanation support 2.png'),
]
urls = re.findall(r'https?://[^\s)]+', NOTE.read_text(encoding='utf-8-sig'))
items = []
for suffix, name in SPECS:
    matches = list(dict.fromkeys(u for u in urls if u.endswith(suffix)))
    assert len(matches) == 1, suffix
    original_url = matches[0]
    parsed = urlsplit(original_url)
    assert parsed.hostname in {'andymatuschak.org', 'notes.andymatuschak.org'}
    assert name == Path(name).name and not re.search(r'[<>:"/\\|?*]', name)
    items.append({'source_URL': original_url, 'fetch_URL': re.sub(r'^http:', 'https:', original_url), 'filename': name})

def fetch(item):
    key = hashlib.sha256(item['fetch_URL'].encode('utf-8')).hexdigest()
    cache = CACHE / (key + '.bin')
    result = dict(item)
    try:
        if cache.exists():
            data = cache.read_bytes()
            result['cached'] = True
        else:
            request = urllib.request.Request(item['fetch_URL'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read(200000001)
                assert len(data) <= 200000000, 'Asset exceeds 200 MB'
                result.update({'resolved_URL': response.url, 'HTTP_status': response.status, 'Content_Type': response.headers.get('Content-Type')})
            cache.write_bytes(data)
        suffix = Path(item['filename']).suffix.casefold()
        if suffix == '.pdf':
            assert data[:1024].lstrip().startswith(b'%PDF-'), 'Not a PDF'
            assert b'%%EOF' in data[-4096:], 'Incomplete PDF'
        elif suffix == '.png':
            assert data.startswith(b'\x89PNG\r\n\x1a\n') and b'IEND' in data[-24:], 'Incomplete PNG'
        elif suffix == '.webp':
            assert data.startswith(b'RIFF') and data[8:12] == b'WEBP', 'Not a WebP image'
        else:
            raise ValueError('Unexpected asset extension')
        result.update({'status': 'downloaded', 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'cache': cache.relative_to(ROOT).as_posix()})
    except Exception as error:
        result.update({'status': 'unavailable', 'error': str(error)})
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, items))
record = {'checked_at': datetime.now(timezone.utc).isoformat(), 'note': NOTE.relative_to(ROOT).as_posix(), 'assets': results,
          'reused_existing_PDF': 'Andy Matuschak/Attachments/Chi et al - 1994 - Eliciting self-explanations improves understanding.pdf'}
(TASK / 'downloads.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
for result in results:
    print(result['status'], result['filename'], result.get('bytes', result.get('error')))
