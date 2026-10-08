"""Fill the existing Patreon index with source-linked summary notes."""
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, unquote
from datetime import datetime, timezone
import hashlib, json, os, re, sys, zipfile
import yaml
from heading_spacing import trim

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent.resolve()
ANDY = ROOT / 'Andy Matuschak'
DATA = WORK / 'patreon-import'
EVIDENCE = json.loads((DATA / 'sources.json').read_text(encoding='utf-8'))
INDEX = 'Patron letters on memory system experiments'
SOURCES = EVIDENCE['sources']

def split_front(text):
    match = re.match(r'\A(\ufeff?---\r?\n)(.*?)(\r?\n---\r?\n)', text, re.S)
    assert match, 'Expected existing YAML properties'
    return match, yaml.safe_load(match[2]) or {}, text[match.end():]

def with_urls(text, urls):
    match, props, body = split_front(text)
    newline = '\r\n' if '\r\n' in text else '\n'
    fm = match[2]
    block = re.search(r'^URL:[^\r\n]*(?:\r?\n(?:[ \t]+[^\r\n]*|))*(?=\r?\n[^ \t\r\n]|\Z)', fm, re.M)
    assert block, 'Expected URL property'
    replacement = 'URL:' + ''.join(newline + '  - ' + json.dumps(u, ensure_ascii=False) for u in urls)
    return match[1] + fm[:block.start()] + replacement + fm[block.end():] + match[3] + body

def identity(url):
    parsed = urlsplit(url.strip('<>'))
    if parsed.netloc.casefold() == 'notes.andymatuschak.org':
        trail = [unquote(parsed.path).strip('/')] + [v for k, v in parse_qsl(parsed.query) if k == 'stackedNotes']
        return ('andy', trail[-1])
    if parsed.netloc.casefold() in {'patreon.com', 'www.patreon.com'} and '/posts/' in parsed.path:
        match = re.search(r'(?:/|-)(\d+)/?$', parsed.path)
        if match:
            return ('patreon', match[1])
    return None

LOOKUP = {}
for source in SOURCES:
    for key in ('Andy_URL', 'Patreon_URL'):
        key_id = identity(source[key])
        assert key_id and key_id not in LOOKUP
        LOOKUP[key_id] = source['title']
LOOKUP[identity(EVIDENCE['index_URL'])] = INDEX

LINK = re.compile(r'(?<!!)(?<!\\)\[([^\]\r\n]+)\]\(\s*(<?https?://[^\s)]+>?)\s*\)')

def internalize(body, path):
    replacements = []
    output = []
    fence = None
    for line in body.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            output.append(line)
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= fence[1] and not mark[2].strip():
                fence = None
            continue
        if mark:
            fence = (mark[1][0], len(mark[1]))
            output.append(line)
            continue
        # Avoid changing examples inside inline code spans.
        spans = [(m.start(), m.end()) for m in re.finditer(r'(`+).*?\1', line)]
        def replace(match):
            if any(start <= match.start() < end for start, end in spans):
                return match[0]
            title = LOOKUP.get(identity(match[2]))
            if not title:
                return match[0]
            label = match[1].replace('|', '\\|')
            replacement = '[[' + 'Andy Matuschak/' + title + '|' + label + ']]'
            replacements.append({'file': path, 'source_URL': match[2], 'target': title, 'label': match[1]})
            return replacement
        output.append(LINK.sub(replace, line))
    result = ''.join(output)
    broken = '([[# 2023-08-01 Patreon letter - Initial experiments in self-explanation support]] '
    repairs = result.count(broken)
    result = result.replace(broken, '')
    return result, replacements, repairs

