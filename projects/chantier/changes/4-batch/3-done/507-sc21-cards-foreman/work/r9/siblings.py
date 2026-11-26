"""Read-only: compare the sibling-card edits table with the changed lines since fe7fbf0f.

Run: python -I siblings.py <worktree> <host-and-shared inventory>
Prints, per file that existed at fe7fbf0f, the lines changed (new-side numbers) with their
text, and the lines the table lists. Renamed files print each new line not in the old file.
"""

import pathlib
import re
import subprocess
import sys

BASE = "fe7fbf0f"
ROOT = "skills/chantier/cards-next/"
SPLITS = {
    "batch-plan-cut": ["batch-plan-cut-p1", "batch-plan-cut-p2"],
    "forge-permissions": ["forge-permissions-p1", "forge-permissions-p2"],
    "main-checkout": ["main-checkout-p1", "main-checkout-p2"],
    "mode-switch": ["mode-switch-p1", "mode-switch-p2"],
    "project-rules": ["project-rules-p1", "project-rules-p2"],
}


def git(tree, *args):
    out = subprocess.run(
        ["git", "-C", tree, *args], capture_output=True, check=True
    ).stdout
    return out.decode("utf-8")


def main():
    tree, inventory = sys.argv[1], pathlib.Path(sys.argv[2])
    listed = {}
    text = inventory.read_text(encoding="utf-8")
    section = text.split("## Sibling-card edits", 1)[1].split("\n## ", 1)[0]
    for line in section.splitlines():
        if line.startswith("| ") and ".md" in line.split("|")[1]:
            cell = line.split("|")[1].strip()
            for name, numbers in re.findall(r"([\w/.-]+\.md)(?::([\d, -]+))?", cell):
                found = listed.setdefault(name, set())
                for first, last in re.findall(r"(\d+)(?:-(\d+))?", numbers or ""):
                    found.update(range(int(first), int(last or first) + 1))
    status = git(tree, "diff", "--name-status", "--no-renames", BASE, "--", ROOT)
    for row in status.splitlines():
        kind, path = row.split("\t")
        name = path[len(ROOT) :]
        if kind == "A" or name == "topics.json":
            continue
        if kind == "D":
            old = set(git(tree, "show", f"{BASE}:{path}").splitlines())
            for part in SPLITS[name[len("topics/") : -3]]:
                new_name = f"topics/{part}.md"
                lines = (
                    pathlib.Path(tree, ROOT, new_name)
                    .read_text(encoding="utf-8")
                    .splitlines()
                )
                print(f"== {new_name} (from {name}) listed {sorted(listed.get(new_name, []))}")
                for number, line in enumerate(lines, 1):
                    if line not in old:
                        print(f"  {number}: {line}")
            if name in listed:
                print(f"== STALE row {name} {sorted(listed[name])}")
            continue
        diff = git(tree, "diff", "-U0", BASE, "--", path)
        changed = []
        number = 0
        for line in diff.splitlines():
            head = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
            if head:
                number = int(head.group(1))
                if head.group(2) == "0":
                    changed.append((number, "(lines deleted after this one)"))
                continue
            if number and line.startswith("+"):
                changed.append((number, line[1:]))
                number += 1
        have = listed.get(name, set())
        numbers = {n for n, _ in changed}
        if numbers == have:
            continue
        print(f"== {name} changed {sorted(numbers)} listed {sorted(have)}")
        for n, line in changed:
            mark = " " if n in have else "+"
            print(f" {mark}{n}: {line}")


if __name__ == "__main__":
    main()
