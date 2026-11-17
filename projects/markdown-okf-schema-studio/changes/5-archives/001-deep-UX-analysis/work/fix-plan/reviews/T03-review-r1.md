# T03 review — round 1

Base: ee8c9bff5f55503eaee652d707e674e04ea1f48b · Reviewed diff: 5 files, +321/-4
(3 tracked: `test/integration/realInput/harness.ts` +46/-4, `test/visual/capture.py` +44/-0,
`test/visual/scenarios.ts` +2; 2 new: `test/shared/geometry-checks.js` 191 lines,
`test/webview/geometryChecks.test.ts` 42 lines). No file under `src/`, no `package.json` or lockfile
change.

## Gates

- compile: PASS (`logs/T03-compile.log`).
- unit: PASS (`logs/T03-unit.log`): 357 tests, 323 pass, 0 fail, 34 todo. T02 r3 had 355/321/0/34,
  so the delta is exactly the two new geometry tests. The todo count is unchanged.
- trusted: PASS (`logs/T03-trusted.log`, exit 0). The log has `PASS real-input screenshot` for all
  5 T02 captures, and the checkbox and frontmatter screenshot suites still pass.
- visual: PASS against the T00 baseline. I re-checked it with `LC_ALL=C comm` on
  `logs/visual-baseline-failures.txt` and `logs/T03-visual-failures.txt`. There are 0 new lines.
  2 lines now pass, and both are expected:
  `08-okf-schema--dark…: narrow schema headers are ['Name', 'Value◀▶']` and
  `failed: okf-schema-narrow (alias of frontmatter-scroll-feedback)`.
- Capture side effects: I compared the PNG hashes of `logs/visual-T00-impl-r2/` (before T03) with
  `logs/visual-T03/`. 89 of the 90 images are byte-identical. The one that differs,
  `frontmatter-links-loading.png`, also differs between every pair of earlier runs (T00, T00-impl,
  T00-impl-r2, T03-impl, T03), so it is nondeterministic and the change did not cause it. The extra
  `page.evaluate` does not change what gets captured.
- I did not re-run any gate. To check the geometry, I ran one read-only Playwright probe on the
  rendered static pages in `.artifacts/visual/pages/`. The figures are in F1.

## Done-when

- [x] The `unit`, `trusted` and `visual` gates pass. Evidence: the logs above.
- [x] Every visual note and every real-input note has a "Machine checks" section. All 90 sidecars in
  `logs/visual-T03/` have one. Alias scenarios have no sidecar of their own, as before T03. All 5
  notes in `.artifacts/real-input-0OA1TK/` have `## Machine checks`. "Real-input" means the T02
  harness, as the task Goal defines it. See F5 for the other screenshot suites.
- [x] `MACHINE-CHECKS.md` exists and `INDEX.md` links it: `logs/visual-T03/MACHINE-CHECKS.md`, and
  `logs/visual-T03/INDEX.md` line 5. The gate deletes the file from the tracked folder after the
  run. That is intended plan tooling, as the orchestrator said, and needs no action.
- [ ] Implicit in the Goal and in step 4 ("they are the known baseline for the UI tasks"): the
  checks print FAIL only for real problems. `identifier-split` does not meet this. See F1.

Specific points from the orchestrator:

1. **Report-only by default: verified.**
   - `capture.py` `check_final_frame` appends a `Failure` only when
     `check["id"] in scenario.get("machineChecks", [])` and the check is applicable and failing.
   - `machineChecks` appears only in the `Scenario` type (`scenarios.ts:47`). No scenario sets it.
   - `renderFixtures.ts` spreads each scenario whole (`...scenario`), so the field would reach
     Python if a scenario set it.
   - `harness.ts` throws only for ids in `options.checks.required`, and no caller passes options.
   - The one way a report-only check can still fail a scenario is an exception inside the geometry
     script. See F3 (MINOR).
2. **The checks judged on real screenshots** (details in F1):
   - `overlay-covers-text` finds real problems:
     - `edit-table-wrapped-dark-900.png`: the table bar covers the "Expected behavior" and
       "Evidence" headers (UX-14).
     - `edit-frontmatter-key-dark.png`: the ⊞/⊟ menu covers `type` and `title (text)` (UX-20).
     - `edit-frontmatter-boolean-dark.png`: the menu covers "Chassis Platform" and the priority
       value "2".
     - I found no false positive.
   - `overlay-clipped` passes in all 9 scenarios where it applies, and none of those images shows a
     clipped overlay.
   - Sticky band versus toolbar is correctly not in scope. The task excludes the toolbar (UX-44),
     and the existing `capture.py` assertions still report it.
   - `identifier-split`: 32 of its 35 rows are false positives. Only the 3 `code-*` rows are real.
