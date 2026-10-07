---
in:
  - "[[Ideaverse Merged/Atlas/Maps/Entities]]"
related: 
created: {{date}}
title: "Entities Template"
---
# Entities Template
> [!industry]+ Mtgs pointing to this note
> All notes in `Calendar` linking to `{{title}}`
> ```dataview
> LIST
> 
> FROM "Ideaverse Merged/Calendar"
> 
> WHERE contains(file.name,this.file.name)
> 
> SORT file.name desc
> ```

