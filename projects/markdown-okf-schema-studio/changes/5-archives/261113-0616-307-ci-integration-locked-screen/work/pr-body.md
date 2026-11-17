## Summary

On macOS, a locked screen keeps the real VS Code window from ever becoming active, so `ci-integration` failed after minutes and `ci-report` and `ci-gallery` then failed from it without naming the cause. `ci-integration` now checks for a locked screen first and stops at once with the cause and the two ways out.

## Deliverables

```text
ci-integration: screen locked, the VS Code window cannot become active; the real VS Code tests did not run.
Unlock the screen and run it again, or prove the branch in CI at once:
  gh workflow run ci.yml --ref <branch> -f heavy=true
To keep the screen from locking during an unattended run, see "App-window tests" in
.agents/guidelines/local-worktree.guidelines.md (caffeinate).
```

Exit code 3 means only "screen locked".

## Changes

- `justfile`: private recipe `_require-unlocked-screen STAGE` (locked when `STUDIO_SCREEN_LOCKED=1` on any OS, or on macOS when `ioreg -n Root -d1` reports `CGSSessionScreenIsLocked = Yes`). It is a dependency of `ci-integration` (so it runs before the campaign `begin` that deletes earlier reports), `ci-stress`, `integration` and `e2e`.
- `preflight` warns early when the screen is locked; when `ci-integration` exits 3 it prints that `ci-report` and `ci-gallery` were skipped because integration did not run, runs neither, and still counts the failure (exit 1). The Windows branch is unchanged.
- Tests in `test/build/test_workflows.py` (override set explicitly, no dependence on the machine's lock state).
- Release guideline step 5 and CONTRIBUTING "How to Release" step 4: dispatch the branch heavy run at once when a locked screen stops local `preflight`.

## Impacts

No visual change. Developer tooling only.

## Blast radius

Grade: 1. Local to the justfile, two documents and tests; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: No behaviour change (developer tooling, no SwRS covers `preflight` or the `ci-*` targets)
- [x] Local gates: `just check` green; `test/build/test_workflows.py` green. Local `just preflight` at de573fea: `ci-static` passed; `ci-visual` (sticky band overlay, CR-306 area) and the real-window scroll-sync step failed, neither touched by this diff; the branch heavy run is the proof.
  Evidence of the new stop (`STUDIO_SCREEN_LOCKED=1 just ci-integration`, exit 3):
  ```text
  ci-integration: screen locked, the VS Code window cannot become active; the real VS Code tests did not run.
  Unlock the screen and run it again, or prove the branch in CI at once:
    gh workflow run ci.yml --ref <branch> -f heavy=true
  To keep the screen from locking during an unattended run, see "App-window tests" in
  .agents/guidelines/local-worktree.guidelines.md (caffeinate).
  error: recipe `_require-unlocked-screen` failed with exit code 3
  ```
- [x] Review
- [x] CI green: heavy run 43321443384 at 450a317 (static, windows, visual, integration, stress, report, checks). An earlier heavy run 43313761803 failed `integration` twice on different real-window steps (checkbox-toggle timeout, myst-blocks toggle) while `stress` passed; the diff has no effect on Linux, so it is judged flaky.
