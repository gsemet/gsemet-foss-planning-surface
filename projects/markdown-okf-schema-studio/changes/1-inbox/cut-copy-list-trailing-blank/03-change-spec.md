# Cut and copy drop a block's trailing blank lines, as Delete block

Cut and copy of a list followed by blank lines are refused today with "The preview is out of date.
Refresh it and try again.". After this change they work like Delete block and a move: the host drops
the blank lines at the end of the range before it plans the copy or the cut.

## Goal

A writer selects a list that has blank lines after it (or a selection that ends on such a list) and
presses Cmd/Ctrl+C or Cmd/Ctrl+X in edit mode. The copy puts the list's Markdown on the clipboard
with no trailing blank lines. The cut does the same and then removes the list. The document keeps one
blank-line separator and gains no blank lines, as Delete block leaves it on the same range.

## Base

Work from `origin/main` at or after `5a84db8b` (version 1.11.0), which holds CR-439 (empty-block
cleanup and Delete block: `719d9140`). The local `main` checkout may be older, so rebase on
`origin/main` first. All files below are named as they are on `origin/main`.

## Why it is refused today

- The renderer maps a list to the blank lines after it, so the page sends a copy or cut range whose
  `endLine` is a blank line (`src/page/features/blockSelectionView.ts`, `previewBlocksCopy` /
  `previewBlocksCut`).
- `planBlocksCopyCut` (`src/core/edits/sourceEdits.ts`) passes that range unchanged to `spanText` and
  `planCut` (`src/core/mapping/blockRange.ts`). Both call `checkSpan`, which refuses a span whose last
  line is blank (`OUT_OF_DATE`).
- `planBlockMoveEdit` and `planBlocksDelete` in the same file first call
  `withoutTrailingBlankLines(text, { line, endLine })`. This decides cc-Q1 and cc-Q2.

## What changes

### Code: `src/core/edits/sourceEdits.ts` only

In `planBlocksCopyCut(text, line, endLine, op)`:

1. First compute `const span = withoutTrailingBlankLines(text, { line, endLine });`, as
   `planBlocksDelete` does.
2. Use `span.line` and `span.endLine` everywhere the function uses `line` and `endLine` now: in
   `spanText` (the copied text), in `linesOpenInclude` (the include refusal) and in `planCut` (the cut
   edit and `followingLine`).
3. Leave the order of the checks and the refusal texts as they are: `spanText`'s refusal, then
   `COPY_INCLUDED`, then `planCut`'s refusal.
4. Update the JSDoc: the span's trailing blank lines are dropped first (a list mapped up to its blank
   separator), as Delete block and a move do.
5. Add `@implements_req SwRS-MDOKFSTUDIO-BLOCK-166` and `@implements_req SwRS-MDOKFSTUDIO-BLOCK-169`
   above `planBlocksCopyCut`. That is two IDs, within the marker-block limit of 3.

This is not a list-only fix (cc-Q2). `planBlocksCopyCut` is the one host path for every copy and every
cut, of any block or selection. So any range that ends on blank lines is trimmed: a list, a list item,
or a selection whose last block is a list.

These stay as they are:

- `withoutTrailingBlankLines`: no change to it or to its `@implements_req SwRS-MDOKFSTUDIO-BLOCK-117`
  marker. It returns an out-of-bounds or non-integer range unchanged, and it never goes above `line`.
  So these are still refused with `OUT_OF_DATE`: a range of blank lines only, a range that starts on a
  blank line, and a range past the end of the text.
- `planCut`, `spanText` and `checkSpan` in `blockRange.ts`. Called directly, they still refuse a span
  that ends on a blank line, and their unit tests keep that.
- `handleBlocksCopyCut` in `src/session/features/sourceEdits.ts`. It already pins on `line` (the
  first line, which does not change) and posts what the plan returns.
- The page. It keeps sending the range as it is mapped.

### What the result is (cc-Q1, cc-Q3)

- **Copy:** the clipboard holds the lines `span.line`..`span.endLine` exactly, with the document's own
  line breaks, no trailing line break and no trailing blank lines. The document does not change.
