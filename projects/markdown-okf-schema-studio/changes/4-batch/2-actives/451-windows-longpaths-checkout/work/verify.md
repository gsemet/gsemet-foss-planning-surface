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
