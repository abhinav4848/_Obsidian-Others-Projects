---
URL:
  - "https://notes.andymatuschak.org/z93QR51f6HAUPLVDxE6KT1T"
  - "https://www.patreon.com/posts/exponentials-and-63206775"
title: "2022-02-28 Patreon letter - Exponentials and forgetting in Quantum Country"
---
# 2022-02-28 Patreon letter - Exponentials and forgetting in Quantum Country
_Private copy; not to be shared publicly; part of [[Andy Matuschak/Patron letters on memory system experiments|Patron letters on memory system experiments]]_

Now equipped with several years of data and the results of several controlled experiments, I’ve spent the last few months making sense of what’s happening on Quantum Country. I’d like to discuss some of what I’ve found along the way, and some of what still confuses me.

> Please note: this is an informal discussion of data from Quantum Country. The analysis is preliminary and shouldn’t be cited or excerpted in other work. I’m [working with the garage door up](https://notes.andymatuschak.org/Work_with_the_garage_door_up) here. There’s no audio recording for this one because it’s quite dependent on data visualization.

## An update on the exponential
The most important and surprising claim of spaced repetition memory systems is that they can offer exponential returns (in memory stability) on your time. Take a moment to consider just how unusual this is! If you read or jog for a few hours a week, and you suddenly double that to four hours a week, you’re likely to get less than double the benefit. Most activities have diminishing returns at everyday scales. But at least in many cases, it seems an extra few minutes of spaced repetition practice can double how long you’ll reliably remember the material.

In 2019, Michael Nielsen and I [published](https://numinous.productions/ttft/#early-impact) some preliminary results displaying this exponential in Quantum Country, but we have a stronger picture now, with two years of additional data and experiments. I’ll focus on the first essay here, since we have the most data for that.

Here’s a birds-eye view of the cost-benefit trade, aggregating much of the detail (clipping a handful of outliers which would uncomfortably shrink the figure).

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 1.png]]  
Very informally, after half an hour of practice most readers can remember the answers to almost all of the essay’s 112 questions across intervals of at least 2 weeks; after an hour, at least 5 weeks; after 1.5 hours, at least 9 weeks. Notice the exponential growth in retention vs. practice time.

To unpack the graph a tad, each point represents a snapshot of a reader after a particular repetition. On the vertical axis is an aggregate measure of their memory stability: the interval over which they’ve successfully recalled 90%+ of questions. On the horizontal axis is the amount of time they practiced to completed that repetition. The “bold” points in the foreground represent the medians of each repetition; the dashed line is an exponential fit.

Of course, as you can see, there’s a great deal of dispersion in the data. Much of that is an artifact of details of the scheduler, which I’ll not discuss now. But I don’t think this changes the overall story. Here I’ve highlighted the 25th and 75th %ile results. For the top quartile, three months of retention can be had for an hour of practice. The 25th %ile grows more slowly but still makes steady progress, reaching a month of demonstrated retention after an hour and a half, still under 50% beyond the initial reading time.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 2.png]]

It’s interesting also to note the negative correlation between practice time and retention within each repetition. “Slower” readers tend to have more trouble remembering. That’s one of many signals we could use in future attempts to optimize the scheduler.

**Problems with demonstrated retention as a metric**  
The biggest problem with this representation is that what we’re really seeing here is an approximate _lower bound_ of a reader’s true retention for a question. What we’d really like to know is the maximum interval a reader could wait and still have (say) a 90% chance of remembering. I’ll call that the “stable retention interval.” But we can’t measure that directly. Instead, the way we measure their retention after five repetitions is that we look at the _sixth_ repetition’s time and result. And that measurement is entangled with our schedule.

In many cases, if the sixth repetition were scheduled later, the reader would still remember, which in turn would produce a larger demonstrated retention value. On the other hand, if a reader fails to remember after 40 days, they might have succeeded after 30… but we didn’t ask then, and so we can only report the last successful interval we attempted (say, 20 days). In this case, too, we under-report.

