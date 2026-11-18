# Verify CR-361

Head: ea3de29cb6b92a4a09bf2b7065106e3d68e664b1

Base judged against: 5717626d (merge-base of the head; origin/main has since moved, the CR's patch is 2 files).

1. New test fails on base, passes at head (judged at ea3de29).
   - Head: `uv run --no-sync pytest -q skills/chantier/scripts/cli/tests/test_summary_lint.py` (worktree) -> `2 passed in 8.53s`.
   - Base: detached worktree at 5717626d + the test file, `PYTHONPATH=<base>/skills/chantier/scripts/cli/src` (import confirmed to resolve to the base) -> `2 failed in 2.08s` (both cases [repo] and [surface], AssertionError on the `projects/`/`.agents/` prefix).
2. Real flow, in-project mode, scratch repo (git init), CLI from the worktree, at ea3de29: `file "Fix login"`, `summary lint` -> exit 2, line `1-inbox/fix-login: no summary -> summary set 1-inbox/fix-login --title ...`; `summary lint 1-inbox/fix-login` -> reads it, same gap; `summary set 1-inbox/fix-login --title T --summary S` -> exit 0; `summary lint` -> `no gap (1 CRs)` exit 0.
3. Real flow, external mode, scratch surface `surf/projects/demo` with `--project`, at ea3de29: same line `1-inbox/fix-login: ...`; `summary lint <path>` reads it; `summary set <path>` exit 0 (`summary set projects/demo/changes/1-inbox/fix-login`, its own output unchanged); `summary lint` -> `no gap (1 CRs)` exit 0.
4. Diff (`git diff origin/main...HEAD`): only `commands/summary.py` (`shown` -> `repo.rel`) and the new `tests/test_summary_lint.py`; `summary set` untouched. The PR body (work/pr-body.md) Summary, Deliverables, Changes and Known gaps ("None") match it; no images, no role names beyond the internal reference.
5. Review box `approved at ea3de29`: `chantier log CR-361` has `r1 approved at 5717626d, committed as ea3de29`. Proved.
6. Gate: CI green at the head (per prompt). `just scenario` long gate: the ship event notes none passed locally; not claimed here.

Scratch folders and the base worktree removed.

VERIFIED
