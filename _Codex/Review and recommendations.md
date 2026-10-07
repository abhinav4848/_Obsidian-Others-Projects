---
title: "Review and recommendations"
---
# Review and recommendations
# Vault cleanup and recommendations
Completed on 7 October 2026.

## Changes applied
- Created `_Codex` for configuration, scripts, reports, and ZIP recovery backups.
- Consolidated 90 redundant LYT note copies. The 537 inventoried notes are now 449 notes, including two recovered linked examples from the Pro reference. Three additional unnamed import artifacts containing only `#` were archived.
- Restored the creator’s newer layout: `Atlas/Maps`; `Atlas/Dots/Things`, `Statements`, `People`, `Sources`, and `X`; `Calendar`; `Efforts`; and `x` for tools, templates, prompts, scripts, and images. Unique Pro source categories remain under `Atlas/Dots/Sources`.
- Preserved richer Pro material and user additions in canonical notes. For example, the full Pro analysis of Atomic Habits now accompanies the Lite copy’s metadata in a single book note. Kept distinct Home interfaces and genuinely different templates or concepts.
- Updated links, embeds, and folder references in queries to the merged-vault location. Preserved link labels and section/block references; added aliases for merged historical names. Consolidated duplicate image and Base files as well.
- Standardized 339 Andy notes to the `URL` property. A long source trail now retains exactly its final three notes: the first is the URL path, followed by up to two `stackedNotes` values. Shorter trails remain shorter. The remaining long inline navigation links were also cropped to the same three-note limit, preserving their link text. Removed standalone source lines and empty source-only headings, while retaining literature citations and inline references.
- Corrected three conflicting Andy source endpoints where the labeled source and copied content identified the intended note. Two were checked against the live source headings: [Elaborative encoding](https://notes.andymatuschak.org/z9Uq4yzBT1QaBU8twwyvm7P) and [In the Cells of the Eggplant](https://notes.andymatuschak.org/zAQj4GEE7PWDDcSreCGHTP9). The Cloze note’s labeled source explicitly names that note. Original trails and metadata conflicts remain in the audit records and backups.

## What I recommend next for Andy
1. **Recover missing provenance and check source identity.** There are 116 notes without an explicit original-note source URL, and 14 source IDs shared by different local titles. A URL may reach a related note instead of the one copied. Confirm headings and content before changing these. See [[_Codex/Andy sources to identify]] and [[_Codex/Source identity conflicts]].
2. **Merge the duplicate working-memory capture after comparing its content.** The two files “Working memory span is mostly independent of item complexity” differ only by an extra space in one filename, but the longer copy includes research citations missing from the other. Preserve those citations and the source URL in one note, with the old title as an alias. This has only been suggested.
3. **Repair a few capture mistakes; leave absent captures recognizable.** There are 30 missing-file link occurrences and one invalid section link. Examples: `Flow (What is a state of flow?)` differs from the existing Windows-safe filename; an OS-level spaced-repetition link accidentally includes “for more” inside its target; a Patreon link uses a heading marker for another note. Most remaining targets are notes or letters you have not captured. Retain their verified remote links rather than treating them as local notes. Details are in [[_Codex/Captured link issues]].
4. **Use a source ID when capturing future notes.** Record the final Andy note ID separately from its useful navigation URL. Keep an alias for the exact website heading when the filename needs Windows-safe punctuation. For existing matched sources, `andy-source-index.json` provides an initial lookup; the 14 identity conflicts need review before relying on it to convert remote links into local links.

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
