# UX-06 — The caret always lands at the end of the block, not where the user clicked

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (paragraph, list, admonition, code block) |
| Area | Inline block editing |
| Evidence | Probe results: clicking "Dry goods" put the caret at offset 44/44, after "Refrigerated goods"; clicking a 326-character paragraph put it at 326/326 |

## Use case

An author spots a typo in the middle of a long paragraph and clicks on the misspelled word to fix
it.

## Steps to reproduce

1. Edit mode on, click the first word of a multi-line paragraph or the first item of a list.
2. Start typing.

## Expected

The caret is placed at (or near) the clicked character, as in every WYSIWYG editor.

## Observed

The textarea opens with the caret after the last non-whitespace character of the block. The user
must navigate back with the keyboard or click a second time inside the textarea, whose layout
differs from the rendered text (raw Markdown, different wrapping).

## Where it comes from

`src/webview/scrollSync.ts` `focusTextControlAtLastContent` (L841-L851) only supports `"start"` or
`"end"`; `openBlockEditor` (L1409-L1470) does not record the clicked text offset.

## Suggested direction

Capture the click position with `document.caretPositionFromPoint` (or `caretRangeFromPoint`),
map the rendered text offset to a source offset (approximate mapping per line is enough: the block
knows its source lines and paragraphs keep `lineTops`), and place the caret there.

## Test to add

E2E: click the first word of a three-line paragraph, type a character, assert the character was
inserted on the first source line.

## Done when

Clicking a word and typing edits that word in the common cases (plain paragraph, list item,
heading).
