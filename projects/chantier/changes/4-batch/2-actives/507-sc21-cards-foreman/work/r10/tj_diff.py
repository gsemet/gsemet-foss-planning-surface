"""Read-only: how cards-next/topics.json differs from fe7fbf0f, 03f973e4 and the pr-body list."""

import json
import re
import subprocess
from pathlib import Path

TREE = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
ROOT = "skills/chantier/cards-next/"
BODY = Path(__file__).resolve().parents[2] / "pr-body.md"

now = json.loads(Path(TREE, ROOT, "topics.json").read_text(encoding="utf-8"))["topics"]
for commit in ("fe7fbf0f", "03f973e4"):
    raw = subprocess.run(["git", "-C", TREE, "show", f"{commit}:{ROOT}topics.json"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    old = json.loads(raw)["topics"]
    print(f"== against {commit}: {len(old)} -> {len(now)}")
    print("new:", ", ".join(sorted(set(now) - set(old))))
    print("gone:", ", ".join(sorted(set(old) - set(now))) or "none")
    for name in sorted(set(old) & set(now)):
        for key in sorted(set(old[name]) | set(now[name])):
            if old[name].get(key) != now[name].get(key):
                print(f"  {name}.{key}: {old[name].get(key)!r} -> {now[name].get(key)!r}")
body = BODY.read_text(encoding="utf-8")
listed = body.split("- All topic names: ", 1)[1].split("\n\n", 1)[0]
names = {n.strip(" .") for n in re.split(r",\s+", listed)}
print("== pr-body list:", len(names))
print("missing from the list:", ", ".join(sorted(set(now) - names)) or "none")
print("listed but unknown:", ", ".join(sorted(names - set(now))) or "none")
review = sorted(n for n, t in now.items() if t.get("review_by"))
marked = body.split("- Topics marked `review_by:", 1)[1].split("- All topic names", 1)[0]
words = set(re.findall(r"[a-z0-9][a-z0-9-]+", marked))
print("review_by:", len(review), "missing from the body:", ", ".join(n for n in review if n not in words) or "none")
