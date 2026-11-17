# CR 227, round 1: Inspector review

Verdict: CHANGES

Scope: the uncommitted diff in `markdown-okf-schema-studio-wt-227` against HEAD 0b4ede78 (6 files
changed, plus the new `test/integration/realInput/wideTableTab.ts`). The worktree was left as I found
it.

## What I checked

- **`revealCellInTable` (src/page/features/tableCellEditor.ts:29-52).** The rect math is right for
  LTR. The table's border box stays put while cells move with `scrollLeft`, so a viewport delta
  equals a `scrollLeft` delta. The visible box is `tableRect.left + clientLeft` plus `clientWidth`.
  The result is clamped to `[0, scrollWidth - clientWidth]`. A table that does not overflow
  returns early. A visible target causes no scroll, measured without the margin as the owner asked.
  A target to the left, or wider than `box - 2 x 16`, is aligned on its start. A target to the
  right is aligned on its end with the 16 px margin. The function only writes `table.scrollLeft`:
  no `scrollIntoView`, no page scroll and no vertical change.
- **Where the reveal runs (tableCellEditor.ts:538).** It runs at the end of `renderTableCellEditor`,
  after the input, the buttons, `resizeInput`, `syncTableMenuSticky` and the focus, which uses
  `preventScroll: true`. The rects are read synchronously after layout. All the owner's paths go
  through this point:
  - cell switch (`switchTableCell`: Tab, Shift+Tab, arrows, wrap);
  - a click in the same table (`openMappedEditor` → `switchTableCell`);
  - the first open and the reopen after a re-render (`resumePendingBlockNavigation` →
    `openBlockEditor` → source reply → `blockSourceEditor.ts:87`);
  - the non-structural toolbar buttons.
- **Effect on the vertical anchor.** `beginEditAnchor`/`applyAnchor` read only `top`, so the vertical
  edit anchor is unaffected. `syncTableMenuSticky` uses only the vertical position.
- **Home and End.** They are untouched: `homeEndInControl` never reaches the reveal, so the TABLE-035
  "neither page nor table scrolls" scenario holds.
- **Clicks.** The editor opens on `click`, which comes after mouseup. Scrolling after it therefore
  cannot redirect the click, and the clicked cell gets the editor. The unit test asserts this
  (`clicked.editor.parentElement === cells[1][1]`).
- **Unit tests fail before the fix.** I checked this in a scratch copy, not in the worktree: I
  restored `tableCellEditor.ts` from HEAD, compiled, and ran `runtimeTableCellEditor.test.js`. The
  result was 49 passed and 4 failed, and the 4 failures are exactly the new tests. The "visible
  cell, no scroll" half of test 3 is a no-op guard and passes either way, which is expected.
- **The E2E fails before the fix, from reading the code.**
  - Without the fix nothing scrolls the table, because the focus uses `preventScroll`.
  - By Tab 3 or 4, the editor's left edge is past `innerWidth` in the CI side preview.
  - The wrap from the scrolled-to-end last cell puts the editor at about -1558 px, as the before
    measures show.
  - So `place.left >= -1 && place.right <= viewRight + 1` fails on the old code.
  - There are no retries around assertions, no `force`, and no raised timeouts.
- **CI wiring.**
  1. `ci.yml` integration job.
  2. `just ci-integration`.
  3. `npm run test:integration`.
  4. `run-tests.ts` → `trusted-suite.js`.
  5. `runRealInput()` → `run.ts:208`, which calls `scenarioWideTableTab`.

  It runs in the full campaign, not only when selected by `STUDIO_REAL_INPUT_SCENARIO`. As for
  every real-window scenario, the job runs only on a heavy dispatch or a release push.
  `markers.ts:39` already carries `@tests_req SwRS-MDOKFSTUDIO-TABLE-035`.
- **Requirement.** The requirement is TABLE-035, `req_lifecycle: proposed`. The new scenario has the
  same GIVEN/WHEN/THEN shape and Input/Outcome table as the rest of the file. The coder touched no
  other requirement file, and no approved requirement changed.
- **Gates, which I ran myself in the worktree.**
  - `UV_NO_CONFIG=1 just check` exited 0:
    - node unit tests: 3324 pass, 0 fail;
    - second node suite: 71 pass, 0 fail;
    - pytest: 153 passed;
    - requirements lint: 1072 requirements, 0 errors, 21 warnings;
    - update-coverage check: 0 files would change.
  - `okfreq validate --check-links`: 1072 requirements, 0 errors, 21 warnings. None of the
    warnings is about TABLE-035; they are existing broken cross-links in other files.

## Findings

### Blocking

