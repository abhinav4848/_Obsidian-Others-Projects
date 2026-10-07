---
up:
  - "[[Ideaverse Merged/Home Pro]]"
related:
  - "[[Ideaverse Merged/Atlas/Maps/Idea Accretion]]"
  - "[[Ideaverse Merged/Atlas/Maps/Idea Development]]"
  - "[[Ideaverse Merged/Atlas/Maps/Idea Maintenance]]"
created: 2023-10-15
tags:
  - map/view
---
Never start with a blank page. Surprise yourself with the work you've invisibly done already.

> [!orbit]- #### Accreting placeholder notes with at least `3` links pointing to it
> If you get the spark, turn the placeholder note into an actual note.
> ```dataviewjs
> const count = 3;
> let d = {};
> function process(k, v) {
>   Object.keys(v).forEach(function (x) {
>     x = dv.fileLink(x);
>     if (d[x]==undefined) { d[x] = []; }
>     d[x].push(dv.fileLink(k));
>   });
> }
> 
> Object.entries(dv.app.metadataCache.unresolvedLinks)
>     .filter(([k,v])=>Object.keys(v).length)
>     .forEach(([k,v]) => process(k, v));
>     
> dv.table(["Accreting placeholder notes", "Linked from"],
>          Object.entries(d)
>          .filter(([k, v]) => v.length >= count)
>          .sort((a, b) => b[1].length - a[1].length)
>          .map(([k,v])=> [k, v.join(" • ")]))
> ```
>  
>  You can also think of these as: shadow seeds, secret slowburns, accreting placeholder notes


