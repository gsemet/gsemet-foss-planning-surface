"""Round 10, read-only: the words each replacement batch added and removed, and the cards-next files
the session wrote with its file tools (from its transcript)."""

import difflib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if len(sys.argv) > 1:
    seen: dict[str, int] = {}
    for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        stamp = entry.get("timestamp", "")
        content = entry.get("message", {}).get("content")
        for part in content if isinstance(content, list) else []:
            if part.get("type") == "tool_use" and part.get("name") in ("Edit", "Write"):
                path = part["input"].get("file_path", "").replace("\\", "/")
                if "/cards-next/" in path or "/evidence/" in path:
                    print(stamp[:19], part["name"], re.split(r"/cards-next/|/507-sc21-cards-foreman/", path)[-1])
    sys.exit(0)
for path in sorted(HERE.glob("*pairs*.json")):
    print("=====", path.name)
    for name, old, new in json.loads(path.read_text(encoding="utf-8")):
        if name.startswith("cards-inventory"):
            continue
        a, b = old.split(), new.split()
        out = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag != "equal":
                out.append(f"-[{' '.join(a[i1:i2])[:90]}] +[{' '.join(b[j1:j2])[:150]}]")
        print(name, " ".join(out))
