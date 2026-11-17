# T11 review — round 1

Base: aa43cbf · Reviewed diff: 8 files (6 modified + 2 new), about +330/-8 (excluding
`book/chapters/05-skills.md`, which is user WIP outside the extension and not part of `diff.sh`)

## Gates
- unit: PASS (logs/T11-unit.log). Re-run by the reviewer: `textEditing.test.js` and
  `scrollSync.test.js` pass, 103/103.
- types: PASS (logs/T11-types.log)
- trusted: PASS incl. RI-T11 (logs/T11-trusted.log, line 348 `PASS real-input screenshot:
  17-enter-continues-list`)
- visual: PASS vs the T00 baseline, 0 new failure lines (logs/T11-visual.log). The remaining
  `preview-sticky-headings-*` failures are baseline.

## Done-when
- [x] Enter continues bullets, numbers (`.`/`)`), tasks, quotes, quote+list, and indentation.
  Evidence: the `textEditing.test.ts` table (21 cases plus a non-collapsed selection case) covers
  every case the task requires, and adds `-| a`, mid-body split, closed fence, and fence indent.
- [x] Exit on an empty item empties the line with no break. Evidence: cases `- |`, `>  |`,
  `a\n  - |\nb`, and the scrollSync test "Enter on an empty list item empties the line…".
- [x] Native Enter in plain text, before the marker, inside an unindented fence, and with
  Shift+Enter. Evidence: the table cases and the scrollSync test "Enter in a list item continues
  the list, and Shift+Enter stays native".
- [x] Wiring: the factory is stringified next to `tableTools`. `applyTextEdit` focuses, selects,
  uses `execCommand` (keeps the T10 undo), and otherwise splices and calls the fallback
  (resize + autosave). The plain-Enter branch sits after `navigateBlockEdit` and before Escape,
  and is gated on no modifiers and `!isComposing`.
- [x] RI-T11 passes. The screenshot `.artifacts/real-input-qxphEa/17-enter-continues-list.png`
  shows `    - Frozen goods` as a sibling of "Refrigerated goods", with `  - Deduplication`
  unchanged in both the buffer and the preview.
- [x] README sentence added verbatim in the Edit mode paragraph.

## Protected features checked
- P-E3 (line breaks/trailing newline): the autosave in the unit test carries `"- a\n- \n"`, so the
  trailing line ending is kept. RI-T11 compares the full buffer byte for byte.
- P-E4 (arrow navigation): `navigateBlockEdit` still runs before the new branch. Existing tests
  are unchanged and pass.
- Cmd/Ctrl+Enter and Escape (T08): the new branch excludes meta/ctrl. Escape is not Enter. The
  code after the branch is unchanged.
- Repeated spaces / native Enter: the "active Markdown editors leave repeated spaces…" test keeps
  all its assertions. Only the caret-setup line was added (amendment 1).
- T10 undo: the edit goes through `execCommand`, which keeps the native undo stack.
  `keepUndoInControl` still runs first.
- Textarea attributes: untouched.
- P-E8 (read-only): the branch lives only inside the block textarea, which is never created in
  read-only mode. No new path.
- P-S2/P-S4: no new message types and no `innerHTML`.
- Conventions §2 (runtime template): the new runtime code has no backticks or `${` (the module's
  fence regex backticks arrive through `${…toString()}` interpolation, like `tableTools`). It has
  no unescaped backslashes and no global `setTimeout`.

## Findings
1. [MINOR] test/integration/realInput.test.ts:`scenarioEnterContinuesList` — the report says
   RI-T11 was not run red before the fix (checklist item 9). By inspection it is a meaningful
   test: with native Enter, "Frozen goods" lands at column 0 and the exact-buffer comparison
   fails. The two unit-level runtime tests were shown red. No action is needed for this task.
   For future interaction tasks, run the E2E scenario once against the base code first and paste
   the failure.
2. [MINOR] src/webview/scrollSync.ts:`applyTextEdit` — for the exit case (empty text and a
   non-empty range) it calls `execCommand("delete")` instead of the specified
   `execCommand("insertText", false, "")`. Both behave the same and both keep undo, so this is
   acceptable. No change requested.
3. [NIT] src/webview/textEditing.ts:`continueOnEnter` — a thematic break written `* * *` or
   `- - -` parses as a list item, so Enter after it inserts `\n* `. This is rare and harmless,
   and could be a follow-up.

## Existing assertions changed
- scrollSync.test.ts "active Markdown editors leave repeated spaces and Enter to native text
  input": only the setup line `textarea.setSelectionRange(0, 0)` and a comment were added. All
  assertions are unchanged. OK (amendment 1).
- capture.py `check_nested_list_typing`: Enter now expects `"\n  - "` (a new assertion), and the
  typed text drops the manual `  - `. The other checks are kept. A `wait_for_timeout(600)` was
  added before reading the autosave because of the T09 debounce. This is test mechanics, not a
  weakening. OK.
- capture.py `check_preview_edit_mode`: the immediate evaluate became `wait_for_function` with the
  same predicate, a 2000 ms timeout, and the same failure message. OK (amendment 2).

VERDICT: PASS
