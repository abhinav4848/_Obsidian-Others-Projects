from pathlib import Path
from urllib.parse import unquote
import json,re,hashlib,sys,os
W=Path('_Codex');R=Path.cwd();plan=json.loads((W/'attachment-relocation-applied.json').read_text(encoding='utf-8'))
for a in plan['assets']:
 for d in a['destinations']:assert hashlib.sha256((R/d).read_bytes()).hexdigest()==a['sha256'],d
 if a['original'] not in a['destinations']:assert not (R/a['original']).exists(),a['original']
# Reparse actual saved references against the current attachment inventory.
source=(W/'relocate_attachments.py').read_text(encoding='utf-8-sig');env={'__file__':str((W/'relocate_attachments.py').resolve())};exec(source.split('refs={p:references')[0],env)
count=0
for p in env['notes']:
 rows=env['references'](p,p.read_text(encoding='utf-8-sig'))
 for row in rows:
  dest=row['asset'].relative_to(R);owner=p.relative_to(R).parts[0]
  assert dest.parts[0]==owner and dest.parts[1]=='Attachments',(p,dest)
  count+=1
assert count==len(plan['link_changes']),(count,len(plan['link_changes']))
assert not (R/'Attachments').exists()
report=['---','title: "Attachment locations"','---','# Attachment locations','Attachments are stored in `Attachments` directly under the collection where their notes are kept.','', '## Locations','| Collection | Files | Folder |','| --- | ---: | --- |']
for owner,total in plan['stats']['attachment_folders'].items():report.append('| '+owner+' | '+str(total)+' | `'+owner+'/Attachments` |')
report+=['','## Changes','Relocated 166 media files into 161 collection attachments, combining five identical Andy images. Updated 272 references in 111 notes. No files were shared across different collections. Eleven unreferenced files remain with their original collection.','', '## Verification','Every moved file was checked against its original content hash. All 272 saved media references were reparsed and resolved to the correct collection’s attachment folder. The root `Attachments` folder and old empty media folders were removed.','', '## Recovery','Original media files, changed notes and task settings: `'+plan['backup']+'`. Detailed mappings: `attachment-relocation-applied.json`. Historical media recovery records retain the locations at the time of their original recovery; the relocation map records current paths.']
(W/'Attachment locations.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
p=W/'README.md';s=p.read_text(encoding='utf-8');s+='\n## Current attachment locations\nAttachments now live directly under each top-level collection: `Snipd/Attachments`, `Andy Matuschak/Attachments`, `Ideaverse Merged/Attachments`, `LizardsFromOuterSpace/Attachments`, and `Workflows/Attachments`. Links use the collection path or a correct relative Markdown path. Shared images have one file within each collection. Historical recovery maps describe their earlier locations; `attachment-relocation-applied.json` records the current mapping.\n';temp=W/'readme-attachment.tmp'
if p.read_text(encoding='utf-8').count('## Current attachment locations')==0:
 temp.write_text(s,encoding='utf-8');os.replace(temp,p)
sys.path.insert(0,str(W));from heading_spacing import trim
bad=[]
for p in R.rglob('*.md'):
 if any(x in {'.git','.obsidian','.trash','__pycache__'} for x in p.relative_to(R).parts):continue
 if trim(p.read_bytes())[1]:bad.append(str(p))
assert not bad,bad
verification={'original_file_hashes_verified':len(plan['assets']),'media_references_resolved':count,'root_attachment_folder_removed':True,'heading_spacing_issues':len(bad)}
(W/'attachment-relocation-verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8');print(json.dumps(verification,indent=2))
