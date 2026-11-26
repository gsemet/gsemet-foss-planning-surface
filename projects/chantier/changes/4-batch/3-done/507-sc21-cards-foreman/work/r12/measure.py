"""Read-only: the byte and file counts that part3-proofs.md and pr-body.md state."""

import json
import re
import subprocess
from pathlib import Path

TREE = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
ROOT = "skills/chantier/cards-next/"
CR = Path(__file__).resolve().parents[2]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", TREE, *args], capture_output=True, check=True).stdout.decode("utf-8")


def tree(commit: str) -> set[str]:
    return {n[len(ROOT) :] for n in git("ls-tree", "-r", "--name-only", commit, "--", ROOT).split()}


base = Path(TREE, ROOT)
now = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
size = {n: len((base / n).read_bytes().replace(b"\r\n", b"\n")) for n in now}
topics = sorted(n for n in now if n.startswith("topics/") and n.endswith(".md"))
host = [n for n in topics if n.startswith("topics/host-")]
others = [n for n in topics if n not in host]
for label, names in (("host topics", host), ("other topics", others)):
    top = max(names, key=size.get)
    print(label, len(names), "files", sum(size[n] for n in names), "largest", size[top], top,
          "over 1500:", sum(size[n] > 1500 for n in names))
for commit in ("bf4e4c42", "03f973e4"):
    was = {n for n in tree(commit) if n.startswith("topics/")}
    new = sorted(set(topics) - was)
    print(f"topics not in {commit}: {len(new)}; gone: {len(was - set(topics))}; "
          f"largest new {max(size[n] for n in new)}; new over 1500: {[n for n in new if size[n] > 1500]}")
print("topics.json", size["topics.json"])
print(".md and .json files under cards-next:", sum(n.endswith((".md", ".json")) for n in now))
names = set(json.loads((base / "topics.json").read_text(encoding="utf-8"))["topics"])
body = (CR / "pr-body.md").read_text(encoding="utf-8")
listed = body.split("- All topic names: ", 1)[1].split("\n\n", 1)[0]
listed = {n for n in re.split(r"[,.\s]+", listed) if n}
print("topic names", len(names), "not in the body's list:", sorted(names - listed), "listed, unknown:", sorted(listed - names))
over = dict((m.group(1), int(m.group(2).replace(",", ""))) for m in re.finditer(
    r"([a-z][a-z-]+)\s+(\d,\d{3})", body.split("- 24 topics over 1,500 bytes", 1)[1].split("\n- ", 1)[0]))
actual = {n[7:-3]: size[n] for n in topics if size[n] > 1500}
print("body's over-1,500 list differs:", sorted(set(over.items()) ^ set(actual.items())))
for name in ("foreman.md", "chief-of-staff.md", "griller-skill.md", "griller.md", "cr-driver.md", "stack-driver.md",
             "release-driver.md", "coder.md", "demo-explorer.md", "retro-critic.md", "spec-critic.md",
             "spec-writer.md", "verifier.md", "concepts.md", "pr-template.md", "release-template.md",
             "status-layout.md", "topics/titles.md", "ticket-summary-example.md", "routing.md", "init.md",
             "review-step.md", "sync-checkout.md", "forges/github.md", "forges/gitlab.md", "hosts/claude-code.md",
             "floor.md"):
    print(name, size[name], end="; ")
print()
for n in ("merge-gaps-p1", "merge-gaps-p2", "merge-stack-ready-p1", "merge-stack-ready-p2", "merge-words-p2"):
    print(n, size[f"topics/{n}.md"], end="; ")
print()
