"""Compare the description's per-key homes list with HOMES at base and head (read only).

Usage: homes_check.py <worktree> <body.md>
"""

import ast
import re
import subprocess
import sys
from pathlib import Path

WT, BODY = sys.argv[1], Path(sys.argv[2])
body = BODY.read_text(encoding="utf-8").replace("\r\n", "\n")


def load(rev):
    src = subprocess.run(
        ["git", "-C", WT, "show", f"{rev}:skills/chantier/scripts/cli/tests/test_card_homes.py"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    ns = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "HOMES":
            ns = ast.literal_eval(node.value)
    return {k: [f"topic {t}" for t in topics.split()] + other for k, (topics, other) in ns.items()}


b, h = load("fbdb53d2"), load("22ccbe0b")
print("base keys", len(b), "homes", sum(map(len, b.values())))
print("head keys", len(h), "homes", sum(map(len, h.values())), "dropped", sum(map(len, b.values())) - sum(map(len, h.values())))
print("added", {k: sorted(set(h[k]) - set(b.get(k, []))) for k in h if set(h[k]) - set(b.get(k, []))})
print("removed keys", {k: b[k] for k in b if k not in h})
sect = body.split("### Homes kept in `test_card_homes.py`")[1].split("## Blast radius")[0]
per = re.findall(r"^- `(test_\w+)`: (\d+) kept, (\d+) dropped\. (.*)$", sect, re.M)
errors = []
for key, kept, dropped, rest in per:
    names = re.findall(r"`((?:topic|card|floor|skill|host) [^`]+)` \(", rest)
    if int(kept) != len(h[key]) or int(dropped) != len(b[key]) - len(h[key]) or sorted(names) != sorted(h[key]):
        errors.append((key, kept, dropped, len(h[key]), len(b[key]), sorted(set(h[key]) ^ set(names))))
print("keys in body", len(per), "missing", set(h) - {k for k, *_ in per}, "errors", errors)
print("listed kept", sum(int(k) for _, k, _, _ in per), "listed dropped", sum(int(d) for _, _, d, _ in per))
