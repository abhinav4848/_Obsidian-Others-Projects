
## Making a TOC:

These are the scripts that I use for building a Table of Contents file from my filesystem. Note: these are all commands to be run from the terminal. I may try to compile them into some sort of tool at some point, but because I work in the terminal a lot anyway this is what I do. The logic of them is pretty straightforward, and there are, I'm sure, many other ways of doing this. 

Also, I work on a mac. I am 99% sure that these will work on any \*nix system (except for the one exception noted below), but if something doesn't work on your raspi running fish shell, please let me know and we'll see if we can get it sorted. 

Let's step through the logic first: 

To output a list of markdown files in the current directory: 
```bash
ls  *.md
```

`ls` is short for "list," and `*` means "match everything." So this says, "list every file that ends in .md", in other words, all markdown files in that directory. 

To output a list of markdown files plus directories, if you have things in subdirectories you want to include: (via @scmwiz)

```bash
find . -name '*.md'
```

This says: 

> `find` me all the files starting from here `.`, including subdirectories, that are `name`d anything `*` as long as it ends in `.md` (so we know it's a markdown file).

```bash
ls **/*.md
```

This does the same thing, but it only does it if you're running `zsh`. So don't use it in a script, but if you're just doing stuff in `zsh`, it's less typing. 

Next we have `sed`. `sed` is a tool for manipulating text. `sed` is subtle and quick to anger, and it speaks a strange and twisted tongue, but it can be your friend.

```bash
sed -E -e 's/^/[[/' -e 's/$/]]/'  
```

This says: 
> hey `sed`, I need you to do a couple of things (`-E`). First thing (`-e`) is, `s`earch for the beginning of each line (`^`) and replace it with `[[`.  Then, (`-e`), `s`earch for the end of each line (`$`), and replace it with `]]`. 
 
So, to put it all together, you use the `|`, which means "pass the output from one thing to another thing," and the `>`, which means "pass the output into a file."

If you're just doing files in a single directory, it looks like 

```
ls '*.md' | sed -E -e 's/^/{{/' -e 's/$/}}/' > TOC.md  
```

And if you need to include files in subdirectories: 

```
find . -name '*.md' | sed -E -e 's/^/{{/' -e 's/$/}}/' > TOC.md  
```

This does all of the above, but then takes the results and writes `>` them to a file named `TOC.md`.

Note that this will include the TOC file that you probably made in a previous attempt and forgot to delete. Remove that entry from the new TOC file.  

The links will have the extension `.md` still in them. This won't cause a problem for Obsidian, it doesn't care. And, depending on how you're going to export the final file (there are several standards for markdown transclusion, and that is beyond the scope of this document)[^1], you're probably going to want them in there. But you can easily get rid of them with a search and replace if you need to. 

Also the files will be in alphabetical order. This usually just means copying blocks of text around until you get them in the order you want. This is simpler if you happen to have named your files something like `001 first scene`, `002 second scene`, etc. But the beauty of making a TOC file is that you can move things around however you want. 

Bonus: To find only the files that match a particular tag: 

```
grep -l "#active" *.md | sed -E -e 's/^/[[/' -e 's/$/]]/' > activeTOC.md    
```

No, you don't need the `ls` or the `find` in that, `grep` is doing those things as well as searching for the string `#active`. You can replace that with any text you'd like, and one of the great things about markdown is that tags are just text. 

[^1]: But, if you're on mac, I can recommend a piece of software that works well, and that is [Marked 2](https://marked2app.com/) by Brett Terpstra. If you take that toc file and replace the `[[` with `{{` and the `]]` with `}}`, Marked will show you your whole book, and export it to many types of files. I merely include this to show how I deal with that part of the problem, there are, as of now, several possible solutions. 

