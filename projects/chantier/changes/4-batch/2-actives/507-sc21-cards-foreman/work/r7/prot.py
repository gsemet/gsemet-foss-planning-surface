"""Which topic rows read as protecting (the selector of the earlier lists), and which are listed."""
import re
import sys

import inv

STRONG = re.compile(
    r"\b(never|not without|only on the user|only with the user|user's (?:own )?(?:word|yes|answer)|"
    r"only after the user|must not|refus\w*|no guess|without the user)\b",
    re.I,
)
for name in inv.NAMES:
    text = (inv.EV / f"cards-inventory-{name}.md").read_text(encoding="utf-8")
    cand = [
        d
        for _, d in inv.rows(name)
        if d["kind"].startswith("e") and "topic " in d["new home"] and STRONG.search(d["behaviour"])
    ]
    m = re.search(r"## Protecting-looking rows[^\n]*\n(.*?)(?=\n## |\Z)", text, re.S)
    listed = re.findall(r"^\| ([A-Z]+-[A-Z0-9]+) \|", m[1], re.M) if m else []
    ids = [d["id"] for d in cand]
    print(name, "candidates", len(ids), "listed", len(listed), "with rule",
          sum("the rule it applies" in d["new home"] for d in cand))
    print("  not listed:", [i for i in ids if i not in listed][:60])
    print("  listed, not candidate:", [i for i in listed if i not in ids][:60])
    if name in sys.argv[1:]:
        for d in cand:
            print(d["id"], "|", d["new home"], "|", d["behaviour"][:170])
