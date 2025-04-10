# Transclusion is limited by the data model’s composability

Type of Link: 📝 Article
Category talked about: Learning
Author: Andy Matuschak
Completion Status: Finished
Last edited time: January 18, 2024 7:55 PM

# **Transclusion is limited by the data model’s composability**

On Wikipedia, you can include one article’s subsection into another. In Xanadu, you can include arbitrary text blocks into another document. In Roam, you can include subtrees in other subtrees. The expressive capacity of [Transclusion](Transclusion.md) is hugely dependent on how composable the transcludable objects are.

In all the examples above, the objects in question are not particularly composable! Arbitrary prose paragraphs aren’t effectively usable in multiple places: good prose depends on arc, narrative, context. Text transclusion is almost always disjointed. I fear that most of the system designers who have been excited about this approach are in love with an idea about technology, rather than an idea about writing or communication.

Figma “components” are an interesting example of where something like transclusion seems to work much better. Visual elements can often be repurposed in multiple related contexts, particularly when they’re partially parametrizable.

---

Q. What’s an example of a transclusion operation that seems to work well?

A. Figma design components

Q. Why does textual transclusion often produce disjointed writing?

A. Arbitrary sentences, paragraphs, and text ranges are not generally written to work in any context or sequence. They’re not reusable blocks; they’re highly dependent on the preceding prose.

# Reference

1. [Andy Link](https://notes.andymatuschak.org/zTpJdbe6ub7uhBFLuHkFsrT?stackedNotes=zWbMsEFW9LD4vsoVhaDcF4u&stackedNotes=zVLVGffrkZiYmahXqFPQtP4&stackedNotes=zBLUefAuJvhXq4p4HhXJqyK)