# Task

Specification: `03-change-spec.md` with `02-answers.md` (the owner's answers, binding; for CR 288 the IMPORTANT note at the top of the spec overrides the toolbar text below it). Part of a stack of six CRs, bottom to top: 290, 289, 293, 292, 291, 288. This CR is based on `change-requests/289-find-scrolls-wide-table-to-hit`; the stack driver restacks; the stack driver orders, restacks and ships. The PR opens **as a draft** (`gh pr create --draft`) and turns ready on its own (`gh pr ready <n>`) as soon as it is mergeable itself: CI green at its head, review approved, Verifier `VERIFIED` at that head (lifecycle step 10).
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/293`, branch `change-requests/293-table-keyboard-row-add-discoverable`.

Starting test: the QA 271 replay(s) and fixtures the spec names, taken from local commit `87307e8f` with `git checkout 87307e8f -- <paths>`; never push branch `qa/271-table-campaign-replays`. Provisional SwRS IDs, visual fixture numbers and scenario numbers are re-checked against the CRs below in the stack at each rebase (the specs of 288 and of 289/290 both claim fixture 84 and `toolbar-navigation/v41`: the lower CR keeps the number).

Layering (constitution, section 2). No new dependency. Inspector: Opus (blast radius 2).

Tests first (see the spec). Gates as listed in the spec: `just check`; headless visual of the group(s); no real VS Code window locally (CI runs them); a heavy CI run on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`). PR body from `.github/PULL_REQUEST_TEMPLATE.md` per `pull-request.guidelines.md`, with the evidence of step 10.
