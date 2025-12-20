# My implementation of a reading inbox
This note describes the system which implements [[A reading inbox to capture possibly-useful references]].

Reading comes in many flavors, and different tools are appropriate for capturing and reading different types of media, but I “drain” all items from this inbox at the same time. [[Inboxes shouldn’t be split into multiple places]], so I create a “virtual” inbox which presents a unified layer across these items.
## Web pages
The database is managed by Pocket. I can add pages via browser extensions on desktop and mobile.
I chose Pocket because it is free, has a somewhat decent API, good extensions, and can double as a bookmarks manager.
I file web pages by archiving them; I trash them by trashing them.
## PDFs
I save them to `~/Documents/Archive/Inbox`. I have an Alfred workflow which copies/moves the PDF currently open in Preview to this folder.

I read PDFs in Skim because it supports linking to specific locations and exportable annotations.

I file PDFs by moving them to `~/Documents/Archive` and adding them to Zotero. I trash them by deleting them.

## e-books
I save them to `~/Documents/Archive/Inbox`.
I read e-books in Clearview, but I hate it (c.f. [[All desktop EPUB readers are awful]]).
I file e-books by moving them to `~/Documents/Archive` and adding them to Zotero. I trash them by deleting them.

## Physical books
I save a .bib representing the book to `~/Documents/Archive/Inbox`. I have a Shortcut to make this quick.

I file e-books by moving them to `~/Documents/Archive` then running `file_epub.sh`, which renames them according to their metadata. Then I remove their entry from the `.bib` from the `Inbox` folder.

# Reference
1. [Andy Link](https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ)