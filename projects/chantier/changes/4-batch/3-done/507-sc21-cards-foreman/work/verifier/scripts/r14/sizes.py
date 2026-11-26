"""Verifier: the body's two size tables and role-card sizes, from the committed blobs (LF bytes)."""

import re
import subprocess
import sys
from pathlib import Path

W = "<worktree>"
CR = Path("<CR folder>")


def git(*a):
    return subprocess.run(["git", "-C", W, *a], capture_output=True, text=True, encoding="utf-8")


def size(rev, path):
    r = git("cat-file", "-s", f"{rev}:{path}")
    return int(r.stdout) if r.returncode == 0 else None


body = (CR / "pr-body.md").read_text(encoding="utf-8").split("\n")
old, new = "24111e6d:skills/chantier/references/", "HEAD:skills/chantier/cards-next/"
rows = [
    ("concepts.md", ["concepts.md"], ["concepts.md"]),
    ("pr-template.md", ["pr-template.md"], ["pr-template.md"]),
    ("release-template.md", ["release-template.md"], ["release-template.md"]),
    ("status-layout.md", ["status-layout.md"], ["status-layout.md"]),
    ("titles.md", ["titles.md"], ["topics/titles.md"]),
    ("ticket-summary-example.md", ["ticket-summary-example.md"], ["ticket-summary-example.md"]),
    ("routing.md", ["routing.md"], ["routing.md"]),
    ("init.md", ["init.md"], ["init.md"]),
    ("review-step.md", ["review-step.md"], ["review-step.md"]),
    ("sync-checkout.md", ["sync-checkout.md"], ["sync-checkout.md"]),
    ("forges", ["forges/github.md", "forges/gitlab.md"], ["forges/github.md", "forges/gitlab.md"]),
    ("hosts json", ["hosts/claude-code.json", "hosts/copilot.json"], ["hosts/claude-code.json", "hosts/copilot.json"]),
    ("hosts/claude-code.md", ["hosts/claude-code.md"], ["hosts/claude-code.md"]),
    ("hosts/copilot.md", ["hosts/copilot.md"], ["hosts/copilot.md"]),
    ("floor.md", ["floor.md"], ["floor.md"]),
]
for name, a, b in rows:
    print(f"{name}: old {[size('24111e6d', 'skills/chantier/references/' + p) for p in a]} "
          f"new {[size('HEAD', 'skills/chantier/cards-next/' + p) for p in b]}")
tree = git("ls-tree", "-r", "--name-only", "HEAD", "skills/chantier/cards-next/topics").stdout.split()
host = [size("HEAD", p) for p in tree if re.search(r"/host-[^/]*\.md$", p)]
print("topics/host-*.md: files", len(host), "total", sum(host), "largest", max(host))
for s in ("chantier", "chief-of-staff", "griller", "status"):
    print(f"skill {s}: old {size('24111e6d', f'skills/{s}/SKILL.md')} new {size('HEAD', f'skills/chantier/cards-next/skills/{s}-SKILL.md')}")
for c in ("foreman.md", "chief-of-staff.md", "griller-skill.md", "griller.md", "cr-driver.md", "stack-driver.md",
          "coder.md", "demo-explorer.md", "retro-critic.md", "spec-critic.md", "spec-writer.md", "verifier.md", "release-driver.md"):
    print(f"card {c}: old {size('24111e6d', 'skills/chantier/references/' + c)} new {size('HEAD', 'skills/chantier/cards-next/' + c)}")
print("--- body lines 29-52")
for line in body[28:52]:
    print(line)