Because of this sampling limitation, the decisive exponential curves we see in the plot above are mostly a result of our scheduler, which is itself exponential (doubling and halving intervals according to success and failure). The stable retention intervals after five repetitions are likely much higher; if we could measure them, we’d see an even more dramatic curve. But as we’ll see later in this post, the true intervals for the first few repetitions are certainly much higher in most cases; if we could measure them directly, the exponential curve would likely flatten.

The plots I’ve shown so far aggregate across all the questions in the essay by defining a reader’s demonstrated retention as the interval that 90%+ of questions have reached. But there’s a lot of interesting detail to be seen at the next level down the ladder of abstraction.

**Slicing by reader**  
For instance, readers near the bottom of this graph are doing better than it might appear. They can remember the vast majority of questions across long intervals—it’s just a handful of straggler questions left behind.

Here’s the 10th %ile user’s distribution of demonstrated retention by question.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 3.png]]

The vast majority of questions are being retained across four months or more. There’s just a handful they’re having trouble pushing over a month. And with one more repetition, a big chunk of those will continue to shift upwards; here’s this same user’s next repetition:

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 4.png]]

**Slicing by question**  
These “straggler questions” are pretty consistent across readers. Just 5 questions account for more than a quarter of the instances in which a reader’s demonstrated retention of a question remains under one month after five repetitions. 13 questions account for half of such instances. From there, it’s mostly scraps spread across the remaining 99 questions.

You can see that trend more clearly in this plot, which shows the demonstrated retention for every question after five repetitions. Each “column” here is a boxplot for one question, with each reader a sample.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 5.png]]

About three quarters of questions have their 25th %ile above 4 months, and most of the rest sit well above 2 months—which is excellent!—though the wider dispersion suggests a clear opportunity for better scheduling. But those bottom few questions seem like they would clearly benefit from some additional support. In that bottom group are mostly difficult rote memory questions: “what’s the matrix representation of the X/Y/Z/Hadamard gate?”, “What are three common names for the dagger operation”, “Who has made progress on using quantum computers to simulate quantum field theory?”. There’s one notably more conceptual question in this group: “What’s an example circuit where the target state input to a CNOT gate is left unchanged by the gate, but the control state changes?” And then a few on key details of Dirac notation and matrix unitarity.

This mode of analysis can point us towards the problems, but it’s not obvious what’s really going on with these troublesome questions. For that, we need to dig into the dynamics of forgetting.

## The counterfactual: forgetting without practice
For the [[Andy Matuschak/Mnemonic medium|mnemonic medium]] to truly be transformative, (at least) these four things must be true:

1. Memory: If you practice as suggested, you’ll durably remember ~everything.
2. Cost: It won’t take that much time.
3. Counterfactual: If you _don’t_ practice, you’ll forget.
4. Transfer: And this durable recall transfers into real understanding and ability outside of artificial practice sessions.

The previous section sketched the state of the first two points. I’ll confess right now that I can’t yet say much about transfer[^1]. But I’ve learned a lot about the counterfactual third point in these past few months.

Most of the data you’ll see in this section comes from an experiment I ran in 2021 which randomly assigns new readers different schedules. For instance, the initial review intervals vary between one week, two weeks, one month, and two months. This variation should let us see what happens if you don’t review.

But as [[Andy Matuschak/2021-11-30 Patreon letter - Quantum Country’s suspiciously flat forgetting curves|I’ve previously discussed]], the picture’s not so clear. Here are the recall rates, averaged across all questions and readers:

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 6.png]]

Really? A 13pp difference between 1 week and 2 months? It’s hard to believe! I discussed a number of interpretations and subanalyses in my previous article, but after another hundred hours on this question, I think the high-order bit is: many questions are easy; many readers are highly proficient; and so you need to look more closely to see dramatic forgetting curves.

My summary impression now from these data: without practice, you’ll likely forget answers to the “harder” questions; if you struggled with the material, you’ll forget many of the rest too. But you’ll probably remember answers to “easy” questions for a month or two without much support.

