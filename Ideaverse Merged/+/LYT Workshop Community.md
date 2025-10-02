---
in:
  - "[[Entities]]"
related: 
created: 2023-11-29
---
 


> [!industry]+ Mtgs pointing to this note
> All notes in `Calendar` linking to `LYT Workshop Community`
> ```dataview
> LIST
> 
> FROM "Calendar"
> 
> WHERE contains(file.name,this.file.name)
> 
> SORT file.name desc
> ```

