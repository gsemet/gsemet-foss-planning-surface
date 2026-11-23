# One blank-line block per extra blank line

In edit mode, each blank line beyond the one Markdown needs as a separator shows as its own
blank-line block, at the top level and inside containers. Typing in one replaces that one line;
deleting one removes that one line. This replaces the one block per run of CR-444.

Short name: `blank-per-line`. Destination: the running batch-09. Part C of the split of
`blank-run-edit-stuck-saving` (issue 485, blank-save-Q8).

## Goal

The reporter of issue 485 wrote a line of text followed by 6 blank lines and expected 6 empty
blocks; the page showed one blank-lines block for the whole run (the CR-444 design). The owner's
answers (`02-answers.md`):

- **One block per line** (blank-per-line-Q1). The CR-444 one-block-per-run design and its SwRS are
  replaced.
- **Each extra line is a block** (Q2). Between two blocks the one separator line stays hidden: N
  blank lines give N−1 blocks. At the end of the body and at the top of a file without frontmatter,
  every blank line is a block. Text typed in one replaces that one line; a blank line is added
  before or after only when Markdown needs one.
- **Delete removes that one line** (Q3); the hidden separator always stays.
- **Everywhere** (Q4): inside lists, quotes, admonitions, definitions and footnotes too; their
  indent and sibling rules stay.
- **A body of only N blank lines after the frontmatter's closing `---` shows N blocks** (Q5), like
  the end of a file. Nothing inside the frontmatter changes.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## Place in the stack (Q6)

This CR is the last of three in batch-09's stack, and its branch starts from the head of the second:

1. `blank-run-edit-stuck-saving` (A, the fix of issue 485): the content patch closes a blank-lines
   block's editor once its final save was posted, while an autosave's re-render still keeps it
   open (CR-444 fix 7). It carries the `issue:` line and closes the issue.
2. `save-guard-never-hangs` (B): every final save ends within `FINAL_SAVE_TIMEOUT_MS` in success or
   a shown error, the frontmatter wait is bounded, Cancel always closes the editor, with the
   BLOCK-053 and TABLE-025 changes and the save-to-render measure.
3. This CR (C): one block per extra blank line.

