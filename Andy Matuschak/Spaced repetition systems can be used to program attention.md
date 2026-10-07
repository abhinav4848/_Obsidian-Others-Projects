---
URL:
  - "https://notes.andymatuschak.org/zSK4LyrCbG9zDrdCWmcovUW?stackedNotes=zB92WZZ5baBHKZPPbWMbYEv&stackedNotes=z53zJy6y76MGuJuWW4Qvab9"
  - "https://notes.andymatuschak.org/zB92WZZ5baBHKZPPbWMbYEv"
title: "Spaced repetition systems can be used to program attention"
---
# Spaced repetition systems can be used to program attention
# Spaced repetition systems can be used to program attention
[[Spaced repetition memory systems make memory a choice]], but the computerized component’s value lies specifically in dynamically scheduling and selecting questions to be reviewed. In some sense, the efficacy of a [[Spaced Repetition memory system]] comes from its power to *program your attention* ([[Programmable attention]]). Think: “{cron} for your mind.” 

Manually making decisions about which cards to review would be far too taxing on a per-card basis. The transaction cost is too high. When that work is mostly outsourced, you can make a coarser decision—to devote your attention to SRS practice for 10 minutes—and then let your attention be directed by the machine within that block.

Systematically, we can generalize spaced repetition to:

- a priority queue of microtasks
    - (for memory tasks, in SM-2: a simple due date)
- an interactive environment which presents sufficiently high-priority tasks
    - (for memory tasks, a flashcard UI which shows “due” cards)
- feedback actions which modify a task’s subsequent priority
    - (for memory tasks, forgotten / remember modify the next due interval)

Within a traditional flashcard-style system, you can use this observation to go far beyond memorization: see [[Spaced repetition memory systems can be used to prompt application, synthesis, and creation]] and [[Spaced repetition may be a helpful tool to develop or change habits]]. [[Spaced repetition prompt design is about designing tasks for your future self]]. 

But the core *concept*—automatically arranging and presenting tasks according to some expanding schedule—can be instantiated in many interfaces and domains. I call this notion [[Andy Matuschak/Spaced everything|Spaced everything]].

As a pianist, I have a huge number of technical exercises that I maintain: e.g. scales, argpeggios, and patterns played in variations across each key. I only want to work on exercises for 20-30 minutes a day. Which ones should I do? You can imagine a system which:

- keeps track of each exercise, including axes of variation (blocked, arpeggiated; keys; modes)
    - priority is a function of both recency and the previous maximum tempo I achieved, relative to my target tempo
- presents a prioritized queue of 20-30 minutes worth of exercises
    - perhaps the exercise durations are estimated by measuring my practice
    - perhaps it can be configured to present at most 5 variations of any single exercise, to ensure breadth
- solicits feedback from me in terms of a subjective rating and/or a maximum tempo marking

It’s interesting to imagine a single interface malleable enough that I could define my piano exercises above as one sort of routine, and a SRS memory system as another routine—both special cases of a single general primitive.

Some examples:
- [[Incremental reading]]
- [[Andy Matuschak/Timeful text|Timeful text]] (Not worth linking)
- [[Spaced repetition may be a helpful tool to incrementally develop inklings]]
-  [[Spaced repetition can lower the stakes around destructive inbox-maintenance operations]] (to-do lists, email, reading lists, etc)
- [[Andy Matuschak/Readwise|Readwise]]

Related: 
- For applications which can use the simple SRS flashcard format, see [[Unusual applications of spaced repetition memory systems]]
- [[Andy Matuschak/Spaced repetition systems as catechism|Spaced repetition systems as catechism]]
- [[Andy Matuschak/OS-level spaced repetition system|OS-level spaced repetition system]]

# Related
**[[Evergreen note maintenance approximates spaced repetition]]** 
[[Triage strategies for maintaining inboxes (e.g. Inbox Zero) are often too brittle]], vs. using spaced-repetition to “approximate” inbox grooming.

I use this concept to engage with my implementation of [[A reading inbox to capture possibly-useful references]]

# References
2. Matuschak, A. (2019, December). *Taking knowledge work seriously*. Presented at the Stripe Convergence, San Francisco.