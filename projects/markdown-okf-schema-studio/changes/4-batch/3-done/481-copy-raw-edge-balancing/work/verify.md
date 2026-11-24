# Verify CR-481

Head: 07aab079913b7c0bbbb62db9dfdcaea53d75e3d3

All claims judged at 07aab07 (worktree HEAD, pushed, PR 499 headRefOid identical).

1. Core, registry and page unit tests (E2, E5). Command: `npm run compile` then
   `node scripts/node-test.mjs unit "out/test/{core/mapping/rawCopy*,core/configuration/*,page/runtimeRawCopy}.test.js"`.
   Output: `tests 101, pass 101, fail 0` (includes the nesting grid, the unplaced-edge snap off/on, the
   boot-setting on/off/absent page test). Log: work/gates/verifier-unit.log.
2. Browser scenarios (E3). Command: `uv run --no-sync --group docs python test/visual/capture.py --scenario block-editing/v55-raw-copy-light-900 --scenario block-editing/v56-raw-copy-balanced-light-900 --workers 1`.
   Output: `passed: block-editing/v55-raw-copy-light-900`, `passed: block-editing/v56-raw-copy-balanced-light-900`.
   Log: work/gates/verifier-visual.log.
3. Settings schema and markers. `just check-settings` -> `check-settings: passed (21 settings)`;
   `just check-markers` -> `check-markers: 10 companion file(s), 453 in-force SwRS marked`.
4. Docs and changelog: grep shows `balanceEdges` in CHANGELOG.md line 7 and docs/user/settings.md line 23.
5. CI at 07aab07 (gh): run 45424277207 (pull_request) success; heavy run 45424510001 (workflow_dispatch)
   success, jobs integration, stress, visual, static, static-windows, viewer-graph, report, gallery all success
   (E4 real VS Code step covered there).
6. PR description (gh pr view 499): sections render, Summary/Deliverables/Changes match the diff (setting,
   four modules, docs, SwRS 278-286), no images, Known gaps lists the unrun local VS Code step (now
   covered by the green heavy run). Clean.
7. Review box: `Review` unchecked in the PR test plan; not claimed approved, nothing to judge.

Not captured: before/after screenshots (behaviour is clipboard text, proved by tests 1 and 2).

Description pass (judged at 07aab07, `gh pr view 499`): Summary, Deliverables and Changes match
`git diff origin/main...HEAD --stat` (53 files; setting, four modules, listMarker move, docs, SwRS 278-286).
FAIL: the Test plan (outside Internal references) reads "Review at 07aab07 (inspector pass at b824913, ...)":
a role name as the doer of the work, outside Internal references (pr-template, rules, item 3). The product has
no inspector role. Fix: drop "inspector" ("Review at 07aab07 (pass at b824913, then docs-only change)").

NOT VERIFIED

Description pass 2 (judged at 07aab079913b7c0bbbb62db9dfdcaea53d75e3d3, `gh pr view 499`): the Review line
now reads "Review at 07aab07 (review pass at b824913, then a docs-only change)": no role name. Log shows
"r3 approved at b824913, committed as 07aab07 (docs only)": the Review box is proved. No role name elsewhere.
Summary, Deliverables, Changes match the diff (53 files: setting in package.json default false, four modules,
listMarker move, docs, glossary, changelog with PR #499, SwRS 278-286 + 272/273, StRS-027). Fold and
blank lines correct, nothing after </details>, no images, Known gaps present. Clean.

VERIFIED