- **Cut:** the same clipboard text. The edit is `planCut` on the trimmed span, with the existing cut
  rules of SwRS-MDOKFSTUDIO-BLOCK-169, which are also the rules of CR-439's Delete block:
  - In the middle, the block goes with the blank lines after it. The blocks around it stay one blank
    line apart.
  - When the block above touches the span, the blank lines after it stay.
  - The last block goes with the blank lines before it, and the final line break is kept or left out
    as before.
  - The only block empties the body.
  So a cut adds no blank lines, and on the same range it gives exactly the text Delete block gives
  (`planBlocksDelete`). `followingLine` is set as in `planBlocksDelete`.

Example (LF): the text `Para\n\n- a\n- b\n\n\nNext\n` with range 3..6.

- Copy gives `- a\n- b`.
- Cut gives the clipboard `- a\n- b` and the document `Para\n\nNext\n`, with `followingLine` 7.
- On the last block, `Para\n\n- a\n- b\n\n\n` with range 3..6 gives `Para\n`.

### Requirements (okfreq)

Read `requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change") first. Edit the authored text only; never the generated fields or link blocks.

- **SwRS-MDOKFSTUDIO-BLOCK-166** (copy): in the host table "The host puts the exact Markdown on the
  clipboard", add the row "A list whose range ends on the blank lines after it (the renderer maps it
  so), followed by two blank lines" → "The clipboard holds the list's lines without the blank lines
  after it, and the document is unchanged". Add this test to the Verification notes method on
  `test/core/edits/sourceEdits.test.ts`, and the real-input step to scenarioBlockSelection.
- **SwRS-MDOKFSTUDIO-BLOCK-169** (cut):
  - Normative behaviour and description: "after the span's trailing blank lines are dropped (a list
    mapped up to its blank separator)".
  - In the boundary table "Where the cut span sits in the document", add the row "A list in the
    middle whose range ends on the two blank lines after it" → "The clipboard holds the list without
    the blank lines; the list and the blank lines after it go, and the blocks around stay one blank
    line apart, as Delete block leaves them".
  - Add to the Criteria: "trailing blank lines of the span are dropped before spanText and planCut".
  - Add the new unit test and the real-input scenario to Verification notes.
- **SwRS-MDOKFSTUDIO-BLOCK-124** (refused ranges): change the row "A cut that starts or ends on a
  blank line" to "A copy or cut that starts on a blank line, or covers blank lines only" → the same
  refusal. Add the note "(blank lines at the end of a copy or cut range are dropped before the check,
  see SwRS-MDOKFSTUDIO-BLOCK-166 and SwRS-MDOKFSTUDIO-BLOCK-169)", the same way its move row cites
  BLOCK-117. This changes what the host refuses, which is the point of this CR. The refusal tests that
  exist stay valid: the integration cut of line 8..8 starts on a blank line, and the core
  `planCut`/`spanText` tests call the core directly.
- **SwRS-MDOKFSTUDIO-BLOCK-265** (Delete block): no change to its text. It already says that the
  trailing blank lines are dropped.
- Run `just requirements-update` and commit the generated files. Add a dated entry in
  `requirements/tiers/log.md` (2026-11-2x: copy and cut drop the trailing blank lines of a range,
  as Delete block does; BLOCK-166, BLOCK-169 and BLOCK-124 updated).

### Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md`: "Copy and cut of a list followed by
blank lines no longer fail with 'The preview is out of date'; the list is copied without the blank
lines and a cut leaves one blank line between the blocks around it."

### Writing skill

No change: no rendered syntax changes.

## Evidence (cc-Q4)

Each new test must fail on the code from before this change: there, the request is refused with
`OUT_OF_DATE`.

### Unit tests: `test/core/edits/sourceEdits.test.ts`

Loop over LF, CR LF and lone CR, as `test/core/edits/blocksDelete.test.ts` does with its `EOLS` and
`join`. Mark each test `@tests_req SwRS-MDOKFSTUDIO-BLOCK-166` and/or `@tests_req
SwRS-MDOKFSTUDIO-BLOCK-169`, the one it checks.

