"""Check a posted PR description against the head of a worktree (read only).

Usage: desc_check.py <worktree> <body.md> <body.html>
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

WT, BODY, HTML = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
BASE, HEAD = "fbdb53d2", "22ccbe0b"
REFS = "skills/chantier/references/"
CLI = "skills/chantier/scripts/cli/src/chantier/"
body = BODY.read_text(encoding="utf-8").replace("\r\n", "\n")
rendered = HTML.read_text(encoding="utf-8")


def show(rev, path):
    run = subprocess.run(["git", "-C", WT, "show", f"{rev}:{path}"], capture_output=True)
    return run.stdout.decode("utf-8") if run.returncode == 0 else None


print("== layout")
for line in body.split("\n"):
    if re.match(r"^(#{2,3} |<details>|<summary>|</details>)", line) or "Generated with" in line:
        print(f"  {line}")
print("blank after </summary>:", "</summary>\n\n" in body, "| blank before </details>:", "\n\n</details>" in body)
print("text after </details>:", repr(body.split("</details>")[-1]))
print("length:", len(body), "| <img>:", "<img" in body, "| '![':", "![" in body)
print("STALE:", body.count("STALE"), "| UNVERIFIED:", body.count("UNVERIFIED"))
print("rendered h2/h3:", re.findall(r"<h([23])[^>]*>(.*?)</h[23]>", rendered))
for tag in ("details", "table", "pre", "li", "input"):
    print(f"rendered <{tag}>:", len(re.findall(rf"<{tag}[ >]", rendered)), "closed:", rendered.count(f"</{tag}>"))
print("task boxes checked:", len(re.findall(r"<input[^>]*checked", rendered)))

print("== list counts")
rules = show(HEAD, "docs/protective-rules.md")
rows = [
    [c.strip() for c in line.split(" | ")]
    for line in rules.split("\n")
    if line.startswith("| ") and re.search(r"\| `(held|restored here|to add)` \|", line)
]
states = {}
for r in rows:
    states[r[2]] = states.get(r[2], 0) + 1
print("file lines:", len(rules.rstrip("\n").split("\n")), "| rows:", len(rows), states)
for r in rows:
    if r[2] == "`to add`":
        ident = r[0].lstrip("| ")
        step = re.search(r"plan step \d+|no step of plan section 6", r[3])
        print("  to add", ident, "->", step.group(0) if step else None)

print("== inventory files at base")
for p in (
    "docs/proofs/cards-inventory.md",
    "docs/proofs/cards-inventory-open.tsv",
    "skills/chantier/scripts/cli/tests/cards_inventory.py",
    "skills/chantier/scripts/cli/tests/test_cards_inventory.py",
):
    size = subprocess.run(["git", "-C", WT, "cat-file", "-s", f"{BASE}:{p}"], capture_output=True, text=True)
    print(" ", p, size.stdout.strip(), "| at head:", show(HEAD, p) is not None)

print("== open rows and per-row lines")
tsv = [l.split("\t") for l in show(BASE, "docs/proofs/cards-inventory-open.tsv").split("\n") if l.strip()]
kinds_of = {}
for cells in tsv:
    rid = cells[0]
    kind = next((c for c in cells[1:] if re.fullmatch(r"[a-f]", c)), None)
    if re.fullmatch(r"[A-Z]+-[A-Z]?\d+", rid):
        kinds_of[rid] = kind
per = {}
for k in kinds_of.values():
    per[k] = per.get(k, 0) + 1
print("open rows:", len(kinds_of), dict(sorted(per.items(), key=lambda x: str(x[0]))))
sect = body.split("### The last reading of the open rows")[1].split("### Homes kept")[0]
lines = re.findall(r"^- ([A-Z]+-[A-Z]?\d+): (.*)$", sect, re.M)
per = {}
for rid, _ in lines:
    per[kinds_of.get(rid)] = per.get(kinds_of.get(rid), 0) + 1
print("pr row lines:", len(lines), "unique:", len({r for r, _ in lines}), dict(sorted(per.items(), key=lambda x: str(x[0]))))
misses = []
hosts = {}
for rid, text in lines:
    m = re.search(r"(?:CLI )?`([^`]+)` \"(.*)\"\s*$", text.split(". ", 0)[0])
    found = re.findall(r"(CLI )?`([^`]+\.(?:md|py|json|yaml|tsx))` \"", text)
    if not found:
        misses.append((rid, "no home parsed"))
        continue
    cli, path = found[-1]
    span = text[text.rindex(f"`{path}` \"") + len(path) + 4 : -1]
    if cli:
        full = CLI + path
    elif path.startswith(("skills/", "agents/")):
        full = path
    else:
        full = REFS + path
    content = show(HEAD, full)
    flat = " ".join((content or "").split())
    if content is None or (" ".join(span.split()) not in flat and span not in content):
        misses.append((rid, full, span))
print("span misses:", len(misses))
for miss in misses:
    print("  ", miss)

print("== homes summary in body")
homes = body.split("### Homes kept in `test_card_homes.py`")[1].split("## Blast radius")[0]
per_key = re.findall(r"^- `(test_\w+)`: (\d+) kept, (\d+) dropped\. (.*)$", homes, re.M)
print("keys:", len(per_key), "kept:", sum(int(k) for _, k, _, _ in per_key), "dropped:", sum(int(d) for _, _, d, _ in per_key))



print("== ids the body gives after homes, against the list")
ids = set()
for r in rows:
    ids.update(r[0].lstrip("| ").split("/"))
named = set()
for _, _, _, rest in per_key:
    for group in re.findall(r"` \(([^()]*)\)", rest):
        named.update(re.findall(r"\b([PABCDN]\d+)\b", group))
print("ids named after homes:", len(named), "not in the list:", sorted(named - ids))

print("== internal references outside the last section")
head_part = body.split("## Internal references")[0]
patterns = {
    "CR-n": r"\bCR[- ]?\d+",
    "batch-n": r"\bbatch[- ]?\d+",
    "round": r"\bround\b|\br\d\b",
    "order O-n": r"\bO-\d+",
    "planning path": r"\.agents/changes|4-batch|2-backlog|3-ready|projects/chantier",
    "question id": r"\b[a-z]+(?:-[a-z]+)*-Q\d+",
    "CR slug": r"cards-inventory-last-reading|cards-delete-|cards-inventory-last",
    "PR number": r"#\d{2,}",
    "machine path": r"[A-Z]:[\\/]|/home/|/Users/",
    "role capitalised": r"\b(Chief of Staff|Foreman|Griller|Driver|Coder|Inspector|Verifier|Investigator|Debugger|Conflict resolver|Spec-writer|Spec critic|Demo explorer)\b",
}
for name, pat in patterns.items():
    hits = [
        (i + 1, m.group(0))
        for i, line in enumerate(head_part.split("\n"))
        for m in re.finditer(pat, line, re.I if name != "role capitalised" else 0)
    ]
    print(f"  {name}: {hits[:12]}")
print("title:", json.dumps("docs(cards): list the protective rules and remove the old cards' inventory"))
print("rendered text sample after </details>:", html.unescape(re.sub(r"<[^>]+>", "", rendered.split("</details>")[-1])).strip())
