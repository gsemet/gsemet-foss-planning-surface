"""Bring the inventory's sibling-card edits table up to the lines changed since fe7fbf0f.

A row whose lines are already right stays as written. Another row keeps its text and gains the
words each newly listed line adds; rows of a file that was split are replaced by its parts'.
Dry without `--apply`.
"""

import difflib
import re
import sys
from pathlib import Path

sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
HERE = Path(__file__).resolve().parent
source = (HERE / "siblings.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")
ns: dict = {"__file__": str(HERE / "siblings.py"), "__name__": "siblings"}
exec(compile(source, "siblings.py", "exec"), ns)

PATH = HERE.parents[1] / "evidence" / "cards-inventory-host-and-shared.md"
BASE = "fe7fbf0f"
ROOT = ns["ROOT"]


def expand(cell: str) -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    for name, numbers in re.findall(r"([\w/.-]+\.md)(?::([\d, -]+))?", cell):
        found = out.setdefault(name, set())
        for first, last in re.findall(r"(\d+)(?:-(\d+))?", numbers or ""):
            found.update(range(int(first), int(last or first) + 1))
    return out


def actual() -> dict[str, tuple[str, list[int]]]:
    present = ns["now"]()
    old_files = ns["tree"](BASE)
    out: dict[str, tuple[str, list[int]]] = {}
    for name in sorted(old_files - {"topics.json"}):
        if name in present:
            lines = ns["changed"](BASE, name)
            if lines:
                out[name] = (name, lines)
            continue
        before = set(ns["git"]("show", f"{BASE}:{ROOT}{name}").splitlines())
        for part in ns["parts_of"](name, present - old_files):
            numbers = [n for n, line in enumerate(ns["read"](part), 1) if line not in before]
            out[part] = (name, numbers)
    return out


def added(old_name: str, new_name: str, number: int) -> str:
    old = ns["git"]("show", f"{BASE}:{ROOT}{old_name}").splitlines()
    line = ns["read"](new_name)[number - 1]
    if number == 1:
        return f"title `{line.lstrip('# ')}`"
    words = line.split()
    best = max(old, key=lambda o: difflib.SequenceMatcher(None, o.split(), words).ratio())
    match = difflib.SequenceMatcher(None, best.split(), words, autojunk=False)
    if match.ratio() < 0.2:
        pieces = [" ".join(words[:12]) + (" ..." if len(words) > 12 else "")]
    else:
        pieces = []
        for tag, i1, i2, j1, j2 in match.get_opcodes():
            if tag in ("insert", "replace"):
                text = " ".join(words[j1:j2])
                pieces.append(text if len(text) <= 90 else text[:90].rsplit(" ", 1)[0] + " ...")
            elif tag == "delete":
                text = " ".join(best.split()[i1:i2])
                pieces.append("cut: " + (text if len(text) <= 50 else text[:50].rsplit(" ", 1)[0] + " ..."))
    pieces = [p.replace("`", "'").replace("|", "\\|") for p in pieces[:4]]
    return ", ".join(f"`{p}`" for p in pieces) or "reflowed"


def main() -> None:
    raw = PATH.read_bytes()
    text = raw.decode("utf-8-sig")
    head, rest = text.split("## Sibling-card edits", 1)
    section, sep, tail = rest.partition("\n## ")
    lines = section.split("\n")
    first = next(i for i, t in enumerate(lines) if t.startswith("| file:line |")) + 2
    last = first
    while last < len(lines) and lines[last].startswith("|"):
        last += 1
    rows = lines[first:last]
    have = actual()
    new_rows: list[str] = []
    union: dict[str, set[int]] = {}
    gone: dict[str, list[str]] = {}
    for row in rows:
        cell = re.split(r"(?<!\)\|", row)[1].strip()
        listed = expand(cell)
        if all(name not in have for name in listed):
            for name in listed:
                gone.setdefault(name, []).append(re.split(r"(?<!\)\|", row)[2].strip())
            print("dropped row (file split):", cell)
            continue
        for name, numbers in listed.items():
            if name not in have:
                print("MULTI-FILE ROW with a split file:", cell)
            elif numbers - set(have[name][1]):
                print("STALE LINES:", cell, sorted(numbers - set(have[name][1])))
            union.setdefault(name, set()).update(numbers)
        new_rows.append(row)
    for name, (old_name, numbers) in have.items():
        fresh = [n for n in numbers if n not in union.get(name, set())]
        if not fresh:
            continue
        extra = "; ".join(f"line {n}: {added(old_name, name, n)}" for n in fresh)
        if old_name != name:
            former = gone.get(old_name)
            kept = "; ".join(former) + "; " if former and name.endswith("p1.md") else ""
            extra = f"split from ; {kept}{extra}"
        new = f"| {name}:{ns['ranges'](fresh)} | {extra} | review |"
        new_rows.append(new)
        print(new)

    def order(row: str) -> tuple:
        name = re.split(r"(?<!\\)\|", row)[1].strip()
        return (name.startswith("topics/"), name)

    new_rows.sort(key=order)
    lines[first:last] = new_rows
    result = head + "## Sibling-card edits" + "\n".join(lines) + sep + tail
    print(len(rows), "rows before,", len(new_rows), "after")
    if "--apply" in ARGS:
        bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
        PATH.write_bytes(bom + result.encode("utf-8"))


main()
