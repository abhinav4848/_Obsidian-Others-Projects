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
