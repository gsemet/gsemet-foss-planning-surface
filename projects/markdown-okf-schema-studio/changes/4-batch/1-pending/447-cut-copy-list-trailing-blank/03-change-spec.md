# Cut, copy and paste work on a list followed by blank lines

In edit mode, a list followed by blank lines cannot be cut, copied, or pasted after. The host refuses
each request with "The preview is out of date. Refresh it and try again.". After this change:

- the host drops the CommonMark blank lines at the end of a copy or cut range before it plans the
  copy or the cut, as Delete block and a move already do;
- the host accepts a paste anchored on the blank line that ends a list.

## Goal

A writer selects a list that has blank lines after it, or a selection that ends on such a list, in
edit mode.

- **Cmd/Ctrl+C** puts the list's Markdown on the clipboard, with no trailing blank lines.
- **Cmd/Ctrl+X** does the same and then removes the list. The document keeps one blank-line separator
  and gains no blank lines, exactly as Delete block leaves it on the same range.
- **Cmd/Ctrl+V** inserts the clipboard after the list. The new block has one blank line before it and
  one after it, and it reuses the blank lines already there, so no blank line is gained.

Only real blank lines are dropped: lines of spaces and tabs only. A selection that ends on a line
holding only a no-break space (a paragraph in CommonMark) is still refused, so nothing is left out
without the writer knowing.

## Base

Work from `origin/main` at or after `5a84db8b` (version 1.11.0), which holds CR-439 (empty-block
cleanup and Delete block, `719d9140`). The local `main` checkout may be older, so rebase on
`origin/main` first. All files below are named as they are on `origin/main`.

## Why it is refused today

- The renderer maps a list to the blank lines after it. So the page sends:
  - a copy or cut range whose `endLine` is a blank line (`src/page/features/blockSelectionView.ts`,
    `previewBlocksCopy` / `previewBlocksCut`);
  - a paste whose `insertAfterLine` is that blank line, either the selection's `range.endLine`
    (`blockSelectionView.ts`, `previewBlocksPaste`) or the `data-sphinx-insert-after-line` of the
    list's insert point, which `src/page/features/insertPoints.ts` places at the block's
    `data-sphinx-source-end-line`.
- `planBlocksCopyCut` (`src/core/edits/sourceEdits.ts`) passes the range unchanged to `spanText` and
  `planCut` (`src/core/mapping/blockRange.ts`). Both call `checkSpan`, which refuses a span whose last
  line is blank.
