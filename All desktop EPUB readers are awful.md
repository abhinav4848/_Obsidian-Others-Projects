# All desktop EPUB readers are awful
It’s pretty shocking how bad e-book readers are on the desktop.

I spent some time evaluating a bunch of them as part of a larger program to [[Write about what you read to internalize texts deeply]]. I tried:
- Apple Books
- Kindle
- Calibre ebook-viewer
- ClearView
- Adobe Digital Editions
- FBReader (doesn’t really work at all)
- Kobo (basically doesn’t work at all)

There’s no solution which both supports annotations and also the ability to jump to durable locations. That’s… pretty awful.

## Referring to pages and locations
These apps have no ability to jump to a specific location:
- Apple Books
- FBReader
- Kobo

Kindle lets you jump to either a specific location or page, depending on the book. Either way, it’ll make sure it’s durable.

Calibre will let you jump to a durable location (meaningful only within Calibre). It has no notion of page numbers.

ClearView and ADE let you jump only to page numbers which depend on the window’s size (not durable).

### Page number support
None of these readers supports the EPUB 3 standard for mapping physical book page numbers onto the e-book page numbers. Kindle supports a proprietary variant of this standard.

### Scriptability
Of these, only Calibre supports jumping to a location programmatically, so it’s not possible to make direct links into books in these other readers.

ClearView has a private API for jumping to a page, but the pages aren’t durable, so that’s not great.

## Annotation support
Calibre and FBReader don’t support annotation at all. The others support basic annotations, but of those, only ClearView offers export. None of them stores the annotations in a fashion which other programs can easily access programmatically. At the UI level, only Apple Books has a decent implementation.

## Multiple windows
None of these editors supports multiple views on a single book. It’s not possible to look at multiple pages at once in any of them. Madness. [[Parallel reading is mostly impossible in digital reading]]

## Syncing
Only Kindle and Apple Books sync across devices. Kindle’s implementation is very limited: it will sync books across Kindle hardware and iOS devices, but not with the Mac. And it won’t sync highlights or metadata at all. Apple Books’s sync implementation is pretty perfect.

# Notes on individual readers
- Clearview X
    - Sort of a decent Mac citizen, reasonably snappy
    - Acts as a document viewer—doesn’t insist on being a “library”
    - Keyboard shortcuts for annotations
    - Marginal notes are hidden: [[Few digital reading environments support marginal notes]]
    - Can manually export highlights / notes as RTF
    - No AppleScript, Shortcuts, or URL scheme support for scriptability
    - Has page numbers / “go to page number”, not clear how they’re implemented
    - Poor typography, as usual
- [[Readwise]] Reader
    - Okay typography!
    - Has marginal notes! contra [[Few digital reading environments support marginal notes]]
    - Graceful highlighting / note-taking interaction; nice keyboard support
    - Doesn’t function as a native app, have to upload epubs to the cloud first
    - Unacceptably slow response to markup interactions
    - Doesn’t seem to respect the ebook’s page layout markup
- MarginNote 3
    - Non-native styling and interaction model; clunky
    - Awful typography
    - Actually supports marginal notes
- Calibre
    - QT abomination; awful typography
    - No marginal notes
- FBReader
    - Cross-platform abomination UI; awful typography

# Reference
1. [Andy Link](https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ&stackedNotes=zX95uZHiGWNiNTDF3wETWtq)