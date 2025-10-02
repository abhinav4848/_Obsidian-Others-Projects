---
in:
  - "[[Collections]]"
tags:
  - "#map/view"
created: 2023-11-21
---
This note collects all notes where the `in` property says `Meeting`.

> [!calendar]+ # Meetings
> ```dataview
> TABLE WITHOUT ID
> 	file.link as Note,
> 	join(list(meetingGroups)) as Group,
> 	one-liner as One-liner
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template")
> SORT file.name desc
> ```

---

> [!calendar] # Inline Meetings `meeting::`
> This works well if you work within your daily note.
> ```dataview  
> TABLE WITHOUT ID
>   file.link as Note,
>   meeting as Meeting
> 
> FROM 
>   "Calendar"  
> 
> WHERE 
>   meeting  
> 
> SORT 
>   rows.file.day desc  
> ```
> 
> 


