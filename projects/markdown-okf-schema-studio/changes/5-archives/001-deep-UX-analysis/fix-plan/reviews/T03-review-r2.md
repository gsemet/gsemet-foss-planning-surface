# T03 review — round 2

Base: ee8c9bff5f55503eaee652d707e674e04ea1f48b · Reviewed diff: 5 files, +469/-4
(3 tracked: `test/integration/realInput/harness.ts` +54/-3, `test/visual/capture.py` +50/-1,
`test/visual/scenarios.ts` +2; 2 new: `test/shared/geometry-checks.js` 201 lines,
`test/webview/geometryChecks.test.ts` 162 lines). The file set is the same as in round 1. All files
are in Allowed files. Nothing under `src/` changed, and `package.json` and the lockfile are unchanged.
`test/visual/screenshots/` is clean in `git status`.

## Gates

- compile: PASS (`logs/T03-r2-compile.log`). I also ran `npm run compile` myself: exit 0.
- unit: PASS (`logs/T03-r2-unit.log`): 361 tests, 327 pass, 0 fail, 34 todo. Round 1 had
  357/323/0/34, so the 4 new tests account for the whole delta, and the todo count is unchanged. I
  also ran `out/test/webview/geometryChecks.test.js` alone: 6 of 6 pass.
- trusted: PASS (`logs/T03-r2-trusted.log`, extension host exit code 0):
  - 5 `PASS real-input screenshot` lines (01 to 05);
  - 4 `PASS checkbox screenshot` lines;
  - 16 `PASS frontmatter screenshot` lines.
- visual: PASS against the T00 baseline. I compared the files with `LC_ALL=C comm` on
  `logs/visual-baseline-failures.txt` (65 lines) and `logs/T03-r2-visual-failures.txt` (63 lines):
  - 0 new lines;
  - 2 lines now pass, the same two as in round 1: `08-okf-schema--dark…: narrow schema headers are
    ['Name', 'Value◀▶']` and `failed: okf-schema-narrow (alias of frontmatter-scroll-feedback)`.
- Capture side effects: 89 of the 90 PNGs in `logs/visual-T03-r2/` are byte-identical to round 1
  (`logs/visual-T03/`). The one exception is `frontmatter-links-loading.png`, which was already
  shown to be nondeterministic in round 1.
- I did not run the trusted or visual gate again. Extra evidence I collected:
  - two mutation runs of the unit tests (below);
  - a scratch probe of the `capture.py` exception path, using a fake `Page`.

## Round-1 findings: verification

1. **[MAJOR] identifier-split false positives: FIXED as specified.**
   - **Code.** `studioGeometryChecks`, block `// identifier-split`:
     - Applicability is unchanged (`td, th` whose trimmed text matches `^\S{1,24}$`).
     - Each text node now gets its own `range.selectNodeContents(textNode)`. Only the tops of that
       one node's non-empty rects are compared, and a node is flagged when one top differs from its
       first top by more than 1 px.
     - Tops are never compared across text nodes. The comment above the block explains this.
   - **Tests.** The three requested tests (a), (b), (c) exist, with the requested fake DOM and
     values.
   - **Mutation check.** In the scratchpad I restored the round-1 cross-node pooling and ran the
     compiled test file against it. (a) and (b) fail, and (c) still passes. So the tests catch the
     old bug, and (c) guards against a fix that never reports anything.
   - **Real pages.** `logs/visual-T03-r2/MACHINE-CHECKS.md` has 3 `identifier-split` rows, down
     from 35. All 3 are the real `code-*` splits (`2024-03-11, FAR-RIGHT-ACCESS, nw-02, 2024-01-28,
     nw-03`), and the 3 `code-*` rows are identical to round 1. `okf-schema-dark.txt` now has
     `PASS identifier-split`. No row lists `type(enum)`, `Description◀▶` or `namesummary`.
2. **[MINOR] duplicate covered text: FIXED.**
   - **Code.** The text nodes of all matching blocks go into one `Set` before testing.
   - **Test.** `overlay-covers-text counts a text node once when nested blocks both contain it`.
   - **Mutation check.** With the `Set` replaced by an array, that test fails and the others pass.
   - **Real pages.** The `overlay-covers-text` rows are byte-identical to round 1 (10 rows), so real
     pages were not affected.
3. **[MINOR] geometry exception fails the scenario: FIXED.**
   - **`capture.py` `check_final_frame`.** Only the geometry `page.evaluate` is wrapped. On error:
     - `result["machineChecks"] = None`, and the rest of the first evaluate is kept;
     - a `Failure` is added only when `scenario.get("machineChecks")` is non-empty;
     - `machine_check_lines(None)` prints `not run: …`;
     - `main` uses `or []`, so `MACHINE-CHECKS.md` tolerates `None`.

     I checked this path with a fake page whose second `evaluate` raises:
     - `machineChecks=[]` → `scrollY=120` kept, `machineChecks=None`, no failure;
     - `machineChecks=['identifier-split']` → one failure, `machine checks not run: ReferenceError:
       boom`.
   - **`harness.ts` `Evidence.capture`.** The evaluate is wrapped in `try/catch`. On error:
     - the note gets `- not run: <message>`;
     - the screenshot and the note are still written;
     - the function throws only after both are written, and only when `required` is non-empty.

     I read this path; no gate exercises it.
