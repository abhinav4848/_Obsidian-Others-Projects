from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,parse_qsl,unquote
import re,json,yaml,hashlib,zipfile,os,sys
W=Path(__file__).resolve().parent;R=W.parent;S=W/'andy-online'
SOURCES=json.loads((S/'verified-sources.json').read_text(encoding='utf-8'))
EXCLUDED={'.git','.obsidian','.trash','__pycache__','_Codex'}
def parts(data):
 raw=data.decode('utf-8-sig');nl='\r\n' if '\r\n' in raw else '\n';raw=raw.replace('\r\n','\n');m=re.match(r'\A---[ \t]*\n(.*?)\n---[ \t]*\n',raw,re.S)
 return (m[1],raw[m.end():],nl) if m else (None,raw,nl)
def blocks(fm):
 starts=list(re.finditer(r'^(?:[A-Za-z_][\w -]*|"[^"\n]+"|\x27[^\x27\n]+\x27):',fm,re.M))
 return [(m[0][:-1].strip('"\x27'),m.start(),starts[i+1].start() if i+1<len(starts) else len(fm)) for i,m in enumerate(starts)]
def listblock(values):return 'URL:\n'+''.join('  - '+json.dumps(u,ensure_ascii=False)+'\n' for u in values) if values else 'URL: []\n'
def replace(fm,values):
 found=[b for b in blocks(fm) if b[0]=='URL']
 if found:
  assert len(found)==1
  _,a,b=found[0];return fm[:a]+listblock(values)+fm[b:]
 return fm.rstrip('\n')+'\n'+listblock(values)
originals={};updates={};expected={};records=[]
for p in sorted(R.rglob('*.md')):
 if any(x in EXCLUDED for x in p.relative_to(R).parts[:-1]):continue
 data=p.read_bytes();fm,body,nl=parts(data)
 if fm is None:continue
 isandy=p.is_relative_to(R/'Andy Matuschak')
 if not isandy and not re.search(r'^URL:',fm,re.M):continue
 props=yaml.safe_load(fm) or {};rel=p.relative_to(R).as_posix();value=props.get('URL');old=value if isinstance(value,list) else [value] if value else [];values=list(old)
 if rel in SOURCES:
  assert not old,'Online recovery planned for a note that now has source URLs: '+rel
  values=[SOURCES[rel]['URL']]
 assert all(isinstance(u,str) and urlsplit(u).scheme in {'http','https'} and urlsplit(u).hostname for u in values),(rel,values)
 out=('---\n'+replace(fm,values).rstrip('\n')+'\n---\n'+body).replace('\n',nl).encode('utf-8')
 if data.startswith(b'\xef\xbb\xbf'):out=b'\xef\xbb\xbf'+out
 fm2,body2,_=parts(out);afterprops=yaml.safe_load(fm2)
 assert body2==body,rel
 assert afterprops['URL']==values,rel
 assert {k:v for k,v in afterprops.items() if k!='URL'}=={k:v for k,v in props.items() if k!='URL'},rel
 originals[p]=data;expected[p]=values
 if out!=data:updates[p]=out
 records.append({'note':rel,'original_URL':old,'URL':values,'source_recovered':rel in SOURCES,'original_value_type':type(value).__name__})
