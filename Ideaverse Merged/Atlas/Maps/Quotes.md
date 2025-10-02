---
up:
  - "[[Statements]]"
in:
  - "[[Collections]]"
tags:
  - "#map/view"
created: 2023-11-24
---
This note collects all notes where their `in` property has `Quotes`.

> [!Keaton]+ # Quotes
> ```dataview
> TABLE WITHOUT ID
> 	file.link as Quote,
> 	join(list(by)) as By,
> 	rank as Rank
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template")
> SORT rank desc, by asc
> ```