This CR changes nothing that A or B deliver, and repeats none of their checks. It relies on them:
a blank-line block's editor (it still carries `replaceBlankRun`) closes on the render of its final
save by A's rule, and any wait is bounded and Cancel works by B's rule. Where A's or B's tests name
a multi-line run (for example a run list `2-7` in A's regression test), this CR rewrites the run to
the per-line ranges of section 1 and keeps what the test asserts. This CR has no `issue:` line: A
closes the issue.

## What exists today

CR-444 (merged 2026-11-21; archived in the planning surface as
`5-archives/261121-0724-444-empty-block-blank-lines-block`) and the CRs built on it, CR-448 (runs
inside lists) and CR-462 (runs inside quotes and containers), deliver:

- **Core.** `blankRuns` and `quoteBlankRuns` (`src/core/mapping/blankRuns.ts`) list every maximal
  run of two or more blank lines after the frontmatter, or of two or more empty quote lines of one
  shape (`emptyQuoteLine`, `sameQuoteShape`).
- **Render.** `blankRunsMarker` (`src/core/render/renderPipeline.ts`) appends
  `<div hidden data-okf-blank-runs="L-E ...">` as the last element of the content.
- **Page.**
  - `installBlankLines` (`src/page/features/blankLines.ts`) parses that list (`parseRuns` keeps a
    pair only when `endLine > line`). It places one blank-lines block per run with `locateRun` and
    `placeInHost` (`src/page/features/blankRunHosts.ts`), labels it `Blank lines (N)` through
    `data-okf-blank-label`, gives it the `aria-label` `Blank lines, N lines. Press Enter to write a
    block here.`, reuses blocks across a refresh by `keyOf`, and opens an insertion editor with
    `replaceBlankRun: { line, endLine, itemLine?, containerLine? }`.
  - `requestDeleteBlankLines`, `stepSelection` and the Ctrl/Cmd+V branch
    (`src/page/features/blockSelectionView.ts`) post `previewBlankRunDelete` and
    `previewBlocksPaste` with the run.
- **Host.**
  - `checkBlankRun(text, line, endLine)` (`src/core/mapping/blockRange.ts`) requires a maximal run
    of two or more lines.
  - `planBlankRunInsertion` (`src/core/mapping/insertion.ts`) replaces the whole run, with one
    separator on each side. `planBlankRunRemoval` keeps one separator; `planBlankRunPaste` is the
    paste plan; `planBlankRunDelete` (`src/core/edits/sourceEdits.ts`) calls the removal.
    `blankRunIndent` (`src/core/mapping/blankRunContainer.ts`) gives the container indent.
  - In `src/session/features/blockEdits.ts`, `handleEditOpen` and the re-created edit path of
    `handleEditSave` check the run, `containerLineHolds` checks the item or container line, and
    `blankRunRegion` holds the run's text for a restore.
- **Protocol.** `isBlankRunFields` (`src/core/protocol/pageToHost.ts`) requires `endLine > line`.
- **Styles.** `BLANK_LINES_BLOCK_CSS` (`src/core/preview/styles/editModeStyles.ts`) and
  `blankLinesInContainersStyles.ts`.

### Decisions this CR replaces

| Earlier decision | Replaced by |
| --- | --- |
| CR-444 blank-runs-Q2: one blank-lines block per run of two or more blank lines; a single blank line at the start or the end of the body shows nothing | One blank-line block per shown blank line (Q1, Q2). Between two blocks, N lines give N−1 blocks. At the end of the body, at the top of a file without frontmatter, and in a body of only blank lines after the frontmatter, every blank line is a block, a single one included (Q2, Q5). |
| CR-444 blank-runs-Q2: an insertion editor replaces the whole run, with one separator on each side | Typed text replaces that one line. A blank line is added before or after it only when Markdown needs one (Q2). |
| CR-444 blank-runs-Q2: Delete removes the extra lines of the run and keeps one separator | Delete, Backspace or the Delete block button removes that one blank line. The hidden separator always stays (Q3). |
| CR-444 blank-runs-Q12: Ctrl/Cmd+V pastes in place of the run | Ctrl/Cmd+V pastes in place of that one line, with the same rule as typing (follows from Q2). |
| CR-448 br-Q2 and CR-462 bq-Q1: the same blank-lines block, one per run, inside lists, quotes and containers | The same per-line block inside lists, quotes, admonitions, definitions and footnotes, with their indent and sibling rules kept (Q4). |

Everything else of CR-444, CR-448 and CR-462 holds: placement inside containers, nothing shown in
folds, closed dropdowns, grids and included files, the host-only run list, the trust rule on
authored attributes, the export removal, line endings, the container indent and the sibling rules.
CR-444 fix 7 (the editor kept across an autosave's re-render) holds as A left it.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs. In a quote run, it is
  the run's first empty quote line.
- **Blank run**: unchanged. A maximal sequence of CommonMark blank lines (spaces and tabs only,
  `isCommonMarkBlank`), or of empty quote lines of one shape, after the frontmatter. It is now also
  read for a single line, where the shown-line rule below shows one.
- **Shown blank line**: a blank line of a run that gets a block. The rules, first match wins:
  1. **End of the body**: a run with nothing but blank lines after it (a body of only blank lines
     included, after the frontmatter's closing `---` or in a file without frontmatter): every line
     shows (N blocks; one for a single line). Q2, Q5.
  2. **Top of a file without frontmatter**: a run that starts at line 1: every line shows. Q2.
  3. **Quote run**: its first line is the separator, so lines `L+1`..`E` show.
  4. **Between two blocks** (the frontmatter counting as the block above): the separator is the
     run's first line, so lines `L+1`..`E` show (N−1 blocks; none for a single line).

  A quote run follows rule 3 wherever it stands (its first line is always kept as the separator).
- **Blank-line block**: the page element that shows one shown blank line in edit mode. It replaces
  the glossary term "Blank-lines block".

## What changes

### 1. The host lists shown blank lines (Q1, Q2, Q5)

- Add a pure function `shownBlankLines(text): BlankRun[]` in `src/core/mapping/blankRuns.ts`. It
  returns, in line order, the ranges of shown blank lines of every plain run and every quote run,
  by the "Shown blank line" rules. A range may be one line (`line === endLine`). It is built on the
  scan of `blankRuns` and `quoteBlankRuns`, which now also report runs of one line where a rule
  shows one. It keeps the existing rules: `splitLines` (the pseudo-line after a final break is
  never a line), frontmatter lines excluded (`frontmatterLineCount`), LF, CR LF and lone CR alike.
  The `@implements_req SwRS-MDOKFSTUDIO-BLOCK-266` marker goes on it.
- `blankRunsMarker` writes `shownBlankLines(text)` as `L-E` pairs (`L-L` for one line). The
  attribute, its place (last element of the content) and its export removal are unchanged.
- Add `blankRunAround(text, line): BlankRun | undefined` in `blankRuns.ts`: the maximal run (plain
  or quote) that holds a line. The host reads the container indent and the sibling rules from the
  whole run through it (section 3).

### 2. The page shows one block per shown line (Q1, Q4)

In `src/page/features/blankLines.ts`:

- `parseRuns` keeps a pair when `endLine >= line`. It still drops malformed and overlapping pairs,
  and still reads only the host's last element (the trust rule).
- Each range is located once (`locateRun`, unchanged: a range lies in the same container, fold or
  fence as its run). Then **one blank-line block per line** of the range is created, all placed at
  that spot, in line order. Each block's run is `{ line: n, endLine: n }`, plus the `itemLine`,
  `containerLine` and holder of its range. Inside lists, quotes, admonitions, definitions and
  footnotes this is the same (Q4); where a run shows nothing today (fold, closed dropdown, grid,
  included file), still nothing shows.
- `keyOf` is per line, so a block whose line is unchanged keeps its element across a re-render.
- **Look** (`BLANK_LINES_BLOCK_CSS` and `blankLinesInContainersStyles.ts`):
  - each block is about one line of body text high, and the blocks of one range stack with no
    gap, so 6 blank lines read as 6 lines;
  - the label is `Blank line`, drawn from `data-okf-blank-label` as today, never in the text
    content;
  - the `aria-label` is `Blank line. Press Enter to write a block here.`;
  - the Delete block button, the selected look and the edit-mode-only rule are unchanged.
- **Arrows** (`stepSelection`, BLOCK-004 and BLOCK-267): Up and Down stop on each blank-line block
  in line order, inside lists and containers too. The other key rules of BLOCK-267 are unchanged:
  the block selection never starts or ends on a blank-line block; Shift+click does nothing on one;
  Alt+Up/Down posts nothing; Escape clears the selection; Ctrl/Cmd+C and Ctrl/Cmd+X post nothing
  with only a blank-line block selected; Delete and Backspace act only on a selected blank-line
  block, not on a focused one.

### 3. Typing or pasting in a blank-line block replaces that one line (Q2)

- **Messages.** `replaceBlankRun` (on `previewEditOpen`, `previewEditSave`, `previewEditCancel` and
  `previewBlocksPaste`) and `previewBlankRunDelete` keep their names and fields; both now name one
  line. `isBlankRunFields` and the `previewBlankRunDelete` validator
  (`src/core/protocol/pageToHost.ts`) require `endLine === line` in place of `endLine > line`. The
  rule `insertAfterLine === line − 1` is unchanged.
- **The check.** `checkBlankLine(text, line): BlockRangeRefusal | undefined` in
  `src/core/mapping/blockRange.ts` refuses with `OUT_OF_DATE` unless `line` is a shown blank line of
  `shownBlankLines(text)`. It replaces `checkBlankRun` at every caller: `handleEditOpen`, the
  re-created edit path of `handleEditSave`, `planBlankRunPaste` and `planBlankRunRemoval`.
  `containerLineHolds` and `blankRunIndent` read the run from `blankRunAround(text, line)`, so the
  item and container checks, the content indent and the sibling rules of CR-448 and CR-462 are
  unchanged: `- c` typed in a blank-line block between two items is still written as a sibling
  item. `checkBlankRun` is removed when no caller is left (the unused-exports check).
- **The plan.** `planBlankRunInsertion` (`src/core/mapping/insertion.ts`) takes one line
  (`planBlankRunInsertion(text, line, itemLine?, containerLine?)`, or keeps `endLine` and requires
  `endLine === line`; the Driver picks):
  - **The region** is line `line` without its line break.
  - **A separator before** is written only when line `line − 1` exists and is not blank. "Not
    blank" means a block line, the frontmatter's closing `---` included, or, in a quote run, not an
    empty quote line of the run's shape. In a quote run, a separator is a copy of the run's first
    line, as today.
  - **A separator after** is written only when line `line + 1` exists and is not blank, by the same
    test.
  - The line break of line `line` stays as it is, so the document's final line break, or its
    absence, is kept.
  - `insertionText` is unchanged: it drops leading blank lines, uses the document's line endings
    and applies the container indent.
- **Host edit** (`blockEdits.ts`). `blankRunRegion` holds the one line, `{ line, endLine: line,
  itemLine?, containerLine?, text }`, and is still never sent to the page; the page-facing
  `originalText` stays `""`.
  - An empty or whitespace-only text, or Cancel after an autosave, writes that line's text back
    byte for byte, and any separator an autosave added goes with it. Nothing else changes.
  - Done with an empty text before any autosave makes no edit, and the editor closes (BLOCK-263).
  - The close after a final save that wrote text is A's (the content patch closes the editor);
    this CR does not change it.
- **Paste** (`planBlankRunPaste`, and `planBlocksPaste` in `src/core/edits/sourceEdits.ts`):
  Ctrl/Cmd+V on a selected blank-line block writes the pasted block in place of that one line, with
  the same separator rule.

### 4. Removing a blank-line block removes that one line (Q3)

- `planBlankRunRemoval(text, line)` (`src/core/mapping/blockRange.ts`, through `planBlankRunDelete`)
  removes line `line` and its line break, in one `TextEdit` through `applyWrittenEdits`, as one undo
  step.
  - When the line is the last line of the text, the removal takes the line break before it instead,
    so the text keeps its final line break, or its absence, as today.
  - A text of only blank lines whose last line goes becomes empty.
- The separator is never a shown line, so it is never removed and two blocks are never glued
  together. In a quote run, the first empty quote line stays byte for byte.
- The answer is unchanged: `previewBlocksResult` with `op: "delete-blank-lines"`, and a stale
  refusal shown next to the blank-line block.
- **Selection afterwards** (`requestDeleteBlankLines`, `blockSelectionView.ts`), in this order:
  1. the blank-line block that now shows at the same place (the next blank line, which takes the
     removed line's number), so repeated Delete clears the lines one by one;
  2. else today's rule: the block that followed, the container that held the run, the block above,
     or "Start writing".

  The cut's viewport pin is unchanged.

### 5. Requirements, vocabulary and docs

Follow the project's requirements guidelines: markers move with the code, run
`just requirements-update`, and add a dated entry in `requirements/tiers/log.md`. All in scope
`block-editing` (`requirements/tiers/swrs/block-editing/`):

- **SwRS-MDOKFSTUDIO-BLOCK-266**: each shown blank line shows as one blank-line block. Between two
  blocks N lines give N−1 blocks; at the end of the body, at the top of a file without frontmatter
  and in a body of only blank lines after the frontmatter, every line is a block; in a quote run
  the first line is the separator; this holds inside lists, quotes, admonitions, definitions and
  footnotes. Its scenarios get the issue's case: a line of text then 6 blank lines gives 6 blocks;
  and the case of Q5: frontmatter then 3 blank lines gives 3 blocks.
- **BLOCK-267**: Up and Down stop on each blank-line block.
- **BLOCK-268**: typed or pasted text replaces that one line; a separator is added only where a
  neighbour line is not blank; Cancel or an emptied editor restores the line. What A wrote in it
  about the close after a final save stays.
- **BLOCK-269**: Delete removes that one line, the separator stays, and the selection goes first to
  the blank-line block now in its place.
- **BLOCK-004**: a scenario row for one stop per blank-line block.
- Their verification notes name the tests of the Evidence. Approved StRS texts are not changed
  (StRS-MDOKFSTUDIO-BLOCK-025 and BLOCK-011 speak of edits landing exactly, which still holds); if
  one must change, its re-approval goes to the owner through the Chief of Staff.

Vocabulary and docs:

- `.agents/glossary/common.md`: rename "Blank-lines block" to "Blank-line block" (one per shown
  blank line, label `Blank line`); add "Shown blank line" and "Separator" as in "Words"; in "Blank
  run", note that the host lists shown lines, single ones included.
- Page text and labels say "blank line". Code identifiers (`installBlankLines`,
  `.sphinx-preview-blank-lines`, `replaceBlankRun`, `previewBlankRunDelete`) keep their names.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes, and the blocks are edit-mode chrome.

## Out of scope

- What A and B deliver: the close of a blank-line editor after its final save, the save time
  limit, the frontmatter wait, Cancel during "Saving…", BLOCK-053, TABLE-025, the save-to-render
  measure.
- Blank lines inside a block (fence, directive body edited whole, HTML block, table), in an
  included file, in a fold or a closed dropdown, in a grid: unchanged (nothing shows).
- Anything inside the frontmatter (Q5).
- Collapsing blank lines on its own, on save or render: the file's format is kept.
- Selecting several blank-line blocks at once to delete them in one step.
- Renaming code identifiers from "blank run" or "blank lines" to "blank line".
- The release notes, written when the release is prepared.

## Evidence

The checks read the shipped files at the head under test: the real core and render functions, the
real page bundle and the real stylesheet module, never a prepared copy. Each check below fails on
A and B's head before this change (constitution, section 3).

**Core (`test/core/mapping/`):**

- `blankRuns.test.ts`, `shownBlankLines`:
  - N blank lines between two paragraphs, N = 1, 2, 3 and 6: 0, 1, 2 and 5 shown lines, starting
    at the second blank line;
  - the issue's text, `Text` then 6 blank lines, with and without a final line break: lines 2..7,
    6 shown;
  - the top of a file without frontmatter: every line shows; after the frontmatter and before a
    block: N−1 lines;
  - frontmatter then only 3 blank lines: 3 shown (Q5); a file of only blank lines: every line;
  - quote runs: the first line is never shown, including at the end of the body;
  - a U+00A0 line breaks a run; LF, CR LF and lone CR;
  - `blankRunAround` returns the maximal run of a line, plain and quote.
- `blockRange.test.ts`:
  - `checkBlankLine` accepts a shown line and refuses the separator, a non-blank line, a line inside
    the frontmatter and a line past the end;
  - `planBlankRunRemoval` removes one line in the middle of a run, the last line of the text with
    and without a final break, and a line of a text of only blank lines; it never removes a
    separator, and adds no bare LF in CR LF and no CR in LF;
  - `planBlankRunPaste` writes in place of one line.
- `insertion.test.ts`, `planBlankRunInsertion` on one line:
  - the first shown line of a 3-line run between blocks adds no separator; the last adds one after;
  - the first line of a run at the end of the body adds one before;
  - line 1 at the top of a file adds one after;
  - the first line of a blank-only body after the frontmatter adds one before (after `---`);
  - a quote run's separator is a copy of its first line;
  - LF, CR LF and CR.
- `blankRunContainer.test.ts`, `blankRunInList.test.ts`, `quoteBlankRuns.test.ts`, updated: a line
  between two list items takes the sibling indent for `- c` and the content indent otherwise; a
  line inside a quote keeps the quote markers; a line in an admonition, a definition and a footnote
  takes the container indent.

**Render and protocol:**

- `renderPreviewSource` ends with `data-okf-blank-runs` holding the shown ranges (`7-7` for one
  line).
- `pageToHost.test.ts`: `replaceBlankRun` and `previewBlankRunDelete` are accepted with
  `endLine === line` and rejected with `endLine !== line`.

**Session (`test/session/blankRunHost.test.ts`, `blankRunInListHost.test.ts`,
`blankRunInContainerHost.test.ts`):**

- a final save of `Middle` in a blank-line block writes it in place of the line with only the
  separators needed;
- an autosave then Cancel restores the line byte for byte;
- an empty Done writes nothing and posts `done: true`;
- a separator line is refused on open, and on a re-created save;
- `previewBlankRunDelete` removes one line in one `applyWrittenEdits` call;
- the same in a list item and in a container.

**Page (`test/page/runtimeBlankLines.test.ts`, `runtimeBlankLinesContainers.test.ts`, with the
runtime bundle; one check per rule):**

- a list `3-4` places two blocks in line order, `7-7` places one; label and `aria-label` as in
  section 2;
- Down stops on each;
- Enter on the second posts `previewEditOpen` with `replaceBlankRun: { line: 4, endLine: 4 }`;
- Delete posts `previewBlankRunDelete` for one line; after the result and the render, the selection
  is on the blank-line block now at that place;
- the same placement and arrows inside a list item and a quote;
- an authored `data-okf-blank-runs` still makes no block;
- A's regression tests, with their run lists rewritten per line, still pass.

**Visual (`just ci-visual`):** `test/visual/capture_blank_lines_block.py`,
`capture_blank_lines_containers.py`, `blankLinesBlockScenarios.ts` and the fixture
`test/visual/fixtures/92-blank-lines-block.md` are updated. The captures, attached to the pull
request as the pull-request guideline asks:

- edit mode with three blank lines between two paragraphs, showing two blank-line blocks;
- the issue's text, with six blank-line blocks at the end of the body;
- one block selected, with its Delete block button;
- blank-line blocks inside a list and a quote;
- reading mode of the same file, with no block.

**Integration (real VS Code, `test/integration/blankLines.test.ts`, the heavy run on the
branch).** The scenario runs once in LF and once in CR LF:

1. A file `Text.` followed by 6 blank lines. Edit mode shows 6 blank-line blocks.
2. Click the first one, type `More` and press Done. The editor closes (A) within
   `FINAL_SAVE_TIMEOUT_MS` (B). The file reads `Text.`, a blank line, `More`, then 5 blank lines:
   the typed text replaces line 2 and adds a separator before it, and lines 3 to 7 stay, with the
   line endings and the final line break kept. 5 blank-line blocks show after `More`.
3. Three blank lines between two paragraphs: 2 blocks show. Select one with the arrows and press
   Delete: 2 blank lines are left and 1 block shows. One Ctrl+Z brings the third line back.
4. Click a block, type a word, wait past the autosave and press Cancel: the blank lines are back
   byte for byte.
5. Three blank lines between two items of a list: 2 blocks show in the list; type `- c` in one and
   press Done: `- c` is a sibling item.

**Requirements:** `just requirements-lint` and `just requirements-update` pass; the updated SwRS
carry `@implements_req` / `@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

The answers leave these points open; each is decided as the option most consistent with them, for
the Chief of Staff to check:

1. **The hidden separator is the first line of a run** (the line right after the block above), and
   in a quote run its first empty quote line, as the removal keeps today.
2. **A quote run keeps its first line as separator even at the end of the body**: dropping it would
   end the quote or merge it with what follows.
3. **A separator before the typed text is added after the frontmatter's closing `---`**, as an
   insertion after the properties section writes one today.
4. **After a Delete, the selection goes to the blank-line block now in its place**, so repeated
   Delete clears the lines one by one.
5. **The label is `Blank line`** with no count, since each block is one line.
6. **Spec critic**: yes, on Fable (Q7, owner's rule). The Chief of Staff runs it.

## Open questions

None.