typepath=R/'.obsidian/types.json';typebefore=typepath.read_bytes() if typepath.exists() else None
native=json.loads(typebefore.decode('utf-8-sig')) if typebefore else {'types':{}}
native.setdefault('types',{})['URL']='multitext';typeafter=(json.dumps(native,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
stats={'missing_sources_recovered':sum(x['source_recovered'] for x in records),'URL_properties_as_lists':len(records),'notes_updated':len(updates),'andy_notes_with_source_URL':sum(bool(x['URL']) and x['note'].startswith('Andy Matuschak/') for x in records),'empty_source_lists':[x['note'] for x in records if not x['URL']],'other_collections_URL_properties':sum(not x['note'].startswith('Andy Matuschak/') for x in records),'property_type':'List'}
plan={'stats':stats,'records':records,'verified_sources':SOURCES,'native_property_types_file':typepath.relative_to(R).as_posix(),'native_property_types_previously_existed':typebefore is not None}
(S/'list-property-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2),flush=True)
if '--apply' not in sys.argv:sys.exit()
assert not (S/'list-property-applied.json').exists(),'Already applied'
backup=W/'backups'/('andy-online-sources-and-URL-lists-before-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.zip')
with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED) as z:
 for p in updates:z.writestr(p.relative_to(R).as_posix(),originals[p])
 if typebefore is not None:z.writestr(typepath.relative_to(R).as_posix(),typebefore)
 z.writestr('_Codex/restore-metadata.json',json.dumps({'types_file_existed':typebefore is not None,'created_types_file':None if typebefore is not None else typepath.relative_to(R).as_posix()},indent=2))
with zipfile.ZipFile(backup) as z:assert z.testzip() is None
for p,out in updates.items():
 assert p.read_bytes()==originals[p],'Concurrent note change: '+str(p)
 temp=S/'note.tmp';temp.write_bytes(out);os.replace(temp,p)
assert (typepath.read_bytes() if typepath.exists() else None)==typebefore,'Concurrent property type change'
temp=S/'types.tmp';temp.write_bytes(typeafter);os.replace(temp,typepath)
for p,values in expected.items():
 data=p.read_bytes();fm,body,_=parts(data);pr=yaml.safe_load(fm);assert isinstance(pr['URL'],list) and pr['URL']==values,p
 assert body==parts(originals[p])[1],p
 if p in updates:assert data==updates[p],p
 for u in values:
  parsed=urlsplit(u)
  if parsed.hostname=='notes.andymatuschak.org':assert 1+sum(k=='stackedNotes' for k,v in parse_qsl(parsed.query))<=3,(p,u)
assert json.loads(typepath.read_text(encoding='utf-8'))['types']['URL']=='multitext'
plan['backup']=backup.relative_to(R).as_posix();plan['hashes']={p.relative_to(R).as_posix():{'before':hashlib.sha256(originals[p]).hexdigest(),'after':hashlib.sha256(out).hexdigest()} for p,out in updates.items()};plan['verification']={'all_URL_values_parse_as_lists':True,'existing_URL_values_preserved':True,'note_bodies_unchanged':True,'native_property_type_is_List':True,'navigation_stacks_at_most_three_notes':True}
(S/'list-property-applied.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
config=json.loads((W/'config.json').read_text(encoding='utf-8'));config['andy_url_property_type']='list';config['url_property_yaml_format']='block sequence';config['obsidian_property_types']={'URL':'multitext'};config['url_list_conversion_scope']='All existing URL properties in working vault; all Andy notes receive URL lists';(W/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(W/'property-types.json').write_text(json.dumps({'types':{'URL':'multitext'}},indent=2)+'\n',encoding='utf-8')
report=W/'Andy sources to identify.md';data=report.read_bytes();fm,_,nl=parts(data);text='---\n'+fm+'\n---\n# Andy sources to identify\nAll 82 copied notes previously lacking source URLs now have sources verified online.\n\n## Local index\n`Andy Matuschak/ReadMe.md` is a user-authored collection index, not a copied article. It has `URL: []`. No source address was invented for it.\n\n## Evidence\nSee `Andy online sources.md` and `andy-online/verified-sources.json` for page addresses and verification evidence.\n';temp=S/'report.tmp';temp.write_bytes(text.replace('\n',nl).encode('utf-8'));os.replace(temp,report)
report=['---','title: "Andy online sources"','---','# Andy online sources','Recovered 82 missing source addresses by checking live page titles and, for renamed notes or excerpts, matching the captured text.','', '## URL lists','All 455 Andy notes and the seven other notes with an existing `URL` property now store the values as YAML lists. Existing addresses were preserved. Obsidian’s native property registry sets `URL` to List (`multitext`). The task configuration remains in `_Codex`; `.obsidian/types.json` is the native copy Obsidian requires.','', '## Local index','`Andy Matuschak/ReadMe.md` is your own collection index and has an empty source list.','', '## Excerpts and other sources','- `Writing notes helps develop exceptional ideas` contains a quotation also found in Andy’s [Knowledge work should accrete](https://notes.andymatuschak.org/zTn3g4wTm1hbkNFUvLLjpev). That verified page is the recovered source.','- `Messy thought, neat thought` was captured from [May-Li Khoe’s original Khan Academy post](https://klr.tumblr.com/post/154784481858/messy-thought-neat-thought).','- `Cloze Deletion` matches the original [SuperMemo definition](https://supermemo.guru/wiki/Cloze_deletion).','- Empty captured stubs were matched by their exact public titles. Their bodies were not filled in.','', '## Recovered addresses']
report+=['- [['+n[:-3]+']]: [Source]('+v['URL']+')' for n,v in sorted(SOURCES.items())]
report+=['','## Recovery and checks','Original changed notes: `'+plan['backup']+'`. The backup also records whether the native property registry existed before this change.','Detailed page evidence: `andy-online/verified-sources.json` and `andy-online/pages`. Full changes and verification: `andy-online/list-property-applied.json`.','All note bodies and unrelated properties were preserved; every resulting URL property was parsed and checked as a list.']
(W/'Andy online sources.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
readme=W/'README.md';text=readme.read_text(encoding='utf-8');text+='\n## URL lists and online sources\nAll copied Andy notes have source URLs. All existing `URL` values across the working vault are YAML lists; Andy’s local ReadMe index uses an empty list. `property-types.json` records the authorized List type, with the required native copy in `.obsidian/types.json`. Online evidence and change records live in `andy-online`. Keep existing navigation trails to at most three notes. Preserve captured names after renames.\n';temp=S/'readme.tmp';temp.write_text(text,encoding='utf-8');os.replace(temp,readme)
print('Applied and verified URL lists and recovered sources.',flush=True)
