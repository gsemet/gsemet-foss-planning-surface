# One blank-line block per line, and no save stuck on Saving

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/485

In edit mode, each blank line beyond the separator that Markdown needs shows as its own blank-line
block. This replaces the one block per run of CR-444. Typing in a blank-line block saves and closes
like any other block. No block editor can stay in "Saving Markdown…" for good: every final save ends
in the rendered block or in an error the editor shows, and Cancel always closes the editor.

Short name: `blank-save`. Destination: the running batch-09 (blank-save-Q4).

## Goal

The issue: a line of text followed by 6 blank lines shows one blank-lines block (the CR-444
design). The writer clicks it and types text. The editor shows "Saving Markdown…" and stays like
that: the text is written and renders below, but the editor never closes, and neither Done nor
Cancel gets the writer out.

The owner's answers:

- **Each blank line is a block** (blank-save-Q1, Q5). The page shows the file's blank lines one
  for one, so the writer sees and edits lines, not one opaque run.
- **Typing or deleting acts on that one line** (Q5, Q7).
- **No save can hang** (Q6). The hang shows the edge case had no test (Q3). This CR adds tests for
  the edge cases the issue lists, plus a general guard: every save ends in success or in an error
  the editor shows, within a time limit, and Cancel always closes the editor.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## What exists today

CR-444 (merged 2026-11-21; its folder in the planning archives is
`5-archives/261121-0724-444-empty-block-blank-lines-block`) and the CRs built on it, CR-448 (runs
inside lists) and CR-462 (runs inside quotes and containers), deliver:

- **Core.** `blankRuns` and `quoteBlankRuns` (`src/core/mapping/blankRuns.ts`) list every maximal
  run of two or more blank lines, or of two or more empty quote lines of one shape.
- **Render.** `blankRunsMarker` (`src/core/render/renderPipeline.ts`) appends
  `<div hidden data-okf-blank-runs="L-E ...">` as the last element of the content.
- **Page.**
  - `installBlankLines` (`src/page/features/blankLines.ts`) parses that list (`parseRuns`, which
    drops a pair with `endLine <= line`). It places one blank-lines block per run, using
    `locateRun` and `placeInHost` (`src/page/features/blankRunHosts.ts`), and opens an insertion
    editor with `replaceBlankRun: { line, endLine, itemLine?, containerLine? }`.
  - `requestDeleteBlankLines` and the Ctrl/Cmd+V branch (`src/page/features/blockSelectionView.ts`)
    post `previewBlankRunDelete` and `previewBlocksPaste` with the run.
- **Host.**
  - `checkBlankRun` (`src/core/mapping/blockRange.ts`) requires a maximal run of two or more
    lines.
  - `planBlankRunInsertion` (`src/core/mapping/insertion.ts`) replaces the whole run, with one
    separator on each side.
  - `planBlankRunRemoval` keeps one separator. `planBlankRunPaste` is the paste plan.
    `blankRunIndent` (`src/core/mapping/blankRunContainer.ts`) gives the container indent.
  - In `src/session/features/blockEdits.ts`, `handleEditOpen` and `handleEditSave` (the re-created
    edit path) check the run, and `blankRunRegion` holds the run's text for a restore.
- **Protocol.** `isBlankRunFields` (`src/core/protocol/pageToHost.ts`) requires
  `endLine > line`.
- **The editor kept across an autosave** (CR-444 fix 7). `applyContentPatch`
  (`src/page/features/contentPatch.ts`, line 58) skips `closeBlockEdit` whenever the open editor
  has `replaceBlankRun`, and `refresh()` in `blankLines.ts` puts that editor's block and frame back.

### Why the editor stays in "Saving Markdown…"

These are read from the code. The Driver confirms them with the failing page test of the Evidence
before fixing.

1. Done calls `postBlockEditSave(true)` (`src/page/features/blockEditor.ts`). It sets
   `edit.finishing = true`, shows "Saving Markdown…" and posts `previewEditSave` with
   `final: true`.