def build():
    index_path = ANDY / (INDEX + '.md')
    original_index = index_path.read_text(encoding='utf-8-sig')
    indexed = re.findall(r'\[\[([^]|]+)(?:\|[^]]+)?\]\]', original_index)
    assert indexed == [s['title'] for s in SOURCES], 'Index changed or source title mismatch'
    originals, updates, new_files, link_changes = {}, {}, [], []
    repairs = 0
    for source in SOURCES:
        path = ANDY / (source['title'] + '.md')
        if path.exists():
            assert source['summary'] is None, 'Existing note must not be replaced by a summary'
            continue
        assert source['summary'] and len(source['summary'].split()) <= 105
        text = '---\nURL:\n' + ''.join('  - ' + json.dumps(source[k], ensure_ascii=False) + '\n' for k in ('Andy_URL', 'Patreon_URL'))
        text += 'title: ' + json.dumps(source['title'], ensure_ascii=False) + '\n---\n'
        text += '# ' + source['title'] + '\n_Summary of the source letter._\n\n'
        text += source['summary'] + '\n\nPart of [[Andy Matuschak/' + INDEX + '|' + INDEX + ']].\n'
        relative = path.relative_to(ROOT).as_posix()
        updates[relative] = text.encode('utf-8')
        new_files.append(relative)
    assert len(new_files) == 15
    by_title = {s['title']: s for s in SOURCES}
    for path in sorted(ANDY.glob('*.md')):
        relative = path.relative_to(ROOT).as_posix()
        original = path.read_bytes()
        text = original.decode('utf-8')
        match, props, body = split_front(text)
        changed, refs, repaired = internalize(body, relative)
        text = text[:match.end()] + changed
        additions = []
        if path.stem in by_title:
            additions = [by_title[path.stem]['Andy_URL'], by_title[path.stem]['Patreon_URL']]
        elif path.stem == INDEX:
            additions = [EVIDENCE['index_URL']]
        if additions:
            assert isinstance(props.get('URL'), list)
            urls = list(dict.fromkeys(additions + props['URL']))
            text = with_urls(text, urls)
        output = text.encode('utf-8')
        if output != original:
            originals[relative] = original
            updates[relative] = output
            link_changes.extend(refs)
            repairs += repaired
    assert repairs == 1
    for relative, content in updates.items():
        assert trim(content) == (content, 0), relative
        path = ROOT / relative
        match, props, body = split_front(content.decode('utf-8'))
        assert isinstance(props.get('URL'), list) and props['URL']
        assert props['title'] == path.stem
        if relative in new_files:
            assert re.findall(r'^# (.+)$', body, re.M) == [path.stem]
            assert not re.search(r'^(?:Type of Link|Author|Completion Status|Last edited time):', body, re.M)
        for url in props['URL']:
            parsed = urlsplit(url)
            if parsed.netloc == 'notes.andymatuschak.org':
                assert len([v for k,v in parse_qsl(parsed.query) if k == 'stackedNotes']) <= 2
    return originals, updates, new_files, link_changes, repairs

def main():
    assert not (DATA / 'applied.json').exists(), 'Already applied; consult the manifest'
    originals, updates, new_files, links, repairs = build()
    plan = {'new_notes': new_files, 'existing_notes_updated': list(originals), 'links_converted': links, 'malformed_links_repaired': repairs,
            'files': [{'path': rel, 'before_sha256': hashlib.sha256(originals[rel]).hexdigest() if rel in originals else None,
                       'after_sha256': hashlib.sha256(content).hexdigest()} for rel, content in updates.items()]}
    (DATA / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'new_notes': len(new_files), 'existing_notes_updated': len(originals), 'links_converted': len(links), 'malformed_links_repaired': repairs}, indent=2))
    if '--apply' not in sys.argv:
        return
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = WORK / 'backups' / ('patreon-links-before-' + stamp + '.zip')
    with zipfile.ZipFile(backup, 'x', zipfile.ZIP_DEFLATED) as archive:
        for relative, content in originals.items():
            archive.writestr(relative, content)
        archive.writestr('_Codex/patreon-import/new-files.json', json.dumps(new_files, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(backup) as archive:
        assert archive.testzip() is None
        for relative, content in originals.items():
            assert archive.read(relative) == content
    temporary = DATA / 'update.tmp'
    for relative, content in updates.items():
        path = (ROOT / relative).resolve()
        assert path.is_relative_to(ANDY.resolve())
        if relative in originals:
            assert path.read_bytes() == originals[relative], 'Concurrent edit: ' + relative
        else:
            assert not path.exists(), 'New file collision: ' + relative
        temporary.write_bytes(content)
        os.replace(temporary, path)
        assert path.read_bytes() == content
    plan.update({'backup': backup.relative_to(ROOT).as_posix(), 'applied_at': datetime.now(timezone.utc).isoformat(), 'content_mode': EVIDENCE['content_mode']})
    (DATA / 'applied.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Applied; backup:', backup.name)

if __name__ == '__main__':
    main()
