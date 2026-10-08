from pathlib import Path
import hashlib, json, os, re, zipfile
from datetime import datetime, timezone
from integrate_remaining_letters import front, display_plain, trim

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / '_Codex'
TASK = WORK / 'letters-integration'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    assert not (TASK / 'verification.json').exists(), 'Already verified'
    record = json.loads((TASK / 'applied.json').read_text(encoding='utf-8'))
    baseline = json.loads((TASK / 'baseline.json').read_text(encoding='utf-8'))
    changed = {row['path']: row for row in record['hashes']}
    checked_targets = set()
    with zipfile.ZipFile(ROOT / record['backup']) as backup:
        assert backup.testzip() is None
        for relative, row in changed.items():
            path = ROOT / relative
            original = backup.read(relative)
            current = path.read_bytes()
            assert digest(original) == row['before'] == baseline[relative]
            assert digest(current) == row['after']
            _, before_props, before = front(original.decode('utf-8'))
            _, props, body = front(current.decode('utf-8'))
            assert props == before_props
            assert props['title'] == path.stem and isinstance(props['URL'], list)
            assert display_plain(before, path.stem) == display_plain(body, path.stem)
            assert re.findall(r'^# (.+)$', body, re.M) == [path.stem]
            assert trim(current)[1] == 0
            assert not re.search(r'!\[[^]]*\]\(https?://', body)
            definitions = re.findall(r'^\[\^(\d+)\]:', body, re.M)
            references = re.findall(r'\[\^(\d+)\](?!:)', body)
            assert len(definitions) == len(set(definitions))
            assert set(definitions) == set(references)
            for target in re.findall(r'\[\[(Andy Matuschak/Attachments/[^]|]+)', body):
                assert (ROOT / target.split('#', 1)[0]).is_file(), target
                checked_targets.add(target)
    for relative, expected in baseline.items():
        if relative not in changed:
            assert digest((ROOT / relative).read_bytes()) == expected, 'Unrelated change: ' + relative
    for target in record['introduced_targets']:
        assert (ROOT / target.split('#', 1)[0]).is_file(), target
        checked_targets.add(target)
    for row in record['letters']:
        body = (ROOT / row['note']).read_text(encoding='utf-8')
        for link in row['links']:
            assert '[[Andy Matuschak/' + link['target'] + '|' + link['label'] + ']]' in body
        for target in row['concepts']:
            assert (ROOT / 'Andy Matuschak' / (target + '.md')).is_file()
            assert '[[Andy Matuschak/' + target + '|' in body
            checked_targets.add('Andy Matuschak/' + target + '.md')
    installed = [a for a in record['assets'] if a.get('install')]
    for asset in record['assets']:
        assert digest((ROOT / asset['destination']).read_bytes()) == asset['sha256']
    native = json.loads((TASK / 'asset-validation.json').read_text(encoding='utf-8'))
    assert len(installed) == 35
    assert len({a['sha256'] for a in installed}) == len(installed)
    assert not ({a['sha256'] for a in installed} & set(baseline.values()))
    result = {
        'verified_at': datetime.now(timezone.utc).isoformat(),
        'letters': len(changed),
        'external_links_converted': sum(len(r['links']) for r in record['letters']),
        'concept_links_added': sum(len(r['concepts']) for r in record['letters']),
        'native_footnotes': sum(r['footnotes'] for r in record['letters']),
        'heading_blank_lines_removed': sum(r['heading_blank_lines_removed'] for r in record['letters']),
        'PDFs_downloaded': sum(a['kind'] == 'PDF' for a in installed),
        'images_downloaded': sum(a['kind'] != 'PDF' for a in installed),
        'PDF_sources_reused': sum(a['status'] == 'reused' for a in record['assets']),
        'local_targets_checked': len(checked_targets),
        'checks': ['Captured prose preserved', 'Properties and page titles preserved',
                   'Footnote references and definitions match', 'New local links resolve',
                   'Final attachments match validated downloads', 'No duplicate downloads',
                   'August letter, index, previous attachments and other Andy files unchanged'],
        'native_asset_validation': '_Codex/letters-integration/asset-validation.json',
        'backup': record['backup']
    }
    (TASK / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    # Preserve configuration history before documenting the completed pass.
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    with zipfile.ZipFile(WORK / 'backups' / ('remaining-letters-config-before-' + stamp + '.zip'), 'x', zipfile.ZIP_DEFLATED) as backup:
        for name in ['config.json', 'README.md']:
            backup.writestr('_Codex/' + name, (WORK / name).read_bytes())
    config = json.loads((WORK / 'config.json').read_text(encoding='utf-8'))
    config['andy_patreon_letters']['integration_records'] = [
        '_Codex/august-letter-integration/applied.json', '_Codex/letters-integration/applied.json']
    config['andy_patreon_letters']['footnotes'] = 'Native Obsidian Markdown footnotes under Footnotes'
    updates = {
        WORK / 'config.json': json.dumps(config, ensure_ascii=False, indent=2) + '\n',
        WORK / 'README.md': (WORK / 'README.md').read_text(encoding='utf-8').rstrip() + '\n\n## Remaining Patreon letter integration\nThe same integration is complete for the other 18 indexed letters. Captured prose and URL-list properties were preserved. Existing article notes are linked internally; cited PDFs and images use Andy Matuschak/Attachments with the established filenames. Native footnotes and heading spacing are standardized. See Remaining letter integration.md and letters-integration for verification and recovery records.\n',
        WORK / 'Remaining letter integration.md': '''---
title: Remaining letter integration
---
# Remaining letter integration
Applied the approved August-letter treatment to the other 18 letters in the existing index.
## Changes
- Converted 28 source-verified article links to existing local notes.
- Added 28 links to existing concept notes, retaining the original wording.
- Standardized 13 footnotes and removed 41 blank lines immediately after headings.
- Downloaded 8 PDFs and 27 images into `Andy Matuschak/Attachments`; reused 11 existing PDF sources.
- Retained native image formats, including the animated GIF.
- Preserved each letter’s captured prose, source URL lists, title properties and filename headings.
## Attachment names and sources
PDFs use `Author(s) - Year - Title.pdf`. Images use `Andy- Letter subject N.ext`.
The old IPFS PDF address returned an error. The same DRAFT 3 was obtained from the [Protocol Labs publisher copy](https://research.protocol.ai/publications/ipfs-content-addressed-versioned-p2p-file-system/benet2014.pdf). Original citation addresses remain in the letters alongside local PDF links; download records include the alternate source.
## Verification
All introduced local links resolve. Footnote references match their definitions. PDF and image files were parsed before installation, and their final hashes match the validated downloads. Captured prose was compared against the recovery ZIP after normalizing link and footnote formatting. No duplicate attachments were installed. The August letter, index, existing attachments and other Andy files were unchanged.
## Recovery records
''' + '- Original notes: `' + record['backup'] + '`\n- Changes and sources: `_Codex/letters-integration/applied.json`\n- Verification: `_Codex/letters-integration/verification.json`\n- Native file checks: `_Codex/letters-integration/asset-validation.json`\n'
    }
    temporary = TASK / 'documentation.tmp'
    for path, text in updates.items():
        temporary.write_text(text, encoding='utf-8')
        os.replace(temporary, path)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
