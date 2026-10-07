---
created: {{date}} 
---






>[!calendar]+ Calendar Time Window (± 7 days)
> These are the calendar notes created in the 7 days before & after this note.
> 
> ```dataview
> LIST
> FROM "Ideaverse Merged/Calendar"
> WHERE date(this.file.ctime) - file.ctime <= dur(1 week)
> SORT file.name asc
> LIMIT 20
> ```

