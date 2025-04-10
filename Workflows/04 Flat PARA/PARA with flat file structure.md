# PARA in a flat file system

The package created by @cotemaxime [[START HERE!]] lays out how to create a PARA system using multiple folders. One of the great strengths of PARA is the ability to file anything relevant to the various sections in one place in a filesystem alongside your notes. However, almost all of my work is done in markdown files, and it is very rare that I have support files that are not viewable within Obsidian. So, I created a version of PARA that works with Virtual Folders, which are just notes containing links to other notes. These are notes inside my root Vault directory, though they could just as easily be moved to a subdirectory if you wanted more separation there. 

I have a file named `000 PARA INDEX`. The numbering is so alphabetical sort brings it near the top of my list, so I can easily access it in the file explorer. It looks like this: 

```
tags: #methodology #para #flatpara
links: [[001 PROJECTS|P]][[002 AREAS|A]][[003 RESOURCES|R]][[004 ARCHIVE|A]]

--- 


![[001 PROJECTS]]
![[002 AREAS]]
![[003 RESOURCES]]
![[004 ARCHIVE]]

```

Note that each of the main files are embedded (using the `![[link]]` syntax), so when viewed in preview mode, the top contents of each of them are displayed as a single file. This gives me a very nice overview. 

The links at the top of the note are a trick I took from [[IMF About|The IMF Method]], for quick access. They are actually pretty redundant, but using the piped link notation (`[[link|name]]`), in preview they just show up as `PARA`, which is pretty cool I think. 

The `001 PROJECTS` note looks like this:

```
tags: #methodology #para #flatpara
links: [[001 PROJECTS|P]][[002 AREAS|A]][[003 RESOURCES|R]][[004 ARCHIVE|A]] - [[000 PARA Index]]

--- 

# projects
> - Projects  => Every current projects (see def. below) that are actionable with their notes, files, artifacts

[[100 Projects MOC]]

[[060 Writings MOC]]

![[100 -- PROJECT codename1]]
![[100 --PROJECT codename2]]
![[100 -- PROJECT codename3]]
![[100 -- PROJECT codename4]]
![[100 --PROJECT codename 5]]

```

Note again the embedding. When I view this in preview mode, I get to see the top of each project file, in which I keep a checklist of the next few actions that need to be done on that project. This gives me an overview of what's going on, overall, a sort of high-level idea of what my next steps are when I'm figuring out what's next. 

The other sections work much the same. The `100`prefix on the filenames is another thing I picked up from IMF. It means if I can't remember the exact name of the project file, if I just type `100` into the Quick Switcher I get a list of all active projects. The rest flows from the standard PARA methodology. 

One of the cool things about Obsidian is that because of the way things link together, this is mostly a lens for filtering things according to whatever I need to be focused on. After the second level pages, the links are all to the notes that I created using IMF methods. So, if I want to look at my notes from a perspective of research, classification, and concepts, I start with my IMF Index page. When I want to look at them from the perspective of what needs to be done next, I start at my PARA Index. This flexibility is what led me to coin the term [[Fluid Taxonomies]] in conversation with Nick. All taxonomies can be viewed as just different paths of getting to different subsets of the same information depending on need. 