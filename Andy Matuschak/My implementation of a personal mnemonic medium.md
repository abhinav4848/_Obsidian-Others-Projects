---
URLs:
  - https://notes.andymatuschak.org/z8kPkXQZ3wVR5DfJ79uhnuz?stackedNotes=z6sX7ZcYdPiya3SzQ5segaq
---
# My implementation of a personal mnemonic medium
I have implemented [[The mnemonic medium can be extended to one’s personal notes]] in my own [[Note-writing system]].

The system works by continuously scanning a set of Markdown files for embedded prompts (see syntax below). Prompts are then considered part of my working set for spaced repetition reviews. I’ve also implemented a component which continuously syncs those extracted prompts to Anki.

Some example notes which include this feature:
- [[Channel capacity of humans as information processors]]
- [[Human channel capacity increases with bits-per-chunk]]

For the implementation, see [https://github.com/andymatuschak/computer-supported-thinking](https://github.com/andymatuschak/computer-supported-thinking). 

For ongoing unprocessed thoughts, see [Log: personal mnemonic medium](https://notes.andymatuschak.org/zDuBTrCGDkf2J2TbtQwKDed) (no access)

## Syntax
### Creating typical two-sided SRS prompts
> Q. How many dimensions are in a qubit’s vector space?  
> A. Two.

The empty line between the question and answer is optional. The question and answer cannot currently span multiple paragraphs: the paragraph including Q. or A. is extracted as that field.

### Creating cloze deletion prompts
In the context of prose notes, I’m finding cloze deletions are often somewhat more natural. This paragraph maps onto a single cloze deletion prompt with three cards:

> Once activated, a service worker {performs one-time startup computation}, then transitions to {idle}. From that state, it’ll handle {fetch or message events} until it eventually terminates.

The cloze prompt will use the entire paragraph surrounding the text. For example, this two-sided prompt is equivalent to one of the cards extracted from the previous example:

> Q. Once activated, a service worker **???**, then transitions to idle. From that state, it’ll handle fetch or message events until it eventually terminates.  
> A. Once activated, a service worker _performs one-time startup computation_, then transitions to idle. From that state, it’ll handle fetch or message events until it eventually terminates.

### Idempotency and identity
This system is meant to operate idempotently. That is: you can keep revising your note files over time, and it’ll keep track of changes accordingly. As you change your notes, the system will maintain your SRS state for all the embedded prompts, except for the prompts you’ve directly edited.

Somewhat more precisely, the embedded prompts have _identity_. You can modify the note around a prompt or even move the prompt to a new note, and your review history will be preserved. But if you modify a prompt’s text, it will be treated as a new prompt, and your review history won’t be ported from the old prompt. That’s because this system’s based on dumb plaintext files, which don’t have enough semantic structure to unambiguously specify whether a given modification represents a new prompt or a modification of an old one. Fixing this would require introducing heuristics or extra identifying markup.

Two-sided prompt identities are derived from the hash of their question and answer text. Cloze prompt identities are derived from the hash of their containing paragraph.

While the system will happily track prompts if you move them between note files, the behavior is undefined if identical prompts appear in multiple note files.

# Reference
1. [Andy Link](https://notes.andymatuschak.org/z8kPkXQZ3wVR5DfJ79uhnuz?stackedNotes=z6sX7ZcYdPiya3SzQ5segaq)