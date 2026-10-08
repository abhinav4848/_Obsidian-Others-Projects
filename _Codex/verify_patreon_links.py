"""Verify the import, unchanged captured text, and formatting preferences."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit, parse_qsl
import hashlib, json, os, re, zipfile
import yaml
from complete_patreon_links import WORK, ROOT, ANDY, DATA, EVIDENCE, SOURCES, INDEX, split_front
from heading_spacing import trim

manifest = json.loads((DATA / 'applied.json').read_text(encoding='utf-8'))
baseline = json.loads((DATA / 'baseline.json').read_text(encoding='utf-8'))
changed = {r['path']: r for r in manifest['files']}
current = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in ANDY.rglob('*') if p.is_file()}
assert set(current) - set(baseline['Andy_files']) == set(manifest['new_notes'])
assert not set(baseline['Andy_files']) - set(current)
for relative, digest in baseline['Andy_files'].items():
    assert current[relative] == (changed[relative]['after_sha256'] if relative in changed else digest), relative
for relative, record in changed.items():
    assert current[relative] == record['after_sha256'], relative
assert hashlib.sha256((ROOT / '.obsidian/types.json').read_bytes()).hexdigest() == baseline['property_registry']
assert json.loads((ROOT / '.obsidian/types.json').read_text(encoding='utf-8'))['types']['URL'] == 'multitext'

def plain(text):
    text = text.replace('([[# 2023-08-01 Patreon letter - Initial experiments in self-explanation support]] ', '')
    text = re.sub(r'(?<!!)\[([^]\n]+)\]\(https?://[^\s)]+\)', lambda m: m[1], text)
    return re.sub(r'\[\[([^]|]+)(?:\|([^]]+))?\]\]', lambda m: m[2] or m[1], text)

with zipfile.ZipFile(ROOT / manifest['backup']) as archive:
    assert archive.testzip() is None
    for relative in manifest['existing_notes_updated']:
        _, before, old_body = split_front(archive.read(relative).decode('utf-8'))
        _, after, new_body = split_front((ROOT / relative).read_text(encoding='utf-8'))
        assert {k:v for k,v in before.items() if k != 'URL'} == {k:v for k,v in after.items() if k != 'URL'}, relative
        assert set(before['URL']).issubset(after['URL']), relative
        assert plain(old_body) == plain(new_body), relative
    _, _, old_index = split_front(archive.read('Andy Matuschak/' + INDEX + '.md').decode('utf-8'))
    _, _, new_index = split_front((ANDY / (INDEX + '.md')).read_text(encoding='utf-8'))
    assert old_index == new_index

for source in SOURCES:
    path = ANDY / (source['title'] + '.md')
    assert path.exists()
    _, props, body = split_front(path.read_text(encoding='utf-8'))
    assert props['title'] == path.stem
    assert isinstance(props['URL'], list)
    assert props['URL'][:2] == [source['Andy_URL'], source['Patreon_URL']]
    if path.relative_to(ROOT).as_posix() in manifest['new_notes']:
        assert re.findall(r'^# (.+)$', body, re.M) == [path.stem]
        assert '_Summary of the source letter._' in body
        assert source['summary'] in body
    assert trim(path.read_bytes()) == (path.read_bytes(), 0)
for link in manifest['links_converted']:
    destination = (ANDY / (link['target'] + '.md')).resolve()
    assert destination.is_relative_to(ANDY.resolve()) and destination.is_file()
    expected = '[[Andy Matuschak/' + link['target'] + '|' + link['label'].replace('|','\\|') + ']]'
    assert expected in (ROOT / link['file']).read_text(encoding='utf-8')

url_properties = 0
spacing_issues = []
for path in ROOT.rglob('*.md'):
    if any(part in {'.git', '.obsidian', '.trash', '__pycache__'} for part in path.relative_to(ROOT).parts):
        continue
    data = path.read_bytes()
    if trim(data)[1]:
        spacing_issues.append(path.relative_to(ROOT).as_posix())
    match = re.match(r'\A\ufeff?---\r?\n(.*?)\r?\n---\r?\n', data.decode('utf-8'), re.S)
    if match:
        # Obsidian templates may contain unexpanded {{date}} values in other fields.
        url_block = re.search(r'^URL:[^\r\n]*(?:\r?\n(?:[ \t]+[^\r\n]*|))*(?=\r?\n[^ \t\r\n]|\Z)', match[1], re.M)
        if url_block:
            props = yaml.safe_load(url_block[0])
            url_properties += 1
            assert isinstance(props['URL'], list), str(path)
            for url in props['URL']:
                parsed = urlsplit(url)
                if parsed.netloc == 'notes.andymatuschak.org':
                    assert len([v for k,v in parse_qsl(parsed.query) if k == 'stackedNotes']) <= 2, str(path)
assert not spacing_issues, spacing_issues

verification = {'verified_at': datetime.now(timezone.utc).isoformat(), 'new_summary_notes': len(manifest['new_notes']),
                'indexed_letters_resolved': len(SOURCES), 'verified_Andy_sources': len(SOURCES), 'verified_Patreon_sources': len(SOURCES),
                'links_converted': len(manifest['links_converted']), 'existing_notes_updated': len(manifest['existing_notes_updated']),
                'malformed_references_repaired': manifest['malformed_links_repaired'], 'existing_prose_preserved': True,
                'unrelated_properties_preserved': True, 'existing_attachments_unchanged': True, 'index_body_preserved': True,
                'URL_properties_using_lists': url_properties, 'blank_lines_after_headings': 0, 'unexpected_Andy_file_changes': 0}
(DATA / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')

report_path = WORK / 'Patreon letter links.md'
report = '---\ntitle: "Patreon letter links"\n---\n# Patreon letter links\n'
report += 'Added 15 clearly labelled summaries for the missing letters in the existing index. All 19 indexed letter links now resolve to local notes. The original full text remains at the source addresses in each note’s `URL` list.\n\n'
report += 'Verified both Andy’s note address and the original Patreon address for each letter using [the letter index](' + EVIDENCE['index_URL'] + ') and [the Patreon sitemap](' + EVIDENCE['Patreon_sitemap'] + '). Dates and captured titles follow the existing vault index, including where Patreon publication dates differ.\n\n'
report += 'Updated 7 existing notes, converted 30 external article links into internal links, and repaired one malformed August-letter reference. Existing prose, personal comments, other properties, attachment locations, and original navigation trails were preserved. Canonical source addresses appear first in the URL lists.\n\n'
report += '## Format\nOne heading matching the captured filename; the same `title` value; YAML `URL` lists; no blank line after headings; no unwanted import fields. New notes identify their content as a summary so they cannot be mistaken for the original letters.\n\n'
report += '## Added notes\n' + ''.join('- [[' + Path(relative).with_suffix('').as_posix() + ']]\n' for relative in manifest['new_notes'])
report += '\n## Recovery and verification\nOriginal notes: `' + manifest['backup'] + '`. The ZIP also lists newly created files for reversal. Detailed source metadata, changes, hashes, and checks are in `_Codex/patreon-import`.\n'
assert trim(report.encode('utf-8')) == (report.encode('utf-8'), 0)
assert not report_path.exists()
report_path.write_text(report, encoding='utf-8')

config_path = WORK / 'config.json'
readme_path = WORK / 'README.md'
originals = {config_path: config_path.read_bytes(), readme_path: readme_path.read_bytes()}
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
config_backup = WORK / 'backups' / ('patreon-config-before-' + stamp + '.zip')
with zipfile.ZipFile(config_backup, 'x', zipfile.ZIP_DEFLATED) as archive:
    for path, data in originals.items():
        archive.writestr(path.relative_to(ROOT).as_posix(), data)
config = json.loads(originals[config_path].decode('utf-8'))
config['andy_patreon_letters'] = {'index': 'Andy Matuschak/' + INDEX + '.md', 'scope': 'Letters linked by the existing index',
                                'missing_note_content': 'Clearly labelled summary with verified Andy and Patreon URL properties',
                                'preserve_existing_captured_text': True, 'source_evidence': '_Codex/patreon-import/sources.json'}
readme = originals[readme_path].decode('utf-8')
readme += '\n## Patreon letter links\nThe existing Patreon-letter index is complete with 15 source-linked summary notes. All 19 letters have verified Andy and Patreon addresses in URL lists. Existing captured prose and personal remarks were retained; article links were made internal where identity was verified. See `Patreon letter links.md` and `patreon-import` for evidence and recovery records.\n'
temporary = DATA / 'report-update.tmp'
for path, data in ((config_path, (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8')), (readme_path, readme.encode('utf-8'))):
    assert path.read_bytes() == originals[path], 'Concurrent configuration edit'
    temporary.write_bytes(data)
    os.replace(temporary, path)
    if path.suffix == '.md':
        assert trim(data) == (data, 0)
verification['configuration_backup'] = config_backup.relative_to(ROOT).as_posix()
(DATA / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(verification, ensure_ascii=False, indent=2))
