# T14 — The caret lands where the user clicked

| Field | Value |
| --- | --- |
| Fixes | [UX-06](../../01-inline-block-editing/UX-06-caret-ignores-click-position.md) |
| Decisions | D-21 |
| Depends on | T12 |
| Gate | `unit trusted` |
| Risk | Low (falls back to today's behaviour) |
| Commit message | `fix(vscode): place the inline caret at the clicked word` |

## Goal

Clicking a word in edit mode opens the raw-Markdown editor with the caret at, or next to, the
corresponding source character, in the common cases: paragraphs (also with emphasis and links),
list items, headings, and code blocks.

When the mapping is not confident, the caret goes to the end of the block, as today (D-21).
Keyboard activation and arrow navigation keep their `"start"`/`"end"` behaviour.

## Context to read first

- `src/webview/scrollSync.ts`: the document `click` listener that calls
  `openMappedEditor(target, event.target)`; `openMappedEditor`, `openBlockEditor`
  (`initialCaretPosition`), `receiveBlockEditSource`, and `focusTextControlAtLastContent(control, caretPosition)`.
- `src/webview/textEditing.ts` (T11/T12).

## Allowed files

- `src/webview/textEditing.ts`
- `src/webview/scrollSync.ts`
- `test/webview/textEditing.test.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T14)
- `test/visual/capture.py` (only the block-editor caret check; added by the orchestrator after
  round 1, see "Expected changes to existing tests")

## Design

### 1. Capture the click context (webview)

In the mapped-block click listener, before calling `openMappedEditor`, compute
`clickContext(editingElement, event.clientX, event.clientY)`:

- The editing element is what the editor will replace: the closest `ul, ol` for list items,
  `target.closest("pre")` for code, otherwise the target. Factor out the same decision
  `openMappedEditor` makes; do not duplicate it divergently.
- Use `document.caretRangeFromPoint?.(x, y)` (Chromium), or
  `document.caretPositionFromPoint?.(x, y)` (`offsetNode`, `offset`). If neither exists, or the
  node is not inside the editing element, the context is `undefined`.
- Walk the editing element's text nodes in order (TreeWalker, `NodeFilter.SHOW_TEXT` = 4) to get
  `renderedOffset`, then take `before = text.slice(max(0, o - 32), o)` and
  `after = text.slice(o, o + 32)` from the full `textContent`.
- Pass `{ before, after }` as `initialCaretPosition` (an object instead of `"start"`/`"end"`).
  Keep `rememberPendingBlockNavigation` working with strings only: object values are not
  persisted.

### 2. Map the context to a source offset (pure)

Add to `createTextEditingTools`:

```ts
mapRenderedCaret(source: string, before: string, after: string): number | undefined
```

- **Projection:** build `projected` from `source` plus `indexMap` (projected index → source index).
  - Skip Markdown syntax characters: `*`, `_`, `` ` ``, `~`, and `#` at a line start (with its
    following spaces).
  - Skip list markers at a line start (`[-*+] ` or `\d+[.)] `, with indentation), and `>` quote
    markers.
  - Skip link destinations: when `](` is found, skip up to the matching `)`; skip `[` and `]`.
  - Collapse every run of whitespace, line breaks included, into one space.
- Normalize `before` and `after` the same way: collapse whitespace; the rendered text has no
  syntax characters.
- Search in `projected`, in this order, and stop at the first unique hit:
  1. `before + after`;
  2. `before.slice(-12) + after.slice(0, 12)`;
  3. `before.slice(-12)` (the caret goes after the match);
  4. `after.slice(0, 12)` (the caret goes at the match start).

  A candidate with more than one occurrence is skipped. Empty strings never match.
- Return `indexMap[hit]` translated to the source caret position (at the end of the source when
  the hit lies past the last mapped character), or `undefined`.

### 3. Apply it

In `focusTextControlAtLastContent` (or in a small wrapper used by `receiveBlockEditSource`): when
`caretPosition` is an object, use
`textEditing.mapRenderedCaret(control.value, caretPosition.before, caretPosition.after)`. If it is
`undefined`, fall back to `"end"`.

## Tests

Write first, and show the failures:

1. `textEditing.test.ts`, table-driven `mapRenderedCaret`:
   - a three-line paragraph, clicking in the first word → offset on line 1;
   - `Some **bold** text` with `before = "Some bo"` → offset inside `bold`, after `bo`;
   - `See [the label](https://x.y/z) here` with `before = "See the la"` → inside `label`;
   - `- Dry goods\n- Refrigerated goods` with `before = "Dry"` → line 1;
   - `## Title here` with `before = "Tit"` → after `Tit`;
   - an ambiguous `a a a a` → `undefined`;
   - no match → `undefined`.
2. `scrollSync.test.ts`: with no `caretRangeFromPoint` in the fake DOM, opening a block behaves as
   today (caret at the end). The existing tests prove it; add one explicit assertion.
3. **Real-input E2E**, scenario **RI-T14**:
   - fixture paragraph `Alpha bravo charlie\ndelta echo foxtrot\ngolf hotel india.`;
   - in edit mode, click on the word `bravo` (use `locator.click({ position })`, or click the
     text locator `getByText("bravo", { exact: false })` at its left edge);
   - type `X`, then `${MOD}+Enter`;
   - assert that `X` landed on source line 1, within `bravo` or immediately next to it.

   It must fail before the fix (today `X` lands after `india.`).

## Expected changes to existing tests

None in the unit or integration suites: they open editors without coordinates and keep the end or
start caret.

**Amended by the orchestrator after round 1 (STOP, test mechanics only).** `test/visual/capture.py`
clicks the centre of a title, paragraph, admonition or list item in a real browser, and its check
"`{edit_target} editor has no caret at the end of its last content line`" asserts
`selectionStart === value.trimEnd().length`. With UX-06/D-21 the caret now lands at the clicked
word, so it fails in 7 lines (`edit-admonition-dark`, `edit-list-narrow`, `edit-paragraph-dark`,
`edit-mode-dark`, and their rendering-check lines). Replace that check with one that verifies the
**new** behaviour, no weaker than before:

1. Just before `target.click()`, for `edit_target in {"title", "paragraph", "admonition", "list"}`,
   record `clicked_word` with `target.evaluate(...)`: take the centre of the target's
   bounding box (the point Playwright clicks), call `document.caretRangeFromPoint(x, y)`, and if it
   lands in a text node, expand to the surrounding word characters (`/[\p{L}\p{N}_-]/u`). Keep it
   only when it has at least 3 characters; otherwise use `None`.
2. In the check, keep `document.activeElement === element`, a collapsed selection
   (`selectionStart === selectionEnd`) and `caretColor !== "transparent"`. Then:
   - when `clicked_word` is set: `value.slice(Math.max(0, s - 40), s + 40)` must include
     `clicked_word` (pass it as the `evaluate` argument);
   - when it is `None`: the D-21 fallback, `s === value.trimEnd().length` (today's assertion).
3. Rename the failure message to `"{edit_target} editor caret is not at the clicked word"` and
   append the observed `selectionStart` and `clicked_word` for diagnosis.

Do not change any other check in `capture.py`. List this change in the report.

## Must not change

- Arrow-key navigation start/end carets (P-E4), keyboard activation, table cell editors (they
  keep their own caret logic), and `pendingBlockNavigation` persistence.

## Done when

- The `unit` and `trusted` gates pass; RI-T14 passes.
