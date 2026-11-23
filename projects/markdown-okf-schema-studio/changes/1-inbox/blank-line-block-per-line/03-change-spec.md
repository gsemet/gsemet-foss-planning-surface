# One blank-line block per extra blank line

In edit mode, each blank line beyond the one Markdown needs as a separator shows as its own
blank-line block, at the top level and inside containers. Typing in one replaces that one line;
deleting one removes that one line. This replaces the one block per run of CR-444, and amends
StRS-MDOKFSTUDIO-BLOCK-011 with the owner's re-approval.

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
- **StRS-MDOKFSTUDIO-BLOCK-011 is amended** (Q8): its text names the blank-line block's rule (text
  typed in one keeps the other blank lines around it), with the owner's re-approval of the new
  wording (section 5, "Proposed text of StRS-MDOKFSTUDIO-BLOCK-011").
- **The selection after a Delete** (Q9) goes to the blank-line block now at that place, else the
  blank-line block just above it in the same run; when the run has none left, nothing is selected,
  so one more Delete removes no text.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there, including "Approved requirements" in
`requirements/guidelines/project.guidelines.md`. This specification restates none of them.

## Place in the stack (Q6)

This CR is the last of three in batch-09's stack, and its branch starts from the head of the second:

1. `blank-run-edit-stuck-saving` (A, the fix of issue 485): the content patch closes a blank-lines
   block's editor once its final save was posted, while an autosave's re-render still keeps it
   open (CR-444 fix 7). It carries the `issue:` line and closes the issue.
2. `save-guard-never-hangs` (B): tests only, around the final save of an editor;
   its own specification says what they cover.
3. This CR (C): one block per extra blank line.

This CR changes nothing that A or B deliver, and repeats none of their checks. It relies on them:
a blank-line block's editor (it still carries `replaceBlankRun`) closes on the render of its final
save by A's rule.

**A's regression tests** (`4-batch/2-actives/474-blank-run-edit-stuck-saving/03-change-spec.md`,
Evidence, steps 1 and 2, in `test/page/runtimeBlankLines.test.ts`) keep their run lists (for example
`2-7`, which now lists 6 shown lines) and every close assertion as A wrote them. Only two things
become per line:

- "One blank-lines block shows" becomes "6 blank-line blocks show";
- the click (on the first of them) posts `replaceBlankRun: { line: 2, endLine: 2 }` in place of
  `{ line: 2, endLine: 7 }`.

The list variant and the fix-7 tests A names are adjusted the same way (the block clicked names one
line), with their assertions kept. This CR has no `issue:` line: A closes the issue.

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
    `data-okf-blank-label` (line 102), gives it the `aria-label` `Blank lines, N lines. Press Enter
    to write a block here.` (line 101), reuses blocks across a refresh by `keyOf`, and opens an
    insertion editor with `replaceBlankRun: { line, endLine, itemLine?, containerLine? }`.
  - `requestDeleteBlankLines`, `stepSelection` and the Ctrl/Cmd+V branch
    (`src/page/features/blockSelectionView.ts`) post `previewBlankRunDelete` and
    `previewBlocksPaste` with the run. `requestDeleteBlankLines` sets `state.pendingBlockSelection`
    to the container that held the run, else the block after it (`afterRunIndex`), else the one
    before. `selectBlank` writes the status text "Blank lines selected" (line 310).
- **Host.**
  - `checkBlankRun(text, line, endLine)` (`src/core/mapping/blockRange.ts`) requires a maximal run
    of two or more lines.
  - `planBlankRunInsertion(text, line, endLine, itemLine?, containerLine?)`
    (`src/core/mapping/insertion.ts`) replaces the whole run, with one separator on each side.
    `planBlankRunRemoval` keeps one separator; `planBlankRunPaste` is the paste plan;
    `planBlankRunDelete` (`src/core/edits/sourceEdits.ts`) calls the removal. `blankRunIndent`
    (`src/core/mapping/blankRunContainer.ts`) gives the container indent.
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
| CR-444: after a blank run delete, the block that followed is selected, else the one above | The blank-line block now at that place, else the one just above it in the same run, else nothing (Q9). |
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
- **Blank, for a neighbour line** (used by the separator rule of section 3): a CommonMark blank
  line, or, in a quote run, an empty quote line of the run's shape. Any other line is "not blank",
  the frontmatter's closing `---` included.
