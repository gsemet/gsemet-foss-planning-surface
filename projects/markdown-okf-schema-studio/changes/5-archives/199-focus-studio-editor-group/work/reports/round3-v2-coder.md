# Round 3 — v2 re-base onto main 95598afa (Coder report)

## Branches (pushed, new, plain pushes)

- `change-requests/198-workbench-focus-thief-v2` — head `2428cf7a6bdc0f39a328707cf4d1811373b8f5f8`
  - 2428cf7a test: dump the workbench focus on real-window failures and quiet the test profile (from 31a540b3)
- `change-requests/199-focus-studio-editor-group-v2` — head `8af91c6725a97a4aea0d848c1684fd028dea3046` (on top of 198-v2)
  - 7e72c76f test: fix the slash-menu undo race and read the focus dump before cleanup (from 128e436e)
  - b2abfb3e fix(review): replacing the comments file no longer deletes it first (from 3ef2dcdc, clean)
  - 8af91c67 test: wait for the active source editor in the checkbox toggle setup (new)

`git cherry` showed 31a540b3 as the only commit of the old 198 branch not in main (no patch-equivalent
skips). Old local branches untouched. No -x, no force push, no PR opened.

## Conflicts and resolutions (all test harness, no product logic)

198-v2 (cherry-pick of 31a540b3):
- `test/integration/realInput/run.ts`: STRESS_SCENARIOS kept main's `toc` + `find-in-preview` and added
  `alert-type-pick-probe`; the single-scenario map kept `find-after-click` and added `alert-type-pick-probe`.
- `test/shared/stressPlan.ts`: kept `toc`, `find-in-preview`, added `alert-type-pick-probe`.
- `test/integration/run-tests.ts` (not announced): main's hang watchdog (`heartbeatFileFor`/`resetHeartbeat`)
  kept; main's inline `settings.json` write (trust prompt only) replaced by `writeTestProfileSettings(...)`,
  which writes the same `security.workspace.trust.startupPrompt: "never"` plus the focus-thief settings.

199-v2 (cherry-pick of 128e436e):
- `run.ts` / `stressPlan.ts`: kept `toc` and `find-in-preview`, dropped the ALERT-PICK-PROBE stress entry;
  the probe's single-scenario entry and its one integration run stay.
- `test/integration/checkboxToggle.test.ts` imports: kept `waitForActiveSourceEditor` in the windowFocus import
  plus main's `markProgress` and `bounded` imports.

New commit 8af91c67: checkboxToggle setup `bounded("workbench.action.focusFirstEditorGroup", ...)` replaced by
`bounded("waitForActiveSourceEditor of tasks.md", waitForActiveSourceEditor(document))`.
Remaining `focusFirstEditorGroup`: src/host-vscode/groupFocus.ts (product), test/host-vscode/groupFocus.test.ts,
and a doc comment in test/integration/windowFocus.ts. No harness call left.

## Gates

- `just check` 198-v2: exit 0 — node tests 3246/3246 pass, pytest 137 passed, okfreq validate 1068 reqs 0 errors,
  lint 0 indexes would change, update-coverage 0 files would change.
- `just check` 199-v2: exit 0 — node tests 3254/3254 pass, pytest 137 passed, same okfreq results.
- No `requirements-update` needed; no locked StRS changed. `npm ci`/`uv sync` not rerun (deps present; lockfile
  diff in main is only the version bump).
- Logs: /private/tmp/claude-502/cr199-driver/v2-198-check.log, /private/tmp/claude-502/cr199-driver/v2-199-check.log
