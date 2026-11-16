"""Repoint `from chantier.x import name` where `name` now lives in another chantier module."""
import ast
import sys
from collections import defaultdict
from pathlib import Path

CLI = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-221\skills\chantier\scripts\cli")
PKG = CLI / "src" / "chantier"


def modname(p):
    return ".".join(p.relative_to(PKG.parent).with_suffix("").parts).removesuffix(".__init__")


defs = defaultdict(set)  # module -> defined names
imported = defaultdict(set)
for p in PKG.rglob("*.py"):
    m = modname(p)
    for n in ast.parse(p.read_text(encoding="utf-8")).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs[m].add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                for e in (t.elts if isinstance(t, ast.Tuple) else [t]):
                    if isinstance(e, ast.Name):
                        defs[m].add(e.id)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            defs[m].add(n.target.id)
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                imported[m].add(a.asname or a.name)
home = defaultdict(set)
for m, names in defs.items():
    for nm in names:
        home[nm].add(m)
files = list(PKG.rglob("*.py")) + list((CLI / "tests").rglob("*.py"))
for p in files:
    t = p.read_text(encoding="utf-8")
    tree = ast.parse(t)
    edits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith("chantier.") and n.level == 0:
            keep, move = [], defaultdict(list)
            for a in n.names:
                spelled = a.name + (f" as {a.asname}" if a.asname else "")
                if a.name in defs[n.module] or a.name in imported[n.module] or n.module not in defs:
                    keep.append(spelled)
                else:
                    cands = home.get(a.name, set())
                    if len(cands) == 1:
                        move[next(iter(cands))].append(spelled)
                    else:
                        print("UNKNOWN", p.name, n.module, a.name, sorted(cands))
                        keep.append(spelled)
            if move:
                new = []
                if keep:
                    new.append(f"from {n.module} import {', '.join(keep)}")
                for mod, ns in move.items():
                    new.append(f"from {mod} import {', '.join(ns)}")
                edits.append((n.lineno, n.end_lineno, "\n".join(new)))
    if edits:
        lines = t.split("\n")
        for a, b, new in sorted(edits, reverse=True):
            lines[a - 1:b] = new.split("\n")
        p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
        print("repointed", p.name)
