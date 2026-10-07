from audit import *
from lyt_cleanup import fm_body
from andy_cleanup import trail
import yaml

lp=json.loads((WORK/'lyt-plan.json').read_text(encoding='utf-8'))
ap=json.loads((WORK/'andy-plan.json').read_text(encoding='utf-8'))
vp=json.loads((WORK/'verification-final.json').read_text(encoding='utf-8'))

def wiki(path,label=None):
    return '[['+path.removesuffix('.md')+'|'+(label or Path(path).stem)+']]'

index=defaultdict(list)
for d in ap['decisions']:
    for url in d.get('URL',[]): index[trail(url)[-1]].append({'path':d['path'],'URL':url})
conflicts={k:v for k,v in index.items() if len(v)>1}
(WORK/'andy-source-index.json').write_text(json.dumps(dict(index),ensure_ascii=False,indent=2),encoding='utf-8')

source_lines=['# Andy sources to identify','',f"{ap['stats']['without_explicit_source']} notes have no clearly identified original-note source URL. Ordinary bibliography and related-note links were retained as citations.",'','Confirm the original note by its title and content before adding a URL. An external link somewhere in a note is not enough evidence that it is the note’s own source.','']
source_lines.extend('- '+wiki(d['path']) for d in ap['decisions'] if 'URL' not in d)
(WORK/'Andy sources to identify.md').write_text('\n'.join(source_lines)+'\n',encoding='utf-8')

conflict_lines=['# Source identity conflicts','',f'{len(conflicts)} source IDs appear as the final note for more than one local title. These may be excerpts from the same source, or captures whose URL continued to a different note. Their source trails have been shortened as requested; their identities still need checking. No notes in these groups were merged.','','For each group, open the original source, compare its heading and text with both local captures, and recover the correct source ID or record that the local note is an excerpt. Keep useful navigation context once the correct endpoint is established.','']
for note_id,notes in conflicts.items():
    conflict_lines.extend(['## '+note_id,''])
    conflict_lines.extend('- '+wiki(x['path']) for x in notes)
    conflict_lines.extend(['','[Open the source endpoint](https://notes.andymatuschak.org/'+note_id+')',''])
(WORK/'Source identity conflicts.md').write_text('\n'.join(conflict_lines),encoding='utf-8')

issue_lines=['# Captured link issues','','These are local file and section checks. They do not establish whether a remote website currently works. No further Andy or Lizards repairs listed here have been applied.','']
for scope in [CFG['andy_folder'],CFG['lizards_folder']]:
    records=vp['links'][scope]['unresolved']
    issue_lines.extend(['## '+scope,'',f'{len(records)} unresolved link occurrences.',''])
    for r in records:
        issue_lines.append('- '+wiki(r['source'])+f" — line {r['line']}: `"+r['target']+f"` ({r['status'].replace('_',' ')}).")
    issue_lines.append('')
issue_lines.extend(['## LYT reference omissions','','The completed LYT collection still contains links to material omitted from the creator’s distributed examples. Many are personal maps, people, publishers, or placeholders in templates. Missing material was not invented. Full locations are recorded in `verification-final.json`.','','There are 425 missing-file occurrences and one missing-section occurrence. All previously valid linked files retain a canonical target. The theme table of contents points to “How to Use LYT Mode”, a section absent from both supplied reference versions. The other stale theme heading was repaired to “Alternative Checkboxes aka Icon Bullets”.','','Frequent missing LYT targets:',''])
freq=Counter(r['target'] for r in vp['links'][CFG['lyt_folder']]['unresolved'] if r['status']=='missing_file')
issue_lines.extend(f'- `{target}` ({count} occurrences)' for target,count in freq.most_common(20))
(WORK/'Captured link issues.md').write_text('\n'.join(issue_lines)+'\n',encoding='utf-8')

andy_names=defaultdict(list)
for p in files(ROOT/CFG['andy_folder']):
    if p.suffix=='.md': andy_names[normalized_name(p)].append(p.relative_to(ROOT).as_posix())
dup_names=[v for v in andy_names.values() if len(v)>1]
lizard_numbers=defaultdict(list)
lizard_notes=[]
for p in files(ROOT/CFG['lizards_folder']):
    if p.suffix=='.md':
        lizard_notes.append(p)
        m=re.match(r'^(\d+[a-z]?)\s*-',p.stem,re.I)
        if m: lizard_numbers[m[1]].append(p.relative_to(ROOT).as_posix())
number_collisions={k:v for k,v in lizard_numbers.items() if len(v)>1}
(WORK/'recommendation-data.json').write_text(json.dumps({'andy_duplicate_title_candidates':dup_names,'andy_source_identity_conflicts':conflicts,'lizard_number_collisions':number_collisions},ensure_ascii=False,indent=2),encoding='utf-8')

