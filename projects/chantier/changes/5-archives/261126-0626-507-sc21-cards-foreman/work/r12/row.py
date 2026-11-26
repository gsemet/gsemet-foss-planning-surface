"""Read-only: the pr-body.md edited-lines rows against the lines changed since fe7fbf0f.

`--text` prints the "rules put back" list the tree asks for.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]
source = (HERE.parent / "r10" / "siblings.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")
ns: dict = {"__file__": str(HERE.parent / "r10" / "siblings.py"), "__name__": "siblings"}
exec(compile(source, "siblings.py", "exec"), ns)

BASE = "fe7fbf0f"
present = ns["now"]()
old_files = ns["tree"](BASE)
actual: dict[str, set[int]] = {}
for name in sorted(old_files - {"topics.json"}):
    if name in present:
        lines = ns["changed"](BASE, name)
        if lines:
            actual[name] = set(lines)
        continue
    before = set(ns["git"]("show", f"{BASE}:{ns['ROOT']}{name}").splitlines())
    parts = ns["parts_of"](name, present - old_files)
    if not parts:
        print("deleted, no part:", name)
    for part in parts:
        actual[part] = {n for n, line in enumerate(ns["read"](part), 1) if line not in before}

whole = (HERE.parents[1] / "pr-body.md").read_text(encoding="utf-8")
if "--pairs" in ARGS:
    import json

    for pair in json.loads((HERE.parent / "r12-body.json").read_text(encoding="utf-8")):
        count = whole.count(pair["old"])
        print("pair: old found", count, "time(s):", pair["old"])
        assert count == 1
        whole = whole.replace(pair["old"], pair["new"])
body = whole.split("\n")
ENTRY = r"([\w./-]+) (\d+(?:(?:, | and )\d+)*)(?![\d,]*[a-z-])"
listed: dict[str, set[int]] = {}
where: dict[str, list[int]] = {}
first = next(i for i, t in enumerate(body) if t.startswith("| File and line (under"))
for number in range(first + 2, len(body)):
    row = body[number]
    if not row.startswith("|"):
        break
    cell = row.split("|")[1].strip()
    prefix = "topics/" if cell.startswith("topics") else ""
    cell = re.sub(r"^topics(?:, rules put back)?: ", "", cell)
    carry = None
    for m in re.finditer(r"([\w./-]+?(?:\.md)?) ((?:\d+(?:-\d+)?)(?:(?:, | and )(?:\d+(?:-\d+)?)(?![\w.-]))*)", cell):
        name = m.group(1)
        if name == "and":
            continue
        if not name.endswith(".md"):
            name += ".md"
        name = prefix + name
        nums = set()
        for a, b in re.findall(r"(\d+)(?:-(\d+))?", m.group(2)):
            nums.update(range(int(a), int(b or a) + 1))
        listed.setdefault(name, set()).update(nums)
        where.setdefault(name, []).append(number + 1)

for name in sorted(set(actual) | set(listed)):
    if actual.get(name) != listed.get(name):
        print(
            f"{name}\tchanged {sorted(actual.get(name, []))}\tlisted {sorted(listed.get(name, []))}"
            f"\trows {where.get(name, [])}"
        )

if "--text" in ARGS:
    other = next(t for t in body if t.startswith("| topics: ")).split("|")[1]
    taken = {
        f"topics/{m.group(1)}.md": {int(n) for n in re.findall(r"\d+", m.group(2))}
        for m in re.finditer(r"([a-z][\w-]*) (\d+(?:(?:, | and )\d+(?![\w-]))*)", other.split(": ", 1)[1])
    }
    items = []
    for name in sorted(n for n in actual if n.startswith("topics/")):
        nums = sorted(actual[name] - taken.get(name, set()))
        if nums:
            words = [str(n) for n in nums]
            tail = words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]
            items.append(f"{name[7:-3]} {tail}")
    print("TAKEN", sorted(taken.items()))
    print("LIST", ", ".join(items))
