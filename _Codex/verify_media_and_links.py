from pathlib import Path
import json,re,hashlib,os,sys
W=Path('_Codex');R=Path.cwd();sys.path.insert(0,str(W));from heading_spacing import trim
m=json.loads((W/'media-recovery/applied.json').read_text(encoding='utf-8'));a=json.loads((W/'andy-internal-links-applied.json').read_text(encoding='utf-8'))
errors=[]
for x in m['assets']:
 if hashlib.sha256((R/x['attachment']).read_bytes()).hexdigest()!=x['sha256']:errors.append(x['attachment'])
for n in m['notes']:
 t=(R/n).read_text(encoding='utf-8-sig')
 if '_media-sync_resources/' in t:errors.append('leftover media reference '+n)
 for dest in re.findall(r'!\[[^\]]*\]\(([^)]+Attachments/[^)]+)\)',t):
  if not ((R/n).parent/dest).is_file():errors.append('missing image '+dest)
for x in a['links']:
 p=R/x['note'];dest=R/x['destination'];target=Path(x['destination']).with_suffix('').as_posix()
 if not dest.is_file() or '[['+target+'|' not in p.read_text(encoding='utf-8-sig'):errors.append('missing internal link '+str(x))
for x in a['source_additions']:
 t=(R/x['note']).read_text(encoding='utf-8-sig')
 for u in x['URLs']:
  if '- Source for this file: [Original article]('+u+')' not in t:errors.append('source missing '+x['note'])
spacing=[]
for p in R.rglob('*.md'):
 if any(x in {'.git','.obsidian','.trash','__pycache__'} for x in p.relative_to(R).parts):continue
 b=p.read_bytes();_,count=trim(b)
 if count:spacing.append((str(p.relative_to(R)),count))
assert not errors,errors
print(json.dumps({'media_verified':len(m['assets']),'internal_links_verified':len(a['links']),'source_notes_verified':len(a['source_additions']),'heading_spacing_issues':spacing},indent=2))
(W/'media-and-links-verification.json').write_text(json.dumps({'media_verified':len(m['assets']),'internal_links_verified':len(a['links']),'source_notes_verified':len(a['source_additions']),'heading_spacing_issues':spacing},indent=2),encoding='utf-8')
p=W/'README.md';s=p.read_text(encoding='utf-8');s+='\n## Later authorized changes\n- Recover media-sync images from exact saved source addresses into root `Attachments`; keep downloaded files and repaired note references verified.\n- Convert Andy article links to existing internal notes when their identity is clear. Add missing source addresses under References, explicitly labelled as sources. Preserve ambiguous links for review.\n';temp=W/'readme-write.tmp';temp.write_text(s,encoding='utf-8');os.replace(temp,p)
