# CR 227, round 2: Inspector review

Verdict: APPROVE

Scope: the uncommitted diff in `markdown-okf-schema-studio-wt-227` against HEAD 0b4ede78. It covers
8 changed files and the new `test/integration/realInput/wideTableTab.ts`. Round 2 changed the
requirement, the E2E file, `run.ts` and `stressPlan.ts`. The product code
(`tableCellEditor.ts`) and the unit tests are the same as in round 1. I left the worktree as I
found it: the porcelain status and the diff hash are identical before and after my gate runs.

## Round-1 findings

1. **Criteria line (blocking 1): resolved.** `SwRS-MDOKFSTUDIO-TABLE-035.md:136` now names the
   three unit-tested cases:
   - a click on a visible cell (no scroll);
   - a click on a partly hidden cell;
   - an editor that opens in a hidden cell on its source reply.

   It also says that the reopen after a re-render goes through the same source-reply open path
   and has no dedicated test. This matches `runtimeTableCellEditor.test.ts` tests 3 and 4.
2. **`setWidthMode` (blocking 2): resolved** (`wideTableTab.ts:95-120`).
   - The click count is computed from the known cycle `margin -> auto -> full`. I checked the
     cycle against `src/page/modules/widthMode.ts:28`.
   - After each click, the helper waits on `html[data-sphinx-preview-width]` for the expected
     next mode, using the harness `waitFor`. That is a state wait, the same pattern as elsewhere
     in realInput.
   - There is no fixed sleep and no re-click based on a read. An unknown starting mode fails
     with the value it got.
   - The restore in `finally` (`:173`) uses the same helper. Rule 12 of `ci.guidelines.md` is
     respected.
3. **SHALL and description (non-blocking 3): resolved.** Both texts got the same clause (`:11-12`
   and `:41`). The generated `table-editing/index.md` changes only the TABLE-035 line, and the
   requirement is still `proposed`. No other requirement file is touched, so no approved
   requirement changed.
4. **Cell start inside the table box (non-blocking 4): resolved** (`wideTableTab.ts:66-68, 88-90`).
   - The box is read as `table.getBoundingClientRect().left + clientLeft`, plus `clientWidth`,
     which matches `revealCellInTable`. The check is `cellLeft in [boxLeft - 1, boxRight + 1]`.
   - **No spurious failure.** A start-aligned target puts the union start at `boxLeft + 16`, and
     the cell start is at or after it. An end-aligned target only happens when the target fits in
     `box - 32`, so its cell start is inside. A target that is already visible is inside by
     definition.
   - **The check bites.** On the old code the cell start is past `boxRight` from about Tab 3 on.
   - The editor's right edge is not asserted against the box, as asked.
5. **Stress plan (non-blocking 5): resolved.**
   - `"wide-table-tab"` is the last entry of both `STRESS_SCENARIOS` (`run.ts:68-69`) and
     `STRESS_SCENARIOS_BY_HOST.trusted` (`stressPlan.ts:74-75`), with the same comment.
   - `runStress` asserts that the two lists are equal, and `test/build/stressPlan.test.ts` stays
     green.
   - The scenario resets its own state between rounds: `withDocument` turns edit mode off
     (`common.ts:110`), and `finally` restores the Margin width.

Findings 6 and 7 were skipped on purpose (the heavy run happens later on the stack top).

## Regression check

- **Product code.** `src/page/features/tableCellEditor.ts` has not changed since round 1, which
  approved its logic.
- **CI rules.**
  - The scenario has no retries, no `force`, no raised timeouts and no sleeps.
  - The double `requestAnimationFrame` in `expectEditorInView` (`:81-82`) waits for a layout
    frame, not for a duration.
  - The scenario is wired both in the required integration flow (`run.ts:209-210`) and in the
    stress list, as the plan's comment describes.
- **Stress budget.** The ci-stress comment gives about 18 min for 20 rounds today, with a 26 min
  launch deadline and a 30 min job.
  - By my estimate, one round of the new scenario takes about 5-10 s: one document open, two
    width modes and about 30 real key presses with state waits.
  - Over 20 rounds that adds about 2-3.5 min, for roughly 20-22 min in total. That is tight, but
    it does not break the deadline. Measure it on the heavy run.

## Gates (run by me in the worktree)

- `UV_NO_CONFIG=1 just check` exited 0:
  - node unit tests: 3324 pass, 0 fail;
  - second node suite: 71 pass, 0 fail;
  - pytest: 153 passed;
  - requirements lint: 1072 requirements, 0 errors, 21 warnings;
  - 0 indexes, 0 OKF projections and 0 coverage files would change.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`
  exited 0: 1072 requirements, 0 errors, 21 warnings. None of the warnings is about TABLE-035;
  they are existing broken cross-links, such as PALETTE-264.

## Findings

### Blocking

None.

### Non-blocking

1. **The width-wait failure message shows the value from before the click**
   (`test/integration/realInput/wideTableTab.ts:113-114`).
   - The `waitFor` description is a template string built before the wait, so `now ${actual}`
     always shows the value before the click.
   - If the mode got stuck, the message is right. If the mode overshot (for example, it reached
     `full` when `auto` was expected), the message says `now margin` and misleads whoever reads
     the failure.
   - **Fix:** wrap the wait and rethrow with a fresh read, for example:
     `try { await waitFor(...) } catch (error) { throw new Error(`width mode ${expected} expected after the Width button, page reports ${String(await widthMode(page))}`, { cause: error }); }`
     Then drop `now ...` from the description.
2. **The Criteria line does not mention the new E2E check**
   (`SwRS-MDOKFSTUDIO-TABLE-035.md:136`).
   - For the real window, the line still reads "the editor rect inside the webview viewport and
     no horizontal page scroll". It does not mention the cell-start-in-table-box assertion added
     this round.
   - **Fix:** add "and the selected cell's start inside the table's visible box".
   - Optionally, the Method line (`:130`) could also list "an editor opening in a hidden cell on
     its source reply".
3. **The restore in `finally` can hide the first failure** (`wideTableTab.ts:171-174`).
   - If an assertion fails and the Width restore then also fails, for example because the frame
     is gone, the restore error replaces the assertion error.
   - **Optional fix:** keep the first error, and log the restore error or attach it as its cause.
4. **The stress margin is thin** (see "Stress budget" above).
   - Not a defect. On the heavy run, check the `PASS stress ... wide-table-tab (N ms)` lines and
     the total trusted-window time against the 26 min launch deadline.
