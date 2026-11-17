# T03 implementation — round 2

STATUS: DONE

## Summary
Fixed the review's MAJOR finding 1: `identifier-split` no longer compares tops across different text
nodes. A cell is split only when one of its own text nodes has client rects on different lines, so
`type(enum)`, `Description◀▶` and `namesummary` pass. Also fixed MINOR 2 (nested blocks counted the
same covered text node twice; now collected into one `Set`) and MINOR 3 (a failing geometry script no
longer discards the final frame in `capture.py` or fails a real-input capture before the screenshot;
it is recorded as `not run`, and the harness rethrows only when `required` is non-empty). NIT 4 is
done: the header comment of `geometry-checks.js` now says that a non-empty `overlays` or
`ignoreWithin` replaces the defaults. No scenario became required.

## Files changed
- `test/shared/geometry-checks.js` — `identifier-split` judged per text node; `overlay-covers-text` dedupes text nodes; header comment on options.
- `test/webview/geometryChecks.test.ts` — four new tests (three identifier-split, one overlay dedupe); fake DOM helpers.
- `test/visual/capture.py` — geometry `page.evaluate` wrapped in try/except; `None` on error; failure only for scenarios that list a check.
- `test/integration/realInput/harness.ts` — geometry evaluate wrapped in try/catch; writes `- not run: <message>`; rethrows only when `checks.required` is non-empty.

## Tests written first (failing before the fix)
- `identifier-split passes when a cell's text nodes share one line at different sizes` — `1 split identifier(s): type(enum)` / `false !== true`
- `identifier-split ignores list items on separate lines` — fails on the same cross-node comparison (`namesummary`).
- `overlay-covers-text counts a text node once when nested blocks both contain it` — `The input did not match the regular expression /^1 covered text excerpt/u. Input: '2 covered text excerpt(s): "covered", "covered"'`
- `identifier-split reports a text node wrapped over two lines` passed before the fix, as expected: a real wrap is still reported. It guards the fix.

Red state, before the checker fix (`logs/T03-impl-r2-unit.log` at that point): 361 tests, 327 pass,
3 fail (the two identifier-split tests and the overlay dedupe test). The first run of the new file
without `nodeType` on the fake elements showed the dedupe test passing for the wrong reason; the fake
was corrected before the red run that is recorded here.

## Tests added or changed
- `geometry checks define one function that reports the four check ids` — unchanged from round 1.
- `without any DOM content every geometry check is not applicable and passes` — unchanged from round 1.
- `identifier-split passes when a cell's text nodes share one line at different sizes` — `type(enum)` with two nodes on one line passes.
- `identifier-split ignores list items on separate lines` — `name` over `summary` in one cell passes.
- `identifier-split reports a text node wrapped over two lines` — `2024-03-11` with two rects in one node is reported, with the value in `detail`.
- `overlay-covers-text counts a text node once when nested blocks both contain it` — one covered text node reached through `li` and `p` gives a count of 1.
- The fake DOM (`fakeDocument`, `fakeRoot`, `textNode`, `rect`) answers only the selectors the checks use; `getComputedStyle` is provided in the vm context.

## Existing assertions changed
- None in this round. The round-1 `visibleHeaders` change in `capture.py` is unchanged.

## Verification
- `scripts/gate.sh T03-impl-r2 unit` → PASS (`logs/T03-impl-r2-unit.log`): 361 tests, 327 pass, 0 fail, 34 todo (round 1: 357/323/0/34; delta is the four new tests).
- `scripts/gate.sh T03-impl-r2 trusted` → PASS (`logs/T03-impl-r2-trusted.log`, exit 0, 35 s); 5 `PASS real-input screenshot` lines; no `Frame was detached` failure.
- `scripts/gate.sh T03-impl-r2 visual` → PASS vs baseline (`logs/T03-impl-r2-visual.log`, failures `logs/T03-impl-r2-visual-failures.txt`, copy `logs/visual-T03-impl-r2/`): 0 new failure lines; 2 baseline lines now passing (same two as round 1). The screenshots folder is restored; `git status` is clean for it.
- Real-input notes: 5 of 5 notes in `.artifacts/real-input-fH4B0d/` have `## Machine checks`; the sixth markdown file there is the index.
- Visual sidecars: 90 of 90 have a `Machine checks` section.
- `python3 -m py_compile test/visual/capture.py` → OK.

## Evidence for reviewers
- Machine-check report from this run: `logs/visual-T03-impl-r2/MACHINE-CHECKS.md` (13 failing applicable checks, all `report-only`).
- `identifier-split` rows now: `code-dark-top`, `code-dark-table`, `code-light-full`, each `10 split identifier(s): 2024-03-11, FAR-RIGHT-ACCESS, nw-02, 2024-01-28, nw-03`. No row lists `type(enum)`, `Description◀▶` or `namesummary`.
- `overlay-covers-text` rows are identical to round 1 (diffed): 10 rows, covering the table headers `Expected behavior` / `Evidence`, the frontmatter menu over `type`, `(enum)`, `title`, `(text)`, `Chassis Platform` and `2`, and the date `2026-09-28`.
- The gate deletes `test/visual/screenshots/MACHINE-CHECKS.md` after the run (round-1 open point 1, unchanged). The copy is in `logs/visual-T03-impl-r2/`.

## Feedback addressed (rounds 2–3)
- Finding 1 (MAJOR, identifier-split false positives): fixed. The check compares tops only within one text node. Result: 35 identifier-split report rows became 3 (only the real `code-*` rows). Three tests added, two of them failing before the fix.
- Finding 2 (MINOR, duplicate covered text): fixed with a `Set` of text nodes. Test added, failing before the fix (`2 covered` → `1 covered`).
- Finding 3 (MINOR, geometry exception fails the scenario or capture): fixed in `capture.py` (`machineChecks = None`, `not run` line, failure only if the scenario lists checks) and in `harness.ts` (`- not run: <message>`, rethrow only when `required` is non-empty). No unit test was asked for this; it is verified only by reading the code and by the passing trusted and visual gates, which take the normal path. The exception path is not exercised by any gate.
- Finding 4 (NIT, options semantics): done, one sentence in the header comment.
- Finding 5 (NIT, follow-up): not in scope; unchanged from round 1.

## Report-only baseline for the UI tasks (replaces the round-1 list)
- `identifier-split`: 3 rows, all in the `code-*` scenarios (real splits `2024-03-11`, `FAR-RIGHT-ACCESS`, `nw-02`, `2024-01-28`, `nw-03`).
- `overlay-covers-text`: 10 rows (the table, frontmatter-key, frontmatter-value, frontmatter-list and frontmatter-boolean edit scenarios).
- Total: 13, all report-only.

## Open points / STOP reason
- None blocking. The `not run` path in `capture.py` and `harness.ts` is untested (see Finding 3).
- The two suites outside `realInput` (`checkboxToggle.test.ts`, `previewEditing.test.ts`) still have no Machine checks section (round-1 open point 2, unchanged, outside Allowed files).
