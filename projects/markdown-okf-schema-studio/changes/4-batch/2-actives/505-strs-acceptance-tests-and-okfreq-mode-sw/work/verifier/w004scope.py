"""Which use cases (StRS) have no `@accepts_req` marker at the head, against the W004 list.

Usage: python -I w004scope.py <worktree> <new-mode.log>
Reads the tracked requirement files and marker lines of the worktree (at its checked-out head).
"""
import re
import subprocess
import sys
from pathlib import Path

worktree, log = sys.argv[1:3]
strs = {}
for path in sorted((Path(worktree) / "requirements" / "tiers" / "strs").rglob("StRS-*.md")):
    front = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n---\n", 1)[0]
    life = re.search(r"^req_lifecycle:\s*(\S+)", front, re.M)
    scen = re.search(r"^scenarios:\n((?:[- ].*\n?)+)", front + "\n", re.M)
    ids = re.findall(r"^- id:\s*(\S+)", scen.group(1), re.M) if scen else []
    strs[path.stem] = (life.group(1) if life else "", ids)
grep = subprocess.run(["git", "-C", worktree, "grep", "-h", "@accepts_req", "HEAD", "--", "test"],
                      capture_output=True, text=True, encoding="utf-8").stdout
marked = set(re.findall(r"(StRS-MDOKFSTUDIO-[A-Z]+-\d+)", grep))
w004 = set(re.findall(r"^W004 .*?: (StRS-MDOKFSTUDIO-[A-Z]+-\d+) has no acceptance test",
                      Path(log).read_text(encoding="utf-8", errors="replace"), re.M))
retired = {k for k, v in strs.items() if v[0] in {"superseded", "deprecated", "archived"}}
live = set(strs) - retired
print(f"StRS files: {len(strs)}, retired: {len(retired)}, live: {len(live)}")
print(f"live StRS with an @accepts_req marker: {len(live & marked)}")
print(f"live StRS without any @accepts_req marker: {len(live - marked)}")
print(f"W004 StRS in the new-mode log: {len(w004)}; same set as the previous line: {w004 == live - marked}")
print(f"in W004 but marked: {sorted(w004 & marked)}")
print(f"unmarked but not in W004: {sorted(live - marked - w004)}")
