"""Read-only: the lines of cards-next changed, against fe7fbf0f for the files that existed
there (the pr-body and sibling tables), and against the head 03f973e4 for the others.

A file split into `<name>-pN.md` shows each part's lines that the old file did not hold.
With `--rows`, also compares with the inventory's sibling table.
"""

import re
import subprocess
import sys
from pathlib import Path

TREE = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
ROOT = "skills/chantier/cards-next/"
EVIDENCE = Path(__file__).resolve().parents[2] / "evidence"


def git(*args: str) -> str:
    out = subprocess.run(["git", "-C", TREE, *args], capture_output=True, check=True).stdout
    return out.decode("utf-8")


def tree(commit: str) -> set[str]:
    names = git("ls-tree", "-r", "--name-only", commit, "--", ROOT).split()
    return {name[len(ROOT) :] for name in names}


def now() -> set[str]:
    base = Path(TREE, ROOT)
    return {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}


def read(name: str) -> list[str]:
    return Path(TREE, ROOT, name).read_text(encoding="utf-8").splitlines()


def changed(commit: str, name: str) -> list[int]:
    old = git("show", f"{commit}:{ROOT}{name}").splitlines()
    new = read(name)
    if old == new:
        return []
    out = []
    for line in git("diff", "-U0", "--ignore-cr-at-eol", commit, "--", ROOT + name).splitlines():
        head = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if head:
            first, count = int(head.group(1)), int(head.group(2) or 1)
            out.extend(range(first, first + count))
    return out


def parts_of(name: str, files: set[str]) -> list[str]:
    stem = re.sub(r"(-p\d+)?\.md$", "", name)
    return sorted(f for f in files if re.fullmatch(rf"{re.escape(stem)}-p\d+\.md", f))


def ranges(numbers: list[int]) -> str:
    return ", ".join(map(str, numbers))


def main() -> None:
    present = now()
    result: dict[str, dict[str, list[int]]] = {"fe7fbf0f": {}, "03f973e4": {}}
    seen: set[str] = set()
    for commit in ("fe7fbf0f", "03f973e4"):
        old_files = tree(commit)
        for name in sorted(old_files):
            if name in seen or name == "topics.json":
                continue
            seen.add(name)
            if name in present:
                lines = changed(commit, name)
                if lines:
                    result[commit][name] = lines
                continue
            parts = parts_of(name, present - old_files)
            if not parts:
                result[commit][name] = []
                continue
            before = set(git("show", f"{commit}:{ROOT}{name}").splitlines())
            for part in parts:
                seen.add(part)
                result[commit][f"{part} (from {name})"] = [
                    n for n, line in enumerate(read(part), 1) if line not in before
                ]
    for name in sorted(present - seen - {"topics.json"}):
        if name not in tree("03f973e4") and name not in tree("fe7fbf0f"):
            result["03f973e4"][f"{name} (new)"] = []
    for commit, files in result.items():
        print(f"#### against {commit}: {len(files)} files")
        for name, lines in files.items():
            print(f"{name}\t{ranges(lines)}")
    if "--rows" not in sys.argv:
        return
    text = (EVIDENCE / "cards-inventory-host-and-shared.md").read_text(encoding="utf-8")
    section = text.split("## Sibling-card edits", 1)[1].split("\n## ", 1)[0]
    listed: dict[str, set[int]] = {}
    for line in section.splitlines():
        if line.startswith("| ") and ".md" in line.split("|")[1]:
            for name, numbers in re.findall(r"([\w/.-]+\.md)(?::([\d, -]+))?", line.split("|")[1]):
                found = listed.setdefault(name, set())
                for first, last in re.findall(r"(\d+)(?:-(\d+))?", numbers or ""):
                    found.update(range(int(first), int(last or first) + 1))
    print("#### inventory sibling table against fe7fbf0f")
    actual = {name.split(" (from ")[0]: set(lines) for name, lines in result["fe7fbf0f"].items()}
    for name in sorted(actual | listed):
        if actual.get(name) != listed.get(name):
            print(f"{name}\tchanged {sorted(actual.get(name, []))}\tlisted {sorted(listed.get(name, []))}")


main()