2. The host writes the text. `completeActiveBlockEdit` (`blockEdits.ts`) then sees a revision not
   yet rendered. It asks for a render and posts no `done`, because the content patch is what
   closes the editor.
3. The content patch arrives. `applyContentPatch` skips `closeBlockEdit` because the editor has
   `replaceBlankRun`, so the editor stays open with `finishing` still true.
4. With `finishing` true, Done (`postBlockEditSave` returns early) and Cancel (`cancelBlockEdit`
   returns early) do nothing. That is the SwRS-MDOKFSTUDIO-BLOCK-053 refusal scenario "Cancel is
   ignored while the final save is in flight".

Nothing on the page bounds the wait. Any final save whose answer never comes (no patch, no `done`,
no error) hangs the same way, for any block.

### Decisions this CR replaces

| Earlier decision | Replaced by |
| --- | --- |
| CR-444 blank-runs-Q2: one blank-lines block per run of two or more blank lines; a single blank line at the start or the end of the body shows nothing | One blank-line block per blank line beyond the separator (blank-save-Q1, Q5). Between two blocks, N lines give N−1 blocks. At the end of the body and at the top of a file without frontmatter, every blank line is a block, a single one included. |
| CR-444 blank-runs-Q2: an insertion editor replaces the whole run, with one separator on each side | Typed text replaces that one line. A blank line is added before or after it only when Markdown needs one (Q2 restated by Q5). |
| CR-444 blank-runs-Q2: Delete removes the extra lines of the run and keeps one separator | Delete, Backspace or the Delete block button removes that one blank line. The hidden separator always stays (Q7). |
| CR-444 blank-runs-Q12: Ctrl/Cmd+V pastes in place of the run | Ctrl/Cmd+V pastes in place of that one line, with the same rule as typing (follows from Q5). |
| CR-444 fix 7: a blank-lines block's editor stays open across every re-render | It stays open across an autosave's re-render only. The render of its final save closes it, like any editor (Q6). |
| SwRS-MDOKFSTUDIO-BLOCK-053, refusal scenario: Cancel is ignored while the final save is in flight | Cancel always closes the editor (Q6). |
| CR-448 br-Q2 and CR-462 bq-Q1: the same blank-lines block, one per run, inside lists, quotes and containers | The same per-line block inside them (decision 1 below, to confirm). |

Everything else of CR-444, CR-448 and CR-462 holds. That covers placement inside containers,
folds, closed dropdowns, the host-only run list, the trust rule on authored attributes, the
export, line endings, the container indent and the sibling rules.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs. In a quote run, it is
  the run's first empty quote line.
- **Blank run**: unchanged. It is a maximal sequence of CommonMark blank lines (spaces and tabs
  only, `isCommonMarkBlank`), or of empty quote lines of one shape (`emptyQuoteLine`,
  `sameQuoteShape`), after the frontmatter. The run is now also used for a single line, where the
  shown-line rule below needs one.
- **Shown blank line**: a blank line of a run that gets a block. These are every line of the run
  except its separator:
  - Between two blocks, the frontmatter counting as a block, the separator is the run's first line,
    so lines `L+1`..`E` show (N−1 blocks; none for a single line).
  - At the end of the body (nothing but blank lines after it, the text of only blank lines
    included) and at the top of a file without frontmatter, every line shows (N blocks, one for a
    single line).
  - In a quote run, the first line is always the separator, so lines `L+1`..`E` show.
- **Blank-line block**: the page element that shows one shown blank line in edit mode. It replaces
  the glossary term "Blank-lines block" (section 6).

## What changes

### 1. The host lists shown blank lines (Q1, Q5)

- Add a pure function `shownBlankLines(text): BlankRun[]` in `src/core/mapping/blankRuns.ts`. It
  returns, in line order, the ranges of shown blank lines of every plain run and every quote run.
  It is built on the same scan as `blankRuns` and `quoteBlankRuns`, which now also report runs of
  one line wherever the "Shown blank line" rule shows a single line. A range may be one line
  (`line === endLine`). It keeps the existing rules: `splitLines` (the pseudo-line after a final
  break is never a line), frontmatter lines excluded, LF, CR LF and lone CR alike.
