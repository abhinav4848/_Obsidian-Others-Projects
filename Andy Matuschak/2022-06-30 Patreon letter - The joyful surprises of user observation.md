---
URL:
  - "https://notes.andymatuschak.org/zKEj4ek9pYukS2sj5jZ1cGo"
  - "https://www.patreon.com/posts/joyful-surprises-68479856"
title: "2022-06-30 Patreon letter - The joyful surprises of user observation"
---
# 2022-06-30 Patreon letter - The joyful surprises of user observation
_Private copy; not to be shared publicly; part of [[Andy Matuschak/Patron letters on memory system experiments|Patron letters on memory system experiments]]_

I designed [something new](https://www.patreon.com/posts/demo-talk-new-66348634?cid=85507220), and I’ve spent much of the past few weeks watching people use it. Those sessions have been generative and energizing. They always are. There’s something magical about this part of the design process, in both the sense of delight and of mystery.

Rocket scientists have it easy. Well, at least along one narrow axis. When you’re trying to launch a rocket, you can’t just sum up its mass and add enough fuel to lift that mass into orbit. The rocket fuel itself adds mass, too. So you add enough extra fuel to launch the rocket, plus the fuel, and then you add enough to launch the extra fuel you just added, and so on. Happily, we know how to solve differential equations, and this infinite loop has a nice closed-form solution.

Design is loopy in a more inconvenient fashion. If you’re designing a new sort of artifact—say, the automobile—you can’t just consider the mechanics of how it moves its passenger from point A to point B. Design is ecological. People who can move at 30mph on demand will often structure their lives quite differently from a pedestrian alternative. When a large group of these people interact, transformed city structures will emerge. And one element of that transformation will be better roads, which might permit 70mph motion, which begets more transformation, and so on.

This loop does not have a predictable fixed point. Sufficiently interesting new artifacts will immediately obviate a designer’s meticulous “user journey” flowchart.

All this is to say: as a designer, it is good to [[Andy Matuschak/2021-02-02 Patreon letter - In search of better questions|make careful questions]] and careful theories, and to form artifacts using those theories. Then it is good to step back, to watch people in action, to see how the artifact’s contours reshape behavior and demand new theories. This is not “user testing.” You’re not primarily interested in “does it work?”. You want an expansive, curious stance—excited to redefine the problem statement based on what you see.

## In praise of lightness
In March, I arrived at a set of design primitives which seemed good enough to be worth trying. In April, I wrote a talk which unpacked my ideas in various contexts. Iteration on the talk drove iteration on the design. In May, I hacked together a prototype to provide the talk’s visuals, recorded it, and [published](https://www.patreon.com/posts/demo-talk-new-66348634?cid=85507220) it. Then I let it sit while I traveled for a few weeks.

When I returned, I watched the talk again and felt an enormous internal… _blecch_. I thought: yeah, I’m still excited about this solution, but it’s so intricate. There are still no onboarding affordances. It’ll take _months_ of unpleasant drudgery to build it out for a public test.

Over dinner, my friend [Rob Ochshorn](https://rmozone.com/) pointed out something terribly important which I’d forgotten. Consider how the following two scenarios feel:

In the first, you’re sitting someone down in a chair next to your laptop. You show them a design and scoot the laptop over so you can watch how they use it. When stuff breaks, you explain what’s going on, laugh at your scrappy prototype, and reach over them to type some reset command. You issue footnotes in realtime as your user moves through the demo: “oh, yeah, that bit’s not implemented yet.”

In the second scenario, you’re emailing someone a link to a prototype. The email has to somehow explain all those caveats and footnotes you were providing in realtime. You realize, seeing that massive text block, that your recipient will probably skip over all that and just click the link. You can’t smooth over the prototype in realtime when it gets wedged, so you work through the dozens of rough edges on your punch list which aren’t really central to the concept.

I’ve been making scrappy prototypes for years, but somehow, I had forgotten this distinction. Rob observed that I seemed to be aiming for the second scenario (or even a more elaborate public variant of it). He gently asked what it might take to make the first scenario happen next week, rather than next month or next quarter. And I felt this absolutely enormous internal unclenching.

The smoke-and-mirrors prototype I’d made for my talk only worked in that one path I demonstrated. I’d planned to throw it out and build a “for real” prototype that integrated with the existing Orbit system. But a “what about next week?” framing made me take a scrappier path, hacking my talk’s demo prototype into something usable, with a lot of asterisks.

It also made me choose my test audience carefully. My design was too incomplete to put in front of people who’d never heard of spaced repetition. Learning from that audience would take many weeks of new design work, but I realized that I could put a prototype in front of experienced users much more rapidly. Ideally, I want primitives with [low floors, wide walls, and high ceilings](https://mres.medium.com/designing-for-wide-walls-323bdb4e7277). Experienced users will help me with the ceilings and walls; I can focus on the floors in future iterations.

I had my first sessions with demo readers that next week, just as Rob had suggested. My prototype broke in all kinds of silly ways, but it didn’t matter, because I was there to laugh at it and smooth over the issues. More importantly, it worked well enough (in my presence, anyway) for people to read the demo text in seriousness—well enough for me to learn an enormous amount about how people interacted with it, and about how it affected their reading behavior.

The following week, I smoothed over the biggest rough edges I’d seen with my in-person testing and held a bunch of demo sessions live over Zoom. Prototypes must be in much better shape to get clear insight from this kind of testing: the rapport is weaker; you can’t easily gesture at elements on their screen; you can’t reach over their arms to fix things. Perhaps more importantly, you miss out on a huge amount of information in body language.

I kept fixing the rough edges people encountered, making the prototype stand on its own with a little more stability. The following week, I [shared](https://www.patreon.com/posts/first-usable-for-68204106) the demo with a limited, high-context audience (you!). I asked people to record stream-of-consciousness thoughts into a text file. This was a low-effort way to collect a lot more data, though of course each log carries a tiny sliver of the information I gleaned from in-person sessions.

This whole sequence felt just great. The incremental steps freed me from the deep aversion I felt upon my return. More importantly, they kept me from building a much higher-fidelity prototype than was necessary to learn what I needed. I’m in the process of substantially redesigning the primitives now based on my observations. It’s much better to be doing that after a few weeks of refining a scrappy prototype than it would be after a few months of building a publicly accessible one!

The main thing I learned last year by shipping Orbit was: the [[Andy Matuschak/Mnemonic medium|mnemonic medium]] won’t work, as originally designed, in most other reading contexts; readers must be given much more control. I think I could have learned that a lot more rapidly and iteratively by building one-offs with a few handpicked authors, rather than building a real “platform” as I did. The solidity of the implementation is higher than the solidity of the design work—that’s never a good idea.

All this is laughably design-101. Yes, dummy, you should make scrappy prototypes and test them and throw them out. On the ground, it’s been hard to reconcile that with my aspiration to explore systems in serious contexts. This month’s prototyping has taught me to pursue a greater feeling of lightness and motion in my work. I’d like to find ways to dodge elements which feel like “infrastructure.” If that means I need to stand there, holding up the retaining walls while I watch you work, maybe that’s fine.

## Some surprising observations
Feedback from the last few weeks uncovered some important issues with the primitives which will lead to fundamental changes. But it’ll be much more interesting to talk about those bits once I have new designs in hand. Instead, I’d like to share a few examples of reader reactions which push around the problem definition, the precious and subtle kind of reactions which only emerge once people are actually using a design to do something real.

### Induced demand
Here’s another analogue to the recursive rocket fuel weight problem. There’s too much traffic on the highway into your city, so you spend a billion dollars and build four extra lanes, massively increasing capacity. Now there are more cars on the road, but everyone’s still stuck in traffic, and their commute takes just as long. Oops: [induced demand](https://en.wikipedia.org/wiki/Induced_demand). “Pent-up” demand is released by increased supply.

I was fascinated to watch a similar dynamic play out with this prototype.

[In this new design](https://www.patreon.com/posts/demo-talk-new-66348634?cid=85507220), I’ve made the spaced repetition prompts feel more like marginalia. They have an object-like tactility, a permanent spatial position on the page in a sidebar element.

![[Andy Matuschak/Attachments/Andy- The joyful surprises of user observation 1.png]]

Immediately, almost every single tester found themselves wanting all the other trappings of marginalia and its attendant facilities. People wanted to highlight; people wanted to make clippings; people wanted to scribble non-prompt textual notes. The cropping rectangle pulls still further back. People wanted to pull those clippings out and connect them across readings. People wanted to transclude and link bits into and out of their personal knowledge management systems.

All this makes sense—truly! It’s why I’ve been living with a [“personal” mnemonic medium for years](https://notes.andymatuschak.org/z5ARNXtS5VxteskEW91S1yYTgAcLABNXsZuJE). But these requests were suddenly so much more intense. These impulses came up rarely in discussions about [Quantum Country](https://quantum.country/) and [Orbit](https://withorbit.com/) as it exists today. Add a sidebar with a nod to peritext, and wham: induced demand. People suddenly felt much more sharply what they wanted.

### Prompts as structured reading affordances
Another surprise was the way these peritextual prompts strongly influenced the reading experience. More than half of my readers found themselves sometimes scanning the spaced repetition prompts _first_—using them as a sort of high-level summary. If a prompt seemed interesting, they’d jump into the associated main text.

This makes some sense. Prompts are a sort of compression: they curate and distill the most important elements of the text for reinforcement. But if structured reading is the aspiration, prompts are probably not the best affordance. They contain syntax noise: extra words necessary to frame the point as a question. And often a single point requires several prompts to capture its various angles.

Several testers suggested a comparison to [Christopher Alexander’s The Timeless Way of Building](https://en.wikipedia.org/wiki/The_Timeless_Way_of_Building), which contains an unusual device for structured reading:  
![[Andy Matuschak/Attachments/Andy- The joyful surprises of user observation 2.png]]

Even if I’m skeptical that spaced repetition prompts are the right primitive, structured reading affordances seem under-explored in the epoch of dynamic media.

### Reading on computers is terrible
A huge fraction of my test readers would happily proceed through the demo, expressing interest in the various affordances and augmentations. Then, as we’re wrapping up, they’d say something like: “But you know, I don’t usually read stuff like this on the computer. I read on paper, or on a Kindle. I kind of hate reading on the computer.” Some of these people offered a grim silver lining: “If I could use this system with everything I read, that might be enough to make me want to read on a computer!”

I’m not sure why this didn’t come up often more during Quantum Country user testing. Maybe it’s because this new prototype invites readers to think about generalizing it to everything they read, whereas Quantum Country seems like a one-off.

These people are right. [Reading long texts on computers is terrible](https://notes.andymatuschak.org/z7yjjydTNu3bujTeFc7Hey1iFbz513SnN6oss), and I’ve been idly collecting notes on the problem for years. I’m certainly not happy with an outcome where we all hate reading texts on computers, but we grumpily put up with it because of the nice cybernetics. This is a problem not just for the mnemonic medium, but for the broader project of “what comes after the book?”. I’ve been mostly shoving this problem under the rug, but this consistent reaction has returned it to the spotlight.

If my thesis is “let’s augment readers using the dynamic medium,” I must either make reading on computers not-terrible, or I must bring the dynamic medium to physical reading experiences.

---

My sincere thanks to all who met with me to try this demo, in-person and online, and to those who sent me notes on their experiences.

Much of the actionable insight occupying my attention has come from generous design crit sessions, rather than from user testing. More on that in a future letter—when I have new design work to share—but I’ll offer pre-emptive thanks here to Rob Ochshorn, Gray Crawford, Niko Klein, Joe Edelman, Yiliu Shen-Burke, Shan Carter, Cameron Burgess, Marisa Lu.