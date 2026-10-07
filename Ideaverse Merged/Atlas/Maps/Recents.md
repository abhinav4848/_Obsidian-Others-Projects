---
up:
  - "[[Ideaverse Merged/Home Pro]]"
related:
  - "[[Ideaverse Merged/Atlas/Maps/Recents Visualized]]"
created: 2023-10-16
tags:
  - map/view
title: "Recents"
---
# Recents
> [!watch]+ Last modified across the ideaverse
> ``` dataview
> TABLE WITHOUT ID
>  file.link as "Note",
>  (date(today) - file.mday).day as "Days since last encounter"
> 
> FROM ""
> 
> SORT file.mtime desc
> 
> LIMIT 100
> ```

