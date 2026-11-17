# T11 — Enter keeps list indentation and markers in the raw-Markdown editor

| Field | Value |
| --- | --- |
| Fixes | [UX-04](../../01-inline-block-editing/UX-04-enter-breaks-list-structure.md) |
| Decisions | D-03 |
| Depends on | T10 (undo-friendly edits must stay undoable) |
| Gate | `unit trusted visual` |
| Risk | Medium (typing path of every block editor) |
| Commit message | `fix(vscode): continue Markdown lists on Enter in the inline editor` |

## Goal

Pressing Enter in the block textarea continues the construct of the current line, so a new list
item becomes a sibling at the same indentation and never re-parents the following items.

## Context to read first

- `conventions.md` §2 and §3. The logic goes in a **new pure module** that is stringified into the
  runtime.
- `src/webview/scrollSync.ts` → `receiveBlockEditSource`: the block textarea, its `input` and
  `keydown` listeners (Escape, Cmd/Ctrl+Enter, `navigateBlockEdit`).
- The existing tests that must keep passing unchanged:
  - `test/webview/scrollSync.test.ts` → "active Markdown editors leave repeated spaces and Enter to
    native text input". The caret is at offset 0 there, before the marker, so Enter must stay
    native.
  - `test/visual/capture.py` → `check_nested_list_typing`. This one **changes** (see below).

## Allowed files

- `src/webview/textEditing.ts` (new)
- `src/webview/scrollSync.ts`
- `test/webview/textEditing.test.ts` (new)
- `test/webview/scrollSync.test.ts` (add tests)
- `test/visual/capture.py` (`check_nested_list_typing` only)
- `test/integration/realInput.test.ts` (add RI-T11)
- `README.md` (one sentence)

## Pure module `src/webview/textEditing.ts`

```ts
export interface TextEdit { start: number; end: number; text: string; selectionStart: number; selectionEnd: number }
export function createTextEditingTools() {
  function continueOnEnter(value: string, selectionStart: number, selectionEnd: number): TextEdit | undefined;
  return { continueOnEnter };
}
```

Rules for `continueOnEnter`, in order:

1. A non-collapsed selection returns `undefined` (native behaviour).
2. Find the current line: `lineStart = value.lastIndexOf("\n", caret - 1) + 1`, and `lineEnd` (the
   next `\n` or the end of the value).
3. **Inside a fence:** count the lines from the start of the value up to the current line
   (excluded) that match `^\s*(```|~~~)`. If the count is odd, the caret is inside a fenced block:
   carry only the line's leading whitespace. With no leading whitespace, return `undefined`.
4. Parse the prefix of the line:
   - `quote = /^(?:[ \t]*>[ \t]?)*/` (possibly empty);
   - then, on the rest, `list = /^([ \t]*)([-*+]|\d{1,9}[.)])([ \t]+)(\[[ xX]\][ \t]+)?/`.

   `prefixEnd` is the offset where the parsed prefix ends.
5. If the caret is before `prefixEnd` (inside the indentation or the marker), return `undefined`.
6. **Body** = the line text after `prefixEnd`.
7. **Exit case:** the body is whitespace-only and the line has a list marker or a quote prefix.
   Return an edit that replaces `[lineStart, lineEnd)` with `""` (the line becomes empty), with the
   caret at `lineStart`. No line break is inserted.
8. **List continuation:** the new prefix is `quote + indentation + nextMarker + spacing + task`.
   - Bullets keep their character.
   - `N.` becomes `N+1.`, and `N)` becomes `N+1)`.
   - A task box becomes `[ ] `, whatever its state.

   The edit inserts `"\n" + newPrefix` at the caret, replacing nothing, and puts the caret after
   the insertion.
9. **Quote only:** insert `"\n" + quote`.
10. **Plain line with leading whitespace:** insert `"\n" + leadingWhitespace`.
11. Otherwise, return `undefined`.

## Runtime wiring

- Next to `tableTools`, add `const textEditing = (${createTextEditingTools.toString()})();` and
  import the factory at the top of `scrollSync.ts`.
- Add a helper `applyTextEdit(control, edit, onFallbackInput)`:
  1. Focus the control, then `setSelectionRange(edit.start, edit.end)`.
  2. If `typeof document.execCommand === "function"`, call
     `document.execCommand("insertText", false, edit.text)` in a `try`. This keeps the native undo
     stack (T10) and fires `input`.
  3. If that is unavailable or returns `false`, splice `control.value` manually and call
     `onFallbackInput()`.
  4. Finally `setSelectionRange(edit.selectionStart, edit.selectionEnd)`.
- In the block textarea keydown listener, after the `navigateBlockEdit` check and before the
  Escape branch, handle a plain Enter (`key === "Enter"`, no Shift/Alt/Meta/Ctrl, not
  `isComposing`): compute `textEditing.continueOnEnter(textarea.value, textarea.selectionStart, textarea.selectionEnd)`.
  If it returns an edit, call `event.preventDefault()` and apply it with the fallback
  `() => { resizeTextarea(); autosaveBlockEdit(); }`. Otherwise do nothing (native newline).
- Shift+Enter stays native: a bare newline (D-03).

## Tests

Write first, and show the failures:

1. `test/webview/textEditing.test.ts`: a table-driven test of `continueOnEnter`, at least:
   - `- a|` → `\n- `;
   - `      - Dry goods|` → `\n      - `;
   - `1. a|` → `\n2. `; `9) a|` → `\n10) `;
   - `- [x] done|` → `\n- [ ] `;
   - `> quote|` → `\n> `; `> - item|` → `\n> - `;
   - `- |` → the line is emptied, with no line break;
   - `>  |` → emptied;
   - `|- a` (caret at 0) → `undefined`;
   - `plain|` → `undefined`;
   - `    code|` → `\n    `;
   - inside a fence: ```` ```\n- a| ```` → `undefined`, since a fence line without indentation
     carries nothing;
   - a non-collapsed selection → `undefined`;
   - CRLF is not expected in a textarea; no test is needed.
