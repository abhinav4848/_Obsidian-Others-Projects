"""Archive the three unnamed '#' import artifacts discovered in the old folders."""
from audit import *
from lyt_cleanup import remove_empty_folders
import zipfile

paths=['Atlas/Notes/People/.md','Atlas/Notes/Sources/Books/.md','Atlas/Utilities/Templates/.md']
backup=WORK/'backups'/'lyt-before-2026-10-07.zip'
data={rel:(LYT/rel).read_bytes() for rel in paths}
assert all(v==b'#' for v in data.values())
with zipfile.ZipFile(backup,'a',zipfile.ZIP_DEFLATED) as z:
    for rel,content in data.items():
        key=CFG['lyt_folder']+'/'+rel
        assert key not in z.namelist()
        z.writestr(key,content)
with zipfile.ZipFile(backup) as z:
    assert z.testzip() is None
    for rel,content in data.items(): assert z.read(CFG['lyt_folder']+'/'+rel)==content
for rel,content in data.items():
    p=(LYT/rel).resolve()
    assert p.is_relative_to(LYT.resolve()) and p.read_bytes()==content
    p.unlink()
remove_empty_folders()
record={'archived_paths':paths,'content':'# only; no note content','backup':str(backup)}
(WORK/'empty-artifacts.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('Three empty unnamed import artifacts archived; obsolete folders removed.')
