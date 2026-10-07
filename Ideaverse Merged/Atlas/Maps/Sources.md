---
up:
  - "[[Ideaverse Merged/Home]]"
created: 2020-06-01
in:
  - "[[Ideaverse Merged/Atlas/Maps/Maps]]"
aliases:
- Sources Map
tags:
  - map
---
This is where I keep tabs on some of the sources I have encountered. 
What "sources" should you track? 
How about books and movies?

> [!Book]- ### Books
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  file.link as Book
>  
> FROM "Ideaverse Merged/Atlas/Dots/Sources" and -#x/readme
> 
> WHERE type = [[Ideaverse Merged/Atlas/Maps/Books]]
> 
> SORT year asc
> ```

> [!video]- ### Movies
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  file.link as Movie
>  
> FROM "Ideaverse Merged/Atlas/Dots/Sources" and -#x/readme
> 
> WHERE type = [[Ideaverse Merged/Atlas/Maps/Movies]]
> 
> SORT year asc
> ```

For the Fall 2023 Ideaverse, I am playing around with a property field called `type`. It allows me a nice way to create a few passive maps for different types of sources. Here's what I have so far, feel free to make more:

- [[Ideaverse Merged/Atlas/Maps/Books]] | [[Ideaverse Merged/Atlas/Maps/Games]] | [[Ideaverse Merged/Atlas/Maps/Movies]] | [[Ideaverse Merged/Atlas/Maps/Papers]] | [[Ideaverse Merged/Atlas/Maps/Songs]] | [[Ideaverse Merged/Atlas/Maps/Speeches]]

For more ideas, check out the tags pane. Find "source" and twirl it down. The sources I have decided to include tracking over the years include: *books, movies, songs, research papers, plays, paintings, quotes, videos, speeches, poems, tweets, articles, and newsletters*. 

> [!Script]- ## ALL SOURCES
> This is a simple data view pulling anything from the **Sources** folder.
> 
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  type as Type,
>  file.link as Source
>  
> FROM "Ideaverse Merged/Atlas/Dots/Sources" and -#x/readme 
> 
> SORT year asc
> ```

Not included here, but in my personal vault, I enjoy checking out the comprehensive [[Source MOC]] and perusing my [[Bookshelf 📚]]. And to honor the old ones, I also keep a [[Ideaverse Merged/Atlas/Dots/Things/Commonplace Book]] based on tags.

> [!NOTE]+ Notes on this note
> This is a sanitized version of my actual note. 
> - Content and links have been removed.
> - This special views 🔬 only render properly in the free downloadable version.
> - You won't be able to see the magic unless you [download the kit](https://www.linkingyourthinking.com/download-lyt-kit).







