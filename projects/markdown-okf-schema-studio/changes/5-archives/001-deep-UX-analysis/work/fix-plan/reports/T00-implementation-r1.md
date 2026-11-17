# T00 implementation — round 1

STATUS: STOP

## Summary
- Replaced the stale properties-table header assertion in `test/integration/previewEditing.test.ts`
  with the two structural assertions from the task. The stale assertion is gone: the suite now
  gets past it.
- The suite then fails on a second, older defect in the same test, which the task does not cover:
  `locator('[data-okf-description-toggle]')` resolves to 2 elements. The product renders the
  description toggle in both the Value and the Description header. Reproduced in 2 of 2 full runs.
  STOP per conventions §9.2; no fix was attempted.
- The `visual` gate rewrote 144 tracked files and created 14 untracked files under
  `test/visual/screenshots/`. This is a side effect of running the
  gate, outside Allowed files. I did not revert it (checkout and reset are forbidden). The
  orchestrator must decide how to handle it before committing.
- The visual gate also has 37 failing checks (classified below). The task's Done-when does not
  cover them. Recorded as a baseline, not fixed.

## Files changed
- `test/integration/previewEditing.test.ts` — the one stale
  assertion (`<thead>…Description<\/th>…`) replaced by the two assertions listed in the task.
  Diff is 6 lines (+4 / −2 incl. the wrapping).
- Side effect, NOT intended, outside Allowed files:
  `test/visual/screenshots/*` — 144 modified (`.png`, `.txt`,
  `INDEX.md`, `run-manifest.json`), 14 new untracked (`edit-list-narrow.*`,
  `frontmatter-scroll-feedback.*`, `preview-sticky-headings-*.*`). Produced by
  `gate.sh T00-impl visual` (`test/visual/capture.py`), run twice. Run `git status --porcelain --
  test/visual/screenshots` to see the full list.

## Tests written first (failing before the fix)
- Not applicable as a bug test. The task's fix is a stale-assertion replacement, and I did not run
  the trusted suite before editing. The pre-existing failure is the stale header regex, as the task
  describes. Note: the new assertions pass in the full run (see the next failure below).

## Tests added or changed
- `previewEditing.test.ts` (preview-editing integration test, inside the test that reads
  `getActivePreviewForTests()?.html`) — the new `Value` assertion proves the Name/Value header uses
  the `okf-column-heading` span; the new `Description` assertion proves the Description header uses
  the same span.

## Existing assertions changed
- `test/integration/previewEditing.test.ts:<preview-editing test>` — old:
  `/<thead><tr><th scope="col">Name<\/th><th scope="col">Value<\/th><th scope="col">Description<\/th><\/tr><\/thead>/u`
  → new: `/<thead><tr><th scope="col">Name<\/th><th scope="col"><span class="okf-column-heading">Value/u`
  and `/<th scope="col"><span class="okf-column-heading">Description/u` — required by: the
  product's properties-table header intentionally wraps Value/Description in the collapse-toggle
  span (`src/frontmatter/propertiesTable.ts`, commit e1b4ad0).

## Verification
- `gate.sh T00-impl unit` → PASS (compile 1s, unit 1s) — `logs/T00-impl-unit.log`
- `gate.sh T00-impl types` → PASS (1s) — `logs/T00-impl-types.log`
- `gate.sh T00-impl contracts` → PASS (contracts 1s, 0 failures) — `logs/T00-impl-contracts.log`
- `gate.sh T00-impl full` → FAIL (122s) — `logs/T00-impl-full.log`; same failure on rerun
  (`logs/T00-impl-rerun-full.log`, 121s)
- `gate.sh T00-impl visual` → FAIL (138s) — `logs/T00-impl-visual.log`; rerun
  (`logs/T00-impl-rerun-visual.log`, 138s) gives an identical result list
  (37 failed / 58 passed, same check messages)
- `gate.sh T00-impl trusted` was not run separately. `full` runs the same integration suite, and
  the trusted suite aborts at the failing preview-editing test. The trusted suite does not pass.

## Baseline (for STATE.md)

- VS Code: 1.141.0 (commit 2a59476c9bfcb90b3ddc372c36762471b7dfad1c; from
  `Code.app/Contents/Resources/app/bin/code --version` and the test host log). The `Code` binary
  itself printed nothing for `--version`.
- Node: v24.21.0 (`fnm exec -- node --version`)
- Gate durations: compile/unit 1 s · types 1 s · contracts 1 s · trusted/full 122 s (aborted at
  preview-editing) · visual 138 s · scroll, reload: not run (the full run stops at the
  preview-editing suite before later suites are reached).
- Known baseline failures:
  1. **full / trusted (c, reproducible, 2/2 runs)**: preview-editing integration test:
     `locator.getAttribute: Error: strict mode violation: locator('[data-okf-description-toggle]')
     resolved to 2 elements` (Value and Description headers both render the toggle). Suites before
     it passed (block keyboard E2E, 12 scroll E2E, 4 checkbox screenshots). Later suites were not
     reached. Needs a decision: the test locator should target a single toggle, or the product
     should render one. Not in T00's Expected changes.
  2. **visual (c, reproducible, 2/2 runs)**: 37 failing scenarios of 95. Check messages seen:
     `sticky heading overlaps the reserved toolbar row` (many scenarios, `sticky-1/2/3`),
     `table action bar is not aligned with its active cell` (08-okf-schema, sticky-3),
     `rightmost preview button is covered or overlaps the sticky heading text row` (05-long-chapter),
     `narrow schema headers are ['Name', 'Value◀▶'], expected Name/Value` (08-okf-schema-dark
     sticky-3). The last one is the same toggle-in-header markup as failure 1. Failing scenario
     names are the `failed:` lines in `logs/T00-impl-visual.log`.
  3. **contracts**: none. **types, unit, compile**: none.
- Flaky: none observed. Both reruns of `full` and `visual` gave the same results.
- Environment: no environment failures (Python docs env, Playwright, fnm all ran).

## Evidence for reviewers
- Logs: `logs/T00-impl-*.log`, `logs/T00-impl-rerun-*.log` (paths above).
- Visual artifacts that changed: see the side-effect list above.

## Feedback addressed (rounds 2–3)
- n/a (round 1).

## Open points / STOP reason
1. **STOP — existing test failure not covered by Expected changes (conventions §9.2).**
   After the stale header is fixed, `previewEditing.test.ts` fails on the strict-mode locator
   `[data-okf-description-toggle]` (two matches). The task's Done-when says `trusted` must pass or
   fail only for documented reasons other than the stale header. This reason is documented, but
   fixing it means changing a second assertion or the product markup. Both are outside T00.
2. **STOP — gate side effect outside Allowed files.** `gate.sh … visual` writes 144 modified and 14
   new files into `test/visual/screenshots/`, including `run-manifest.json` and `INDEX.md`. These
   are generated, not intended edits. They must be reverted or excluded before any commit. I did not
   revert them (no checkout or reset allowed). The orchestrator should decide, and may want
   `visual` to write elsewhere in future gate runs.
3. Visual baseline has 37 failing checks, several in sticky and table-bar behaviour (UX-14 / UX-34
   area). They are pre-existing: product source is unchanged by this task. Recorded only.
4. Left untouched: pre-existing modified files (`.agents/thinking/...`, `book/chapters/05,08,09`)
   that were already dirty at the start of the session.
5. Logs for this round are in `logs/` of the fix-plan folder. No commits, no staging.
