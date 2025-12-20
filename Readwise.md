# Readwise
Readwise is a service which tries to help you remain engaged with interesting ideas you’ve read. It extracts highlights from Kindle, “read later” services, physical books via photos + OCR, etc. Then it sends you a daily email with a random assortment of those highlights so that they’re periodically refreshed in your mind.

Founded by Tristan Homsi and Daniel Doyon.
## SRS-like functionality
They’ve gradually introduced some features of a [[Spaced repetition memory system]]. In the course of reading through your daily highlights, you can smoothly “upgrade” the interesting ones into cloze deletions or even custom question/answer prompts. This is a clever strategy for onboarding people new to spaced repetition: the product delivers (slight) value if you’re totally passive, but as users become invested, they can apply incremental effort over time and get more out of the product.

![](https://notes.andymatuschak.org/BearImages/31E707AF-E39B-4749-8E19-D5F70280DA6F/cloze-deletion.gif)

Note that the core feedback actions in Readwise are knobs tuning when to show the highlight again (sooner, later, eventually). You don’t mark yourself as having remembered correctly or incorrectly.

If the goal were to produce good SRS recall prompts, I’d worry that this wouldn’t work well: [[Cloze deletion prompts seem to produce less understanding than question answer pairs in spaced repetition memory systems|Cloze deletion prompts seem to produce less understanding than question/answer pairs in spaced repetition memory systems]], and people mostly won’t write good Q/A prompts because [[Writing good spaced repetition memory prompts is hard]]. This interface also encodes a 1:1 relationship between passages and prompts, which is not good for thoroughly learning material: [[Spaced repetition memory prompts should encode ideas from multiple angles]].

But the goal _isn’t_ to produce detailed memory: it’s closer to the aspiration described in [[Timeful text]], focusing on the effect I describe in [[The mnemonic medium keeps readers in contact with material over time]]. “…the point is to reprogram your brain. To prime your mind to spot patterns, form connections, and resurface the right idea at the right time.” Does this approach actually do that? Hard to know! The evidence for this isn’t clearly available like it is for memory, but that’s part of the fun. Because it’s hard to quantify this kind of outcome, this actually makes a business a better place to test the idea: if people continue paying for the service, they clearly find it valuable.

This detailed UI for managing the intervals of specific books is a thoughtful touch. I wonder how many users edit these. Rather than setting a value explicitly, I wonder if it would make more sense to tune these incrementally over time through “see less” / “see more” type interactions during reviews (which they have as well?):  
![](https://notes.andymatuschak.org/BearImages/4F509D09-20ED-4E69-8105-54FB334812A0/tuning.gif)

## Note management
Readwise also offers note organization features: you can tag and add notes on your highlights.
In general, I fear that the choice to organize everything around books falls afoul of [Do your own thinking](https://notes.andymatuschak.org/zLdprTyt7Ca2z2LUGLtFMSs) and [Collecting material feels more useful than it usually is](https://notes.andymatuschak.org/zQm6XAB3XXrXLHzF7gahpJ2). You’re reading these highlights, and you can make a note about an individual highlight, but the product makes it difficult to draw those insights together into something larger. For that, the workflow is to export your highlights to some other environment (Notion, Evernote, etc). But there’s no connection (as far as I can see) between the review workflow and that environment.

## Organization

Readwise was created by {Daniel Doyon} and {Tristan Homsi}. It’s a bootstrapped business.

Perhaps because it’s a business, it’s often misleadingly confident in its claims, contra [Pitching out corrupts within](https://notes.andymatuschak.org/z4ehFvVvhxoMGtBudLpDoeN):

> We don’t remember things by just reading them once. Readwise fixes this using a scientific process called Spaced Repetition.

> For example, if you apply Mastery to Deep Work and your weekly calendar starts to fill with shallow calls and meetings, your mind will likely notice the pattern and then start nudging you to create some uninterrupted space.  
> …  
> The sky is the limit.  
> …  
> But until Elon Musk finishes his [Neuralink](https://www.neuralink.com/) , the combination of books, Readwise, and Mastery is one of the most effective techniques we've got.

---

## References

- [Using Spaced Repetition and Active Recall with Books to Hack Your Brain](https://blog.readwise.io/hack-your-brain-with-spaced-repetition-and-active-recall/)
- [Remember Significantly More of What You Read With Readwise](https://blog.readwise.io/remember-more-of-what-you-read-with-readwise/)
# Reference
1. [Andy Link](https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ&stackedNotes=zX95uZHiGWNiNTDF3wETWtq&stackedNotes=zAt1K9ARQYguinoHH8cfaqQ)