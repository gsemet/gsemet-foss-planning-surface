"""List, per trust SwRS, the marked test files its notes omit and the reverse."""

import os
import re
import sys

root = sys.argv[1]
ids = "001 002 005 007 011 012 022 025 036 042 052 059 065 074 086 090 091 092".split()
marks = {}
for top in ("test", "tests", "scripts"):
    for folder, _, names in os.walk(os.path.join(root, top)):
        for name in names:
            if not name.endswith((".ts", ".py", ".js", ".mjs")):
                continue
            path = os.path.join(folder, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if "@tests_req" not in line:
                        continue
                    for match in re.finditer(r"SwRS-MDOKFSTUDIO-TRUST-(\d{3})(#S\d+(?:,\s*#?S\d+)*)?", line):
                        found = marks.setdefault(match.group(1), {}).setdefault(rel, set())
                        found.update(re.findall(r"S\d+", match.group(2) or ""))
for ident in ids:
    doc = os.path.join(root, "requirements/tiers/swrs/trust-security", f"SwRS-MDOKFSTUDIO-TRUST-{ident}.md")
    with open(doc, encoding="utf-8") as handle:
        text = handle.read()
    notes = text.split("### Verification notes")[1].split("<!-- okf:links")[0] if "### Verification notes" in text else ""
    named = set(re.findall(r"(?:test|tests)/[\w./-]+\.(?:ts|py)", notes))
    marked = marks.get(ident, {})
    print("==", ident)
    for rel in sorted(set(marked) - named):
        print("   marked, not in notes:", rel, sorted(marked[rel]))
    for rel in sorted(named - set(marked)):
        print("   in notes, no marker:", rel)
