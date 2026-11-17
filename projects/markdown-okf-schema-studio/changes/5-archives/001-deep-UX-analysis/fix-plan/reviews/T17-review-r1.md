# T17 review — round 1

Base: 7041461 · Reviewed diff: 4 task files (scrollSync.ts +81/-1, scrollSync.test.ts, realInput.test.ts, README.md)

## Gates
compile/unit/types: PASS (logs/T17-*.log); re-ran `node --test out/test/webview/scrollSync.test.js` locally: 0 failures.
trusted: PASS (logs/T17-trusted.log); RI-T17 red run before fix recorded in logs/T17-red-trusted.log.
visual: PASS vs baseline (0 new failure lines; 4 known moved-coordinate lines).

## Done-when
- [x] Tab / Shift+Tab move between cells, wrapping rows — unit tests + RI-T17 (`one` -> `beta` -> `two`).
- [x] Tab on last cell inserts a row and resumes in its first cell — unit (pending nav {row 3, col 0}) + RI-T17 (`gamma`/`three` row; screenshot 24-table-tab shows `| gamma | three |` and `betaX`).
- [x] Shift+Tab on first header cell is a no-op — unit test.
- [x] Focus loss commits — unit blur tests + RI-T17 `showTextDocument` part (buffer gets `oneQ`).
- [x] Escape anywhere commits — unit test (document keydown, single save).
- [x] README sentence added.

## Protected features checked
P-E5 cell switching by click: `switchTableCell` untouched; blur check is guarded by the capture-phase pointerdown timestamp (blur fires at pointerdown, the 0 ms timeout runs well inside 500 ms), and additionally bails when `edit.tableInput !== input` after the switch re-renders. Edits are stored in the model by `switchTableCell` before the switch. Existing cell-switch tests pass unchanged.
P-E5 toolbar: pointerdown on a toolbar button -> textarea blur -> check skipped (< 500 ms); the button click handler calls `rememberCellValue()` then `renderTableCellEditor`, which replaces `tableInput`, so the stale check bails. Escape with focus on a toolbar button now commits (desired). Header/last-body-row delete guards untouched.
P-E5 after the guard: when no click is in progress, blur commits through `postBlockEditSave(true)`, which serializes the full model including the current cell (`input` listener keeps the model current), so nothing is lost. Inside a click, the edit stays open with autosave active, so no edit is lost either.
P-E5 arrow navigation / Enter: Tab handled before `navigateBlockEdit`, only for Tab; Enter/Escape branches unchanged.
P-E8 read-only: new listeners act only when `activeBlockEdit` has a `selectedCell`, which requires edit mode.
Conventions §2: no backticks or `${` in the template additions, `window.setTimeout` used.

## Findings
1. [MINOR] scrollSync.ts:commitCellEditorOnFocusLoss — a click in the cell followed by switching to another VS Code editor within 500 ms leaves the cell editor open (blur ignored). No data loss (autosave keeps running), documented in the report. Follow-up option: re-check once on `window` `focus`/`blur` or after the guard expires. No change required for this task.
2. [NIT] Diff vs base also shows `book/chapters/05-skills.md`; that is the user's pre-existing working-tree change (listed in the initial git status), not T17 work. Exclude it from the T17 commit.

## Existing assertions changed
None (test diff contains only additions plus the harness widening of fake `rows`/`cells`, which is OK).

VERDICT: PASS
