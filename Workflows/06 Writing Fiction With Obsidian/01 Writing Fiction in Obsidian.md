# Writing Fiction with Obsidian 

Obsidian can be used to write long or short form fiction. Its powerful capabilities give it the ability to compete in many ways with more complex tools such as Scrivener or Ulysses, with the added advantage that your work is always in plain markdown files, and thus never trapped inside proprietary software. I (@mediapathic) am currently experimenting with doing so and it's working great so far. 

If you're writing short fiction and submitting it places, you may also be interested in [[03 Tracking Submissions in Obsidian]]

Here are some notes on my process:

- The first and most obvious advantage is that it is easy to link together notes to form a "Story Bible". I have a series of notes tagged with the name of my novel, and I can easily look things up or add to them while I am writing. They are, of course, wildly interlinked. I have a folder in my Vault which contains the text of my novel, and my notes are kept in my main vault. This allows me to keep separation between notes and text in the filesystem, but be able to link between them at will as I develop ideas. 

- My basic method is this: I write each scene in a single markdown file. I build a Table of Contents note, a list of these scene files, each as a link. Then, I open each scene in a new pane and edit or write it. I can then move links around in the file at will, to rearrange scenes, split them into chapters or acts, or anything else. When the time comes for publishing, I will convert this file into a format that can be used for markdown transclusion, and output it. 

![[Screen Shot 2020-05-17 at 02.58.59.png]]

- Here is an example Table of Contents Page for what is clearly going to be the next great classic of western literature: [[WFIO-TOC]]. Note that only the first link in there goes to an example note. Clicking on the others will create them in your Vault, which you are welcome to do if you wish to finish this masterpiece for me. 

- That Table of Contents file can also be used as an outline. Mine has some occasional brief notes below some scenes so I can remember things like "X has to come before Y." Nothing long form, just structural stuff that is relevant to the overall shape of the story, because I'm going to have to edit it out before exporting. If you're just starting out on a project, you can write your outline as a series of scene titles, one per line, and then make them into links when you are ready to write each one. 

- I had my files numbered when I imported them in Obsidian due to methodologies I was using with an older system. I don't think it's strictly necessary, but I'm finding it useful for keeping a rough idea where scenes will go that I've written but happen somewhere in the unknown future. Also, this ensures that they sort in the correct order in the file system, and Obsidian's link auto-updating means that you can change the filenames to rearrange them, and links will not break. 

- If you already have a work in progress split into multiple markdown files, it is relatively simple to convert a file listing into a TOC file, per the method in [[Scripts for Building TOC files]] (If you are on Mac or Linux. There are definitely ways of doing this on Windows, but I don't know them. If you are sufficiently conversant in Powershell, you might be able to figure it out from the logic I use there). Be aware that the things in that file are pretty nerdy, but they should be pretty straightforward if you are comfortable with the command line. 

- Writing in markdown also gives you the ability to tag a scene file with anything you'd like. You can track characters, locations, beats, or anything else that is relevant to the piece at hand, and see them all with a click. If you keep your tags before the first blank line of the file, most markdown parsers will ignore them, so you don't even have to remove them when you export. 

- With multiple vaults, you can have a vault specifically for a project, and keep all your notes and text in one place. This also means that you can have a custom CSS theme for your writing space, if you want to keep it psychologically distinct from a work space, which is a thing that some writes find invaluable. And even without needing the psychological difference, setting up a writing-specific theme can help with things like better line spacing. Or maybe having a cool typewriter font.  
