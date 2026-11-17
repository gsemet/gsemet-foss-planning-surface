# T00 implementation — round 2

STATUS: DONE

## Summary
- Round 2 applies the user-approved toggle-locator fix on top of the accepted round-1 header change.
  Every `[data-okf-description-toggle]` locator on the lines listed in task step 2b now reads
  `[data-okf-description-toggle]:visible`, so Playwright strict mode sees one element. Test-only.
- Product source is untouched. The stale header assertion from round 1 is kept as accepted.
- `full` passed on two of three runs with no source change between them. The one failure was a
  timeout in the scroll campaign, which is outside the edited code; classified as flaky (below).
- `visual` has 37 failing scenarios, identical to the baseline recorded in round 1 (0 new). It is
  recorded, not fixed.

## Files changed
- `test/integration/previewEditing.test.ts` — round-1 header
  assertion (kept); toggle locators at lines 98, 506, 507, 510, 518 changed to `:visible`.
- `test/integration/reload-suite.ts` — toggle locators at lines 79
  and 90 (two occurrences on line 90) changed to `:visible`. Line 65 (`.count() === 0`) unchanged.

## Tests written first (failing before the fix)
- Round 1 is the failing run for the locator defect: `test/integration/previewEditing.test.ts`
  (preview-editing test) — failure excerpt: `locator.getAttribute: Error: strict mode violation:
  locator('[data-okf-description-toggle]') resolved to 2 elements` (`logs/T00-impl-full.log`, lines
  915–924). Reproduced in 2 of 2 round-1 runs. No new bug test was written: the defect is in the
  test locators, and the task asks for test-only changes.

## Tests added or changed
- Header assertions in `previewEditing.test.ts` (carried from round 1) — prove the Name/Value
  header and the Description header use the `okf-column-heading` span.
- Toggle locators (`:visible`) in `previewEditing.test.ts` and `reload-suite.ts` — target the one
  toggle that is displayed (`.okf-description-restore` is `display: none` unless collapsed), so the
  strict-mode violation is gone. No assertion logic changed.

## Existing assertions changed
- `test/integration/previewEditing.test.ts:<preview-editing test>` (header) — old:
  `/<thead><tr><th scope="col">Name<\/th><th scope="col">Value<\/th><th scope="col">Description<\/th><\/tr><\/thead>/u`
  → new: `/<thead><tr><th scope="col">Name<\/th><th scope="col"><span class="okf-column-heading">Value/u`
  and `/<th scope="col"><span class="okf-column-heading">Description/u` — required by: the properties
  table intentionally wraps Value/Description in the collapse-toggle span (commit e1b4ad0). Accepted in round 1.
- `test/integration/previewEditing.test.ts:<preview-editing test>` lines 98, 506, 507, 510, 518 —
  old: `[data-okf-description-toggle]` → new: `[data-okf-description-toggle]:visible` — required by:
  the description toggle is rendered twice on purpose (Description heading and `.okf-description-restore`
  in the Value heading); only one is visible at a time.
- `test/integration/reload-suite.ts` lines 79, 90 (×2) — same change, same reason.

## Verification
- `scripts/gate.sh T00-impl-r2 unit types contracts` → PASS (`logs/T00-impl-r2-unit.log`,
  `-types.log`, `-contracts.log`; compile in `-compile.log`)
- `scripts/gate.sh T00-impl-r2 full` → FAIL, first run (`logs/T00-impl-r2-full.log`): scroll campaign
  `locator.inputValue: Timeout 30000ms exceeded … waiting for locator('[data-sphinx-preview-block-editor] textarea')`
  after `PASS scroll E2E: solo-block-anchored`.
- `scripts/gate.sh T00-impl-r2b full` → PASS, exit 0, 150 s (`logs/T00-impl-r2b-full.log`)
- `scripts/gate.sh T00-impl-r2c full` → PASS, exit 0, 150 s (`logs/T00-impl-r2c-full.log`)
- `scripts/gate.sh T00-impl-r2 visual` → PASS vs baseline (0 new failure lines, exit 1 with the 37
  known failures, 138 s) (`logs/T00-impl-r2-visual.log`, screenshots in `logs/visual-T00-impl-r2/`).
  The gate restored `test/visual/screenshots/`.
- `git status --porcelain -- src/markdown-okf-schema-studio` → only the two allowed test files.

## Baseline (for STATE.md)
- VS Code: 1.141.0. Node: v24.21.0 (`fnm exec -- node --version`).
- Durations: compile 2 s · unit 0 s · types 1 s · contracts 1 s (contracts-compile 2 s) ·
  full 150 s (passing runs; a failing run aborted at 65 s) · visual 138 s · trusted: covered by
  `full` (the trusted suite runs inside it) · scroll and reload: run inside `full`, durations not
  split out by the gate · no separate `trusted`, `scroll`, or `reload` levels were run.
- Known failures:
  1. **full (b, flaky, 1 of 3 runs)**: scroll campaign, `waiting for locator('[data-sphinx-preview-block-editor] textarea')`
     timeout after `solo-block-anchored`. The scroll code is unchanged by T00 and the same suite
     passed in the two later runs. Classified as flaky, but the evidence is one failure in three runs.
     Worth watching in later gates.
  2. **visual (c, reproducible, 37 of 95 scenarios, same as round 1)**: check messages
     `sticky heading overlaps the reserved toolbar row` (36), `sticky heading top 0.0px overlaps toolbar
     bottom 50.0px` (5), `rightmost preview button is covered or overlaps the sticky heading text row` (5),
     `table action bar is not aligned with its active cell` (5), and
     `narrow schema headers are ['Name', 'Value◀▶'], expected Name/Value` (1, the same
     toggle-in-header markup as the header change; the visual check in `test/visual/capture.py` is
     stale). Failing scenario names are the `failed:` lines in `logs/T00-impl-r2-visual.log`.
  3. **contracts, types, unit, compile**: none.
- Environment: no environment failures.

## Evidence for reviewers
- Logs: `logs/T00-impl-r2-*.log`, `logs/T00-impl-r2b-full.log`, `logs/T00-impl-r2c-full.log`.
- Visual screenshots of this run: `logs/visual-T00-impl-r2/`.
- Tracked screenshot folder: unchanged (restored by the gate).

## Feedback addressed (rounds 2–3)
- Round-1 STOP reason 1 (toggle strict-mode violation): fixed by the `:visible` locators at the
  exact lines in task step 2b, approved by the user.
- Round-1 STOP reason 2 (gate side effect in `test/visual/screenshots/`): handled by the gate script
  change made by the orchestrator. After this round's visual run the tracked folder is clean.
- Round-1 open point 3 (37 visual failures): recorded as baseline, unchanged, matches the baseline file.

## Open points / STOP reason
- No STOP. The `full` level has one flaky failure in three runs (scroll campaign, unrelated to the
  edited files). The orchestrator decides whether to rerun.
- The visual baseline check `narrow schema headers ... expected Name/Value` is stale against the
  intended toggle-in-header markup. Its fix would be in `test/visual/capture.py`, which is not in
  Allowed files. Not changed; the orchestrator may schedule it.
- VS Code version was read again this round with `code --version` (first line 1.141.0), matching round 1.
