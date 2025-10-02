---
in:
  - "[[Entities]]"
related: 
created: 2023-11-29
---
 


> [!industry]+ Mtgs pointing to this note
> All notes in `Calendar` linking to `LYT Team`
> ```dataview
> TABLE WITHOUT ID
> file.link as Meeting,
> one-liner as One-liner
> 
> FROM "Calendar"
> 
> WHERE contains(file.name,this.file.name)
> 
> SORT file.name desc
> ```

