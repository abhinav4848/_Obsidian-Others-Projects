Not only can you use Obsidian for writing, you can also use it for tracking submissions for publication. 

Disclaimer: I'm a writer of Science Fiction, mostly, and the publication process for that is slightly different than it is for non-genre work. These things should still work for you if you're shooting for _The New Yorker_, but I probably have some blind spots you'll hit. 


--- 

# Tracking Submissions with Obsidian

A lot of what I write is short fiction, and a lot of the process of writing short fiction is submitting it to places for publication. And a big part of *that* is tracking what stories you've submitted where, whether they were rejected or had edits requested, how long the market took getting back to you, and a host of other logistical details that prevent you from embarrassing mishaps. The question of how to track submissions is one that is probably as old as Gutenberg (I'm pretty sure most of the medieval monasteries were In House Only).

Most writers use spreadsheets, and this is a tried and true method that allows for ease of cross-referencing and locating information. But, as I am perversely determined to use plain text for everything, and one of the strengths of Obsidian is ease of cross-referencing, I'm doing it this way and finding it works quite well.  

My current system looks like this. There is a single file for each story, here's the one for the story codenamed "The Specialist" (all projects get codenames, as titles are subject to change). 

```
uid: 201707052332
tags: #jobsheet, #sub

---

#  The Specialist  #
WC 1754

## Actions

- [x] fix the middle scene 
- [ ] look to see when the next Fireside opening is

## Notes

- [[Crits from Writing Group]]

## Status

statCollect
statWrite
statEdit
#statSub
statWait 
statPub

- [x] Sketches
- [x] Outline
- [x] First Draft
- [x] Edits
- [x] Readers?
- [x] (Nth) Draft
- [x] Shipping
- [ ] Published!


## Subs Record ##

- Wordfire Press: "Monsters, Movies, & Mayhem", anthology call, [2019-10-02]--[2019-11-18]
    Anthology call
    - R 
    
- Asimov's [2019-11-27]--[2019-11-29]
    - R, form

- Clarkesworld [2019-11-30]--[2019-12-02]
    - R, Personal: "I thought the pacing needed work"
    
- Strange Horizons [2020-04-27]

```

A lot of this is an expansion of what Antony Johnston implemented in his [Getting Things Written](http://antonyjohnston.com/forwriters/gtw.php) article. Essentially I took his notion of "jobsheets" and expanded it to also include submissions data.
 
The top section is metadata which gets ignored by most markdown parsers. That's where I put tags, as well as a searchable unique identifier for each file. "sub" is the general tag for everything related to submissions process, including another document that lists markets I'm interested in, as well as some other general housekeeping documents. "jobsheets" is a list of just these per-story documents. 

Underneath the title is the Word Count of the story. It's the piece of information I always have to look up again every time I submit, so I just leave it in the file now. Under that is the "Actions" section, where I keep things I need to do. Usually by the time I get to submissions this is empty, because it's mostly useful when actually writing, but sometimes there's research to be done on markets. Then, under "Notes," I'll link to notes I've made about feedback or other research. 

The "Status" section is the secret sauce. It contains a list of tags, the same list for every story. Or rather, it contains a list of potential tags. I only put a `#` in front of the one that reflects the current status of the story. You can see this one has #statSub , which to me means "It's been rejected and is ready to be sent to the next market." And what this means is that I can click on #statSub and find every story that needs to be sent out. There are always too many, but solving that is outside the scope of this guide. 

I also have section of checklists here that are the same across all stories, showing the status before it's in submission. I took this idea from Antony Johnston's article, I've not found it to be particularly useful for the way I work, but I leave it here as a demonstration in case you find it helpful.

The Subs Record is where you keep track of history. For each submission there is a bullet point (they can also be headers if you wish to link to them, I never do so the bullet points are an aesthetic choice). Next to each one, I put the date I sent it out, and when it comes back I put an R for rejection, and any notes, such as feedback from the editors. I also add the date it came back, so I can easily see how long different pieces spent at different places. If there's significant feedback, I put it in its own note and link to it. 

Yes that story is still out at Strange Horizons at the time of this writing. Wish me luck! 

And here's the other half of the equation: 

```
tags: #stories #MOC #qqq 
links: [[060 Writings MOC|Writings]] 

---

# Stories


### On the market 

[[201910011903 --JOBSHEET-- Specialist Movie]]

### Ready to ship

[[201912011739 --JOBSHEET-- Breakers Field]]
[[201909170115 --JOBSHEET-- Lonely Probe]]
[[201909061614 --JOBSHEET-- City in a wild garden]]
[[201710230610 --JOBSHEET - GLOWWORMS]]
[[201707052332 --JOBSHEET-- -Tattoo]]
[[201910291708 --JOBSHEET - She Dances]]
[[202005082115 --JOBSHEET- Spider]]
[[201909170114 --JOBSHEET-- Liza Monroe]]
[[201707052334 --JOBSHEET-- -FirstThing]]

### Needs Editing 

[[202005050024 --JOBSHEET-- Missoula Praha]]

### Being Written

[[100 --PROJECT -- CLOCKS]]

### Published

[[201707052333 --JOBSHEET-- -FallingThrough]]
```

This file is called "Stories MOC" (for more on why "MOC," see [[IMF Glossary]]). It lists every story, from the moment they become a first draft, sorted by current status under headers. Yes, those are my actual story files. No, those are code names and not titles. I'm bad at titles but I'm not that bad. They all have JOBSHEET in the name to make them easier to find in the file system. 

Whenever a story's status changes, the first thing I do is edit this file, and immediately after, I edit the jobsheet for the story. That way I have a duplication of information for when I inevitability forget. I also track submissions on the wonderful [Submissions Grinder](https://thegrinder.diabolicalplots.com) (which I _highly_ recommend using if you're doing SFF), so I have multiple redundancy for when I inevitably forget something. 

Why track locally as well as on The Grinder? Honestly, I like having local data in case I'm offline, I like being able to store my notes on submissions and on the stories themselves in the same system so I can access either one easily. And, man, it is just so _satisfying_ to be able to mix and match searches and criteria to get exactly the information I'm looking for. And all in plain text files that are infinitely portable. 