**Make-up sessions**  
One of the more dramatic forgetting curves can be seen in what I call “make-up” sessions. In this newest schedule, if you forget an answer while reading the essay, we’ll prompt you to review it again one day later—a “make-up” session for extra reinforcement. If you recall the answer at that session, then we’ll schedule you for the first longer interval. (So samples used in the forgetting curve above are for the first repetition _after_ these make-up sessions—i.e. after the reader’s demonstrated they can remember for one day.)

But people don’t always do the review right when it’s assigned. Emails can sit around for a few days. So we can see how much forgetting happens by examining recall rates at the actual time of review.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 7.png]]  
The red line is the forgetting curve for the readers we’ve been discussing, who were assigned a “make-up” session after 1 day. The blue line tracks a different pool of users using an older schedule, which initially assigned forgotten questions after 5 days. So recall drops from ~85% to ~55% over three weeks.

The blue line also addresses a concern I had about doing this type of analysis: selection bias. Aren’t “late” students less conscientious, less serious, less likely to remember? The close overlap between the red and blue lines suggests that this effect isn’t very substantial after all: tardy readers perform about the same as dutiful readers; the interval dominates.

These initially-forgotten questions also have much steeper curves in the next session, the first one scheduled across a longer interval which varies between the experimental groups.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 8.png]]

Most readers forget about a dozen questions while reading the essay. For these questions at least, the counter-factual seems clear: without multiple rounds of practice, you’re quite likely to forget in the subsequent weeks.

There’s an interesting compounding effect here, too, which makes it harder to recover from forgetting. If you forget an answer at this first delayed repetition, you’ll get a “make-up” session one day later, just as would happen if you forgot in-essay. Readers perform worse in these make-up sessions when they forget after longer intervals. When the initial interval is 2 months, readers will forget in both the delayed repetition _and_ the following make-up session 16% of the time, compared to just 2% of the time for readers in the 1-week condition.

**Slicing by question**  
“Difficult” questions have steeper forgetting curves, too. Here, by “difficult”, I mean “had a low in-essay recall rate”. This turns out to correlate moderately well (r=0.65) with recall rate in the first repetition—actually, better than difficulty parameters fit through an [item response](https://en.wikipedia.org/wiki/Item_response_theory)theory-  
based model.

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 9.png]]

Here’s the forgetting curve for the first repetition, sliced by question quartile. The top line represents the “easiest” questions and the bottom line the “hardest” ones (i.e. highest and lowest in-essay recall rates).

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 10.png]]

So without practice, you’re pretty likely to forget “hard” questions after two months, and you’ll drop to C-level performance on the middle quartiles. The easiest questions might be fine!

You can see the shape of the penalty somewhat more clearly in this figure, which shows the recall rates for every question (ranked low to high) for each initial interval. Vertical grid lines indicate question deciles.  
![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 11.png]]  
The gap is quite narrow for the easiest ~third of questions, then widens until the bottom decile or so before converging again. (You can see also that we have fewer samples for the two months interval—another interesting result, but I’ll skip that discussion for now.)

A natural next angle would be to slice by reader quartile, but we don’t have enough samples for that. But we can get a pretty good sense for this effect by noticing that a) struggling readers will forget more questions in-essay; and b) questions forgotten in-essay have steep forgetting curves, as we discussed in the previous section.

**The value of practice**  
In this experiment, readers who begin with a 1-week interval follow that with a 3-week interval. This lets us evaluate the following rough situation: say that you’re going to need some knowledge one month from now. If you review that material one week from now, then wait three weeks (for a total of about a month), how will your performance compare to someone who didn’t review at all over that period?

![[Andy Matuschak/Attachments/Andy- Exponentials and forgetting in Quantum Country 12.webp]]

Unfortunately, I didn’t set this up to be able to make a _totally_ fair comparison: if a reader forgets a question at the 7 day mark, they’ll try again at 7 days before attempting the 21 day interval. So some of these questions got a little extra practice. And there’s also probably a meaningful selection effect in the pool of readers who stuck around for the second repetition here. I’ve tried to control for that in the other comparisons I’ve shared in this post, but I don’t have enough data to do that here.

