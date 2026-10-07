---
title: "README"
---
# README
# Codex workspace
This folder holds the configuration, audit reports, scripts, and recovery backups for work on this vault.

## Scope
- The Popular Vaults vault is the working collection.
- The two separate LYT vaults are read-only references.
- Consolidate LYT copies using the newer Lite layout, retaining unique Pro material and user additions.
- Preserve note content, aliases, links, and useful version-specific features.
- Standardize Andy Matuschak source URLs into the `URL` property, preserving the final three notes of each navigation stack (the first becomes the URL path, the other two remain `stackedNotes` parameters).
- Other Andy and LizardsFromOuterSpace changes are recommendations only.
- Keep recovery copies in ZIP files so that backups do not create duplicate Obsidian notes.

All task-specific configuration lives here. Existing Obsidian settings are not moved into this folder.

## Markdown preference
Do not put blank lines immediately after headings. This preference applies throughout Popular Vaults, including reports in this folder. Preserve whitespace inside code blocks. Vault-wide heading spacing changes are authorized across all collections, including Andy and Lizards; their other content changes remain recommendations only.

`heading_spacing.py` applies this preference and saves a ZIP recovery snapshot of changed notes. Its change record is independent of the earlier content-consolidation checksums, which describe the state before this later formatting edit.

## Later authorized changes
- Recover media-sync images from exact saved source addresses into root `Attachments`; keep downloaded files and repaired note references verified.
- Convert Andy article links to existing internal notes when their identity is clear. Add missing source addresses under References, explicitly labelled as sources. Preserve ambiguous links for review.

## Captured filenames and Andy properties
Every Markdown file in the working vault has its current filename (without `.md`) in its first heading and `title` property. These are stored values: retain them after a future file rename so the captured name remains retrievable. Existing different headings were preserved below the filename heading.

Andy import fields Type of Link, Author: Andy Matuschak, Completion Status and Last edited time were removed. Explicit source links from the body were consolidated into the `URL` property, including links previously labelled Source for this file. Other reference material was retained. Remaining notes without an identifiable source are listed in `Andy sources to identify.md`.

The original notes for this pass are saved in the ZIP named in `note-titles-and-sources-applied.json`. The separate LYT reference vaults were not edited.

## URL lists and online sources
All copied Andy notes have source URLs. All existing `URL` values across the working vault are YAML lists; Andy’s local ReadMe index uses an empty list. `property-types.json` records the authorized List type, with the required native copy in `.obsidian/types.json`. Online evidence and change records live in `andy-online`. Keep existing navigation trails to at most three notes. Preserve captured names after renames.
