"""Integrate the user's full August letter without rewriting its prose."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit, parse_qsl
import hashlib, json, os, re, sys, zipfile
import yaml
from heading_spacing import trim

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent.resolve()
TASK = WORK / 'august-letter-integration'
ANDY = ROOT / 'Andy Matuschak'
ATTACHMENTS = ANDY / 'Attachments'
TITLE = '2023-08-01 Patreon letter - Initial experiments in self-explanation support'
INDEX = 'Patron letters on memory system experiments'
BOOK = 'Comprehension - Kintsch'
PAPER = 'Kintsch, W. (1994). Text comprehension, memory, and learning. American Psychologist, 49(4), 294–303'
downloads = json.loads((TASK / 'downloads.json').read_text(encoding='utf-8'))
verified = json.loads((TASK / 'asset-verification.json').read_text(encoding='utf-8'))
assets = downloads['assets']
assert len(assets) == 6 and all(a['status'] == 'downloaded' for a in assets)
assert all(not a['existing_byte_matches'] and not a.get('existing_pixel_matches') for a in verified['assets'])
assert all(a.get('valid_PDF') and a.get('title_found_in_first_pages') for a in verified['assets'] if a['kind'] == 'PDF')

def split_front(text):
    match = re.match(r'\A(\ufeff?---\r?\n)(.*?)(\r?\n---\r?\n)', text, re.S)
    assert match
    return match, yaml.safe_load(match[2]) or {}, text[match.end():]

def newline(text):
    return '\r\n' if '\r\n' in text else '\n'

def add_source(text, url):
    match, props, body = split_front(text)
    assert isinstance(props['URL'], list)
    values = list(dict.fromkeys(props['URL'] + [url]))
    block = re.search(r'^URL:[^\r\n]*(?:\r?\n(?:[ \t]+[^\r\n]*|))*(?=\r?\n[^ \t\r\n]|\Z)', match[2], re.M)
    assert block
    replacement = 'URL:' + ''.join(newline(text) + '  - ' + json.dumps(u, ensure_ascii=False) for u in values)
    fm = match[2][:block.start()] + replacement + match[2][block.end():]
    return match[1] + fm + match[3] + body

def wiki(title, label=None):
    return '[[Andy Matuschak/' + title + ('|' + label if label is not None else '') + ']]'

def media(name):
    return '[[Andy Matuschak/Attachments/' + name + ']]'

def plain(body):
    body = re.sub(r' \(PDF: \[\[Andy Matuschak/Attachments/[^]]+\]\]\)', '', body)
    body = re.sub(r'^## Footnotes\r?\n', '', body, flags=re.M)
    body = re.sub(r'^\[\^(\d+)\]: ', r'[\1] ', body, flags=re.M)
    body = re.sub(r'\[\^(\d+)\]', r'[\1]', body)
    body = re.sub(r'!\[\[Andy Matuschak/Attachments/[^]]+\]\]', '<image>', body)
    body = re.sub(r'!\[[^]]*\]\(https?://[^)]+\)', '<image>', body)
    body = re.sub(r'(?<!!)\[([^]\r\n]+)\]\(https?://[^)]+\)', lambda m:m[1], body)
    body = re.sub(r'\[\[([^]|]+)(?:\|([^]]+))?\]\]', lambda m:m[2] or m[1], body)
    return [line for line in body.splitlines() if line.strip()]

def build():
    originals = {}
    updates = {}
    records = []
    def read(path):
        relative = path.relative_to(ROOT).as_posix()
        originals[relative] = path.read_bytes()
        return originals[relative].decode('utf-8')
    def save(path, text):
        relative = path.relative_to(ROOT).as_posix()
        updated, blanks = trim(text.encode('utf-8')) if path.suffix == '.md' else (text.encode('utf-8'), 0)
        updates[relative] = updated
        records.append({'path': relative, 'heading_blank_lines_removed': blanks})

    path = ANDY / (TITLE + '.md')
    text = read(path)
    match, props, original_body = split_front(text)
    body = original_body
    link_log = []
    mapping = { 'https://notes.andymatuschak.org/zY3RYK9gJ6eDnq27vSwBDQh': INDEX,
                'https://notes.andymatuschak.org/zLButXjJvGCpWKHzqhXEhhm': '2023-06-30 Patreon letter - Reading comprehension and memory systems'}
    def replace_link(match):
        target = mapping.get(match[2])
        if not target:
            return match[0]
        assert (ANDY / (target + '.md')).is_file()
        link_log.append({'URL': match[2], 'target': target, 'alias': match[1]})
        return wiki(target, match[1])
    body = re.sub(r'(?<!!)\[([^]\r\n]+)\]\((https?://[^)]+)\)', replace_link, body)
    assert len(link_log) == 3
    reference_assets = {}
    for asset in assets:
        original = asset['source_URL']
        name = asset['filename']
        if name.endswith('.pdf'):
            pattern = r'(?<!!)\[([^]\r\n]+)\]\(' + re.escape(original) + r'\)'
            matches = list(re.finditer(pattern, body))
            assert len(matches) == 1, name
            label = matches[0][1]
            linked_note = BOOK if name.startswith('Kintsch - 1998') else PAPER if name.startswith('Kintsch - 1994') else None
            main_link = wiki(linked_note, label) if linked_note else matches[0][0]
            body = re.sub(pattern, lambda m: main_link + ' (PDF: ' + media(name) + ')', body)
            if linked_note:
                reference_assets[linked_note] = asset
        else:
            old_image = '![](' + original + ')'
            assert body.count(old_image) == 1
            body = body.replace(old_image, '!' + media(name))
    chi_name = 'Chi et al - 1994 - Eliciting self-explanations improves understanding.pdf'
    chi_path = ATTACHMENTS / chi_name
    assert chi_path.is_file() and chi_path.read_bytes().startswith(b'%PDF-')
    chi_url = 'http://andymatuschak.org/files/papers/Chi%20et%20al%20-%201994%20-%20Eliciting%20self-explanations%20improves%20understanding.pdf'
    pattern = r'(?<!!)\[([^]\r\n]+)\]\(' + re.escape(chi_url) + r'\)'
    assert len(re.findall(pattern, body)) == 1
    body = re.sub(pattern, lambda m:m[0] + ' (PDF: ' + media(chi_name) + ')', body)
    assert body.count('“text comprehension.”') == 1
    assert body.count('_self-explanation._') == 1
    body = body.replace('“text comprehension.”', '“' + wiki('Reading comprehension', 'text comprehension') + '.”', 1)
    body = body.replace('_self-explanation._', '_' + wiki('Self-explanation', 'self-explanation') + '._', 1)
    for target in ['Reading comprehension', 'Self-explanation']:
        assert (ANDY / (target + '.md')).is_file()

    nl = newline(text)
    marker = nl + '[1] '
    assert body.count(marker) == 1
    start = body.index(marker) + len(nl)
    prefix, definitions = body[:start], body[start:]
    for number in (1,2,3):
        assert prefix.count('[' + str(number) + ']') == 1
        prefix = prefix.replace('[' + str(number) + ']', '[^' + str(number) + ']')
        definitions, count = re.subn(r'^\[' + str(number) + r'\] ', '[^' + str(number) + ']: ', definitions, flags=re.M)
        assert count == 1
    body = prefix + '## Footnotes' + nl + definitions
    assert plain(body) == plain(original_body), 'Author prose or caveats changed'
    save(path, text[:match.end()] + body)

    for title, asset in reference_assets.items():
        path = ANDY / (title + '.md')
        original = read(path)
        updated = add_source(original, asset['fetch_URL'])
        _, _, previous_body = split_front(original)
        assert '## References' not in previous_body
        suffix = newline(original) + '## References' + newline(original) + '- ' + media(asset['filename']) + newline(original)
        if not updated.endswith('\n'):
            suffix = newline(original) + suffix
        save(path, updated + suffix)
        _, _, updated_body = split_front(updates[path.relative_to(ROOT).as_posix()].decode('utf-8'))
        assert updated_body.startswith(previous_body)

    path = ANDY / (INDEX + '.md')
    original = read(path)
    old_heading = '## Notes created by Codex'
    new_heading = '## Previously missing letters'
    assert original.count(old_heading) == 1
    cut = original.index(old_heading)
    updated = original.replace(old_heading, new_heading, 1)
    assert updated[:cut] == original[:cut]
    save(path, updated)

    path = WORK / 'config.json'
    config = json.loads(read(path))
    config['andy_patreon_letters']['missing_note_content'] = 'User-supplied full-text copies replaced the summary notes; preserve captured prose'
    config['andy_patreon_letters']['integration_record'] = '_Codex/august-letter-integration/applied.json'
    config['andy_attachment_naming'] = {'papers': 'Author(s) - Year - Title.pdf', 'letter_images': 'Andy- Letter subject N.ext; retain the original image format'}
    save(path, json.dumps(config, ensure_ascii=False, indent=2) + '\n')
    path = WORK / 'README.md'
    original = read(path)
    section = '\n## Full Patreon captures and August letter integration\nThe user supplied full-text captures to replace the 15 summary notes. The lower index section is now labelled Previously missing letters. The August 1 letter uses existing local notes, collection attachments, and native footnotes while preserving the author’s prose. Recovery and verified downloads are recorded in `august-letter-integration`.\n'
    save(path, original + section.replace('\n', newline(original)))
    path = WORK / 'Patreon letter links.md'
    original = read(path)
    heading = '# Patreon letter links' + newline(original)
    assert original.count(heading) == 1
    notice = 'The user has replaced the 15 summary notes with existing full-text captures. The previous summary import is recorded below as history; the current index labels these Previously missing letters.\n\n## Initial summary import\n'
    updated = original.replace(heading, heading + notice.replace('\n', newline(original)), 1)
    save(path, updated)
    return originals, updates, records, link_log, hashlib.sha256(chi_path.read_bytes()).hexdigest()

def main():
    assert not (TASK / 'applied.json').exists(), 'Already integrated'
    originals, updates, records, links, chi_hash = build()
    for relative, content in updates.items():
        path = ROOT / relative
        if path.suffix != '.md':
            continue
        match, props, body = split_front(content.decode('utf-8'))
        assert props['title'] == path.stem
        assert trim(content) == (content, 0)
        if path.parent == ANDY:
            assert isinstance(props['URL'], list)
            for url in props['URL']:
                assert len([v for k,v in parse_qsl(urlsplit(url).query) if k == 'stackedNotes']) <= 2
    plan = {'note': 'Andy Matuschak/' + TITLE + '.md', 'files': records, 'letter_links_converted': links,
            'bibliographic_links_converted': 2, 'concept_links_added': 2, 'native_footnotes': 3,
            'author_prose_preserved': True, 'private_notice_preserved': True, 'upper_index_preserved': True,
            'assets': [{'source_URL': a['source_URL'], 'fetch_URL': a['fetch_URL'], 'destination': 'Andy Matuschak/Attachments/' + a['filename'], 'sha256': a['sha256'], 'cache': a['cache']} for a in assets],
            'existing_Chi_PDF_reused': True, 'Chi_PDF_sha256': chi_hash,
            'hashes': [{'path': relative, 'before': hashlib.sha256(originals[relative]).hexdigest(), 'after': hashlib.sha256(content).hexdigest()} for relative,content in updates.items()]}
    (TASK / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'notes_updated': 4, 'configuration_and_reports_updated': 3, 'new_PDFs': 4, 'new_images': 2, 'existing_PDF_reused': 1, 'footnotes': 3, 'heading_blank_lines_removed': sum(r['heading_blank_lines_removed'] for r in records)}, indent=2))
    if '--apply' not in sys.argv:
        return
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = WORK / 'backups' / ('august-letter-integration-before-' + stamp + '.zip')
    with zipfile.ZipFile(backup, 'x', zipfile.ZIP_DEFLATED) as archive:
        for relative, content in originals.items():
            archive.writestr(relative, content)
        archive.writestr('_Codex/august-letter-integration/new-assets.json', json.dumps([a['destination'] for a in plan['assets']], ensure_ascii=False, indent=2))
    with zipfile.ZipFile(backup) as archive:
        assert archive.testzip() is None
        for relative, content in originals.items():
            assert archive.read(relative) == content
    for relative, original in originals.items():
        assert (ROOT / relative).read_bytes() == original, 'Concurrent edit: ' + relative
    temporary = TASK / 'update.tmp'
    for asset in plan['assets']:
        path = (ROOT / asset['destination']).resolve()
        assert path.is_relative_to(ATTACHMENTS.resolve()) and not path.exists()
        content = (ROOT / asset['cache']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == asset['sha256']
        temporary.write_bytes(content)
        os.replace(temporary, path)
    for relative, content in updates.items():
        path = (ROOT / relative).resolve()
        assert path.is_relative_to(ROOT)
        assert path.read_bytes() == originals[relative]
        temporary.write_bytes(content)
        os.replace(temporary, path)
        assert path.read_bytes() == content
    plan.update({'backup': backup.relative_to(ROOT).as_posix(), 'applied_at': datetime.now(timezone.utc).isoformat()})
    (TASK / 'applied.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Applied; backup:', backup.name)

if __name__ == '__main__':
    main()
