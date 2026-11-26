"""Verifier: the Foreman inventory's boundary rows against the PR body's table."""

import re
import sys
from pathlib import Path

CR = Path("<CR folder>")
inv = (CR / "evidence/cards-inventory-foreman.md").read_text(encoding="utf-8").splitlines()
body = (CR / "pr-body.md").read_text(encoding="utf-8").splitlines()
SPLIT = re.compile(r"(?<!\\)\|")


def cells(line):
    return [x.strip() for x in SPLIT.split(line.strip().strip("|"))]


rows = {}
begin = next(i for i, l in enumerate(inv) if l.startswith('## "The user'))
stop = next((i for i, l in enumerate(inv[begin + 1:], begin + 1) if l.startswith("## ")), len(inv))
print("boundaries section lines", begin + 1, stop)
for line in inv[begin:stop]:
    if re.match(r"^\| *FM-B0\d\d ", line):
        c = cells(line)
        rows[c[0]] = {"label": c[2].split(":")[0], "kind": c[5], "home": c[6], "behaviour": c[3]}
print("inventory FM-B rows", len(rows), "ids", min(rows), max(rows))

table = {}
start = next(i for i, l in enumerate(body) if l.startswith("## The user's boundaries"))
for line in body[start:]:
    if line.startswith("## Human"):
        break
    if re.match(r"^\| B\d", line):
        c = cells(line)
        ids = []
        for part in c[2].split(","):
            part = part.strip()
            m = re.match(r"B(\d{3})(?:-B(\d{3}))?$", part)
            assert m, part
            a, b = int(m[1]), int(m[2] or m[1])
            ids += [f"FM-B{n:03d}" for n in range(a, b + 1)]
        table[c[0]] = {"protects": c[1], "ids": ids, "home": c[3], "topic": c[4]}
print("body labels", len(table), " ".join(table))

by_label = {}
for k, v in rows.items():
    by_label.setdefault(v["label"], []).append(k)
print("inventory labels", len(by_label))
print("labels only in body", sorted(set(table) - set(by_label)))
print("labels only in inventory", sorted(set(by_label) - set(table)))
for lab, t in table.items():
    have = sorted(by_label.get(lab, []))
    if have != sorted(t["ids"]):
        print("MISMATCH", lab, "body", t["ids"], "inventory", have)
listed = [i for t in table.values() for i in t["ids"]]
print("ids in body table", len(listed), "dup", sorted({i for i in listed if listed.count(i) > 1}),
      "missing", sorted(set(rows) - set(listed)), "unknown", sorted(set(listed) - set(rows)))
print()
for lab, t in table.items():
    print("==", lab, t["protects"])
    for i in t["ids"]:
        r = rows[i]
        print("  ", i, r["label"], "k=" + r["kind"], "::", r["home"][:200])
        if "-v" in sys.argv:
            print("        >", r["behaviour"][:260])