- `blankRunsMarker` writes `shownBlankLines(text)` as `L-E` pairs (`L-L` for one line). The
  attribute, its place (last element of the content) and its export removal are unchanged.
- One more pure helper, `blankRunAround(text, line): BlankRun | undefined` (in `blankRuns.ts`),
  gives the maximal run (plain or quote) that holds a line. The host uses it to read the container
  indent and the sibling rules from the whole run (section 3).

### 2. The page shows one block per shown line (Q1, Q5)

In `src/page/features/blankLines.ts`:

- `parseRuns` accepts `endLine >= line`. It still drops malformed and overlapping pairs, and it
  still reads only the host's last element.
- Each range is located once (`locateRun`, unchanged: a range lies inside the same container, fold
  or fence as its run). Then **one blank-line block per line** of the range is created, all placed
  at that spot, in line order. Each block's run is `{ line: n, endLine: n }`, plus the
  `itemLine`, `containerLine` and `holder` of its range.
- The refresh's reuse key (`keyOf`) is per line, so a block whose line is unchanged keeps its
  element across a re-render.
- **Look** (`BLANK_LINES_BLOCK_CSS`, `src/core/preview/styles/editModeStyles.ts`, and
  `blankLinesInContainersStyles.ts`):
  - each block is about one line of body text high, and the blocks of one range stack with no gap,
    so 6 blank lines read as 6 lines;
  - the label is "Blank line", drawn from `data-okf-blank-label` as today, never in the text
    content;
  - the `aria-label` is "Blank line. Press Enter to write a block here.";
  - the Delete block button, the selected look and the edit-mode-only rule are unchanged.
- **Arrows** (`stepSelection`, BLOCK-004 and BLOCK-267): Up and Down stop on each blank-line block
  in line order, inside lists and containers too. The other key rules of BLOCK-267 are unchanged:
  - the block selection never starts or ends on a blank-line block;
  - Shift+click does nothing on one;
  - Alt+Up/Down posts nothing;
  - Escape clears the selection;
  - Ctrl/Cmd+C and Ctrl/Cmd+X post nothing with only a blank-line block selected;
  - Delete and Backspace act only on a selected blank-line block, not on a focused one.

### 3. Typing or pasting in a blank-line block replaces that one line (Q5)

- **Messages.** `replaceBlankRun` (on `previewEditOpen`, `previewEditSave`, `previewEditCancel`
  and `previewBlocksPaste`) and `previewBlankRunDelete` keep their names and fields. Both now name
  one line: `endLine === line`. `isBlankRunFields` and the `previewBlankRunDelete` validator
  (`src/core/protocol/pageToHost.ts`) require `endLine === line`, in place of `endLine > line`. The
  rule `insertAfterLine === line − 1` is unchanged.
- **The check.** `checkBlankLine(text, line): BlockRangeRefusal | undefined` in
  `src/core/mapping/blockRange.ts` refuses with `OUT_OF_DATE` unless `line` is a shown blank line
  of `shownBlankLines(text)`. It replaces `checkBlankRun` at every caller:
  - open: `handleEditOpen`;
  - save: the re-created edit path of `handleEditSave`;
  - paste: `planBlankRunPaste`;
  - removal: `planBlankRunRemoval`.

  `containerLineHolds` and `blankRunIndent` read the run from `blankRunAround(text, line)`. So the
  item and container checks, the content indent and the sibling rules of CR-448 and CR-462 are
  unchanged: for example, `- c` typed between two items is still written as a sibling item.
  `checkBlankRun` is removed if no caller is left (the unused-exports check).
