# T00 — Baseline measurements and the stale header assertion

| Field | Value |
| --- | --- |
| Fixes | Pre-existing red test (not a UX finding) |
| Depends on | — |
| Gate | `unit types contracts full visual` |
| Risk | Low |
| Commit message | `test(vscode): match the properties table header markup` |

## Goal

Every later review compares its gate results with this baseline, so the baseline must be green, or
its remaining failures must be documented precisely.

## Context

- HEAD is expected to be `1a5f8d8` or a descendant. The checkbox feature is committed.
- `test/integration/previewEditing.test.ts` asserts the old properties-table header with this regex:

  ```
  /<thead><tr><th scope="col">Name<\/th><th scope="col">Value<\/th><th scope="col">Description<\/th><\/tr><\/thead>/u
  ```

  Since commit `e1b4ad0`, `renderPropertiesTable` (`src/frontmatter/propertiesTable.ts`) wraps the
  Value and Description headings in `<span class="okf-column-heading">…` with a collapse toggle
  button. The product markup is intended; the assertion is stale and makes the trusted suite exit 1.
- **Added after round 1 (approved by the user).** The same commit renders the description toggle
  **twice** on purpose: once in the Description heading (collapses the column) and once inside
  `.okf-description-restore` in the Value heading (expands it again). The unit test
  `test/frontmatter/propertiesTable.test.ts` asserts exactly 2 toggles. CSS shows exactly one of
  them at a time (`previewStyles.ts`: `.okf-description-restore` is `display: none` unless
  `html[data-okf-descriptions-collapsed="true"]`, which also hides the Description column). The
  integration tests still use the bare locator `[data-okf-description-toggle]`, which Playwright's
  strict mode rejects (`resolved to 2 elements`). The fix is test-only: target the visible toggle.
- Round 1 is in `PLAN/reports/T00-implementation-r1.md`. Its header assertion change is already in
  the working tree and is accepted: keep it.

## Allowed files

- `test/integration/previewEditing.test.ts` (only the stale assertion and the toggle locators)
- `test/integration/reload-suite.ts` (only the toggle locators)

## Steps

1. Pre-flight: `git status --porcelain -- src/markdown-okf-schema-studio` must be empty. If not,
   STOP; the orchestrator asks the user.
2. Replace the stale assertion. Find it with `rg -n 'scope="col">Name' test/integration/previewEditing.test.ts`.
   Use two assertions that check the intended structure without depending on the toggle button's
   inner markup:
   - `/<thead><tr><th scope="col">Name<\/th><th scope="col"><span class="okf-column-heading">Value/u`
   - `/<th scope="col"><span class="okf-column-heading">Description/u`
2b. Replace the ambiguous toggle locator `"[data-okf-description-toggle]"` with
   `"[data-okf-description-toggle]:visible"` at exactly these places (line numbers at base
   `1a5f8d8`; find them with `rg -n 'data-okf-description-toggle' test/integration`):
   - `previewEditing.test.ts`: line 98 (`const toggle = …`), lines 506, 507, 510 and 518;
   - `reload-suite.ts`: lines 79 and 90 (line 90 has two occurrences).

   Leave `reload-suite.ts` line 65 unchanged: it uses `.count() === 0` to find the preview frame,
   which works with two matches. Do not change anything else in these files.
3. Run `PLAN/scripts/gate.sh T00-impl unit types contracts full visual`. It takes a long time; run it
   in the foreground, with a timeout of 600000 ms per call.
   - If one call cannot cover everything, run one level per call.
   - Record each level's duration from the gate output.
   - The `visual` level now copies its screenshots to `PLAN/logs/visual-<label>/`, restores the
     tracked `test/visual/screenshots/` folder by itself, and compares the failures with
     `PLAN/logs/visual-baseline-failures.txt` (recorded from round 1). It fails only on new
     failures. Do not edit or regenerate the baseline file.
   - After the gate, `git status --porcelain -- src/markdown-okf-schema-studio` must list only the
     two allowed test files.
4. For every failing level, read the log and classify each failure:
   - (a) environment unavailable, for example no Python docs env or Playwright browsers missing;
   - (b) flaky: it fails, then passes on rerun with no change;
   - (c) a real, reproducible failure.

   Do not fix (c) failures, except the stale assertion and the toggle locators above. List them
   precisely: test name and the first assertion message. A remaining (c) failure in another suite
   is **not** a STOP: document it and report `STATUS: DONE`; the orchestrator decides.
5. Report the VS Code version (`"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" --version`,
   first line; round 1 found 1.141.0) and the Node version (`cd src/markdown-okf-schema-studio && fnm exec -- node --version`).

## Expected changes to existing tests

- The one assertion above, replaced by the two assertions above.
- The toggle locators listed in step 2b, from `[data-okf-description-toggle]` to
  `[data-okf-description-toggle]:visible`. No other change to these tests.

## Must not change

- Any product source file.

## Done when

- `trusted` passes, or fails only for documented reasons other than the stale header.
- The report contains a "Baseline" section the orchestrator can copy into the top of `STATE.md`:
  versions, durations per level, and known failures with classification.
