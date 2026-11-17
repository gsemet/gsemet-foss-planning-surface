"""Rename marker IDs of absorbed SwRS to their survivors (CR-344 round 1). Scaffolding only."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
P = "SwRS-MDOKFSTUDIO-"
MAP = {
    "REVIEW-069": "REVIEW-054",
    "REVIEW-070": "REVIEW-074",
    "REVIEW-071": "REVIEW-074",
    "REVIEW-101": "REVIEW-100",
    "REVIEW-216": "REVIEW-017",
    "REVIEW-156": "REVIEW-152",
    "REVIEW-005": "REVIEW-009",
    "REVIEW-010": "REVIEW-009",
    "REVIEW-200": "REVIEW-195",
    "REVIEW-203": "REVIEW-195",
    "REVIEW-208": "REVIEW-207",
    "FMEDIT-054": "FMEDIT-016",
    "FMSCHEMA-060": "FMSCHEMA-050",
}
# line-specific overrides (file, 1-based line) -> replacement ID(s)
SPECIAL = {
    ("src/core/protocol/pageToHost.ts", 258): ("REVIEW-007", "REVIEW-006"),
    ("src/core/protocol/hostToPage.ts", 400): ("REVIEW-007", "REVIEW-009"),
    ("test/core/protocol/pageToHost.test.ts", 378): ("REVIEW-007", "REVIEW-006"),
    ("test/core/protocol/hostToPage.test.ts", 137): ("REVIEW-007", "REVIEW-009"),
    ("src/core/protocol/pageToHost.ts", 268): ("REVIEW-178", "REVIEW-186 SwRS-MDOKFSTUDIO-REVIEW-192"),
    ("test/core/protocol/pageToHost.test.ts", 303): ("REVIEW-178", "REVIEW-186 SwRS-MDOKFSTUDIO-REVIEW-192"),
}
pat = re.compile(re.escape(P) + r"(" + "|".join(MAP) + r")\b")
files = subprocess.run(["git", "ls-files", "src", "test"], cwd=ROOT, capture_output=True, text=True).stdout.split()
changed = []
for f in files:
    p = ROOT / f
    try:
        lines = p.read_text(encoding="utf8").split("\n")
    except Exception:
        continue
    out = []
    mod = False
    for i, line in enumerate(lines, 1):
        new = line
        sp = SPECIAL.get((f, i))
        if sp and P + sp[0] in line:
            new = line.replace(P + sp[0], P + sp[1])
        else:
            new = pat.sub(lambda m: P + MAP[m.group(1)], line)
        if new != line:
            mod = True
        out.append(new)
    if mod:
        p.write_text("\n".join(out), encoding="utf8", newline="")
        changed.append(f)
print("\n".join(changed))
