"""Read-only: topic files not in fe7fbf0f, and which of its topic files share their words."""

import difflib
import subprocess
from pathlib import Path

TREE = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
ROOT = "skills/chantier/cards-next/"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", TREE, *args], capture_output=True, check=True).stdout.decode("utf-8")


def tree(commit: str) -> set[str]:
    return {n[len(ROOT) :] for n in git("ls-tree", "-r", "--name-only", commit, "--", ROOT + "topics").split()}


old = tree("fe7fbf0f")
head = tree("03f973e4")
texts = {n: git("show", f"fe7fbf0f:{ROOT}{n}").split() for n in old}
present = sorted(f"topics/{p.name}" for p in Path(TREE, ROOT, "topics").glob("*.md"))
for name in present:
    if name in old:
        continue
    words = Path(TREE, ROOT, name).read_text(encoding="utf-8").split()
    shared = []
    for other, was in texts.items():
        blocks = difflib.SequenceMatcher(None, was, words, autojunk=False).get_matching_blocks()
        same = sum(b.size for b in blocks if b.size >= int(__import__("os").environ.get("BLOCK", "8")))
        if same >= int(__import__("os").environ.get("SAME", "20")):
            shared.append((round(100 * same / len(words)), other))
    shared.sort(reverse=True)
    print(f"{name}\t{'in 03f973e4' if name in head else 'uncommitted'}\t{shared[:4]}")