But still, the take-home message is clear: more practice probably makes a much bigger difference than scheduling differences. To a first approximation, and with some notable exceptions we’ve discussed, the schedule appears not to matter _that_ much. Repetition is what matters.

But we have to think of repetition in terms of cost and benefit. For instance, if you look at the “easiest” quartile of questions in the graph above, the extra round of practice doesn’t seem to matter much: it’s a bump from 95% to 100%! The cost may be greater than the benefit. Arguably this is true for the next quartile, too. Of course, we wouldn’t want to take this too far. Recall rates don’t tell the whole story. The extra repetition probably reinforces understanding in small ways we’re not seeing here. More subtly, it reinforces the emotional connection to the material. I think the decay of that connection is part of why fewer of the readers in the 2-month initial review condition stick around.

Ideally, we’d like to be able to compare schedule A and schedule B, to plot an efficient frontier. If I’m interested in putting in X minutes, what’s the best performance I can get? Or if I’m interested in a particular stable retention interval, what’s the lowest-cost schedule to get there?

There are many papers on this subject, of course, but all involve constructing predictive models for forgetting curves, and I’ve been idiosyncratically trying to avoid that, to focus on eye-visible patterns in the data. But I’ve not succeeded. If I want to push this cost/benefit topic further, I expect I’ll need to build some models.

**Forgetting without in-essay prompts**  
So far, we’ve discussed the counterfactual of what would happen if you read Quantum Country as it exists today and then didn’t practice for some period of time. But it’s also worth asking: what would happen if you just read Quantum Country’s text—without any of the embedded prompts, and also without practice?

We ran an experiment in 2020 which we can (scrappily) combine with the experimental data above to estimate this. In the 2020 experiment, we hid one set of 9 questions from some readers’ essays, then surreptitiously re-inserted those questions into a review session one month later.

Happily, these experimental cards span all four quartiles of “question difficulty”, as we discussed earlier. I’m running out of steam for making plots, so I’ll just compare the “easiest” and “hardest” of these questions to illustrate the range of results. Those questions, respectively, are “|psi> is an example of a…?” and “How can you write the _jk_th component of the matrix M, in terms of the Dirac notation and the unit vectors |e_j>?”.

- “Hard” questions need support to be reliably recalled at a month:
    - Without in-essay prompts or practice, one month later: 42%
    - In-essay practice and make-up sessions, then one month later: 71%
    - In-essay practice and make-up sessions, practice at 1 week (possibly with make-up sessions), then 3 weeks later: 90%
- “Easy” questions need less support:
    - Without in-essay prompts or practice, one month later: 89%
    - In-essay practice and make-up sessions, then one month later: 91%
    - In-essay practice and make-up sessions, practice at 1 week (possibly with make-up sessions), then 3 weeks later: 100%

But the situation also varies by reader.

- For readers whose in-essay recall rates were in the bottom quartile:
    - The “hard” question figures are: 23%; 62%; 75%
    - The “easy” question figures are: 79%; 93%; 100%
- For readers whose in-essay recall rates were in the top quartile:
    - The “hard” question figures are: 56%; 67%; 100%
    - The “easy” question figures are: 97%; 87% (?); 100%

This data makes the counterfactual claims somewhat starker. Without support of any kind, difficult details are very likely to be forgotten. And for readers who struggled with the material, even “easy” questions need at least in-essay prompts to maintain reliable recall.

---

Thanks to Gary Bernhardt, Michael Nielsen, and Giacomo Randozzo for helpful discussions on these topics.

## Footnotes
[^1]: Of course there are many prior experiments on this question, mostly in a laboratory setting; see e.g. [Butler (2010)](http://andymatuschak.org/files/Butler%20-%202010%20-%20Repeated%20Testing%20Produces%20Superior%20Transfer%20of%20Learning%20Relative%20to%20Repeated.pdf) (PDF: [[Andy Matuschak/Attachments/Butler - 2010 - Repeated Testing Produces Superior Transfer of Learning Relative to Repeated Studying.pdf]]) for a review.