- **The plan.** `planBlankRunInsertion` (`src/core/mapping/insertion.ts`) takes one line
  (`planBlankRunInsertion(text, line, itemLine?, containerLine?)`, or `endLine === line`):
  - **The region** is line `line` without its line break: from the start of the line to the end of
    its text.
  - **A separator before**: one is written only when line `line − 1` exists and is not blank. "Not
    blank" means a block line, the frontmatter's closing line included, or, in a quote run, not an
    empty quote line of the run's shape. In a quote run, the separator is a copy of the run's first
    line, as today.
  - **A separator after**: one is written only when line `line + 1` exists and is not blank, by the
    same test.
  - The line break of line `line` stays as it is, so the document's final line break, or its
    absence, is kept.
  - `insertionText` is unchanged: it drops leading blank lines, uses the document's line endings
    and applies the container indent.
- **Host edit** (`blockEdits.ts`). `blankRunRegion` holds the one line, `{ line, endLine: line,
  itemLine?, containerLine?, text }`, and is still never sent to the page. The page-facing
  `originalText` stays `""`.
  - An empty or whitespace-only text, or Cancel after an autosave, writes that line's text back
    byte for byte, and any separator an autosave added goes with it. Nothing else changes.
  - Done with an empty text before any autosave makes no edit, and the editor closes (BLOCK-263).
- **Paste** (`planBlankRunPaste`, `planBlocksPaste` in `src/core/edits/sourceEdits.ts`): Ctrl/Cmd+V
  on a selected blank-line block writes the pasted block in place of that one line, with the same
  separator rule.

### 4. Removing a blank-line block removes that one line (Q7)

- `planBlankRunRemoval(text, line)` (`src/core/mapping/blockRange.ts`, through `planBlankRunDelete`
  in `src/core/edits/sourceEdits.ts`) removes line `line` and its line break, in one `TextEdit`
  through `applyWrittenEdits`, as one undo step.
  - When the line is the last line of the text, the removal takes the line break before it
    instead. The text then keeps its final line break, or its absence, as `planBlankRunRemoval`
    does today.
  - A text of only blank lines whose last line goes becomes empty.
- The separator is never a shown line, so it is never removed, and two blocks are never glued
  together. In a quote run, the first empty quote line stays byte for byte.
- The answer is unchanged: `previewBlocksResult` with `op: "delete-blank-lines"`, and a stale
  refusal shown next to the blank-line block.
