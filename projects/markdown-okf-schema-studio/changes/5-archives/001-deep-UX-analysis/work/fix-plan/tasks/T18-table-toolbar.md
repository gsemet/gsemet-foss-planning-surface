# T18 — The table toolbar never covers cells

| Field | Value |
| --- | --- |
| Fixes | [UX-14](../../02-table-editing/UX-14-table-toolbar-covers-content.md) |
| Decisions | D-18 |
| Depends on | T17, T03 |
| Gate | `unit trusted visual` |
| Risk | Medium (P-E5 toolbar; R7 anchoring while it appears) |
| Commit message | `fix(vscode): place the table toolbar above the table with readable labels` |

## Goal

While a cell editor is open:

- the table toolbar sits **in the document flow, directly above the table**, so it never covers
  any row;
- each action shows a short text label next to its icon: `Row +`, `Row −`, `Col +`, `Col −`;
- the position text reads `Header · column 2 of 5`, or `Row 2 of 6 · column 2 of 5`. Body rows
  are counted from 1, without the header;
- the selected cell has a visible focus outline.

## Context to read first

- `src/webview/scrollSync.ts` → `renderTableCellEditor`:
  - the `menu` creation: appended to `document.body`, with `position: fixed` placement through
    `positionMenu` and the scroll/resize listeners;
  - `addAction`, and `edit.status.textContent = "Row " + …`;
  - `closeBlockEdit`, which removes `edit.tableMenu` and the position listeners.
- `src/preview/previewStyles.ts`: `.sphinx-preview-table-menu` rules, and
  `html[data-sphinx-preview-edit-mode="on"] [data-sphinx-preview-table-cell-selected="true"] { outline: none; }`.
- `beginEditAnchor(selectedCell)` keeps the cell fixed on screen when the toolbar insertion shifts
  the table (R7).

## Allowed files

- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/webview/scrollSync.test.ts`
- `test/webview/previewStyles.test.ts`
- `test/visual/scenarios.ts` (`machineChecks` on the table-cell scenarios)
- `test/visual/capture.py` (only assertions about the old floating placement)
- `test/integration/realInput.test.ts` (add RI-T18)

## Steps

1. Write the tests first and record the failures.
2. **Placement.** Insert the menu as the previous sibling of the table's outermost wrapper (the
   `table` itself, or its closest wrapper element whose only child is the table), not into
   `document.body`.
   - Remove `positionMenu`, its listeners, and the `--sphinx-preview-table-menu-*` properties.
   - Keep `edit.tableMenuPositionListener` handling in `closeBlockEdit` harmless (it may simply be
     undefined).
   - Keep the element's class, `role`, `aria-label`, `data-sphinx-table-menu`, and the button
     attributes unchanged: tests query them.
3. **CSS** for `.sphinx-preview-table-menu`:
   - `position: static`;
   - `margin: 0 0 6px`;
   - keep `display: flex`, `gap` and the colours;
   - `flex-wrap: wrap`;
   - drop `top`/`left` and the max-width calc that existed for fixed placement.

   Buttons: `width: auto; padding: 0 8px; gap: 4px; display: inline-flex; align-items: center; border-radius: 14px;`.
   Add a `span.sphinx-preview-table-menu-label` inside each button after the SVG.
4. **Labels.** In `addAction`, append the label span: `Row +` for insert row, `Row −` for delete
   row, `Col +` for insert column, `Col −` for delete column. Keep `aria-label`, `title` and
   `data-tooltip` as they are.
5. **Status.** With `bodyRows = edit.tableModel.rows.length - 2` and
   `columns = edit.tableModel.rows[0].length`:
   - header: `"Header · column " + (c + 1) + " of " + columns`;
   - body: `"Row " + r + " of " + bodyRows + " · column " + (c + 1) + " of " + columns`, where `r`
     is `edit.tableRowIndex` (rendered index; body rows start at 1).
6. **Selected-cell outline.** Replace the `outline: none` rule with
   `outline: 2px solid var(--vscode-focusBorder, Highlight); outline-offset: -2px;`.
7. **Visual.** In `scenarios.ts`, add `machineChecks: ["overlay-covers-text", "overlay-clipped"]`
   to every scenario that captures an open table cell editor (search for the table `editTarget`).

## Tests

**Unit:**

- After opening a cell, the menu's parent is the table's parent, not `body`; it precedes the
  table.
- The status text matches the new format for the header and for a body cell.
- Each button contains its label text.
- `closeBlockEdit` removes the menu.

Extend the fake DOM's `insertBefore` and `parentElement` support only as needed.

**`previewStyles.test.ts`:** the new menu rules and the outline rule.

**Real-input E2E**, scenario **RI-T18** (the T02 `smoke.md` table):

- Click `one` → `capture(..., { checks: { required: ["overlay-covers-text", "overlay-clipped"] } })`.
- Assert the status text `Row 1 of 2 · column 2 of 2`.
- Assert that the selected cell's viewport top moved by at most 2 px between before the click and
  after the toolbar appeared (R7).

## Amendment after round 1 — the toolbar must be visible when it appears (orchestrator)

Round 1 showed that at 460 px the labelled bar wraps to two rows (about 76 px). When the clicked
cell is near the top of the viewport, the R7 anchor keeps the cell fixed, so the bar inserted above
the table ends up above the viewport (`edit-table-wrapped-*-460`: bar at y = -28, clipped). UX-14
requires a toolbar the user can use; an off-screen toolbar is not acceptable, and the visual
scenarios must **not** be changed to hide this case. Add this rule, inside D-18:

1. After the toolbar is inserted for a table and the R7 anchor has been restored, call
   `refreshReadingOffset()` and measure `toolbarRect = menu.getBoundingClientRect()`. The usable top
   is `readingOffsetValue` (the strip reserved for the sticky heading band; 0 without it).
2. If `toolbarRect.top < usableTop`, scroll the preview up by `usableTop - toolbarRect.top` (the
   bar becomes fully visible just below the band), **only if** the selected cell's bottom stays
   inside the viewport after that scroll. Otherwise keep today's R7 behaviour.
3. Do it only when the toolbar first appears for a table, not on every cell switch inside the same
   table, so moving between cells never makes the page jitter.
4. Use the same scrolling primitive the runtime already uses for programmatic scrolls, so the
   scroll-sync code treats it as preview-owned, not as a user scroll. Read how `beginEditAnchor` and
   the edit-anchor restore scroll the page, and reuse that path.
5. Tests: a unit test in `scrollSync.test.ts` where the fake menu rect is above the usable top →
   one scroll by the exact delta; one where it is visible → no extra scroll; one where revealing
   would push the cell out of the viewport → no extra scroll. RI-T18's "cell moves at most 2 px"
   assertion stays as is (it clicks a cell away from the top).
6. Visual: the `edit-table-wrapped-*-460` scenarios must pass their "outside the screenshot viewport"
   and `overlay-clipped` checks with `scenarios.ts` scroll positions unchanged.

## Expected changes to existing tests

- `scrollSync.test.ts` table tests asserting:
  - the menu is appended to `body`;
  - `data-placement`, or the `--sphinx-preview-table-menu-left`/`-top` properties;
  - the old status text `Row N, column M`.

  These change to the new placement and format. List each one.
- `previewStyles.test.ts` assertions on `position: fixed` for `.sphinx-preview-table-menu`, and on
  `outline: none` for the selected cell. List each one.
- `capture.py`: checks of the floating placement. List each one.
- **Amended by the orchestrator after round 1 (STOP, contradicts step 3).**
  `previewStyles.test.ts` → "control tooltips retain their offset while sticky headings remain at
  the top" loops over `["table", "frontmatter"]` and asserts `flex-wrap: nowrap` for both menus.
  Step 3 (D-18) makes the table menu `flex-wrap: wrap`. Replace the loop with two explicit
  assertions: the frontmatter menu keeps `flex-wrap: nowrap` (unchanged), and the table menu now
  asserts `flex-wrap: wrap;` with the same regex shape. Do not touch the other assertions of that
  test. List this in the report.

## Must not change

- The toolbar's actions and guards. The frontmatter menu (T23 handles it).

## Done when

- The `unit`, `trusted` and `visual` gates pass, with the table scenarios' required machine checks
  passing.
- The reviewer looked at the table-cell screenshots: the toolbar is above the table, labels are
  readable, and the selected cell is outlined.
