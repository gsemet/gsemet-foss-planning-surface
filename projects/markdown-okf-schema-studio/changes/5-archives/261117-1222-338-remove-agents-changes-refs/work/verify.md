# Verify CR-338

Head: f6482d008d63b769531c958519d389b3e1fbbd24

All claims judged at f6482d00 (PR 408, draft). CI green not rerun, per brief.

1. Leftover references. `git grep -n '\.agents/changes\|3-requests\|4-archives\|5-trash\|generate_orchestrator\|just orchestrator'` output:
   `.agents/guidelines/change-requests-lifecycle.guidelines.md:54:The old lifecycle ... (the `3-requests/` PRD folders ...` and `.gitignore:14:.agents/changes/`. Only the two intentional lines. OK.
2. justfile parses: `just --list` lists all recipes, no `orchestrator`; `release-tests` no longer names test_generate_orchestrator.py. OK.
3. `uv run --no-project --with pytest pytest test/build/test_guideline_isolation.py -q` -> `9 passed in 0.06s`. OK.
4. QA scripts: `python -m py_compile` on coverage-map.py, fmt-probe.py, new-features.py -> compiled; `new-features.py --help` prints usage. coverage-map.py: with QA_CHANGES_ROOT=X:/override `changes_root()` -> X:\override; unset -> `<REPO.parent>/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes` (from the worktree this is the sibling of the worktree folder, a non-existing path, so "no campaign found ... set QA_CHANGES_ROOT" is printed; the docstring states a worktree needs the variable). Archive glob is `5-archives`. Behaves as documented. OK.
5. Stage names: the guideline lists `1-inbox`, `2-backlog/P1..P4`, `3-ready`, `4-batch/1-pending|2-actives|3-done`, `5-archives`, `6-trash`; the planning folder `changes/` holds 1-inbox, 2-backlog/P1..P4, 3-ready, 4-batch/{1-pending,2-actives,3-done}, 5-archives, 6-trash. Match. OK.
6. Description: `gh pr view 408` body equals work/pr-body.md (trailing newline only). Summary, Deliverables and Changes match the diff (guideline rewrite; pull-request, owner-review, short-demo guidelines, AGENTS.md, QA skill SKILL/charters/harness-pitfalls/scripts, two test comments in captureRegistry.ts and e2eGroups.ts; orchestrator recipe, generator and its test removed; .gitignore kept). The two diff items not named one by one (charters.md, harness-pitfalls.md) fall under "the exploratory QA skill (docs...)". Unchecked boxes are honest (Review, CI). Local `just ci-static` failure is unrelated (diagnosis.md) and the body does not claim it passed. OK.

Evidence pairs: none captured; the change is documentation and tooling with no UI.

VERIFIED

## Description pass at 884949f433e3b793e9e73f7fec636ab54e8c6a07

Head: 884949f433e3b793e9e73f7fec636ab54e8c6a07

- Patch unchanged: `git range-diff origin/main f6482d00 HEAD` prints `1: f6482d00 = 1: 884949f4`. The f6482d0 verdict is carried (clean rebase).
- Gate: gates/20261117-115826.log first line names CR-338 and head 884949f4...; driver log: `gate result=pass head=884949f4... just ci-static`.
- CI: `gh pr checks 408`: static, static-windows, visual, report, checks pass; others skipping.
- Review: log note `r2 approved at 16105e0f, committed as 0a60fd3d`; the box cites 0a60fd3d (same patch, rebased): proven.
- Body vs diff (`git diff origin/main...HEAD --stat`, 15 files): guideline rewrite, guidelines, AGENTS.md, QA skill and scripts, two test comments, justfile recipe, generate_orchestrator.py and its test removed; `.gitignore` line 14 `.agents/changes/` kept; `QA_CHANGES_ROOT` override present in coverage-map.py:66. Matches.
- Template sections all present, ids only under Internal references, no images, Known gaps not needed (no UNVERIFIED claim, no STALE).

VERIFIED
