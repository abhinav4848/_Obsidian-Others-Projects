---
up:
  - "[[Home Pro]]"
in:
  - "[[Collections]]"
  - "[[Collections (Nick)]]"
related:
  - "[[Templates]]"
created: 2023-01-01
tags:
  - map/view
---
These are collections across your ideaverse. 

> [!planet]+ ## Atlas Collections
> 
> > [!map] [[Maps]] 
> 
> > [!aperture] [[Things]] | [[Concepts]] | [[People]] | [[Entities]]
> 
> > [!waves] [[Statements]] | [[Questions]] | [[Ideaverse Merged/Atlas/Maps/Quotes]]
> 
> > [!armchair] [[Books]] | [[Movies]] | [[Series]]

> [!Calendar]+ ## Calendar Collections
> 
> > [!calendar] [[Meetings]]
> 

> [!Training]+ ## Efforts Collections
> 
> > [!Training] [[Efforts]] 

![[whelan-space-station-1978-narrow.jpg|700]]

> [!NOTE] **Collections** are a work in progress because they leverage "Obsidian Properties", which is still under development, with new features still expected. What you see here is very much a test...or as we like to say, a "minimum shareable draft".

# Installation instructions for special collections

## Books
- [[Books]] | [[Book Template]]
	- Current Install Instructions (Difficulty Level: 5/10)
		- Hit `cmd-p`, type `book search`, select `create new book note`.
		- Type the book you want, select it from the list, and voila!
		- Of course, make sure the plugin "Book Search" is downloaded and that it knows to look for the [[Book Template]] provided with Ideaverse Pro.
	- Personal note: This is the easiest one to develop, but I need to be conscious to preserve the Shadow Mapping work I did.

## Movies
- [[Movies]] | [[Movie Template (QuickAdd)]] | if needed [[Movie Template (Backup)]]
	- Current Instructions Instructions (Difficulty Level: 10/10)
		- Make sure your vault has the the community plugin "Quick Add".
		- In "Pro", go to `Settings/Community Plugins` and click on the 'open folder' icon. 
		- In the File Browser, find the folder called `quickadd`. Click and hit copy.
		- In Your Vault, go to `Settings/Community Plugins` and click on the 'open folder' icon. 
		- In the File Browser, find the folder called `quickadd`. Click and hit paste.
		- Now restart Obsidian. 
		- To test this, try to hit `Cmd-p` and type `add a movie`. Do you see the QuickAdd option? Good. You're 1/3 of the way there.
		- ---
		- In "Pro", find the `Atlas/Utilities/Scripts` folder. Right click and "Reveal in Finder". 
		- You will find a file called `movie.js`. This hidden js file is used by a QuickAdd macro. If you want it to work immediately without change the QuickAdd settings, put this file in your vault at exactly this folder path: `Atlas/Utilities/Scripts`. 
		- It won't show up in Obsidian; you'll need to move it in Finder on Mac or File Explorer on Windows.
		- Now restart Obsidian. 
		- ---
		- In Your Vault, go to Settings and click Quick Add in the sidebar.
		- Find `Movie Template (OuickAdd)` and click on its cog wheel.
		- Change the "Template Path" to wherever you keep your templates.
		- Make sure you added the "Pro" templates, especially "Movie Template (QuickAdd)"
		- Delete the file path `Atlas/Notes/Sources/Shows` and add your preferred file path for where you want movies to go.
	- Instructions to Use
		- Hit `Cmd-p`, type `add a movie`, hit enter, then type the movie name, select it. 
		- Voila, a new note will open with cool information auto-populated.

## Series
- [[Series]] | [[Series Template (QuickAdd)]] | if needed [[Series Template (Backup)]]
	- If you got "movies" to work, then you should be 90% of the way there. 
	- To test this, try to hit `Cmd-p` and type `add a series`. Do you see the QuickAdd option? Good. All you need to do is change where these notes get saved.
	- ---
	- In Your Vault, go to Settings and click Quick Add in the sidebar.
	- Find `Series Template (OuickAdd)` and click on its cog wheel.
	- Change the "Template Path" to wherever you keep your templates.
	- Make sure you added the "Pro" templates, especially "Series Template (QuickAdd)"
	- Delete the file path `Atlas/Notes/Sources/Shows` and add your preferred file path for where you want movies to go.

# Works in progress, maybe...
For future releases of Ideaverse Pro, I may add more collections:

- [[Outputs]] | [[Game]] | [[Paper]] | [[Song]] | [[Speech]] 

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
> FROM "Atlas/Notes/Sources" and -#x/readme 
> 
> SORT year asc
> ```

Not included here, but in my personal vault, to honor the old ones, I also keep a [[Ideaverse Merged/Atlas/Dots/Things/Commonplace Book]] based on tags.

> [!NOTE]+ This is a sanitized version of my actual note. 
> - Content and links have been removed.


