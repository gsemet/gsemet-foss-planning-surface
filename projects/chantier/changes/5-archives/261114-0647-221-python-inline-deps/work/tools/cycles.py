"""Print the import cycles among chantier's modules (imports inside functions counted)."""
import ast
import sys
from pathlib import Path

PKG = Path(sys.argv[1])
mods = {}
for p in PKG.rglob("*.py"):
    rel = p.relative_to(PKG.parent).with_suffix("")
    name = ".".join(rel.parts)
    if name.endswith(".__init__"):
        name = name[: -len(".__init__")]
    mods[name] = p
graph = {}
for name, p in mods.items():
    deps = set()
    for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
        if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 and n.module.startswith("chantier"):
            base = n.module
            for a in n.names:
                cand = f"{base}.{a.name}"
                deps.add(cand if cand in mods else base)
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name.startswith("chantier"):
                    deps.add(a.name)
    graph[name] = {d for d in deps if d in mods and d != name}
sys.setrecursionlimit(10000)
seen, stack, onstack, found = set(), [], set(), set()


def visit(n):
    seen.add(n)
    stack.append(n)
    onstack.add(n)
    for d in sorted(graph[n]):
        if d in onstack:
            cyc = stack[stack.index(d):] + [d]
            found.add(" -> ".join(cyc))
        elif d not in seen:
            visit(d)
    stack.pop()
    onstack.discard(n)


for m in sorted(graph):
    if m not in seen:
        visit(m)
print("\n".join(sorted(found)) or "no cycle")
