---
in:
  - "[[Collections]]"
tags:
  - "#map/view"
created: 2023-11-27
---
This note collects all notes where the `in` property says `Entities`.

> [!industry]+ # Entities
> ```dataview
> TABLE WITHOUT ID
> 	file.link as Note
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template")
> SORT rank desc, year asc
> ```
