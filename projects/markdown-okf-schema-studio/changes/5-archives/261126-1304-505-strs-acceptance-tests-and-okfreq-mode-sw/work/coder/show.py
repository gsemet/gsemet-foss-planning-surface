"""Print, for each SwRS number given as NNN:S1,S2 (or NNN:all), its statement, the named scenario
sections, the other body sections and the marked files (read only).

usage: python -I show.py <worktree> NNN:S1,S2 ...
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(sys.argv[1])
for spec in sys.argv[2:]:
    num, frags = spec.split(":")
    wanted = frags.split(",")
    path = root / f"requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-{num}.md"
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    front, body = text.split("\n---\n", 1)
    print("=" * 20, num)
    for key in ("title", "description", "req_lifecycle", "implemented_in_files", "tested_in_files"):
        m = re.search(rf"^{key}:(.*(?:\n(?:  |- ).*)*)", front, re.M)
        if m:
            print(key, ":", " ".join(m.group(1).split()))
    body = body.split("<!-- okf:links:start -->")[0]
    sections = re.split(r"^(?=###? )", body, flags=re.M)
    for section in sections:
        m = re.match(r"### Scenario (S\d+)\b", section)
        if m:
            if m.group(1) in wanted or "all" in wanted:
                print(section.rstrip())
        else:
            print(section.rstrip())
