# We lack UI patterns for non-destructive filtering and rearrangement on a 2D canvas
If you have a table of information, we have a litany of standard patterns for manipulating it non-destructively: you can filter; you can sort; you can manually reorder; you can hide individual elements; etc.

But on a 2D canvas, e.g. in [[Figma]]? We’ve got very little! Imagine that you’ve just done a sticky note brainstorm. Everyone’s put little voting stickers on their favorite. You’d like to regroup around the votes, and perhaps leave the non-voted items off to the side. But if you took the time to arrange the stickies into clusters, this is a destructive operation! How to allow “sort by” or “arrange by” or “filter by” operations on a 2D canvas? Ideally in a way which permits comparisons across multiple arrangements? ([[We lack UI patterns for linked representations for arrangements on a 2D canvas]])

Another motivating example: in my messy iteration Figma page, I might have a hundred alternate artboards for each screen. Can we imagine some workflow in which I designate the canonical artboards and rearrange them into a sequence for presentation?

Another: imagine that I import my reading list into Figma. The whole point of bringing those items onto a 2D canvas is so that I can move them around in 2D space to make sense of them. But once I’ve arranged them into clusters, or pulled a few out to put “on top”, I might also like to view my reading list in a grid sorted by recency. How to offer that without mucking up my arrangement?

One simplistic solution would be to offer “arrangement snapshots”: at any time, you can save the position of all the artboards to some named configuration. You can sort by some other attribute for a while, then later restore your earlier arrangement. This strikes me as too “manual.”

Related:
- [Physical cut and paste is a parallel act involving informal intermediate states](https://notes.andymatuschak.org/zCRXo3avHi3fNuw43BHM8ch)

## References
1. [Andy Link](https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ&stackedNotes=zX95uZHiGWNiNTDF3wETWtq&stackedNotes=zBeBbzwU8LAyi2D5jqBJpS&stackedNotes=zCRXo3avHi3fNuw43BHM8ch&stackedNotes=zSL87LuijMXkMput8dd1f61)
This observation came up during a jam session with [Taylor Rogalski](https://notes.andymatuschak.org/Taylor_Rogalski) on [2022-10-17](https://notes.andymatuschak.org/2022-10-17).