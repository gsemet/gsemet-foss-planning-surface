import sys, re
from pathlib import Path
sys.path.insert(0, "scripts")
import release_notes as r
d = Path("docs/release-notes/2026-11-13-v0.9.0"); orig = (d/"release-notes.md").read_text(encoding="utf-8")
base = orig.replace("0.9", "0.10")
def add(t, line): return t.replace("<summary><b>🛠 For contributors</b></summary>\n", "<summary><b>🛠 For contributors</b></summary>\n\n"+line+"\n", 1)
cases = [("0.10.0 no bullet", base, "0.10.0"),
 ("0.10.0 bullet listing", add(base, "- **Not exercised by an eval.** a thing."), "0.10.0"),
 ("0.10.0 None form", add(base, "- **Not exercised by an eval.** None: every change of this release came up in an eval run."), "0.10.0"),
 ("0.9.0 no bullet", orig, "0.9.0")]
for name, t, v in cases:
    try: r.validate_notes(t, d, v); print(name, "-> accepted")
    except ValueError as e: print(name, "-> refused:", e)
