# 056-refactor-host-neutral-core — steps S1..S8

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-056 (branch
`changes-requests/056-refactor-host-neutral-core` from origin/main). Work ONLY there. Read
`00-request.md` (decisions = the spec), `01-analysis.md`, `02-multi-host.md` and `rules.md`.

## Per step

One coder pass per round on the current step only (`S<k>`), then a reviewer on the round diff.
APPROVE → the driver commits the step (one commit, Conventional Commits, `refactor(...)` or
`test(...)` for S1, `build(...)` if only tooling), pushes, updates STATE.md, starts S<k+1>.
FIX-REQUIRED → next round of the same step (max 3). A step still failing after 3 rounds: stop and
report to the orchestrator (do not skip to the next step).

## Gates per step

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual` (baselines unchanged); real VS
Code `npm run test:integration` under the lock (rules.md) after S2, S4, S5 and the last step.

## Docs

README / CONTRIBUTING architecture section (new folder layout, boundaries, ratchet, how to add a
message, a palette action, a directive, a setting). CHANGELOG: one Unreleased bullet only if a
contributor-visible rule changes (no user-visible change expected).

## Reports

reports/S<k>-r<round>.md (coder), reviews/S<k>-r<round>.md (reviewer), in
/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/056-refactor-host-neutral-core/
