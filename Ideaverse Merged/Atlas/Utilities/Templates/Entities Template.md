---
in:
  - "[[Entities]]"
related: 
created: {{date}}
---
 


> [!industry]+ Mtgs pointing to this note
> All notes in `Calendar` linking to `{{title}}`
> ```dataview
> LIST
> 
> FROM "Calendar"
> 
> WHERE contains(file.name,this.file.name)
> 
> SORT file.name desc
> ```

