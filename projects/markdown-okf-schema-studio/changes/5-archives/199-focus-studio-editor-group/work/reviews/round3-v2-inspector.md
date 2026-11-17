# Round 3 — v2 re-base onto main 95598afa (Inspector review)

**Verdict: APPROVE**

## Scope

- 198: `origin/change-requests/198-workbench-focus-thief` (31a540b3, base cb1f2adc) vs
  `origin/change-requests/198-workbench-focus-thief-v2` (2428cf7a, base origin/main 95598afa).
- 199: `origin/change-requests/199-focus-studio-editor-group` (128e436e, 3ef2dcdc on old 198) vs
  `origin/change-requests/199-focus-studio-editor-group-v2` (7e72c76f, b2abfb3e, 8af91c67 on 198-v2).
- Method: `git range-diff` per stack, plus a `--numstat` comparison of each stack's net diff against its own base.
  Coder report read: `reports/round3-v2-coder.md`.

## Findings

1. **198-v2 range-diff: only conflict context changed.** In `run.ts` and `stressPlan.ts`, main's `toc`,
   `find-in-preview` and `find-after-click` are kept and `alert-type-pick-probe` is added after them.
   `reload-suite.ts` and `scroll-sync-suite.ts` show only moved hunk context (main's `onSpawn` and
   `runScrollSyncSuite`). The commit makes no other change.
2. **run-tests.ts is correct.** Main's heartbeat watchdog (`heartbeatFileFor`, `resetHeartbeat`, the
   `hangWatchdog` import) is intact. The inline `settings.json` write in `runUntrustedScenario` is replaced by
   `writeTestProfileSettings(userDataDirectory)`. That function writes the same
   `security.workspace.trust.startupPrompt: "never"` (testProfile.ts:88) plus the focus-thief settings, so no
   setting is lost.
3. **199-v2 commit 1 (7e72c76f) range-diff: only conflict changes.** `run.ts` and `stressPlan.ts` keep `toc` and
   `find-in-preview` and drop only the `alert-type-pick-probe` stress entry. On 199-v2 the net `stressPlan.ts`
   diff against main is zero, and the probe's single-scenario entry (`run.ts:119`) stays next to `find-after-click`.
   The `checkboxToggle.test.ts` imports keep `waitForActiveSourceEditor` and also main's `markProgress` and
   `bounded`. Nothing is duplicated (each scenario key appears once).
4. **199-v2 commit 2 (b2abfb3e)** is identical to 3ef2dcdc (`=` in range-diff).
5. **199-v2 commit 3 (8af91c67, new)** is a one-line swap in checkboxToggle setup:
   `bounded("workbench.action.focusFirstEditorGroup", …)` becomes
   `bounded("waitForActiveSourceEditor of tasks.md", waitForActiveSourceEditor(document))`. It follows #193's
   `bounded(label, promise)` style. The helper returns `Promise<void>` with a 10 s timeout. After this commit,
   the only `focusFirstEditorGroup` left under `test/integration` is a doc comment in `windowFocus.ts`.
6. **Nothing from main is lost or duplicated.** The per-file `--numstat` of old-199 vs cb1f2adc and of
   new-199-v2 vs origin/main are identical (27 files) except `checkboxToggle.test.ts` (2/2 → 3/4). That
   difference is fully explained by main's `bounded` setup line and commit 8af91c67.
7. **No locked StRS changed.** The only requirements file in the stack diff is
   `SwRS-MDOKFSTUDIO-REVIEW-054.md` (SwRS, same as the old stack). None of CORE-001, GFM-002, MYST-001, DIAG-001,
   DIAG-006, REVIEW-001/003/012/015, BLOCK-003/025, PALETTE-015, TABLE-001/012 or LAYOUT-001/003 is touched.

No change requested. I did not rerun the gates. The coder reports `just check` exit 0 on both v2 heads.