2. `scrollSync.test.ts`: with the fake DOM (no `execCommand`), set
   `textarea.value = "- a"`, put the caret at 3, dispatch keydown Enter → `preventDefault` called,
   `textarea.value === "- a\n- "`, caret at 6, and after `flushTimers()` an autosave carries the new
   text.
3. **Real-input E2E**, scenario **RI-T11**. Fixture: copy
   `test/visual/fixtures/04-code-and-tables.md` or use the nested list from the bug sheet:

   ```markdown
   - Intake
     - Dry goods
       - Refrigerated goods
     - Deduplication
   ```

   Adapt the steps to the actual innermost list the click opens.
   - Edit mode, click "Refrigerated goods", press `${MOD}+End`, press `Enter`, type `Frozen goods`,
     click the heading.
   - Assert that the buffer has `Frozen goods` as a sibling at the same indentation as
     "Refrigerated goods", and that `- Deduplication` keeps its original indentation and line.
   - It must fail before the fix.

## Expected changes to existing tests

- `capture.py` → `check_nested_list_typing`. It currently presses Enter and then types
  ``  - `new-skill` `` expecting a bare newline. Change it to press Enter, assert that the inserted
  text is `"\n  - "` (the continuation of the current list line), then type `` `new-skill` `` and
  assert the final text accordingly. Keep every other check (spaces preserved, focus, caret,
  autocorrect, autosave content).
- No other existing assertion changes. "active Markdown editors leave repeated spaces and Enter to
  native text input" keeps **all its assertions unchanged**.
- **Amended by the orchestrator after round 1 (STOP, test mechanics only).** That test focuses the
  editor with the caret at the **end** of the text (`initialCaretPosition` defaults to `"end"`),
  which is the end of a list line. D-03 makes Enter there a list continuation, so the test fails
  for an intended reason. Fix the test's **setup only**: before the key loop, put the caret at
  offset 0 (`textarea.selectionStart = 0; textarea.selectionEnd = 0;`, or the fake DOM's
  equivalent), where `continueOnEnter` returns `undefined` (rule 5). Add a comment saying why. Do
  not change its assertions. List this change in the report under "Existing assertions changed"
  (setup line only).
- **Amended by the orchestrator after round 1 (second STOP, T09 test follow-up).** T09 made inline
  autosave debounced (400 ms, D-02) but its gate did not include `visual`. In `capture.py` →
  `check_preview_edit_mode`, the check "wrapped table-cell edit did not autosave its updated
  Markdown" reads `window.visualMessages` right after `cell_input.fill(...)`, before the debounce
  fires (scenario 08, dark and light). Replace that immediate `page.evaluate(...)` with
  `page.wait_for_function(...)` on the **same predicate** (non-final `previewEditSave` whose
  `editedText` includes `" updated"`), timeout 2000 ms. On a Playwright timeout, append the same
  failure message. Do not change the predicate or anything else in that function. This is the
  only allowed change outside `check_nested_list_typing`; list it in the report.

## Must not change

- Cmd/Ctrl+Enter commits, Escape (T08), arrow-key navigation (P-E4), and repeated spaces typed
  natively.
- The textarea attributes (`spellcheck`, `autocorrect`, `autocapitalize`, `autocomplete`).
- Which source range a click opens (the innermost list); do not switch to the top-level list.

## Done when

- The `unit`, `trusted` and `visual` gates pass; RI-T11 passes.
- README, "Edit mode" paragraph, gains: "Enter continues lists and quotes; Shift+Enter inserts a
  plain line break."