report='''# Vault cleanup and recommendations

Completed on 7 October 2026.

## Changes applied

- Created `_Codex` for configuration, scripts, reports, and ZIP recovery backups.
- Consolidated 90 redundant LYT note copies. The 537 inventoried notes are now 449 notes, including two recovered linked examples from the Pro reference. Three additional unnamed import artifacts containing only `#` were archived.
- Restored the creator’s newer layout: `Atlas/Maps`; `Atlas/Dots/Things`, `Statements`, `People`, `Sources`, and `X`; `Calendar`; `Efforts`; and `x` for tools, templates, prompts, scripts, and images. Unique Pro source categories remain under `Atlas/Dots/Sources`.
- Preserved richer Pro material and user additions in canonical notes. For example, the full Pro analysis of Atomic Habits now accompanies the Lite copy’s metadata in a single book note. Kept distinct Home interfaces and genuinely different templates or concepts.
- Updated links, embeds, and folder references in queries to the merged-vault location. Preserved link labels and section/block references; added aliases for merged historical names. Consolidated duplicate image and Base files as well.
- Standardized 331 Andy notes to the `URL` property. A long source trail now retains exactly its final three notes: the first is the URL path, followed by up to two `stackedNotes` values. Shorter trails remain shorter. Removed standalone source lines and empty source-only headings, while retaining literature citations and inline references.
- Corrected three conflicting Andy source endpoints where the labeled source and copied content identified the intended note. Two were checked against the live source headings: [Elaborative encoding](https://notes.andymatuschak.org/z9Uq4yzBT1QaBU8twwyvm7P) and [In the Cells of the Eggplant](https://notes.andymatuschak.org/zAQj4GEE7PWDDcSreCGHTP9). The Cloze note’s labeled source explicitly names that note. Original trails and metadata conflicts remain in the audit records and backups.

## What I recommend next for Andy

1. **Recover missing provenance and check source identity.** There are 124 notes without an explicit original-note source URL, and 13 source IDs shared by different local titles. A URL may reach a related note instead of the one copied. Confirm headings and content before changing these. See [[_Codex/Andy sources to identify]] and [[_Codex/Source identity conflicts]].
2. **Merge the duplicate working-memory capture after comparing its content.** The two files “Working memory span is mostly independent of item complexity” differ only by an extra space in one filename, but the longer copy includes research citations missing from the other. Preserve those citations and the source URL in one note, with the old title as an alias. This has only been suggested.
3. **Repair a few capture mistakes; leave absent captures recognizable.** There are 30 missing-file link occurrences and one invalid section link. Examples: `Flow (What is a state of flow?)` differs from the existing Windows-safe filename; an OS-level spaced-repetition link accidentally includes “for more” inside its target; a Patreon link uses a heading marker for another note. Most remaining targets are notes or letters you have not captured. Retain their verified remote links rather than treating them as local notes. Details are in [[_Codex/Captured link issues]].
4. **Use a source ID when capturing future notes.** Record the final Andy note ID separately from its useful navigation URL. Keep an alias for the exact website heading when the filename needs Windows-safe punctuation. For existing matched sources, `andy-source-index.json` provides an initial lookup; the 13 identity conflicts need review before relying on it to convert remote links into local links.

## What I recommend next for LizardsFromOuterSpace

1. **Record the exact forum post URL in properties.** Keep the forum topic ID, post number, original note label, author, and capture date as separate provenance. A displayed note number and its actual forum post number can differ. The [original Zettelkasten post](https://forum.obsidian.md/t/obsidian-zettelkasten/1999/2) includes links to other posts whose titles/numbering have not all survived the capture.
2. **Preserve the numbered sequence and resolve naming issues with aliases first.** There are 13 unresolved local link occurrences. `168- To Index or Not Index` is already present; the broken link contains nonbreaking spaces. The link “114- Zettelksaten is about Knowledge Development” should be compared with the existing “114- Knowledge Development” before repair. Several targets in the opening Zettelkasten note were never captured.
3. **Treat citations as citations.** In `043- Concept`, copied reference labels `[[4]]` and `[[5]]` have become links to nonexistent notes. Restore them as external references or footnotes. Retrieve the missing “The Knowledge cycle Option C.png” diagram from its original forum post if you want a complete offline copy.
4. **Check the two notes labeled 055 against their original posts.** “External Models” and “Internal models” are different concepts sharing that prefix. Avoid renumbering the sequence until their source identity is confirmed. The External Models note also links to itself where the sentence discusses internalization; that warrants a content check against the original post.

## Verification and remaining limits

The final LYT collection has no duplicate normalized titles or identical Markdown files. Every previously valid linked file still has a canonical destination. All updated Andy source properties parse correctly and retain at most three notes; repeating the source transformation produces no further changes. Parsed non-template LYT properties pass validation.

The two LYT reference collections, Lizards files, other collection files, and Andy attachments passed preservation checks. Obsidian settings and your existing unrelated changes were retained.

LYT still has 425 missing-file link occurrences and one absent theme section. Many come from the creator’s deliberately omitted personal material or template placeholders, rather than from the consolidation. These have been recorded rather than fabricated. Static checks cannot confirm all remote URLs or query rendering in Obsidian; only selected sources were checked online.

## Recovery and records

- `backups/lyt-before-2026-10-07.zip` holds the original LYT files, including the three unnamed artifacts.
- `backups/andy-before-2026-10-07.zip` holds all original Andy Markdown notes.
- `lyt-plan.json` records each source-to-canonical mapping, merged metadata, and version decisions.
- `andy-plan.json` records original and shortened source URLs per note.
- `verification-final.json` lists unresolved link locations and verification results.

ZIPs keep recovery copies out of Obsidian’s note index. No further Andy or Lizards edits proposed in this report have been applied.
'''
report=report.replace('Standardized 331 Andy notes',f"Standardized {ap['stats']['source_properties_standardized']} Andy notes").replace('124 notes',f"{ap['stats']['without_explicit_source']} notes").replace('13 source IDs',f'{len(conflicts)} source IDs').replace('the 13 identity conflicts',f'the {len(conflicts)} identity conflicts')
report=report.replace('Shorter trails remain shorter.','Shorter trails remain shorter. The remaining long inline navigation links were also cropped to the same three-note limit, preserving their link text.')
(WORK/'Review and recommendations.md').write_text(report,encoding='utf-8')
print(json.dumps({'report':'_Codex/Review and recommendations.md','source_identity_conflict_groups':len(conflicts),'andy_duplicate_title_candidates':dup_names,'lizard_number_collisions':number_collisions,'lizard_notes':len(lizard_notes)},ensure_ascii=False,indent=2))
