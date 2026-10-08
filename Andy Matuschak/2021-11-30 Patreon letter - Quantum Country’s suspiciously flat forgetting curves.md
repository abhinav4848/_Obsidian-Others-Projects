---
URL:
  - "https://notes.andymatuschak.org/zLMSaF4f9LoF9RR8HGxpyKN"
  - "https://www.patreon.com/posts/quantum-countrys-59365357"
title: "2021-11-30 Patreon letter - Quantum Country’s suspiciously flat forgetting curves"
---
# 2021-11-30 Patreon letter - Quantum Country’s suspiciously flat forgetting curves
_Private copy; not to be shared publicly; part of [[Andy Matuschak/Patron letters on memory system experiments|Patron letters on memory system experiments]]_

Since 2019, I’ve been running a series of randomized controlled experiments on [Quantum Country](https://quantum.country/) readers. The main reason I haven’t published these is that I don’t understand what’s going on. Readers are forgetting very slowly. Too slowly! I’ve been crossing off theories with each experiment, but the data seem to defy a core assumption of memory systems: that we forget more and more over time, along a steep curve. This has left me awfully confused all year, but I now have one theory which might explain what’s going on. If I’m right, it’ll mean that general-purpose memory systems won’t be able to reuse the ==approaches== which traditional vocabulary-focused memory systems have used to evaluate and improve themselves.

> Please note: this is an informal discussion of data from Quantum Country. The analysis is preliminary and shouldn’t be cited or excerpted in other work. I’m [working with the garage door up](https://notes.andymatuschak.org/Work_with_the_garage_door_up) here.

**Quantum Country’s ecological niche**  
Quantum Country is a sort of observatory for human memory—or at least a very limited slice of it. There have of course been countless studies of human memory, but Quantum Country lets us observe an underserved niche:

- readers are adults in a self-motivated setting, rather than kids or undergrads in a formal schooling or artificial lab environment
- the material is largely conceptual, rather than facts, vocabulary, definitions, arbitrary data, etc

This niche is important because it represents the sort of meaningful learning which most adults must do in the course of their own creative work.

Of course, some professionals use tools like SuperMemo, Anki, and Mnemosyne in the course of their work, but analyses of those data have an important limitation: they have only one data point per item per repetition, because items are (generally) authored by each user. Developers must rely on [significant model assumptions](https://supermemo.guru/wiki/Three_component_model_of_memory) to make sense of this sparse data. With Quantum Country, we can (I hope!) analyze how large cohorts of readers perform on the same set of questions, and largely avoid these model assumptions. Duolingo and Quizlet can make the same move, but mostly for vocab/fact-oriented material, rather than conceptual topics. Meanwhile, datasets from academic studies are almost exclusively restricted to artificial and classroom contexts—though, it should be noted, their data is often much cleaner and better controlled!

For me, the point of all this data is to learn something about how memory systems and human memory work, so that we can design better systems, so that we can give people superpowers. I’m not studying Quantum Country data to understand how people learn Quantum Country, but to indirectly understand how people might learn with these systems in general. At a high level, we want to answer questions like:

- How efficient can these systems become? Optimally, when should a given user review a given prompt?
- What are the boundary conditions of these systems? What are they terrible at? How far can their scope be pushed?
- How do these review interactions transfer to a person’s capacity to solve problems and do things with this knowledge in other contexts?
- … and so on.

These of course shatter fractally. Two related sub-questions I’ve been trying to answer:

1. What’s the counterfactual? Without the review mechanisms, to what extent do people remember the text’s key details?
2. Is Quantum Country’s current schedule too short? Too long? For which readers and questions?

These turn out to be much more difficult to answer than I’d expected!

**Schedule experiments: the basics**  
In this post I’ll focus on the most recent experiment I’ve run, since at least for the questions I’ve described above, it’s better controlled.

Each new reader is assigned to one of four schedules, having initial intervals of one week, two weeks, one month, and two months. That is, a reader in the “two week” condition will be prompted to review a question two weeks after they initially answer it in the essay. I’m over-simplifying a bit here, but this is enough to get us started.

These conditions, taken together, should help us find a “sweet spot” for an initial review. Additionally, the two month condition should tell us something about the counterfactual: what happens if a reader doesn’t review for two whole months?

And so, here are the median reader’s accuracy rates at their first delayed review, by condition (25th and 75th %ile reader accuracies in parentheses):

- 1 week: 87% (81-92%, N=35 readers)
- 2 weeks: 87% (81-91%, N=35 readers)
- 1 month: 85% (77-92%, N=25 readers)

These data are constrained to the first essay of Quantum Country—where we have the most data—and represent readers who have collected at least 50 questions and reviewed 90%+ of those they collected. (You’ll notice I’m intentionally eschewing models and statistical tests in this article. That’s because we’re discussing effects which I expect to be large enough to be obvious at a glance!)

Only a handful of readers in the 2-month condition have fully completed their first review, so I can’t report per-reader statistics for that condition yet, but we can get some sense of what’s going by lumping all reviews in each condition into one big bucket and looking at the fraction of remembered questions in each bucket:

- 1 week: 86% (N=138 readers, 6381 reviews)
- 2 weeks: 84% (N=142 readers, 6319 reviews)
- 1 month: 83% (N=90 readers, 4477 reviews)
- 2 months: 81% (N=50 readers, 1744 reviews)

We can add one more data point by adding readers from early 2019, when the first review after just one day. This isn’t a clean comparison, both because there may be cohort effects and because these users didn’t have a “retry” feedback mechanism, but just to get a sense:

- 1 day: 89% (N=2210 readers, 122139 reviews)

This is an almost unbelievably gentle forgetting curve: from 89% to 81% across two months! This shallow slope is at the heart of my confusions, but first let’s talk about the parts which make sense.

**Initially-forgotten questions should get tighter schedules**  
The data get more predictable if we look exclusively at delayed recall accuracy of questions which readers _forgot_ when first answering the question in the essay. Such questions will first be assigned again one day later, repeatedly if necessary, until the reader remembers—after which they’ll the question will be assigned after a delay. Recall accuracies, by delay:

- 1 week: 84% (N = 79 readers, 626 reviews)
- 2 weeks: 77% (N = 73 readers, 447 reviews)
- 1 month: 69% (N = 57 readers, 341 reviews)
- 2 months: 56% (N = 27 readers, 138 reviews)

This data paints a more familiar picture, and it suggests a fairly clear course for memory system authors. It the goal is to ensure that recall rates stay above, say, 90%, then when a reader forgets a question initially, we should assign it to be reviewed again quite soon. The automatic one-day-later “retry” session is not enough to support lengthy subsequent intervals.

In fact, this effect compounds. If readers forget a question in this first delayed review, then it’s assigned to them again one day later. Readers with longer initial intervals were less likely to recover in that subsequent session—that is, they were more likely to forget yet again. Recovery rates by first review session delay (note that these sample sizes are now getting small):

- 1 week: 90% (N = 31 readers, 79 reviews)
- 2 weeks: 78% (N = 33 readers, 86 reviews)
- 1 month: 83% (N = 24 readers, 70 reviews)
- 2 months: 57% (N = 9 readers, 44 reviews)

OK, so that’s one pretty clear implication for memory system designers that we’ve extracted: the initial schedule should contract decisively when a prompt is forgotten in-essay.

**The trouble begins: when questions are initially remembered**  
But questions aren’t often forgotten in-essay. Aggregated across readers in these four conditions, in-essay accuracy rates are 91-92%. So what about the common case where questions are initially remembered? Here’s where the trouble comes in.

First review recall rates for questions remembered in-essay:

- 1 week: 86% (N=137 readers, 6174 reviews)
- 2 weeks: 85% (N=140 readers, 5814 reviews)
- 1 month: 84% (N=89 readers, 4108 reviews)
- 2 months: 83% (N=49 readers, 1599 reviews)

As in the previous section, we can irresponsibly use data from 2019 readers to add a data point at 1 day: 90% (N = 2207 readers, 109031 reviews). As before, note that this isn’t a well-controlled comparison.

That forgetting curve is unreasonably shallow! Sure, if we want to target a 90% recall rate, this data suggests we should schedule the first review after less than one week. But each review has a cost; if readers can skip an initial review or two in exchange for a few percentage points lower accuracy, I suspect most would take that trade. After all, each full repetition of the first essay’s 112 questions takes about 25 minutes. How should we think about this?

One consideration is the “recovery” effect we saw in the previous section. Do the people who forget after longer periods struggle more to recover in the following session, relative to those who forget after one week? Here are the recovery rates (i.e. accuracy rates one day after forgetting in the first delayed session, after remembering in-essay):

- 1 week: 84% (N=68 readers, 600 reviews)
- 2 weeks: 81% (N=66 readers, 529 reviews)
- 1 month: 85% (N=44 readers, 384 reviews)
- 2 months: 74% (N=16 readers, 147 reviews)

This doesn’t look very compelling. Maybe there’s trouble at 2 months, but I’d like to see more samples first. It sure looks here like we can defer the first review for a month without real penalty.

Another reason to delay initial reviews is to invoke the [spacing effect](https://en.wikipedia.org/wiki/Spacing_effect), but I’ll skip discussing that in this post. Suffice it to say that (with sparse data) I don’t yet observe a spacing effect in the interactions between first and second session intervals.

What about slicing by question? Looking at the ten questions in the first essay with the lowest initial accuracies, but where readers _remembered_ the answers to those questions while reading, we still see a sharp forgetting curve in that first delayed review:

- 1 week: 74% (N=74 readers, 273 reviews)
- 2 weeks: 71% (N=67 readers, 277 reviews)
- 1 month: 65% (N=47 readers, 210 reviews)
- 2 months: 65% (N=25 readers, 85 reviews)

This is pretty compelling, but the curve rapidly disappears. Here are the accuracies for the next ten “hardest” questions, by initial delay:

- 1 week: 73% (N=129 readers, 474 reviews)
- 2 weeks: 74% (N=114 readers, 446 reviews)
- 1 month: 74% (N=77 readers, 312 reviews)
- 2 months: 75% (N=40 readers, 151 reviews)

We don’t have enough data to extract trustworthy forgetting curves on a per-question basis, but the flat curves continue with increasing intercepts for the remaining groups of ten. The median ten are flat at 82%; the easiest ten are flat at 95%.

So questions vary in difficulty, but don’t seem to decline in recall rates as more time passes. What should we take from this? Sure, we could schedule “hard” prompts earlier, but would that actually do anything? Except for the ten hardest prompts, this data shows no improvement in recall with shorter intervals.

One way to interpret this is that the main thing here is that people just need to practice. The timing is not terribly important. Indeed, [[Andy Matuschak/2021-03-25 Patreon letter - Too easy to be effortless|we previously found]] that once the median reader remembers an answer after a delay (of any length), their recall rate over the following year of reviews is 95%!

But I find myself simply not believing this data. The forgetting curves are too flat. This just doesn’t reflect my experience. If I don’t practice something I’ve learned for two months, I’m much less likely to remember it than I would be one week later. Our data suggest that after the first successful delayed recall, we could safely delay subsequent reviews for many months. I just don’t buy it.

What’s going on here?

**My theory: cuing effects**  
I think the picture gets clearer if you look at a specific question. Consider this question (which has ~75th %ile in-essay recall accuracy):  
![[Andy Matuschak/Attachments/Andy- Quantum Country’s suspiciously flat forgetting curves 1.png]]

This task strongly shapes the retrieval you perform: it makes you look for connections between the normalization condition and measurement probabilities. You might have instant access to this answer; but you might also consider the question on the spot and infer that this is the only reasonable answer.

The accuracy rates we collect don’t distinguish between these two possibilities. But the difference matters! If we asked you instead to solve some problem which indirectly relies on this property, you might not make a leap you need to make.

What we really care about here is fluency: your readiness to think interesting thoughts, to solve interesting problems, to notice connections and apply your knowledge creatively. You want to train a richly patterned reasoning apparatus.

My hunch is that even though _cued_ recall doesn’t seem to dip substantially between 1 week and 2 months, free recall and transfer tasks would show a sharper curve. The kind of fluency I just described does decline. And if you could see that decline, you might want to schedule the next review earlier.

If this theory is right, it means Quantum Country and general-purpose memory systems need to follow a very different path than most prior work in this space. Following SuperMemo’s lead, most systems generally think about scheduling in terms of a simple threshold: schedule a review when the estimated probability of recall drops to 90%. That way, your expected recall rate at any given moment should remain at least 90%.

I think this is a reasonable heuristic for language learning, facts, and term-definition pairs. You can’t usually re-derive those answers on the spot. The goal is to produce the answer from memory. The effect of explicitly cuing the retrieval should be much smaller than we’d observe for conceptual material like Quantum Country’s.

If we can’t approximate a conceptual detail’s depth of encoding with cued recall rates, we can’t use the traditional scheduling heuristics. We need to establish some other way to drive the control loop.

Response time seems like an interesting proxy for fluency, but I’ve had surprisingly little success finding patterns in Quantum Country readers’ response times.

A more intrusive approach would be to insert questions which require readers to indirectly use knowledge in some new context. If it’s true that cuing effects are particularly significant for conceptual knowledge, we should see a decline in transfer performance over time even if recall accuracies remain steady. I’d like to do something like this anyway, to establish the flexibility of the knowledge reinforced by the review system.

Another way to test this theory is to consider questions which I expect to be more “rote” and less conceptual. These should have a more pronounced forgetting curve. For example, here are the recall rates for the questions asking for the matrix values of the X, Y, Z, and H gates:

- 1 week: 56% (N=91 readers, 234 reviews)
- 2 weeks: 60% (N=87 readers, 215 reviews)
- 1 month: 56% (N=59 readers, 144 reviews)
- 2 months: 48% (N=26 readers, 54 reviews)

Not a lot of samples here, but this data doesn’t support my theory. The flat curve between 1 week and 1 month still strikes me as highly implausible. I suppose that people could be re-deriving these values from what they remember of these gates’ desired effects, but I don’t find that especially plausible.

One simple answer here, and perhaps for this whole confusion, is that people are simply lying. Quantum Country is self-graded. Maybe people are inappropriately marking answers as remembered? I don’t find this plausible. Remember, the median reader has a self-reported accuracy of 85-87% from 1 week to 1 month. That median user is still marking plenty of questions as forgotten. What’s confusing is why the median 1-month user doesn’t mark _more_ questions as forgotten than the median 1-week user.

Another important factor distorting my data is survivorship bias. Readers who come back and review after 2 months are probably more conscientious than readers who reviewed after 1 week. They probably care more about the topic and read more closely. This effect is probably inflating the performance of the later intervals, but I don’t have a good way to establish by how much.

I think my next step here is to dig deeper into the literature, which does include numerous memory experiments focused on conceptual knowledge and transfer learning. Perhaps some of those methods or discussions can help me here.

---

Thanks to Gary Bernhardt for helpful discussions about this topic. And thank you to you all for your ongoing support, which makes it possible for me to conduct long-term studies like this. We’re about 3/4 of the way to the equivalent of an NSF CAREER grant now, and I’m continuously shocked that such a thing might be possible. Happy holidays!