3. **Implementer's open point 2** (no Machine checks in `checkbox-e2e-*` and `frontmatter-e2e-*`
   notes): acceptable for T03. The Goal names "the real-input E2E campaign (T02 harness)", and
   `checkboxToggle.test.ts` and `previewEditing.test.ts` are not in Allowed files. Log it as a
   follow-up (F5).
4. **New untracked files:** I read both in full (`diff.sh` output).

## Protected features checked

T03 changes only test tooling. No product file under `src/` changed, so no behaviour can regress.
For each area the diff touches, I checked that its coverage is intact:

- P-R1, P-R2, P-R3, P-R6, P-R7 (visual coverage): the existing `capture.py` assertions are
  unchanged. The one exception is the `visibleHeaders` probe, which the task lists. The visual gate
  has 0 new failure lines, and the captured images are identical (hash check above).
- P-E2, P-E3, P-E4, P-E5, P-L2 (T02 real-input scenarios): `Evidence.capture` keeps its order:
  scroll, then pointer move, then blur, then tooltip wait, then screenshot. The geometry evaluate
  only reads layout and runs before the screenshot. The trusted gate passes all 5 captures.
- P-R5 and P-R7 screenshot suites (`checkboxToggle.test.ts`, `previewEditing.test.ts`): not
  touched, and they still pass in the trusted log.
- P-S1 to P-S4, P-N*, P-L*, P-P*: not touched. `test/**` is excluded from the VSIX by
  `.vscodeignore`, so the new JS file does not ship.

## Findings

1. **[MAJOR] `test/shared/geometry-checks.js`, `studioGeometryChecks`, block `// identifier-split`:
   false positives on every properties table.** The block pools the `top` of rects from all text
   nodes of a cell and flags the cell when any two tops differ by more than 1 px. Several text
   nodes on one line with different font sizes then count as "split". So do block children that
   sit on separate lines by design. Measured on the rendered pages with Playwright:
   - Name cell `type` + `(enum)` (`.okf-type-label`, 0.84em, inline-flex centered): `type` top 83.5,
     `(enum)` top 85.1, both on one line.
   - Header `Description` + toggle `◀`: tops 53.0 and 51.9, both on one line.
   - SKILL page `required` cell: list items `name` (top 226.8) and `summary` (top 251.5). Its
     `textContent` is `namesummary`, so it qualifies as an identifier.
   - Real splits, for comparison: `2024-03-11` is one text node with tops 1101.5 and 1123.9, and
     `FAR-RIGHT-ACCESS` is one text node on 3 lines.

   `okf-schema-dark.png` shows every name and header on one line, yet its sidecar says
   `FAIL identifier-split: 10 split identifier(s): Description◀▶, type(enum), title(text)…`.
   In `MACHINE-CHECKS.md`, only `code-dark-top`, `code-dark-table` and `code-light-full` are real.
   The other 32 rows, every scenario with a properties table plus `standalone-frontmatter-*`, are
   false.

   This blocks because the task makes this file the baseline for T19 and T23. A Haiku implementer
   asked to make `identifier-split` required could change the properties-table name cell layout
   (P-R7) to satisfy a false check. It also defeats QA-03's "a human only looks at failures".

   **Fix** (it deviates on purpose from the task table's "all rects share the same top" wording;
   the orchestrator should note this in the task file):
   - Keep applicability unchanged: a `td`/`th` whose trimmed `textContent` matches `^\S{1,24}$`.
   - Judge each text node of the cell on its own. For each text node, collect the `top` of its own
     non-empty client rects (`range.selectNodeContents(textNode)` as today). The cell is split when
     **one text node** has two rects whose tops differ by more than 1 px.
   - Never compare tops across different text nodes.
   - Update the comment above the block, for example: "an identifier is split when one of its text
     nodes wraps onto several lines; text nodes of different sizes on one line are not a split".

   **Tests** (in `test/webview/geometryChecks.test.ts`; write them first, run them against the
   current code, and paste the failure excerpt in the report):
   - Add a small fake DOM:
     - `document.querySelectorAll(sel)` returns `[root]` for `'#sphinx-myst-preview-content'` and
       `[]` for every other selector.
     - `root.querySelectorAll('td, th')` returns the fake cells.
     - A cell is `{ textContent, childNodes: [textNode…] }`.
     - A text node is `{ nodeType: 3, textContent, rects: [{ top, bottom, left: 0, right: 40, width: 40, height: bottom - top }] }`.
     - `document.createRange()` returns
       `{ selectNodeContents(n) { this.n = n; }, getClientRects() { return this.n.rects; } }`.
   - (a) `identifier-split passes when a cell's text nodes share one line at different sizes`: one
     cell `type(enum)` with nodes `type` [83.5–98.5] and `(enum)` [85.1–97.1]. Expect
     `applicable: true, pass: true`. It fails on the current code.
   - (b) `identifier-split ignores list items on separate lines`: one cell `namesummary` with nodes
     `name` [226.8–241.8] and `summary` [251.5–266.5]. Expect `pass: true`. It fails on the current
     code.
   - (c) `identifier-split reports a text node wrapped over two lines`: one cell `2024-03-11` with
     one node and rects [1101.5–1118.5] and [1123.9–1140.9]. Expect `applicable: true`,
     `pass: false`, and `detail` containing `2024-03-11`.

   **Then:**
   - Run `PLAN/scripts/gate.sh T03-impl unit visual`.
   - In the report, show the new `MACHINE-CHECKS.md` identifier-split rows. Expected:
     `code-dark-top`, `code-dark-table` and `code-light-full` still list `2024-03-11`,
     `FAR-RIGHT-ACCESS` and `nw-02`, and no row lists `type(enum)`, `Description◀▶` or
     `namesummary`.
   - The visual gate still reports 0 new failure lines.
   - Replace the report's "report-only failures" baseline list with the new one.

