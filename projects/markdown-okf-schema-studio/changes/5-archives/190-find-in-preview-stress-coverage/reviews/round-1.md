# Review round 1 — CR 190 (find in preview in the stress plan)

Inspector: Opus, 2026-10-29. Worktree `markdown-okf-schema-studio-wt-190`, uncommitted diff (7 files, +64/-8).

## Verdict: APPROVE

No blocking finding. Notes below are non-blocking (wording, CI budget to watch, stack merge).

## Checks

1. **Coverage (cream + dark + replace).** `scenarioFindInPreview` is the full former body of
   `run()`: cream find (count, Enter/Shift+Enter, highlights, native widget closed), match case,
   folded section unfold, replace all + one undo (cream); dark find + replace toggle enabled +
   replace field filled. Registered as `find-in-preview` in `STRESS_SCENARIOS_BY_HOST.trusted`
   (test/shared/stressPlan.ts:70-71) and in the stress table (test/integration/realInput/run.ts:54);
   the runtime key-equality assert in `runStress` holds. Replace all runs in cream only (as before);
   dark exercises the replace toggle/field, which is where the CR 169 race showed. Matches the intent.
2. **Waits.** All new waits are `settle(...)` on reported state: bar hidden, `data-sphinx-preview-edit-mode="off"`,
   and the host's `storedEditModeForTests() !== true`. No new fixed sleep, retry, `force:true`,
   raised timeout or weakened assertion. The only `setTimeout` sleeps are in the pre-existing
   `before` (screenshot-only) branch, unchanged. Single-click edit toggle + settle mirrors the existing
   `focusPageWithoutEdit` (no retry loop like harness `setEditMode`), and waits on the host instead of
   the 250 ms sleep of `leaveEditModeOff` — better.
3. **Trusted run behaviour / cleanup / idempotence.**
   - `run()` keeps env semantics (`STUDIO_FIND_PHASE`, `STUDIO_FIND_SHOTS`), browser closed in `finally`.
   - In the full trusted suite the five preceding tests leave edit mode on, so `editModeBefore === true`
     and the toggle-off branch does not run: the only new steps there are Escape + bar-closed settle +
     "source unchanged" assert in dark (findInPreview.test.ts:319-321).
   - Stress: `alert-dropdown` ends through `withDocument` → `leaveEditModeOff`, so find starts with
     edit mode off and restores off (waiting for the host to store it); round N+1 starts as round 1.
   - Viewport: the real-input `run()` set 1400x900 on the same `Page`, so `page.viewportSize()` returns
     it and it is restored (findInPreview.test.ts:110, 334); in the trusted `run()` it is null and the
     browser closes as before.
   - Theme restored to the workspace value, stored choices re-pinned, temp folder `find-e2e-*` is new
     per round and removed, document reverted and closed (undo stack dies with it), preview disposed
     (find query, case option and folds are page-local: `findBar.ts` has no persisted state, the input
     is `select()`ed on open).
4. **Conflicts.** `realWindowGaps.ts` untouched (PR #200 safe). PR #201 also edits
   `realInput/run.ts` (import at line ~32, single-scenario map, sequence) — different hunks from this
   diff (line 10 and the stress table), so it merges cleanly.
5. **Requirements.** Only SwRS TOOLBAR-009/012 verification notes and `tiers/log.md`. No locked StRS
   touched. `okfreq validate`: 1067 requirements, 0 errors; lint/update-coverage: nothing to change.
6. **Gates.** `just check` exit 0 locally (includes the new unit test
   "find in preview ... runs in the trusted window's stress plan" ✔). No real-window/stress run locally.

## Non-blocking findings

1. requirements/tiers/log.md:5-6 — "cream and dark, with replace all": replace all runs in the cream
   pass only; dark covers the replace toggle and field. Suggest "cream and dark, with replace (replace
   all in cream)". Wording only.
2. Stress budget (.github/workflows/ci.yml stress `timeout-minutes: 30`, `ci-stress` REPEAT=20): the
   last green heavy run's stress job took 18-20 min (~55 s per round). Find opens two previews per
   round; expect +5-15 s/round, i.e. +2-5 min. Should still fit, but the Driver should read the
   `PASS stress 1/20 find-in-preview (N ms)` lines and the job duration in the heavy run and report them.
3. test/integration/findInPreview.test.ts:322-327 — the edit-mode restore is in `try`, not `finally`,
   so a failing round leaves edit mode on. Acceptable: a failing scenario aborts the stress run, and the
   trusted run already leaves it on. No change asked.
4. requirements/tiers/log.md top-of-file insert will textually conflict with #198/#154/#155 when
   stacked; trivial resolution for the Foreman.
