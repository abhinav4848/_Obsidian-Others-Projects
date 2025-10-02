---
up: []
in:
  - "[[Collections]]"
tags:
  - "#map/view"
created: 2023-10-12
cssclasses:
  - wide-page
---
This note collects all notes where the `in` property says `People`. The views provided focus on prominent people so you can get plenty of ideas on how to do cultural sensemaking.

Ideaverse Pro also comes with [[People ROARs]] for managing your "Reach-Outs And Replies".

> [!contact]+ # People by date born
> ```dataview
> TABLE WITHOUT ID
> 	file.link as People,
> 	lifespan as "Lifespan",
> 	finalAge as "Final Age",
> 	join(list(peopleDomain)) as Domain
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template") and
> 	!contains(file.name, "People Classification Master Key")
> SORT lifespan asc, file.name asc
> ```

> [!contact]- # People by first name
> ```dataview
> TABLE WITHOUT ID
> 	file.link as People,
> 	lifespan as "Lifespan",
> 	finalAge as "Final Age",
> 	join(list(peopleDomain)) as Domain
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template") and
> 	!contains(file.name, "People Classification Master Key")
> SORT file.name asc
> ```

> [!contact]- # People by date born, with images
> ```dataview
> TABLE WITHOUT ID
> 	file.link as People,
> 	"![|60](" + image + ")" as Image,
> 	lifespan as "Lifespan",
> 	finalAge as "Final Age",
> 	join(list(peopleDomain)) as Domain
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template") and
> 	!contains(file.name, "People Classification Master Key")
> SORT lifespan asc, file.name asc
> ```