2. **[MINOR] `test/shared/geometry-checks.js`, block `// overlay-covers-text`: the same text node can
   be tested more than once.** `textBlockSelector` matches nested blocks (`li > p`, `dd > p`,
   `td > p`), and `collectTextNodes` is called once per matching block. A covered text inside a
   loose list item is then counted twice in the detail, and its excerpt is listed twice.
   **Fix:** collect the text nodes of all blocks into one `Set` before testing them, or skip a
   block whose `parentElement.closest(textBlockSelector)` is inside `root`. Optional test: a fake
   `li` containing a fake `p` with one covered text node gives a count of 1. The fake needs
   `getComputedStyle` and `getBoundingClientRect` on the overlay. Can be deferred to
   `followups.md`.

3. **[MINOR] `capture.py` `check_final_frame` and `harness.ts` `Evidence.capture`: an exception in
   the geometry script fails the scenario.** In `capture.py`, an exception from the geometry
   `page.evaluate` goes up to `main`, which then:
   - records `final frame unavailable`;
   - loses the whole `finalState` (scroll position, editors, visible content);
   - skips the existing bottom and selector landmark assertions.

   In the harness, it fails the real-input test before the screenshot is taken.
   **Fix:**
   - In `capture.py`, wrap only the geometry evaluate in `try/except Exception as error`. On error,
     set `result["machineChecks"] = None`, keep the `result` from the first evaluate, and append a
     `Failure` only if `scenario.get("machineChecks")` is non-empty. Change `machine_check_lines`
     so `None` prints `not run`.
   - In `harness.ts`, wrap the evaluate in `try/catch`. Write `- not run: <message>` in the note,
     and rethrow only when `checkOptions.required` is non-empty.

   Can be deferred to `followups.md`.

4. **[NIT] `geometry-checks.js` options semantics.** A non-empty `overlays` or `ignoreWithin`
   replaces the defaults, and an empty array means "use the defaults". This is reasonable but not
   written down. A later task that passes `ignoreWithin: ['.x']` silently drops
   `[data-sphinx-preview-block-editor]` and the other defaults. Add one sentence to the file's
   header comment.

5. **[NIT, follow-up] Implementer's open point 2.** `checkboxToggle.test.ts` `capture()` and the
   frontmatter screenshot writer in `previewEditing.test.ts` produce notes without a Machine checks
   section. This is accepted for T03 (Goal scope and Allowed files). For `followups.md`: reuse the
   harness evaluation, for example an exported `runGeometryChecks(frame, options)` in
   `realInput/harness.ts`, from those two files in the first task allowed to touch them, or at T40.

Notes for later tasks, not findings against T03:

- UX-20's clipped tooltips are `button[data-tooltip]::after` pseudo-elements. DOM rect checks
  cannot see them, so `overlay-clipped` will not catch that bug. T23 needs its own assertion if it
  wants one.
- The frontmatter key-suggestion list (it covers the `owner` row in
  `edit-frontmatter-key-dark.png`) is not in the default overlays. T24 and T25 can pass it in
  `overlays`.

## Existing assertions changed

- `test/visual/capture.py` `OKF_SCHEMA_CHECKS`, `visibleHeaders` probe. The `.map` now clones each
  cell, removes its `button` elements, and reads the trimmed text. The code matches the task's
  snippet exactly, and the comparison with `["Name", "Value"]` is unchanged. Effect as predicted:
  the baseline line `narrow schema headers are ['Name', 'Value◀▶']` now passes.
  **OK, justified** (listed in "Expected changes to existing tests").
- No other assertion was modified, removed, skipped or weakened.

VERDICT: CHANGES REQUESTED
