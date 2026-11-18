"""Bytes of what a fresh Foreman or Chief of Staff must read at startup, from the startup manifest.

Command: python 10-startup-sizes.py [<chantier checkout>] > 10-startup-sizes.csv
(default checkout: C:/Users/gaeta/Projets/chantier). Read-only. Figures only: file, section heading,
bytes, and bytes / 4 as a rough token count (a ratio, not a measured tokenisation).
"""
import csv
import json
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/gaeta/Projets/chantier"
man = json.load(open(os.path.join(root, "skills/chantier/references/startup-manifest.json"), encoding="utf-8"))


def section(path, heading):
    text = open(os.path.join(root, path), encoding="utf-8").read()
    i = text.find("\n" + heading + "\n") + 1
    if i == 0:
        return None
    j = text.find("\n## ", i + len(heading))
    return text[i:] if j < 0 else text[i:j + 1]


w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["role", "host", "file", "part", "bytes", "approx_tokens_bytes_div_4"])
for role in ("foreman", "chief-of-staff"):
    rows = []
    for p in (man["common"], man["role_core"], man["hosts"]["claude"]["core"]):
        rows.append(("", p, "whole file", len(open(os.path.join(root, p), "rb").read())))
    for s in man["mandatory_sections"].get(role, []):
        sec = section(s["file"], s["heading"])
        rows.append((s.get("host", ""), s["file"], s["heading"], len(sec.encode("utf-8")) if sec else "not found"))
    if role == "chief-of-staff":
        p = man["roles"][role]
        rows.append(("", p, "whole file (role file)", len(open(os.path.join(root, p), "rb").read())))
    rows.append(("", "AGENTS.md", "whole file", len(open(os.path.join(root, "AGENTS.md"), "rb").read())))
    for host, f, part, n in rows:
        w.writerow([role, host, f, part, n, round(n / 4) if isinstance(n, int) else ""])