- **Selection afterwards** (`requestDeleteBlankLines`, `blockSelectionView.ts`), in this order:
  1. the blank-line block that now shows at the same place (the next blank line, which takes the
     removed line's number), so repeated Delete clears the lines one by one;
  2. else today's rule: the block that followed, the container that held the run, the block above,
     or "Start writing".

  The cut's viewport pin is unchanged.

### 5. No save stays in "Saving…" (Q6)

**a. The content patch closes the editor of a final save.** In `applyContentPatch`
(`src/page/features/contentPatch.ts`, line 58), the exception for `replaceBlankRun` holds only while
no final save of that editor was posted. Once one was posted (`finishing`, or the timed-out state
of b), the patch closes the editor with `closeBlockEdit(false)`, as for any block. The next
`blankLines.refresh()` then drops the held block. An autosave's re-render keeps the editor open as
today (CR-444 fix 7).

**b. Every final save ends in a bounded time.**

- When `postBlockEditSave(true)` posts a final save, the page starts one timer,
  `FINAL_SAVE_TIMEOUT_MS = 10000`, a named constant in `blockEditor.ts`. The timer is cleared when
  the editor closes, which covers a content patch, `done: true` and Cancel, or when an error
  answer arrives (`receiveBlockEditSource`, `src/page/features/blockSourceEditor.ts`).
- When the timer fires with the editor still open and `finishing`:
  - `finishing` becomes false and `lastPostedText` is cleared, as an error answer does today;
  - the status shows "The save did not finish. Your text is kept: press Done to try again, or
    Cancel to close the editor.";
  - Done posts the final save again.
- A content patch or a `done: true` that arrives after the timer still closes the editor (a).
- This covers the block editor and the table cell editor, which share `postBlockEditSave`.
- **Frontmatter saves** (blank-save-Q6 "every save"): a field save or a field action save that
  posted `previewFrontmatterSave` and gets no result within the same time limit takes the existing
  error path of `frontmatterEditor.ts` (around line 335). That path shows the error, sets `saving`
  to false and enables the controls again. The message is the same as for the block editor, with
  "frontmatter" in place of "Markdown". The timer lives in `frontmatterValueEditor.ts` and
  `frontmatterEditor.ts` beside `saving = true`, and is cleared on any result.

**c. Cancel always closes the editor.** `cancelBlockEdit` (`blockEditor.ts`) no longer returns
early on `finishing`. The Cancel button and Escape always close the editor:

- **No final save in flight**: unchanged (BLOCK-053). The editor posts `previewEditCancel` when an
  autosave reached the document.
- **A final save in flight or timed out**: the editor closes with no `previewEditCancel`. The save
  the writer already asked for with Done goes on and completes on the host. The page stops
  waiting for it.
- The host edit lock is released as today when that save ends. The page's next `previewReady`
  carries `blockEditOpen: false`.

The table cell editor's Cancel (`cancelTableCellEdit`) follows the same rule.

### 6. Requirements, vocabulary and docs

Follow the project's requirements guidelines: IDs come from `okfreq new`, markers move with the
code, run `just requirements-update`, and add a dated entry in `requirements/tiers/log.md`. All of
the following are in scope `block-editing`, except the frontmatter one.

- **Update SwRS-MDOKFSTUDIO-BLOCK-266**: each shown blank line shows as one blank-line block.
  Between two blocks N lines give N−1 blocks; at the end of the body and at the top of a file
  without frontmatter, every line is a block; this holds inside lists and containers. Its
  scenarios get the issue's case: a line of text then 6 blank lines gives 6 blocks.
- **Update BLOCK-267**: Up and Down stop on each blank-line block.
- **Update BLOCK-268**:
  - typed or pasted text replaces that one line;
  - a separator is added only where a neighbour line is not blank;
  - Cancel or an emptied editor restores the line;
  - the editor stays open across an autosave's re-render and closes on the render of its final
    save.
- **Update BLOCK-269**: Delete removes that one line, the separator stays, and the selection goes
  first to the blank-line block now in its place.
- **Update BLOCK-053**: its refusal scenario "Cancel is ignored while the final save is in flight"
  becomes "Cancel during a final save closes the editor and the save completes".
- **Update BLOCK-004**: a scenario row for one stop per blank-line block.
- **New SwRS (block-editing)**: "A block editor's final save always ends". The page shows an error
  and enables Done and Cancel again when no answer comes within the time limit, and a late answer
  still closes the editor.
- **New SwRS (frontmatter-editing)**, or a scenario on the FMEDIT SwRS of the field save error,
  whichever the requirements guidelines prefer: a frontmatter save with no result within the time
  limit shows an error and enables the field again.
- Approved StRS texts are not changed. If BLOCK-025's text must change, its re-approval goes to the
  owner through the Chief of Staff.

Vocabulary and docs:

- `.agents/glossary/common.md`:
  - rename "Blank-lines block" to "Blank-line block" (one per shown blank line);
  - add "Shown blank line" and "Separator" as in "Words";
  - in "Blank run", note that the host now lists shown lines.
- Page text and labels use "blank-line block". Code identifiers (`installBlankLines`,
  `.sphinx-preview-blank-lines`, `replaceBlankRun`, `previewBlankRunDelete`) may keep their names.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes, and the blocks are edit-mode chrome.

## Out of scope

- Blank lines inside a block (fence, directive body edited whole, HTML block, table), in an included
  file, in the frontmatter, in a fold or a closed dropdown: unchanged (nothing shows).
- Collapsing blank lines on its own, on save or render: the file's format is kept.
- Selecting several blank-line blocks at once to delete them in one step.
- A save time limit for messages other than final block saves and frontmatter saves (block moves,
  pastes and cuts already have their own `blocksFlight` and move timeouts).
- Renaming code identifiers from "blank run" or "blank lines" to "blank line".
- The release notes, written when the release is prepared.

## Evidence

The checks read the shipped files at the head under test: the real core and render functions, the
real page bundle and the real stylesheet module, never a prepared copy. Each check below fails on
the code before the change (constitution, section 3).

**Core (`test/core/mapping/`):**

- `blankRuns.test.ts`: `shownBlankLines`.
  - Segmentation of N blank lines between two paragraphs, for N = 1, 2, 3 and 6: 0, 1, 2 and 5
    shown lines, starting at the second blank line.
  - The issue's text, `Text` then 6 blank lines with and without a final line break: lines 2..7,
    6 shown.
  - The top of a file without frontmatter: every line shows. After the frontmatter: N−1 lines.
  - A text of only blank lines: every line shows.
  - Quote runs: the first line is never shown.
  - A U+00A0 line breaks a run.
  - LF, CR LF and lone CR.
  - `blankRunAround` returns the maximal run of a line.
- `blockRange.test.ts`:
  - `checkBlankLine` accepts a shown line and refuses the separator, a non-blank line and a line
    past the end.
  - `planBlankRunRemoval` removes one line in the middle of a run, the last line of the text with
    and without a final break, and a line of a text of only blank lines. It never removes a
    separator, and adds no bare LF in CR LF and no CR in LF.
  - `planBlankRunPaste` writes in place of one line.
- `insertion.test.ts`: `planBlankRunInsertion` on one line.
  - The first shown line of a 3-line run between blocks adds no separator.
  - The last shown line adds one after.
  - The first line of a run at the end of the body adds one before.
  - Line 1 at the top of a file adds one after.
  - A quote run's separator is a copy of its first line.
  - LF, CR LF and CR.
- `blankRunContainer.test.ts`, `blankRunInList.test.ts`, `quoteBlankRuns.test.ts`, updated: a line
  between two list items takes the sibling indent for `- c` and the content indent otherwise. A
  line inside a quote keeps the quote markers.

**Render and protocol:**

- `renderPreviewSource` ends with `data-okf-blank-runs` holding the shown ranges (`7-7` for one
  line).
- `pageToHost.test.ts`: `replaceBlankRun` and `previewBlankRunDelete` are accepted with
  `endLine === line` and rejected with `endLine !== line`.

**Session (`test/session/blankRunHost.test.ts`, `blankRunInListHost.test.ts`,
`blankRunInContainerHost.test.ts`):**

- Typing in a blank-line block, with the region a single line:
  - a final save of `Middle` writes it in place of the line with only the separators needed;
  - an autosave then Cancel restores the line byte for byte;
  - an empty Done writes nothing and posts `done: true`;
  - a separator line is refused on open, and on a re-created save.
- `previewBlankRunDelete` removes one line in one `applyWrittenEdits` call.
- A final save of a blank-line insertion that writes text ends the host edit and asks for a render
  (`refreshPreviewDocument`). No `done` is posted: the patch closes the editor.

**Page (`test/page/`, with the runtime bundle as `runtimeBlankLines.test.ts` does; one check per
rule):**

- `runtimeBlankLines.test.ts` and `runtimeBlankLinesContainers.test.ts`, updated:
  - a list `3-4` places two blocks in line order, and `7-7` places one;
  - Down stops on each;
  - Enter on the second posts `previewEditOpen` with `replaceBlankRun: { line: 4, endLine: 4 }`;
  - Delete posts `previewBlankRunDelete` for one line;
  - after the result and the render, the selection is on the blank-line block now at that place;
  - an authored `data-okf-blank-runs` still makes no block.
- **The regression of the issue** (new test, for example in `runtimeBlankLines.test.ts`):
  1. Open the editor from a blank-line block, type `Text` and press Done. "Saving Markdown…"
     shows.
  2. Apply a content patch whose run list no longer has that line. The editor is closed,
     `state.activeBlockEdit` is undefined and the held block is gone.

  A second case: autosave, then a content patch without the line. The editor stays open (fix 7
  kept).
- **The save guard** (new file, for example `test/page/runtimeBlockEditorSaveGuard.test.ts`, with
  fake timers):
  - a final save with no answer for `FINAL_SAVE_TIMEOUT_MS` shows the timeout message and clears
    `finishing`, and Done posts the final save again;
  - a content patch after the timeout still closes the editor;
  - Cancel and Escape during "Saving…" close the editor and post no `previewEditCancel`;
  - Cancel with no save in flight behaves as BLOCK-053 says;
  - all of this holds for an ordinary paragraph editor and for a table cell editor.
- **Frontmatter**: a field save with no result for the time limit shows the error and enables the
  control again.

**Visual (`just ci-visual`):** `test/visual/capture_blank_lines_block.py`,
`blankLinesBlockScenarios.ts` and the fixture `92-blank-lines-block.md` are updated. The captures,
attached to the pull request as the pull-request guideline asks:

- edit mode with three blank lines between two paragraphs, showing two blank-line blocks;
- the issue's text, with six blank-line blocks at the end of the body;
- one block selected, with its Delete block button;
- reading mode of the same file, with no block.

**Integration (real VS Code, `test/integration/blankLines.test.ts`, the heavy run on the branch).**
The scenario runs once in LF and once in CR LF:

1. A file `Text.` followed by 6 blank lines. Edit mode shows 6 blank-line blocks.
2. Click the first one, type `More` and press Done. Within the time limit the editor closes and
   "Saving Markdown…" is gone. The file reads `Text.`, a blank line, `More`, then 4 blank lines,
   with its line endings and final line break kept.
3. Three blank lines between two paragraphs: 2 blocks show. Select one with the arrows and press
   Delete: 2 blank lines are left. One Ctrl+Z brings the third back.
4. Click a block, type a word, wait past the autosave and press Cancel: the blank lines are back
   byte for byte.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. The updated and new
SwRS carry `@implements_req` / `@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

The answers leave these points open. Under the owner's autonomy rule, each is decided here as the
option most consistent with the answers, for the Chief of Staff to check:

1. **Per-line blocks also inside lists, quotes and containers.** Q1 says a run "no longer shows as
   one blank-lines block", with no exception, and one rule everywhere keeps the arrows and Delete
   consistent. The container indent and the sibling rules are read from the whole run, so they are
   unchanged.
2. **The hidden separator is the first line of a run** (the line right after the block above), and
   in a quote run its first empty quote line, as the removal keeps today.
3. **A separator before the typed text is added after the frontmatter's closing line**, as an
   insertion after the properties section writes one today.
4. **After a Delete, the selection goes to the blank-line block now in its place**, so repeated
   Delete clears the lines one by one.
5. **Cancel during a final save closes the editor without a cancel**, and the save the writer asked
   for with Done completes. Reverting it would undo a Done the writer already pressed, and it could
   race the host's write.
6. **The time limit is 10 seconds**, one named constant for block and frontmatter saves. It is long
   enough for a slow render, and a late answer still closes the editor.
7. **The guard covers frontmatter saves too**, because Q6 says "every save".
8. **The label is "Blank line"** with no count, since each block is one line.
9. **Spec critic**: yes, on Fable (blank-save-Q8, owner's rule). The Chief of Staff runs it.

## Open questions

1. Decision 1: should the per-line blocks also apply inside lists, quotes, admonitions,
   definitions and footnotes (CR-448, CR-462), or only to top-level runs?
2. Decision 5: Cancel pressed while "Saving…" shows closes the editor and lets the Done save
   complete. Is that right, or should it also try to restore the original text?
3. Decision 6: is 10 seconds the right time limit before "The save did not finish" shows?
