"""Check live note targets, footnotes, downloads, and preservation against the ZIP."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile
from integrate_august_letter import ROOT, WORK, TASK, ANDY, ATTACHMENTS, TITLE, INDEX, BOOK, PAPER, split_front, plain
from heading_spacing import trim

manifest = json.loads((TASK / 'applied.json').read_text(encoding='utf-8'))
for item in manifest['hashes']:
    assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['after'], item['path']
for asset in manifest['assets']:
    path = ROOT / asset['destination']
    assert path.is_file() and path.parent == ATTACHMENTS
    assert hashlib.sha256(path.read_bytes()).hexdigest() == asset['sha256']
    assert not re.search(r'[<>:"/\\|?*]', path.name)
chi = ATTACHMENTS / 'Chi et al - 1994 - Eliciting self-explanations improves understanding.pdf'
assert hashlib.sha256(chi.read_bytes()).hexdigest() == manifest['Chi_PDF_sha256']

letter = ANDY / (TITLE + '.md')
_, props, body = split_front(letter.read_text(encoding='utf-8'))
assert props['title'] == TITLE and isinstance(props['URL'], list)
assert re.findall(r'^# (.+)$', body, re.M) == [TITLE]
assert trim(letter.read_bytes()) == (letter.read_bytes(), 0)
assert '_Private copy; not to be shared publicly;' in body
assert not re.search(r'!\[[^]]*\]\(https?://', body), 'Remote image remains'
assert body.count('![[Andy Matuschak/Attachments/') == 2
references = re.findall(r'(?m)(?<!^)\[\^(\d+)\](?!:)', body)
definitions = re.findall(r'^\[\^(\d+)\]: ', body, re.M)
assert sorted(references) == ['1','2','3'] and sorted(definitions) == ['1','2','3']
assert not re.search(r'(?<!\^)\[(?:1|2|3)\]', body)
targets = []
for token in re.findall(r'\[\[([^]]+)\]\]', body):
    target = token.split('|', 1)[0]
    assert target.startswith('Andy Matuschak/')
    path = ROOT / (target if target.endswith(('.pdf','.png','.webp')) else target + '.md')
    assert path.is_file(), target
    targets.append(target)
assert len(targets) == 14
asset_map = {Path(a['destination']).name: a for a in manifest['assets']}
with zipfile.ZipFile(ROOT / manifest['backup']) as archive:
    assert archive.testzip() is None
    relative = letter.relative_to(ROOT).as_posix()
    _, before_props, before_body = split_front(archive.read(relative).decode('utf-8'))
    assert before_props == props
    assert plain(before_body) == plain(body)
    for title in [BOOK, PAPER]:
        path = ANDY / (title + '.md')
        relative = path.relative_to(ROOT).as_posix()
        _, before_props, before_body = split_front(archive.read(relative).decode('utf-8'))
        _, after_props, after_body = split_front(path.read_text(encoding='utf-8'))
        assert {k:v for k,v in before_props.items() if k != 'URL'} == {k:v for k,v in after_props.items() if k != 'URL'}
        assert set(before_props['URL']).issubset(after_props['URL'])
        assert after_body.startswith(before_body)
        linked = re.findall(r'\[\[Andy Matuschak/Attachments/([^]]+)\]\]', after_body)
        assert len(linked) == 1 and (ATTACHMENTS / linked[0]).is_file()
        assert asset_map[linked[0]]['fetch_URL'] in after_props['URL']
        assert trim(path.read_bytes()) == (path.read_bytes(), 0)
    path = ANDY / (INDEX + '.md')
    before = archive.read(path.relative_to(ROOT).as_posix()).decode('utf-8')
    after = path.read_bytes().decode('utf-8')
    assert after == before.replace('## Notes created by Codex', '## Previously missing letters', 1)

record = {'verified_at': datetime.now(timezone.utc).isoformat(), 'letter_internal_links_resolved': len(targets),
          'new_PDFs': 4, 'new_images': 2, 'existing_PDFs_reused': 1, 'download_integrity_verified': True,
          'PDFs_and_images_validated': True, 'source_URLs_added_to_existing_reference_notes': 2,
          'native_footnotes_resolved': 3, 'author_prose_and_caveats_preserved': True, 'private_notice_preserved': True,
          'letter_properties_preserved': True, 'blank_lines_after_changed_note_headings': 0,
          'index_change_limited_to_lower_heading': True, 'backup': manifest['backup']}
(TASK / 'verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
name = 'August letter integration'
report = '---\ntitle: "' + name + '"\n---\n# ' + name + '\n'
report += 'Integrated the user-supplied full text of [[' + letter.relative_to(ROOT).with_suffix('').as_posix() + ']]. The author’s prose, caveats, private notice, title, and URL list were preserved.\n\n'
report += '## Changes\n- Three article links now open the existing letter index and June letter.\n- Two Kintsch citations now open existing reference notes, with their PDF sources added to URL lists.\n- Relevant terms link to the existing Self-explanation and Reading comprehension notes.\n- Three citations use native footnotes under Footnotes.\n- Three blank lines immediately after headings were removed.\n- The index’s lower heading is Previously missing letters; everything above it is unchanged.\n\n'
report += '## Local attachments\nDownloaded four PDFs and two images. Reused the existing Chi PDF. All downloads passed native PDF/image validation and were checked against active local media before installation.\n\n'
report += ''.join('- [[' + asset['destination'] + ']]\n' for asset in manifest['assets'])
report += '\nPDF filenames follow `Author(s) - Year - Title.pdf`. Letter images follow `Andy- Letter subject N.ext`, retaining the original file format.\n\n'
report += '## Recovery\nOriginal notes and configuration are saved in `' + manifest['backup'] + '`. Download URLs, hashes, identity checks, duplicate checks, and new-file paths are recorded in `_Codex/august-letter-integration`.\n'
assert trim(report.encode('utf-8')) == (report.encode('utf-8'), 0)
path = WORK / (name + '.md')
assert not path.exists()
path.write_bytes(report.encode('utf-8'))
print(json.dumps(record, ensure_ascii=False, indent=2))