1. A list in the middle followed by two blank lines, `join("Para", "", "- a", "- b", "", "", "Next", "")`,
   range 3..6:
   - copy gives `{ copied: join("- a", "- b") }`;
   - the cut's `copied` is the same, applying `cut.edit` gives `join("Para", "", "Next", "")`, and
     `followingLine` is 7;
   - the result has no run of three line breaks.
2. A list as the last block followed by two blank lines, `join("Para", "", "- a", "- b", "", "", "")`,
   range 3..6: the cut gives `join("Para", "")`, `followingLine` is `undefined`, and the clipboard
   text is `join("- a", "- b")`.
3. A selection of two blocks that ends on a list with its trailing blank line,
   `join("Alpha", "", "- a", "- b", "", "Omega", "")`, range 1..5: copy gives
   `join("Alpha", "", "- a", "- b")`, and the cut leaves `join("Omega", "")`.
4. Same result as Delete block. For each range of tests 1 to 3, and for a list that touches the block
   above, `join("Para", "- a", "- b", "", "", "Next", "")` with range 2..5, the cut's edit applied
   gives the same text as `planBlocksDelete` on the same range, and the same `followingLine`.
5. Still refused. A range of blank lines only (`join("A", "", "", "B", "")`, range 2..3), a range that
   starts on a blank line, and a range past the end still give `"refused"` for both copy and cut.
   This test checks SwRS-MDOKFSTUDIO-BLOCK-124, so mark it `@tests_req SwRS-MDOKFSTUDIO-BLOCK-124`.

The existing tests in `test/core/mapping/blockRange.test.ts` (`spanText refuses bad ranges...`,
`cut refuses the frontmatter and bad ranges`) and the existing `planBlocksCopyCut` tests stay
unchanged and must pass.

### Real-input scenario: `scenarioBlockSelection` in `test/integration/realInput/blockKeys.ts`

Extend the existing scenario. Add a second `withDocument` block at its end, so the steps that exist
keep their document. The new block uses the document
`["# Clip", "", "Alpha paragraph.", "", "- item a", "- item b", "", "", "Omega paragraph.", ""].join("\n")`,
a list followed by two blank lines. Its steps:

1. Open the side preview, wait for the render, and turn edit mode on.
2. Select the list block alone, with the keyboard or a Shift+click on the list. Wait until exactly
   one block is selected and its text holds "item a".
3. Sanity check: read the list's mapped range from the page, as the page sends it. Assert that its
   last line is blank in the document. This proves that the step goes through the trimmed path.
4. Copy. Write a sentinel to the clipboard, press `${MOD}+C`, and wait for the clipboard to read
   `"- item a\n- item b"`. Assert that `bufferText(document)` is unchanged.
5. Cut. Press `${MOD}+X` with the list still selected, or selected again. Wait for the clipboard to
   read `"- item a\n- item b"` and for the buffer to equal
   `["# Clip", "", "Alpha paragraph.", "", "Omega paragraph.", ""].join("\n")`, which has one blank
   line between Alpha and Omega and no `\n\n\n`.
6. Take the screenshot `captureAfter(evidence, page, "block-editing/r<next free number>-cut-list-trailing-blank", "<what it shows>")`.
   Use a number no other capture uses.
7. Restore the clipboard in a `finally`, as the scenario does now.
8. Add `@tests_req SwRS-MDOKFSTUDIO-BLOCK-169` to the scenario's marker block. It then names
   BLOCK-254, StRS-BLOCK-016 and BLOCK-169. If that goes past the marker-block limit (3 distinct IDs),
   put the new marker on the new block's code instead.

Real VS Code scenarios run on pushes to `main` or on a heavy dispatch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`), not on a pull request. So the PR shows one
heavy run in which `scenarioBlockSelection` passes, along with the new screenshot.

### Gates

`just check` (unit, markers, file size: `blockKeys.ts` is at 624 lines, within the limit of 1 500),
`just requirements-lint`, `just requirements-update` with no diff left, and `just preflight`.

## Out of scope

- No change to the page, to the renderer's mapping of lists, or to `checkBlockLines`.
- No change to `planCut`'s rules, to Delete block, to paste, or to blank-run removal.
- The integration test `test/integration/blockClipboard.test.ts` gets no new case. cc-Q4 names unit
  tests and the real-input scenario.
- Moves are not touched: they already trim.
