---
in:
  - "[[Collections]]"
related:
  - "[[Statements]]"
down:
  - "[[Concepts]]"
tags:
  - "#map/view"
created: 2021-01-01
---
This note collects all notes in the folder `Things`.

> [!waves]+ ## Things
> ```dataview
> TABLE WITHOUT ID
>  file.link as "Things",
>  (date(today) - file.cday).day as "Days alive"
>  
> FROM "Atlas/Notes/Things" or "Atlas/Notes/Vaults/Ideaverse/Atlas/Notes/Things"
> 
> SORT file.ctime desc
> ```


These things act as a cabinet of curiosities, each with a story.