4. **[NIT] options semantics: done, but the sentence is partly wrong.** See finding 1 below.
5. **[NIT, follow-up] Machine checks in the `checkboxToggle`/`previewEditing` notes:** unchanged.
   This is accepted, as in round 1, and stays in `followups.md`.

## Done-when

- [x] The `unit`, `trusted` and `visual` gates pass: see Gates above.
- [x] Every visual note and every real-input note has a "Machine checks" section:
  - visual: all 90 sidecars in `logs/visual-T03-r2/` (`grep -L '^Machine checks$'` returns
    nothing);
  - real-input: all 5 notes in `.artifacts/real-input-Mry0Lw/`, which `REAL-INPUT-LATEST.md` points
    to, have `## Machine checks`.
- [x] `MACHINE-CHECKS.md` exists and is linked from `INDEX.md`:
  - the file is `logs/visual-T03-r2/MACHINE-CHECKS.md`, with 95 scenarios and 13 failing applicable
    checks, all `report-only`;
  - the link is line 5 of `logs/visual-T03-r2/INDEX.md`, under the run status.
- [x] The criterion left open in round 1 is now met: the report-only baseline lists only real
  problems.
  - The 3 `identifier-split` rows are real wraps.
  - The 10 `overlay-covers-text` rows were confirmed in round 1. I looked at
    `edit-frontmatter-value-dark.png` again: the ⊞/⊟ menu covers `swrs` and the start of
    `Brake pedal release detection`, as the row says.
- [x] No scenario is required. `machineChecks` appears only in the `Scenario` type, and the harness
  has no caller that passes `options.checks`.

## Protected features checked

T03 changes only test tooling. No product file changed, so no product behaviour can regress. For
each area the diff touches, coverage is intact:

- **P-R1, P-R2, P-R3, P-R6, P-R7 (static visual coverage):**
  - the `capture.py` assertions are unchanged, apart from the `visibleHeaders` probe that the task
    lists;
  - the new geometry evaluate runs after the existing evaluate and only reads layout;
  - the visual gate shows 0 new failure lines, and 89 of 90 PNGs are byte-identical to round 1.
- **P-E2, P-E3, P-E4, P-E5, P-L2 (T02 real-input scenarios):**
  - `Evidence.capture` keeps its order: scroll, pointer move, blur, tooltip wait, geometry
    read-only evaluate, screenshot, note;
  - all 5 captures pass in the trusted gate.
- **P-R5, P-R7 (screenshot suites in `checkboxToggle.test.ts` and `previewEditing.test.ts`):** not
  touched; they still pass in the trusted log.
- **P-S1 to P-S4, P-N\*, P-L\*, P-P\*:** not touched. `test/**` is not shipped in the VSIX.

## Findings

1. **[MINOR] `test/shared/geometry-checks.js`, header comment (lines 4–5): the last clause
   contradicts the first.**
   - The comment says that a non-empty `overlays`/`ignoreWithin` replaces the defaults. That part is
     correct.
   - It then ends with "so a caller cannot drop a default by passing a short list". That part is
     false: `ignoreWithin: ['.x']` drops all four default ignores.
   - **Risk.** A later task (T15, T18, T19, T23) that trusts the comment gets false
     `overlay-covers-text` failures from text inside the open editors. Or it silently stops
     checking the default overlays.
   - **Fix.** Replace lines 4–5 with:

     ```js
     // options.overlays and options.ignoreWithin replace the defaults when they are non-empty: passing
     // ['.x'] drops every default, so repeat the defaults you still need. An empty or missing array
     // keeps the defaults.
     ```

   - No test needed. The orchestrator can apply this before the commit, or log it in
     `followups.md`.
2. **[NIT] `test/visual/capture.py`, `machine_check_lines`: the `None` line names the wrong
   cause.**
   - It always prints `not run: the final frame was unavailable`, even when only the geometry
     script threw.
   - For report-only scenarios, the geometry error text is not recorded anywhere.
   - **Optional fix:**
     - in the `except` branch of `check_final_frame`, also set
       `result["machineChecksError"] = str(error)`;
     - in `sidecar_text`, print `not run: <that error>` when it is present.
   - Defer to `followups.md`.
3. **[NIT] Report: the red-state counts do not add up.**
   - "361 tests, 327 pass, 3 fail" with 34 todo totals 364, so the passing count was 324.
   - The failing-before-fix evidence is still sound: the excerpts are consistent, and my mutation
     runs reproduce the 2 + 1 failures independently.
   - No action.

Notes for later tasks, not findings against T03:

- By design, `identifier-split` judges each text node on its own. It cannot see a wrap between
  sibling inline elements, for example:
  - `type` on one line and `(enum)` wrapped to the next;
  - an identifier split across several `<span>`s.

  T19 (UX-15) should add its own assertion if it needs that case.
- No gate exercises the exception paths of finding 3 in round 1. My scratch probe covers
  `capture.py`. `harness.ts` was verified by reading only.

## Existing assertions changed

- `test/visual/capture.py` `OKF_SCHEMA_CHECKS`, `visibleHeaders` probe: unchanged since round 1.
  It matches the task's snippet, and the comparison with `["Name", "Value"]` is unchanged.
  **OK, justified** (listed in "Expected changes to existing tests").
- No other assertion was modified, removed, skipped or weakened. Round 2 added 4 tests and changed
  none.

VERDICT: PASS
