"""Dump the base host JSON rows, one line per sentence of `means`, with its line in the file."""

import json
import sys

sys.path.insert(0, __file__.replace("\\", "/").rsplit("/", 1)[0])
from hsplit import REFS, base_text  # noqa: E402

for host in ("claude-code", "copilot"):
    raw = base_text(REFS + f"hosts/{host}.json")
    lines = raw.split("\n")
    print("=====", host)
    for row in json.loads(raw)["rows"]:
        first = next(i for i, t in enumerate(lines, 1) if f'"{row["capability"]}"' in t)
        print(f"-- {row['capability']} @{first} [{row.get('mark')}] {row.get('roles')}")
        for s in row.get("means", []):
            print("   ", s)
