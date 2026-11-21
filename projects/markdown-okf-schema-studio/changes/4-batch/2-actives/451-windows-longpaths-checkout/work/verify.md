Head: bec8d0d30c5d0a7fa91299d023801ce75b9abc3f

All claims judged at bec8d0d30c5d0a7fa91299d023801ce75b9abc3f (Windows host).

1. Tests pass at head: `pytest test/build/test_workflows.py -q` -> `81 passed in 16.99s`.
2. Fail-before: the head test file copied onto a detached worktree of base be10fe81, `pytest -k long_paths` -> `3 failed, 78 deselected` (`justfile does not contain recipe _git-long-paths`). Worktree removed.
3. `just --dry-run dev` prints the `git config core.longpaths true` script (guarded by `git rev-parse --is-inside-work-tree`) before `fnm install`.
4. Docs: `git grep -nE '^\s*git commit\b.*(\s-s\b|--signoff)' -- '*.md'` prints nothing (exit 1); `CONTRIBUTING.md:632: git commit --amend --no-edit CHANGELOG.md`.
5. core.longpaths named in AGENTS.md:65, local-worktree guideline:22, CONTRIBUTING.md:32 (Windows paragraph).
6. PR #459 description vs `git diff be10fe81 HEAD` (5 files: justfile, AGENTS.md, CONTRIBUTING.md, local-worktree guideline, test_workflows.py): matches, no missing or unmentioned change; renders, no images, no role names beyond CR/batch reference.
7. Real long-path run: judged from the Driver's logs (work/dev*.log, compile-long.log), not repeated, as instructed.

VERIFIED

## Description pass (posted body, judged at bec8d0d30c5d0a7fa91299d023801ce75b9abc3f)

Command: `gh pr view 459 -R gsemet/markdown-okf-schema-studio --json body,headRefOid`; `git diff --stat be10fe81 HEAD` (5 files, 78+/6-); `gh pr checks 459`.
- Summary, Deliverables, Changes match the diff (justfile twins, docs, CONTRIBUTING no -s, 3 tests): true.
- Impacts filled; Blast radius, Test plan filled; Known gaps "None" consistent (no UNVERIFIED claim, no accepted failure).
- Review box: e962787 matches the log note "committed as e962787" (patch unchanged by rebase, carry event).
- CI at bec8d0d: checks, report, static, static-windows, viewer-graph, visual pass (gh pr checks).
- No stale SHA, no STALE mark, no images, no role names outside "Internal references" (CR-451, batch-07).

VERIFIED
