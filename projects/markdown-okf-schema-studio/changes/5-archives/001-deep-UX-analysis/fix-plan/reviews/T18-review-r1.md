# T18 review — round 1

Base: fa73a7f · Reviewed diff: 7 T18 files (scrollSync.ts, previewStyles.ts, scrollSync.test.ts,
previewStyles.test.ts, realInput.test.ts, scenarios.ts, capture.py)

## Gates
compile/unit/types: PASS. trusted: PASS (logs/T18-trusted.log, includes RI-T18). visual: PASS vs T00
baseline (logs/T18-visual.log), 0 new failure lines. The gate result is not enough here: the
screenshots show a defect that the gate cannot see, because capture.py lost two checks (finding 1).

## Done-when
- [x] Toolbar in flow above the table, labels, new status text — unit tests, RI-T18, 900 px shots.
- [x] Selected cell outlined — screenshots (blue 2px outline), capture.py outline check.
- [ ] "Toolbar visible when it appears" (amendment, UX-14) — `edit-table-wrapped-dark-460.png` and
  `-light-460.png`: the bar's first row sits under the sticky heading band. The tops of the icons
  and the "Row +" / "Row −" labels are cut at the band's lower edge. The fixed preview controls pill
  (top right) also covers "Col −". The bar is not fully readable, and you cannot reliably click it.
- [x] 900 px (dark/light): the bar sits fully below the band, above the table, and covers no cell.
  The labels are readable.

## Protected features checked
- P-E5: the action handlers and guards are unchanged (only a `label` argument was inserted in
  `addAction`). `rememberCellValue` still runs before each operation. `closeBlockEdit` still removes
  `edit.tableMenu`, and the listener removal is harmless when undefined. Cell switching reuses
  `edit.tableMenu`, so there is no re-insertion and no second reveal. The coverage is the existing
  `scrollSync.test.ts` table tests and markdownTable tests, which pass in the unit gate.
- R7 / scroll sync: the reveal uses `programmaticScroll`. That function sets `expectedScroll`, so the
  scroll handler (lines ~422) ignores the event as preview-owned and the source editor does not move.
  `editAnchor.viewportTop += delta` keeps later `applyAnchor` calls consistent. RI-T18 checks that the
  cell moves by at most 2 px.
- P-E8: the toolbar exists only inside the edit path, so read-only mode is unaffected.
- P-S4: the labels use `textContent`.

## Findings
1. [BLOCKER] test/visual/capture.py:check_preview_edit_mode — the replacement of the "aligned with its
   active cell" check is weaker than the original. It drops two checks:
   - the overlap check against the fixed controls: `controlsBottom` is still computed but never
     compared;
   - the `hitTarget` check: `elementFromPoint` at the bar's centre must land inside the toolbar.

   Those are exactly the checks that would catch the 460 px defect above. Fix: in the
   `anchor_layout` evaluate, compute `usableTop` as the bottom of `[data-sphinx-preview-sticky-headings]`
   when it is visible, otherwise 0. Then fail with "table action bar is hidden under the sticky band
   or preview controls" when either of these holds:
   - `barTop < usableTop - 1`;
   - `elementFromPoint` at the centre of **each** button returns an element outside the toolbar.
     Use `button.getBoundingClientRect()` for every `[data-sphinx-table-operation]` button. This catches
     the controls pill covering "Col −".

   Keep the new `barBottom <= tableTop + 1` and `covered == 0` conditions.
2. [BLOCKER] src/webview/scrollSync.ts:revealTableToolbar — at 460 px the bar ends up partly under the
   sticky band, and the controls pill covers it (screenshots above). So the reveal does not achieve
   "fully visible just below the band". Investigate in the 460 scenario with the new capture check:
   - Log `readingOffsetValue`, `bar.top` and the band's real `getBoundingClientRect().bottom` at
     reveal time.
   - Check whether a later layout change moves the bar back up after the reveal. Two candidates:
     `applyAnchor` called by autosave/status updates, or the status text changing to "Saving
     Markdown…", which changes the wrap.

   Expected behaviour:
   - After the toolbar appears, and after any later `applyAnchor` while the same table edit is open,
     the toolbar's top must be ≥ the sticky band's bottom. Use the measured band bottom when
     `readingOffsetValue` underestimates it.
   - No toolbar button may sit under the fixed preview controls. Either use the controls' bottom as
     the usable top when they overlap the bar horizontally, or give the menu enough right margin or
     width limit so it never shares the controls' rectangle.

   Keep the "only if the cell stays in the viewport" and "first appearance only" rules. Add a unit test
   in scrollSync.test.ts: the bar is revealed, then a later `applyAnchor` (simulate an autosave
   status change) must not move it above `readingOffsetValue`.
3. [MINOR] scrollSync.ts:revealTableToolbar — the anchor line (`anchor = {line, owner}`) is not
   refreshed after the reveal scroll, unlike `applyAnchor`. Call `lineAtScroll` the same way after
   `programmaticScroll`.
4. [NIT] realInput.test.ts RI-T18 waits a fixed 300 ms with `setTimeout`. Prefer `waitFor` on a stable
   cell top.

## Existing assertions changed
- scrollSync.test.ts table test (BODY parent, data-placement, --menu-top/left): OK, listed in the task.
- previewStyles.test.ts flex-wrap loop split: OK, matches the amendment exactly.
- previewStyles outline `none`: OK, replaced by the 2px solid rule.
- capture.py "missing or hidden", "position fixed" → "static", "parent is body" → "precedes table",
  Save/Cancel wording, outline check: OK, equivalent or stronger.
- capture.py "not aligned with its active cell": NOT JUSTIFIED as written. It drops the
  `controlsBottom` and `hitTarget` checks, which still apply to an in-flow bar (finding 1).

VERDICT: CHANGES REQUESTED
