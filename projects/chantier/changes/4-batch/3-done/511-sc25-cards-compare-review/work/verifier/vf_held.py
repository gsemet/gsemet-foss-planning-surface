import re
import sys
from pathlib import Path

wt = Path(sys.argv[1])
triage = Path(sys.argv[2]).read_text("utf-8").splitlines()
want = sys.argv[3]  # "held" or "restored"
lo, hi = int(sys.argv[4]), int(sys.argv[5])


def cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip()[1:-1])
    return [p.strip().replace("\\|", "|") for p in parts]


rows = {}
section = None
for line in (wt / "docs/proofs/cards-inventory.md").read_text("utf-8").splitlines():
    if line.startswith("## "):
        section = line[3:]
    elif section == "Rows" and line.startswith("|"):
        c = cells(line)
        rows[c[0]] = c

picked = []
for line in triage:
    m = re.match(r"^\| (\S+) \| yes \| (held|restored) at (\S+):(\d+) \|", line)
    if m and m[2] == want:
        picked.append((m[1], m[3], int(m[4])))
print("count", len(picked))
for rid, path, n in picked[lo:hi]:
    text = (wt / path).read_text("utf-8").splitlines()
    r = rows[rid]
    print(f"== {rid} [{r[5]}] old: {r[3]}")
    print(f"   inventory home: {r[6]} | check: {r[7][:160]}")
    print(f"   head {path.split('references/')[-1]}:{n}: {text[n - 1]}")
