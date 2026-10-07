from pathlib import Path
from collections import defaultdict, Counter
from urllib.parse import urlsplit, parse_qsl, unquote
import hashlib, json, re, unicodedata

WORK = Path(__file__).resolve().parent
CFG = json.loads((WORK / 'config.json').read_text(encoding='utf-8'))
ROOT = Path(CFG['working_vault'])
LYT = ROOT / CFG['lyt_folder']
TEXT_EXT = {'.md', '.canvas', '.base'}

def read(p):
    return p.read_bytes().decode('utf-8-sig')

def normalized_name(p):
    s = unicodedata.normalize('NFKC', p.stem).casefold()
    s = ''.join(c for c in s if unicodedata.category(c)[0] in 'LN' or c.isspace())
    return re.sub(r'\s+', ' ', s).strip()

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def files(base):
    return sorted(p for p in base.rglob('*') if p.is_file() and not any(x.startswith('.') for x in p.relative_to(base).parts))

def group(items, key):
    groups = defaultdict(list)
    for p in items:
        groups[key(p)].append(str(p.relative_to(LYT)).replace('\\','/'))
    return [v for v in groups.values() if len(v) > 1]

def audit():
    lf = files(LYT)
    refs = {k: files(Path(v)) for k,v in CFG['reference_vaults'].items()}
    notes = [p for p in lf if p.suffix == '.md']
    by_name = group(notes, lambda p: p.stem.casefold())
    norm_groups = group(notes, normalized_name)
    duplicates = group(lf, digest)
    ref_inventory = {k: [{'path': str(p.relative_to(Path(CFG['reference_vaults'][k]))).replace('\\','/'), 'sha256':digest(p)} for p in v] for k,v in refs.items()}
    url_re = re.compile(r'https?://notes\.andymatuschak\.org/[^\s<>\)\]"\}]+')
    andy = []
    for p in files(ROOT / CFG['andy_folder']):
        if p.suffix != '.md': continue
        t = read(p)
        urls = list(dict.fromkeys(url_re.findall(t)))
        andy.append({'path':p.relative_to(ROOT).as_posix(), 'url_count':len(urls), 'stack_lengths':[1+sum(k=='stackedNotes' for k,v in parse_qsl(urlsplit(u).query)) for u in urls], 'has_frontmatter':t.startswith('---'), 'source_lines':[line for line in t.splitlines() if '[Andy Link]' in line or re.match(r'^(?:URL|url|source):',line)]})
    data = {'lyt_file_count':len(lf), 'lyt_note_count':len(notes), 'lyt_folders':dict(Counter(p.relative_to(LYT).parent.as_posix() for p in lf)), 'reference_counts':{k:len(v) for k,v in refs.items()}, 'same_name_groups':by_name, 'normalized_name_groups':norm_groups, 'exact_duplicate_groups':duplicates, 'reference_inventory':ref_inventory, 'andy':andy}
    target=WORK/('audit-current.json' if (WORK/'audit-initial.json').exists() else 'audit-initial.json')
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    summary = {k:v for k,v in data.items() if k not in ('reference_inventory','andy')}
    summary['andy_summary'] = {'notes':len(andy),'with_frontmatter':sum(x['has_frontmatter'] for x in andy), 'with_andy_link_label':sum(bool(x['source_lines']) for x in andy), 'without_any_andy_url':[x['path'] for x in andy if not x['url_count']]}
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__': audit()
