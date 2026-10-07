from pathlib import Path
import json,re,concurrent.futures,difflib,hashlib
W=Path(__file__).resolve().parent;S=W/'andy-online';R=W.parent
source=(W/'find_andy_sources_online.py').read_text(encoding='utf-8-sig');exec(source.split('items=[]')[0])
rows=json.loads((S/'candidate-URLs.json').read_text(encoding='utf-8'))
def words(t):
 t=re.sub(r'^#{1,6}\s+.*$','',t,flags=re.M)
 t=re.sub(r'\[\[([^]]+)\]\]',lambda m:m[1].split(':::')[-1].split('|')[-1].rsplit('/',1)[-1],t)
 t=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',t)
 return norm(t).split()
def check(row):
 result=get(row['URL']);props,body=front((R/row['note']).read_text(encoding='utf-8-sig'))
 for note in result.get('notes',[]):
  if norm(note.get('title',''))!=norm(row['expected_title']):continue
  local=words(body);public=words(note.get('contentMarkdown',''));run=difflib.SequenceMatcher(None,local,public,autojunk=False).find_longest_match().size
  overlap=len(set(local)&set(public))/max(1,len(set(local)))
  if row.get('requires_content_match') and run<18 and norm(Path(row['note']).stem)!=norm(row['expected_title']):return {**row,'status':'needs_review','longest_matching_word_run':run,'body_word_overlap':round(overlap,3)}
  return {**row,'status':'verified','URL':'https://notes.andymatuschak.org/'+note['slug'],'online_title':note['title'],'longest_matching_word_run':run,'body_word_overlap':round(overlap,3),'cache':str((C/(hashlib.sha256(row['URL'].encode()).hexdigest()+'.json')).relative_to(W))}
 return {**row,'status':'needs_review','fetch_error':result.get('error'),'received_titles':[n.get('title') for n in result.get('notes',[])]}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:out=list(pool.map(check,rows))
(S/'verified-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verified',sum(r['status']=='verified' for r in out),'of',len(out))
print(json.dumps([r for r in out if r['status']!='verified'],ensure_ascii=False,indent=2))
print([(Path(r['note']).stem,r.get('longest_matching_word_run')) for r in out if r.get('requires_content_match')])