- **Shown blank line**: a blank line of a run that gets a block. The rules, first match wins:
  1. **Quote run**, wherever it stands (at the end of the body and at line 1 too): its first line
     is the separator, so lines `L+1`..`E` show.
  2. **Plain run at the end of the body**: a plain run with nothing but blank lines after it (a
     body of only blank lines included, after the frontmatter's closing `---` or in a file without
     frontmatter): every line shows (N blocks; one for a single line). Q2, Q5.
  3. **Plain run at the top of a file without frontmatter**: a plain run that starts at line 1:
     every line shows. Q2.
  4. **Plain run between two blocks** (the frontmatter counting as the block above): the separator
     is the run's first line, so lines `L+1`..`E` show (N−1 blocks; none for a single line).
- **Blank-line block**: the page element that shows one shown blank line in edit mode. It replaces
  the glossary term "Blank-lines block".

## What changes

### 1. The host lists shown blank lines (Q1, Q2, Q5)

- Add a pure function `shownBlankLines(text): BlankRun[]` in `src/core/mapping/blankRuns.ts`. It
  returns, in line order, the ranges of shown blank lines of every plain run and every quote run,
  by the "Shown blank line" rules, one range per run that shows at least one line. A range may be
  one line (`line === endLine`). It is built on the scan of `blankRuns` and `quoteBlankRuns`, which
  now also report runs of one line where a rule shows one. It keeps the existing rules: `splitLines`
  (the pseudo-line after a final break is never a line), frontmatter lines excluded
  (`frontmatterLineCount`), LF, CR LF and lone CR alike. The
  `@implements_req SwRS-MDOKFSTUDIO-BLOCK-266` marker goes on it.
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
  `containerLine` and holder of its range; the page also keeps the first line of the range the
  block came from (the "same run" of section 4). Inside lists, quotes, admonitions, definitions
  and footnotes this is the same (Q4); where a run shows nothing today (fold, closed dropdown,
  grid, included file), still nothing shows.
- `keyOf` is per line, so a block whose line is unchanged keeps its element across a re-render.
- **Look** (`BLANK_LINES_BLOCK_CSS` and `blankLinesInContainersStyles.ts`):
  - each block is about one line of body text high, and the blocks of one range stack with no
    gap, so 6 blank lines read as 6 lines;
  - the label is `Blank line` (in place of `Blank lines (N)`, `blankLines.ts` line 102), drawn from
    `data-okf-blank-label` as today, never in the text content;
  - the `aria-label` is `Blank line. Press Enter to write a block here.` (in place of `Blank lines,
    N lines. ...`, line 101);
  - the Delete block button, the selected look and the edit-mode-only rule are unchanged.
