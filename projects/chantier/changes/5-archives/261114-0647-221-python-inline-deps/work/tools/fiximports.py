"""Add the missing `from chantier.x import name` for each undefined name (ruff F821) that has one home."""
import ast
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

CLI = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-221\skills\chantier\scripts\cli")
PKG = CLI / "src" / "chantier"
index = defaultdict(set)
for p in PKG.rglob("*.py"):
    rel = p.relative_to(PKG.parent).with_suffix("")
    mod = ".".join(rel.parts).removesuffix(".__init__")
    for n in ast.parse(p.read_text(encoding="utf-8")).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            index[n.name].add(mod)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                for e in (t.elts if isinstance(t, ast.Tuple) else [t]):
                    if isinstance(e, ast.Name):
                        index[e.id].add(mod)
out = subprocess.run(["uvx", "ruff@0.17.5", "check", "src", "tests", "--select", "F821", "--output-format", "json"],
                     cwd=CLI, capture_output=True, text=True).stdout
need = defaultdict(set)
for d in json.loads(out):
    name = d["message"].split("`")[1]
    need[d["filename"]].add(name)
for fn, names in need.items():
    path = Path(fn)
    this = ".".join(path.relative_to(PKG.parent).with_suffix("").parts) if PKG in path.parents else None
    add = defaultdict(list)
    for nm in sorted(names):
        homes = index.get(nm, set()) - {this}
        if len(homes) == 1:
            add[next(iter(homes))].append(nm)
        else:
            print("AMBIGUOUS/UNKNOWN", path.name, nm, sorted(homes))
    if not add:
        continue
    t = path.read_text(encoding="utf-8")
    lines = [f"from {m} import {', '.join(ns)}" for m, ns in sorted(add.items())]
    marker = "from __future__ import annotations\n"
    if marker in t:
        i = t.index(marker) + len(marker)
        t = t[:i] + "\n" + "\n".join(lines) + "\n" + t[i:]
    else:
        t = "\n".join(lines) + "\n" + t
    path.write_text(t, encoding="utf-8", newline="\n")
    print("fixed", path.name, [n for ns in add.values() for n in ns])