1. **The verification note says the opposite of what the tests do**
   (requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-035.md:135).
   - The Criteria say the reveal on a click and on a reopen "is asserted for a click on a visible
     cell only".
   - In fact, the 4th unit test (`runtimeTableCellEditor.test.ts`, "a click on a partly hidden
     cell and an editor opening in a hidden cell…") asserts two more cases. A click on a partly
     hidden cell scrolls by `120 + 16`. An editor that opens on its source reply in a hidden cell
     is revealed.
   - **Fix:** replace that clause with: "the reveal is asserted for a click on a visible cell
     (no scroll) and on a partly hidden cell, and for an editor that opens on its source reply in
     a hidden cell. The reopen after a re-render (Tab in the last cell, a structural button of the
     table bar) goes through the same source-reply path and has no dedicated test."
   - The Method line (:129) could also name the 4th test ("a click on a partly hidden cell").
2. **`setWidthMode` waits for time and retries the click**
   (test/integration/realInput/wideTableTab.ts:87-95).
   - The helper clicks the Width button, sleeps a fixed 250 ms, and loops up to 4 clicks until the
     attribute matches.
   - This breaks `.agents/guidelines/ci.guidelines.md` rule 12: "the test waits for a state the
     product reports … never for time: no sleep, no 'poll until it works', no retry loop around an
     action".
   - If the page applies the mode later than 250 ms, the loop clicks again and goes past the
     target (margin → auto → full). The scenario then fails or runs in the wrong mode for reasons
     unrelated to this CR.
   - **Fix:** the cycle is known (margin → auto → full → margin). Compute the number of clicks
     from the current mode. After each click, `waitFor` until `html[data-sphinx-preview-width]`
     equals the next expected mode, with a failure message that names the current value. Do not
     sleep, and do not re-click based on a stale read.
   - The final restore to Margin in `finally` should use the same deterministic helper.

### Non-blocking

3. **The SHALL does not cover the new behaviour**
   (SwRS-MDOKFSTUDIO-TABLE-035.md:6-12 and :40).
   - The scenario adds a horizontal-reveal outcome, but the description and the normative
     statement still only say "move the editor to the next … cell".
   - Per requirements.guidelines.md, an SwRS is "one observable, bounded SHALL response" that the
     scenarios refine. The requirement is `proposed`, so it can still change.
   - **Fix:** append to both: "…, and bring that cell and its editor into the visible part of the
     table's sideways scroll box without scrolling the page". Then re-run the requirements
     update so the OKF projection follows.
4. **The E2E checks the viewport, not the table box**
   (wideTableTab.ts:79).
   - The assertion is against the webview viewport, not the table box and its 16 px margin. The
     after-measures show the editor at 90..390 while the box is 62..362, so 28 px of the editor
     are clipped by the box and the assertion still passes.
   - The test does fail on the old code, but it does not check the rule that was approved.
   - **Fix:** also read the table box in `editorPlace`:
     `boxLeft = table.getBoundingClientRect().left + table.clientLeft` and
     `boxRight = boxLeft + table.clientWidth`.
   - Then assert that the selected cell's start lies inside it:
     `cellLeft >= boxLeft + 16 - 1` when start-aligned, or more generally
     `cellLeft >= boxLeft - 1 && min(cellRight, editorRight) <= boxRight + 1` when the target fits.
   - At minimum, assert `editor.left >= boxLeft - 1`.
5. **The new scenario is not in the stress plan**
   (test/shared/stressPlan.ts:51-75 and the `STRESS_SCENARIOS` table in
   test/integration/realInput/run.ts:48).
   - The plan's own comment says "CI rule 12: a new real-window scenario is added here and proved
     by the `stress` job before it stays in the required integration job".
   - **Fix:** add `"wide-table-tab": scenarioWideTableTab` to `STRESS_SCENARIOS` and
     `"wide-table-tab"` to `STRESS_SCENARIOS_BY_HOST.trusted`, in the same order. The
     `stressPlan.test.ts` T2 check keeps the two lists in step.
6. **The E2E has never run**
   (wideTableTab.ts, whole file).
   - Local real-window runs are forbidden, so the scenario was only type-checked. Its selectors
     (`td` filtered by `/^a{24}$/` and `/^LASTCELL$/`) and the width toggle are plausible. But a
     row handle or an extra text node inside a `td` would break `hasText`, and nothing has
     checked that.
   - **Fix:** before merge, the Driver dispatches a heavy run (`gh workflow run ci.yml --ref
     <branch> -f heavy=true`) and checks that `wide-table-tab` passes in both modes.
7. **A `.table-wrapper` scroll box is not handled**
   (tableCellEditor.ts:30).
   - `revealCellInTable` assumes the `<table>` is the scroll box.
   - `contentBlockStyles.ts:481` also gives `.table-wrapper` `overflow-x: auto`. Today the inner
     table (`max-width: 100%`) keeps the scroll, so the wrapper never overflows and this is
     latent only.
   - **Optional fix:** use `cell.closest("table, .table-wrapper")`, or the nearest ancestor whose
     `scrollWidth > clientWidth`, as the box.
