# Verify CR-472

Head: 024003d50d6072895d28b88210410a901145ae73

All claims judged at 024003d.

- Script behaviour, recipe, ci-static first step, `_merge-check-base`, `fetch-depth: 0` in static and static-windows, guideline section, AGENTS.md and CONTRIBUTING.md lines: `git diff origin/main...HEAD` read; matches spec sections 1-4.
- Linear branch passes: `just check-no-merge-commits` -> `check-no-merge-commits: passed (1 commits since origin/main, no merge commit)`, exit 0.
- Merge branch fails, rebase fixes (scratch repo in TEMP, bare origin + clone, `git merge --no-ff origin/main`, shipped justfile): output `7249f58 Merge origin/main`, reason line, `git fetch origin && git rebase origin/main && git push --force-with-lease`, `check-no-merge-commits: FAILED`, exit=1. After `git fetch origin && git rebase origin/main`: `passed (1 commits since origin/main, no merge commit)`, exit=0.
- Tests: `pytest test/build/test_no_merge_commits.py` -> 12 passed; with `test_workflows.py` -> 93 passed (matches PR body). Test file is in `release-tests`.
- CI at head: `gh run view 45143134552 --log` shows `static` and `static-windows` both print `check-no-merge-commits: passed (1 commits since origin/main, no merge commit)`; checks static, static-windows, visual, viewer-graph, report, checks SUCCESS.
- PR description: body read via `gh pr view 488`; sections, mermaid and fold render-clean; Changes match the 7-file diff; no image; Known gaps present. Review box "approved at 024003d" is backed by the Driver notes: approved at abe5e15, committed as abce636, rebased clean with patch unchanged to 024003d (carried).
- Guideline: forge-neutral, GitHub button only as example, no process role.