- `planPaste` (`blockRange.ts`) refuses an `afterLine` that is blank, even though `planInsertion`
  (`src/core/mapping/insertion.ts`) already handles a blank anchor ("a list ending on its blank
  separator").
- `planBlockMoveEdit` and `planBlocksDelete` already trim, with `withoutTrailingBlankLines`.

## What changes

### Copy and cut: `src/core/edits/sourceEdits.ts` (cc-Q1, cc-Q2, cc-Q6)

1. Add `withoutTrailingCommonMarkBlankLines(text, block): BlockLines` next to
   `withoutTrailingBlankLines`. It has the same shape and the same guards: a range that is out of
   bounds or not made of integers comes back unchanged, and the end never goes above `line`. The one
   difference is the test of a blank line: `isCommonMarkBlank`, imported from
   `src/core/mapping/blockRange.ts` (exported there, `@implements_req SwRS-MDOKFSTUDIO-BLOCK-266`).
   - Do not change `withoutTrailingBlankLines`. It still uses `trim()`, and Delete block and moves
     keep their meaning.
   - The new function's JSDoc says why it differs: copy and cut drop only spaces-and-tabs lines, so a
     no-break-space paragraph at the end of a selection is never left out without the writer knowing.
2. In `planBlocksCopyCut(text, line, endLine, op)`:
   - first compute `const span = withoutTrailingCommonMarkBlankLines(text, { line, endLine });`;
   - use `span.line` and `span.endLine` in `spanText` (the copied text), in `linesOpenInclude` (the
     include refusal) and in `planCut` (the edit and `followingLine`);
   - keep the order of the checks and the refusal texts.
3. Update the JSDoc of `planBlocksCopyCut`, and add `@implements_req SwRS-MDOKFSTUDIO-BLOCK-166` and
   `@implements_req SwRS-MDOKFSTUDIO-BLOCK-169` above it.

This is not a list-only fix (cc-Q2). `planBlocksCopyCut` is the one host path for every copy and cut,
so any range that ends on CommonMark blank lines is trimmed: a list, a list item, or a selection whose
last block is a list.

These are still refused with `OUT_OF_DATE`, by `checkSpan` after the trim:

- a range that starts on a blank line;
- a range of blank lines only;
- a range past the end of the text;
- a range that ends on a line with a no-break space only (it is not CommonMark blank, so it is not
  dropped, and `checkSpan`'s `trim()` test refuses it). This is cc-Q6.

`planCut`, `spanText`, `checkSpan`, `handleBlocksCopyCut` (`src/session/features/sourceEdits.ts`) and
the page do not change.

**What copy and cut give** (cc-Q1, cc-Q3):

- **Copy:** the clipboard holds lines `span.line`..`span.endLine` exactly, with the document's line
  breaks and no trailing line break. The document does not change.
- **Cut:** the same clipboard text, then `planCut` on the trimmed span, under the existing rules of
  SwRS-MDOKFSTUDIO-BLOCK-169, which are also the rules of CR-439's Delete block. On the same range, a
  cut gives exactly the text and the `followingLine` of `planBlocksDelete`. When no no-break-space
  line is involved, both trims give the same span.

For example (LF), with `Para\n\n- a\n- b\n\n\nNext\n` and range 3..6:

- copy gives `- a\n- b`;
- cut gives the same clipboard and the document `Para\n\nNext\n`, with `followingLine` 7.

### Paste: `src/core/mapping/blockRange.ts`, `planPaste` (cc-Q5)

Change only the anchor check in `planPaste`, the `afterLine > 0` branch:

1. These stay as they are: an empty clipboard, a non-integer or negative `afterLine`, an `afterLine`
   past the end (`OUT_OF_DATE`), and the frontmatter check on a non-blank anchor (`IN_FRONTMATTER`).
2. A blank anchor line is accepted when it is a CommonMark blank line and the nearest line above it
   that is not CommonMark blank (`above`) is a body line.
   - Refuse with `OUT_OF_DATE`, as today, when no such line exists (blank lines at the start of the
     text) or when `above` lies in the frontmatter (`above <= frontmatterLineCount(text)`). A paste
     right under the frontmatter keeps going through `afterLine` 0.
   - An anchor whose `trim()` is empty but which is not CommonMark blank (no-break space only) is
     still refused with `OUT_OF_DATE`, as for cut and copy (cc-Q6).
3. An accepted blank anchor is moved up to `above + 1`, the first blank line under that block (the
   list's own separator). Then `planInsertion(text, above + 1)` is called as today.
   - `planInsertion` gives a blank anchor the prefix of one line break, and a suffix of one line
     break before a non-blank line, or nothing before a blank line.
   - So the new block reuses the blank lines already there: one blank line before it, one after it,
     and no blank line gained.
   - The page may send the first or the last blank line of a run (it depends on how far the renderer
     maps the list). Both give the same text.
4. Update the JSDoc of `planPaste`. It keeps `@implements_req SwRS-MDOKFSTUDIO-BLOCK-174`, and gains
   `@implements_req SwRS-MDOKFSTUDIO-BLOCK-124` if the refusals there are not already marked.

The host cannot tell a list from its lines without parsing. So the rule accepts any CommonMark-blank
anchor under a body line, which covers a list and any other block the renderer maps to its blank
separator.

The include check does not change. `checkBlocksPaste` (`sourceEdits.ts`) still runs on the raw
`insertAfterLine`. A paste after the blank line under an include directive was already "accepted" by
the include check (SwRS-MDOKFSTUDIO-BLOCK-127, scenario "after the closing fence"). It now also passes
`planPaste`, which is what BLOCK-127 already states. `planBlankRunPaste`, `planInsertion` and the page
do not change.

For example (LF), pasting `X`:

| Document | `afterLine` | Result |
| --- | --- | --- |
| `Para\n\n- a\n- b\n\nNext\n` | 5 | `Para\n\n- a\n- b\n\nX\n\nNext\n` |
| `Para\n\n- a\n- b\n\n\nNext\n` | 5 | `Para\n\n- a\n- b\n\nX\n\nNext\n` |
| `Para\n\n- a\n- b\n\n\nNext\n` | 6 | `Para\n\n- a\n- b\n\nX\n\nNext\n` |
| `Para\n\n- a\n- b\n\n` | 5 | `Para\n\n- a\n- b\n\nX\n` |

### Requirements (okfreq)

Read `requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change") first. Edit the authored text only, never the generated fields or link blocks.

**SwRS-MDOKFSTUDIO-BLOCK-166** (copy):

- In its `description` and its normative sentence: the host puts the exact Markdown of those lines on
  the clipboard "after the range's trailing blank lines (spaces and tabs only) are dropped".
- In the host table, add the row "A list whose range ends on the blank lines after it (the renderer
  maps it so), followed by two blank lines" → "The clipboard holds the list's lines without the blank
  lines after it, and the document is unchanged".
- Add the row "A selection that ends on a line holding only a no-break space" → "Refused with 'The
  preview is out of date. Refresh it and try again.', and nothing is copied".
- In Verification notes, add the new tests of `test/core/edits/sourceEdits.test.ts` and the
  real-input copy step.

**SwRS-MDOKFSTUDIO-BLOCK-169** (cut):

- In its `description` and its normative sentence: "after the range's trailing blank lines (spaces
  and tabs only) are dropped".
- In the table "Where the cut span sits in the document", add the row "A list in the middle whose
  range ends on the two blank lines after it" → "The clipboard holds the list without the blank
  lines; the list and the blank lines after it go, and the blocks around it stay one blank line
  apart, as Delete block leaves them".
- In Criteria: "trailing CommonMark blank lines of the range are dropped before spanText and
  planCut".
- In Verification notes: the new unit tests and the real-input cut step.

**SwRS-MDOKFSTUDIO-BLOCK-174** (paste):

- In the normative sentence, add: "a selection or insert point whose last line is the blank line
  that ends a block (a list mapped to its blank separator) inserts after that block, using the blank
  lines already there as separators, so no blank line is gained".
- Add the scenario table "Paste after a list followed by blank lines", with the rows of the paste
  example above.
- Change its closing sentence from "a line that ... is blank" to "a blank line with no body block
  above it, a line holding only a no-break space".
- In Verification notes, add the new `blockRange.test.ts` paste test and the real-input paste step.
  In Criteria, add "a CommonMark-blank anchor is moved up to the first blank line under the nearest
  body line above it".

**SwRS-MDOKFSTUDIO-BLOCK-124** (refused ranges):

- Change the row "A cut that starts or ends on a blank line" to "A copy or cut that starts on a blank
  line, covers blank lines only, or ends on a line holding only a no-break space" → same refusal.
  Add the note "(spaces-and-tabs lines at the end of a copy or cut range are dropped before the
  check, see SwRS-MDOKFSTUDIO-BLOCK-166 and SwRS-MDOKFSTUDIO-BLOCK-169)".
- Change the row "A paste after a line that does not exist or that is blank" to "A paste after a line
  that does not exist, a line holding only a no-break space, or a blank line with no body line above
  it (the start of the text, right under the frontmatter)" → same refusal. Add the note "(a blank
  line that ends a block is accepted, see SwRS-MDOKFSTUDIO-BLOCK-174)".
- In Verification notes, add the new `test/core/edits/sourceEdits.test.ts` guard test (test 6 below)
  and the changed `blockRange.test.ts` paste refusal test.
- In Criteria, add: "the trailing CommonMark blank lines of a copy or cut range are dropped before
  checkSpan; planPaste moves a CommonMark-blank anchor under a body line before planInsertion".

This changes what the host refuses, which is the point of this CR. The integration refusals that
exist stay valid:

- `test/integration/blockClipboard.test.ts`: cut 8..8 starts on a blank line, and the pastes after
  lines 2 and 12 are in the frontmatter and on an include.
- The core `planCut`/`spanText` tests call the core directly.

**Unchanged:** SwRS-MDOKFSTUDIO-BLOCK-265 (Delete block) and SwRS-MDOKFSTUDIO-BLOCK-127. BLOCK-127's
sentence "a paste after the blank line that follows the directive is accepted" becomes true end to
end. Re-read it, but it needs no edit.

Run `just requirements-update` and commit the generated files. Add a dated entry in
`requirements/tiers/log.md`: copy and cut drop the trailing CommonMark blank lines of a range; paste
accepts the blank line that ends a list; BLOCK-166, BLOCK-169, BLOCK-174 and BLOCK-124 updated.

### Changelog

Add one line under `## Unreleased` in `CHANGELOG.md`: "Copy, cut and paste on a list followed by
blank lines no longer fail with 'The preview is out of date': the list is copied without the blank
lines, a cut leaves one blank line between the blocks around it, and a paste after the list gets one
blank line on each side."

### Writing skill

No change: no rendered syntax changes.

## Evidence (cc-Q4)

**Before and after:**

- Must fail on the code from before this change: tests 1 to 4, 7 and 8, and every real-input step
  below that copies, cuts or pastes. Before the change, each of these is refused with `OUT_OF_DATE`.
- Guards that pass before and after: tests 5, 6 and 9.
- Test 10 is an existing assertion that this change flips, on purpose.

### Unit tests: copy and cut, in `test/core/edits/sourceEdits.test.ts`

Loop over LF, CR LF and lone CR, as `test/core/edits/blocksDelete.test.ts` does with `EOLS` and
`join`. Mark each test `@tests_req` with the IDs it checks.

1. **List in the middle** (BLOCK-166, BLOCK-169). Document
   `join("Para", "", "- a", "- b", "", "", "Next", "")`, range 3..6:
   - copy gives `{ copied: join("- a", "- b") }`;
   - the cut's `copied` is the same, its edit gives `join("Para", "", "Next", "")`, and
     `followingLine` is 7;
   - the result has no run of three line breaks.
2. **List as the last block** (BLOCK-169). Document `join("Para", "", "- a", "- b", "", "", "")`,
   range 3..6: the cut gives `join("Para", "")`, `followingLine` is `undefined`, and the clipboard is
   `join("- a", "- b")`.
3. **Selection ending on a list** (BLOCK-166, BLOCK-169). Document
   `join("Alpha", "", "- a", "- b", "", "Omega", "")`, range 1..5: copy gives
   `join("Alpha", "", "- a", "- b")`, and the cut leaves `join("Omega", "")`.
4. **Same result as Delete block** (BLOCK-169). For each range of tests 1 to 3, and for
   `join("Para", "- a", "- b", "", "", "Next", "")` with range 2..5 (a list that touches the block
   above), the cut's edit applied gives the text and the `followingLine` of `planBlocksDelete` on the
   same range. A line of spaces and a tab (`" \t"`) inside the trailing blank lines is dropped too.
5. **Still refused** (BLOCK-124, guard). For both copy and cut, these give `"refused"`:
   - a range of blank lines only: `join("A", "", "", "B", "")`, range 2..3;
   - a range that starts on a blank line;
   - a range past the end.
6. **No-break space** (BLOCK-124, BLOCK-166, BLOCK-169, guard, cc-Q6). Document
   `join("Alpha", "", " ", "")`, range 1..3: copy and cut give
   `{ refused: "The preview is out of date. Refresh it and try again." }`, and the cut leaves the
   document untouched. This proves that `planBlocksCopyCut` uses the CommonMark trim, not
   `withoutTrailingBlankLines`.

### Unit tests: paste, in `test/core/mapping/blockRange.test.ts`

Use the file's `paste` helper. Mark the tests `@tests_req SwRS-MDOKFSTUDIO-BLOCK-174`, and test 9
`@tests_req SwRS-MDOKFSTUDIO-BLOCK-124`.

7. **Paste after a list's blank separator** (BLOCK-174). The four rows of the paste example above
   give exactly those results. Run them in LF, and the first row also in CR LF:
   `paste("Para\r\n\r\n- a\r\n- b\r\n\r\nNext\r\n", 5, "X1\nX2")` gives
   `"Para\r\n\r\n- a\r\n- b\r\n\r\nX1\r\nX2\r\n\r\nNext\r\n"`.
8. **Both blank lines of a run give the same text** (BLOCK-174): with two blank lines after the list,
   `afterLine` 5 and 6 give the same result, which has no `\n\n\n`.
9. **Still refused** (BLOCK-124, guard). These give `"refused"` with `OUT_OF_DATE`:
   - `paste("\nA\n", 1, "X")`, a blank line with nothing above it;
   - `paste("---\na: 1\n---\n\nA\n", 4, "X")`, a blank line right under the frontmatter;
   - `paste("A\n \n\nB\n", 2, "X")`, a no-break-space line.
10. **Changed assertion**. In `paste refuses an empty clipboard, the frontmatter and stale lines`, the
    line `assert.deepEqual(Object.keys(paste("A\n\nB\n", 2, "X") as object), ["refused"], "blank line")`
    changes to `assert.equal(paste("A\n\nB\n", 2, "X"), "A\n\nX\n\nB\n")`. That is the same text as a
    paste after line 1, because a blank line under a block is now its separator (cc-Q5). The commit
    message and the PR say why this assertion changes. Its blank-anchor refusal moves to test 9.

The existing tests stay unchanged and must pass:

- `test/core/mapping/blockRange.test.ts`: `spanText refuses bad ranges...`,
  `cut refuses the frontmatter and bad ranges`, and the other paste tests;
- the existing `planBlocksCopyCut` tests;
- `test/core/edits/blocksDelete.test.ts`.

### Real-input scenario: `scenarioBlockSelection` in `test/integration/realInput/blockKeys.ts`

Extend the existing scenario. Add new `withDocument` blocks at its end, so the steps that exist keep
their document. Each new block uses the document
`["# Clip", "", "Alpha paragraph.", "", "- item a", "- item b", "", "", "Omega paragraph.", ""].join("\n")`,
a list followed by two blank lines.

**Copy and cut**, in one document block:

1. Open the side preview, wait for the render, and turn edit mode on.
2. Select the list block alone, with the keyboard or a Shift+click on the list. Wait until exactly
   one block is selected and its text holds "item a".
3. Sanity check: read the list's mapped range from the page, as the page sends it. Assert that its
   last line is blank in the document. This proves that the steps go through the new path.
4. **Copy.** Write a sentinel to the clipboard, press `${MOD}+C`, and wait for the clipboard to read
   `"- item a\n- item b"`. Assert that `bufferText(document)` is unchanged.
5. **Cut.** Press `${MOD}+X` with the list selected. Wait for the clipboard to read
   `"- item a\n- item b"` and for the buffer to equal
   `["# Clip", "", "Alpha paragraph.", "", "Omega paragraph.", ""].join("\n")`.
6. Take a screenshot with `captureAfter(evidence, page, "block-editing/r<next free number>-cut-list-trailing-blank", ...)`.

**Paste**, in a second document block with the same text, so that the paste meets the two blank
lines:

7. Steps 1 to 3 again.
8. **Paste.** Write `"Pasted paragraph."` to the clipboard and press `${MOD}+V` with the list
   selected. Wait for the buffer to equal
   `["# Clip", "", "Alpha paragraph.", "", "- item a", "- item b", "", "Pasted paragraph.", "", "Omega paragraph.", ""].join("\n")`,
   which has one blank line on each side and no blank line gained.
9. Take a screenshot with `captureAfter(evidence, page, "block-editing/r<next free number>-paste-after-list-trailing-blank", ...)`.

**For both blocks:**

- Restore the clipboard in a `finally`, as the scenario does now.
- Use capture numbers that no other capture uses.
- Each copy, cut and paste step fails on the code from before this change: the request is refused,
  so the clipboard or the buffer never reaches the expected value and `waitFor` times out.
- Markers: the scenario's block already names BLOCK-254 and StRS-BLOCK-016. Put `@tests_req
  SwRS-MDOKFSTUDIO-BLOCK-169` and `@tests_req SwRS-MDOKFSTUDIO-BLOCK-174` on the code of the new
  blocks (for example a helper that each block calls), so that no marker block names more than 3
  IDs.

Real VS Code scenarios run on pushes to `main` or on a heavy dispatch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`), not on a pull request. The PR shows one heavy
run in which `scenarioBlockSelection` passes, with the two new screenshots.

### Gates

Run:

- `just check` (unit, markers, file size: `blockKeys.ts` is at 624 lines, `blockRange.ts` at 270,
  `sourceEdits.ts` at 366, all well within the limits);
- `just requirements-lint`;
- `just requirements-update`, with no diff left;
- `just preflight`.

## Out of scope

- No change to the page, to the renderer's mapping of lists, to `insertPoints.ts`, or to
  `checkBlockLines`.
- No change to `withoutTrailingBlankLines`, to Delete block, to moves, to `planCut`'s rules, to
  `planInsertion`, to blank-run paste or removal, or to the include checks.
- No new case in `test/integration/blockClipboard.test.ts`: cc-Q4 names unit tests and the
  real-input scenario.