- **Status text.** `selectBlank` (`src/page/features/blockSelectionView.ts`, line 310) writes
  "Blank line selected" in place of "Blank lines selected".
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
  - **A separator before** is written only when line `line − 1` exists and is not blank ("Blank,
    for a neighbour line" in "Words": a CommonMark blank line, or, in a quote run, an empty quote
    line of the run's shape).
  - **A separator after** is written only when line `line + 1` exists and is not blank, by the same
    test. A CommonMark blank line after a quote run counts as blank: for `> a`, `>`, `>`, a blank
    line, `Text`, text typed in line 3 gives `> a`, `>`, `> <text>`, the blank line, `Text`, with
    no extra `>` line.
  - In a quote run, a separator is a copy of the run's first line, as today.
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

### 4. Removing a blank-line block removes that one line (Q3, Q9)

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
- **Selection afterwards** (Q9; `requestDeleteBlankLines`, `blockSelectionView.ts`). The page
  remembers the deleted line `n` and its run (the first line and the holder of the range it came
  from; removing a line at or after a range's first line never moves that first line). After the
  result and the render, in this order:
  1. the blank-line block of line `n` in the same run (the next blank line, which took the removed
     line's number), so repeated Delete clears the lines one by one, top down;
  2. else the blank-line block of line `n − 1` in the same run (the line deleted was the run's
     last shown line), so repeated Delete goes on upward;
  3. else nothing is selected: no blank-line block and no block selection (the run has no shown
     line left). One more Delete or Backspace then posts nothing and removes no text.

  This replaces, for a blank-line block, today's `pendingBlockSelection` target (the container
  that held the run, the block after it via `afterRunIndex`, else the one before). The cut's
  viewport pin is unchanged. A refused delete keeps the block selected, as today.

### 5. Requirements, vocabulary and docs

Follow the project's requirements guidelines: markers move with the code, run
`just requirements-update`, and add a dated entry in `requirements/tiers/log.md`. All in scope
`block-editing` (`requirements/tiers/swrs/block-editing/`):

- **SwRS-MDOKFSTUDIO-BLOCK-266** (title and text): each shown blank line shows as one blank-line
  block. Between two blocks N lines give N−1 blocks; at the end of the body, at the top of a file
  without frontmatter and in a body of only blank lines after the frontmatter, every line is a
  block; in a quote run the first line is the separator wherever the run stands; this holds inside
  lists, quotes, admonitions, definitions and footnotes. Its scenarios get the issue's case: a line
  of text then 6 blank lines gives 6 blocks; and the case of Q5: frontmatter then 3 blank lines
  gives 3 blocks.
- **BLOCK-267** (title and text): Up and Down stop on each blank-line block.
- **BLOCK-268** (title and text): typed or pasted text replaces that one line; a separator is added
  only where a neighbour line is not blank; Cancel or an emptied editor restores the line. What A
  wrote in it about the close after a final save stays.
- **BLOCK-269** (title and text; today "Removing a blank-lines block keeps one separator"): Delete
  removes that one line, the separator stays, and the selection goes to the blank-line block now at
  that place, else the one just above it in the same run, else nothing, so one more Delete removes
  no text (Q9).
- **BLOCK-265**, scenario "A blank-lines block" (line 78, today "previewBlankRunDelete removes the
  extra blank lines and keeps one separator"): "A blank-line block" / previewBlankRunDelete removes
  that one blank line and the separator stays (see SwRS-MDOKFSTUDIO-BLOCK-269).
- **BLOCK-004**: a scenario row for one stop per blank-line block.
- Their verification notes name the tests of the Evidence.
- **StRS-MDOKFSTUDIO-BLOCK-011** is amended (Q8) by the text below, which the owner approved on
  2026-11-23 (Q10), and becomes approved (Q11): `req_lifecycle: approved`,
  `approved_by: gaetan@xeberon.net`, `approved_at: '2026-11-23T14:00:00+01:00'`, in the same form as
  the other approved StRS. The PR body lists it under "Approved requirements changed", and the
  agent that opens the PR requests the owner's review. StRS-MDOKFSTUDIO-BLOCK-025 (approved;
  edits land exactly, in one undo step, keep line endings) still holds and is not changed.

#### Proposed text of StRS-MDOKFSTUDIO-BLOCK-011 (for the owner's re-approval)

Today (line 39, and the same sentence in `description:`):

> When a writer clicks the insert point after a block in edit mode, or opens the preview of a
> document with no body in edit mode and uses the Start writing button or the Enter key, the Studio
> SHALL open an empty editor at that place and insert the typed text as a new block with one blank
> line on each side.

Proposed, for both the `### Normative behavior` paragraph and the `description:` field, verbatim:

> When a writer clicks the insert point after a block in edit mode, or opens the preview of a
> document with no body in edit mode and uses the Start writing button or the Enter key, the Studio
> SHALL open an empty editor at that place and insert the typed text as a new block with one blank
> line on each side. When a writer types in a blank-line block of edit mode, the Studio SHALL write
> the typed text in place of that one blank line and keep the other blank lines around it, adding a
> blank line before or after the text only where Markdown needs one to separate it from a
> neighbouring block.

Proposed, added at the end of `### Main paths`, verbatim:

```markdown
#### Path 3: Write on a blank line

1. Edit mode is on and the document has extra blank lines
   - SwRS-MDOKFSTUDIO-BLOCK-266: each extra blank line shows as a blank-line block
2. A blank-line block is shown
   - SwRS-MDOKFSTUDIO-BLOCK-268: the writer types in it and the host writes the text in place of that one blank line, keeping the other blank lines
   - Option SwRS-MDOKFSTUDIO-BLOCK-269 (nominal): Delete removes that one blank line
3. The typed text is in the document where the blank line was
```

The title, `user_need`, "Preserved stakeholder intent", "Rationale and constraints", the diagram,
paths 1 and 2 and the relations are unchanged; the generated Links block follows the new SwRS
titles through `just requirements-update`.

Vocabulary, test texts and docs:

- `.agents/glossary/common.md`: rename "Blank-lines block" to "Blank-line block" (one per shown
  blank line, label `Blank line`); add "Shown blank line" and "Separator" as in "Words"; in "Blank
  run", note that the host lists shown lines, single ones included.
- `test/shared/e2eGroups.ts` line 78, the `locks` text of `test/integration/blankLines.test.ts`
  (today "one block with one blank line on each side, one blank line kept on delete, one undo brings
  the run back"): it says what the file now locks, for example "One blank line written in place and
  removed on a real LF and CRLF file: the other blank lines stay, a separator only where needed,
  Delete removes that one line, one undo brings it back".
- Visual texts: the scenario descriptions in `test/visual/blankLinesBlockScenarios.ts` (v44 to v53;
  v44 says "one dashed blank-lines block labelled 'Blank lines (3)'") and their copies in
  `test/visual/scenarioIds.ts` (lines 777 to 786), and the expectations of
  `test/visual/capture_blank_lines_block.py` (one block expected, "Blank lines (3)" at line 78, two
  blocks in lists) and `test/visual/capture_blank_lines_containers.py` (one block per container)
  say blank-line blocks, one per shown line. The fixtures `92-blank-lines-block.md`,
  `93-blank-lines-in-lists.md` and `95-blank-lines-in-containers.md` keep their 3-line runs (each
  now shows 2 blocks); their heading and lead texts that say "a run" are updated when they describe
  one block.
- Page text and labels say "blank line". Code identifiers (`installBlankLines`,
  `.sphinx-preview-blank-lines`, `replaceBlankRun`, `previewBlankRunDelete`) keep their names.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes, and the blocks are edit-mode chrome.

## Out of scope

- What A and B deliver: the close of a blank-line editor after its final save (A) and B's tests.
- Blank lines inside a block (fence, directive body edited whole, HTML block, table), in an
  included file, in a fold or a closed dropdown, in a grid: unchanged (nothing shows).
- Anything inside the frontmatter (Q5).
- Collapsing blank lines on its own, on save or render: the file's format is kept.
- Selecting several blank-line blocks at once to delete them in one step.
- Renaming code identifiers from "blank run" or "blank lines" to "blank line".
- Any StRS other than BLOCK-011.
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
  - quote runs: the first line is never shown, at the end of the body and at line 1 included
    (rule 1 comes before the plain-run rules);
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
  - `> a`, `>`, `>`, a blank line, `Text`: line 3 adds no separator after (the blank line counts as
    blank), so no extra `>` line is written;
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

- a list `3-4` places two blocks in line order, `7-7` places one; label, `aria-label` and the
  status text "Blank line selected" as in section 2 (the `aria-label` check at line 87 of
  `runtimeBlankLines.test.ts` is updated);
- the issue's list `2-7` places 6 blocks;
- Down stops on each, inside a list item and a quote too;
- a click on a block, and Enter on the second, post `previewEditOpen` with
  `replaceBlankRun: { line: n, endLine: n }`;
- Delete posts `previewBlankRunDelete` for one line;
- selection after Delete (Q9), replacing the test "after a blank run is deleted the block that
  followed it is selected, else the one above" (line 235):
  - from the middle or the top of a run: list `3-5`, Delete on line 4, then the result and a patch
    with `3-4`: the block of line 4 is selected;
  - from the bottom of a run: list `3-5`, Delete on line 5, then a patch with `3-4`: the block of
    line 4, just above, is selected;
  - the last one: list `3-3`, Delete on line 3, then a patch with no range: no blank-line block and
    no block is selected, and one more Delete and one more Backspace post no message (no
    `previewBlankRunDelete`, no `previewBlocksDelete`): no text is removed;
- an authored `data-okf-blank-runs` still makes no block;
- A's regression tests and the fix-7 tests, adjusted per line as "Place in the stack" says (6
  blocks, `{ line: 2, endLine: 2 }`), keep their run lists and close assertions and pass.

**Visual, real input (`just ci-visual`, `test/visual/blankLinesBlockScenarios.ts`,
`capture_blank_lines_block.py`, `capture_blank_lines_containers.py`):** the scenarios drive the
page with Playwright's real clicks and keys. They are updated as section 5 says and check:

- edit mode with three blank lines between two paragraphs (`92-blank-lines-block.md`): two
  blank-line blocks, each about one line high, stacked with no gap, label `Blank line`;
- a new scenario with the issue's text (`Text.` then 6 blank lines, a new fixture): six blank-line
  blocks at the end of the body;
- Down from the first paragraph selects the first block, Down again the second; the selected one
  shows its Delete block button;
- blank-line blocks inside a list (`93-blank-lines-in-lists.md`: 2 per 3-line run, none in the
  fence) and in each container (`95-blank-lines-in-containers.md`: 2 per container);
- a click on a block opens its editor at that place (in the list item, in the quote), as the
  existing typing steps do;
- reading mode of the same files, with no block.

The captures are attached to the pull request as the pull-request guideline asks.

**Integration (real VS Code, `test/integration/blankLines.test.ts`, the heavy run on the
branch).** The file drives the host by messages (`sendPreviewMessageForTests`) and sees no page: it
checks the file's text, undo and line endings only. Each case runs once in LF and once in CR LF,
with no bare LF in CR LF:

1. A file `Text.` followed by 6 blank lines. A `previewEditSave` with
   `replaceBlankRun: { line: 2, endLine: 2 }` and `More`: the file reads `Text.`, a blank line,
   `More`, then 5 blank lines, with the final line break kept. One undo brings the 6 blank lines
   back.
2. Three blank lines between two paragraphs (`LINES`): `previewBlankRunDelete` on line 5: 2 blank
   lines are left; one undo brings the third back. The same message on line 4 (the separator) is
   refused and the file does not change.
3. An autosave (`final: false`) then `previewEditCancel`: the blank lines are back byte for byte.
4. In `LIST_LINES`, `- c` saved on line 5 between two items is a sibling item; `More` saved on
   line 11 inside the item is written with the content indent; a delete on line 5 removes one line.
5. In `CONTAINER_LINES`, the quote (line 5), the admonition (line 14) and the footnote (line 23):
   `More` is written in place of that line with the container's markers or indent, the other
   empty lines stay, and one undo brings the file back.

Block counts, clicks, arrows, the selection after Delete and the editor's close are proven by the
page tests and the visual scenarios above, not here.

**Requirements:** `just requirements-lint` (including `scripts/check_main_paths.py` on the new
path 3 of BLOCK-011) and `just requirements-update` pass; the updated SwRS carry `@implements_req` /
`@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

The answers leave these points open; each is decided as the option most consistent with them, for
the Chief of Staff to check:

1. **The hidden separator is the first line of a run** (the line right after the block above), and
   in a quote run its first empty quote line, as the removal keeps today.
2. **A quote run keeps its first line as separator wherever it stands**, at the end of the body and
   at line 1 too: dropping it would end the quote or merge it with what follows. The quote-run rule
   is therefore checked first.
3. **A separator before the typed text is added after the frontmatter's closing `---`**, as an
   insertion after the properties section writes one today.
4. **The selection after a Delete** follows Q9: the block now at that place, else the one just
   above in the same run, else nothing. "The same run" is the range of the marker the block came
   from, known on the page by its first line and holder.
5. **The label is `Blank line`** with no count, since each block is one line; the status text is
   "Blank line selected".
6. **A CommonMark blank line next to a quote run counts as blank** for the separator test, so no
   extra empty quote line is written before a blank line (spec critic).
7. **Spec critic**: yes, on Fable (Q7, owner's rule). The Chief of Staff runs it.

8. **BLOCK-011's text and lifecycle**: the owner approved the proposed text verbatim (Q10) and
   asked that the StRS become `approved` (Q11).

## Open questions

None.
