# Show blank-line runs inside quotes, alerts, admonitions, definitions and footnotes

In edit mode, a run of two or more blank lines inside a quote or a GitHub alert (its empty `>`
lines), inside a MyST admonition or another directive that holds Markdown, inside a definition of a
definition list, or inside a footnote definition shows as the same blank-lines block CR-444 and
CR-448 show. It is placed inside the container where the run is. The writer reaches it, types in it
or removes it as with any blank-lines block. A block typed there takes the container's `>` prefix
and content indent, so it stays inside. Removing the run keeps one line (one empty `>` line in a
quote), and nothing else in the file changes.

Origin: verbal (split off from CR-448 blank-runs-inside-lists, 2026-11-21; owner's goal,
2026-11-20; owner's answers, 2026-11-21). No issue.

## Goal

The owner's goal (2026-11-20): blank lines beyond the one separator are always reachable in edit
mode. CR-444 (PR #453) made the runs between top-level blocks reachable, and CR-448 (PR #463) the
runs inside lists. A run inside any other container is still unreachable, or reachable with a wrong
result:

- Inside a quote or a GitHub alert, the empty lines are `>` lines. They are not CommonMark blank
  lines, so `blankRuns` never lists them.
- A MyST admonition, a definition list and the other directive containers are top-level blocks that
  hold the run, and the page skips every run that a block other than a list holds.
- A footnote definition's paragraphs are top-level mapped blocks (the footnotes `section`, its `ol`
  and its `li` carry no source line), so by the code read a run between two paragraphs of a
  footnote shows today by CR-444's top-level rule. But a block typed there is written at column 0
  and leaves the footnote (`renderPreviewSource` reads a paragraph indented 2 spaces after
  `[^a]: f1` as a body paragraph, and one indented 4 spaces as part of the footnote).

This CR covers all of them at once (bq-Q1, "Tout d'un coup"). It reuses everything CR-444 and
CR-448 built. Their specifications are
`4-batch/3-done/444-empty-block-blank-lines-block/03-change-spec.md` and
`4-batch/3-done/448-blank-runs-inside-lists/03-change-spec.md` in the planning folder. This file
restates what a Driver needs from them.

Base: `origin/main` of markdown-okf-schema-studio, at or after `2d3187b6` (version 1.11.0), which
holds CR-444 (`399f1d05`) and CR-448 (`3eca44a4`). The references below are read from that commit,
and the rendered HTML quoted below comes from its `renderPreviewSource`.

Project rules: this change follows the project's constitution (`.agents/constitution.md`), its
`AGENTS.md` (requirements, completion gate `just preflight`) and the requirements guidelines named
there. This specification restates none of them.

Batch: once specified, this CR joins the running batch-07, in the stack shape (owner, 2026-11-21).

## Words

- **Blank run**, **Blank-lines block**, **Separator**, **CommonMark blank line**: as in CR-444 and
  `.agents/glossary/common.md`. **Holder**, **Host item**, **Item line**, **Columns**, **List
  marker**, **Item indent**, **Content indent**: as in CR-448 ("Words").
- **Quote marker**: a `>` that opens or continues a quote level, as CommonMark reads it: after the
  line's leading spaces and tabs, or after the previous quote marker and the spaces and tabs after
  it.
- **Empty quote line**: a line made only of spaces, tabs and one or more quote markers, with nothing
  after the last marker but spaces and tabs (`>`, `> `, `> >`, `  >`). Its **depth** is its number
  of quote markers. Its **quote prefix** is its text up to and including its last quote marker.
- **Quote run**: a maximal sequence of two or more consecutive empty quote lines of the same depth,
  whose quote markers sit at the same columns (CR-448's column count, a tab to the next stop of 4),
  after the frontmatter. "Maximal": the line above and the line below are not empty quote lines of
  that same depth and columns. Lines of another depth do not join it: in `> > c`, `> >`, `>`,
  `> > d`, the `> >` line belongs to the inner quote and the `>` line closes it, so keeping one of
  them would merge or split quotes (bq-Q2: "the quote stays one quote"). Such a mix is no run.
- **Plain run**: a blank run as CR-444 defines it (CommonMark blank lines). Every run is either a
  plain run or a quote run. A plain run and a quote run can be next to each other (`> a`, `>`, `>`,
  blank, blank, `b`).
- **Container**: an element of the page that holds Markdown blocks. The closed list is in section
  2. A **quote container** is a quote or an alert. A **directive container** is an admonition or
  another directive of the list. A **definition** is a `dd` of a definition list. A **footnote** is
  an `li` of the footnotes section (`section[data-footnotes] li`).
- **Host container** of a run: the innermost container that holds it, where its blank-lines block
  goes (section 2).
- **Container line**: the source line the host reads a container's indent from: a directive's
  opening fence line, a definition's marker line (`:` or `~`), or a footnote's label line
  (`[^label]:`). A list item's is its item line (CR-448). A quote container has none: its prefix is
  read from the run's own lines.
- **Container indent**: the text a block typed in place of a run takes before each of its lines so
  it stays in the host container (section 4).

## What CR-444 and CR-448 already give, unchanged

- **The page reads only the host's run list** (`readRuns` in `src/page/features/blankLines.ts`,
  the last element of the content, `<div hidden data-okf-blank-runs="L-E ...">`) and builds every
  blank-lines block itself (`create`). CR-444's guard against an authored attribute holds.
- **The block's look, label, keys and messages**: the dashed bar with the CSS label "Blank lines
  (N)", `role="button"`, `tabindex="0"`, the Delete block button at its left edge; Enter or a click
  opens the insertion editor (`open`); Delete and Backspace act on a selected block
  (`deleteSelection`); the messages `previewBlankRunDelete`, `previewEditOpen`/`Save`/`Cancel` and
  `previewBlocksPaste` with `replaceBlankRun`; the editor stays open across an autosave's
  re-render.
- **Plain runs keep every rule**: `blankRuns`, `isCommonMarkBlank`, today's branch of
  `checkBlankRun` and of `planBlankRunRemoval` (`src/core/mapping/blockRange.ts`), and the
  separators of `planBlankRunInsertion` (`src/core/mapping/insertion.ts`). Plain runs inside a
  directive container, a definition or a footnote are already in the host's list (the hidden list
  of origin/main shows them) and pass the run checks: only their placement on the page and the
  indent of a typed block change for them.
- **Lists keep CR-448's rules**: placement in the host item, `itemLine`, `listItemIndent`
  (`src/core/mapping/listItemIndent.ts`), the item indent for a list marker typed between items,
  the content indent otherwise. This CR applies them also to a list inside a quote, by reading the
  item line and the line after the run without their quote prefix (section 4).
- **The keyboard order**: `neighbourStop` in `src/page/features/blockSelectionView.ts` already
  orders the stops by first line, so Down from a selected top-level block reaches each blank-lines
  block inside it, in line order, then the block after it; Shift+Up/Down from a blank-lines block
  starts the block selection on the nearest body block in that direction (CR-448 section 3). This
  holds for any container.

## What changes

### 1. The host lists quote runs (bq-Q1)

- Add a pure function, for example `quoteBlankRuns(text): BlankRun[]`, in
  `src/core/mapping/blankRuns.ts`, beside `blankRuns`. It returns every quote run (see "Words") as
  1-based document lines, in document order. It uses `splitLines`, skips the frontmatter
  (`frontmatterLineCount`) and works the same in LF, CR LF and lone CR. Add a helper that reads an
  empty quote line, for example `emptyQuoteLine(text): { depth: number; columns: number[]; prefix:
  string } | undefined`, exported for the run checks and the plan (sections 3 and 4). It has no
  other caller.
- Like `blankRuns`, it lists runs wherever they are, including inside a fence held by a quote
  (`> ```` ... `> ````) or in an indented code block (`    >`). The page decides where a run shows
  (section 2); a run inside a fence or a code block shows nothing.
- `blankRunsMarker` (`src/core/render/renderPipeline.ts`) writes the plain runs and the quote runs
  in one list, sorted by line, in the same `L-E` format. No other change to the element.
- **The page accepts runs next to each other.** `parseRuns` in `blankLines.ts` today drops a run
  unless `run.line > last.endLine + 1`. It becomes `run.line > last.endLine`: runs in order, never
  overlapping. A plain run right after a quote run is kept.

### 2. Placement inside a container (bq-Q1, bq-Q2)

All of it is in `refresh()` of `src/page/features/blankLines.ts` (`spotOf`, `hostItemOf`,
`placeInItem`). `blankLines.ts` is 290 lines; the Driver may move the container rules to a new file
of `src/page/features/` (for example `blankRunHosts.ts`) to keep it readable. Every limit stays
under 800 lines.

**The containers.** A holder of a run (CR-448: `line < run.line && run.endLine < endLine`) is one
of these, recognised on the page element; any other holder makes the run show nothing, as today:

| Container | Element (as rendered on origin/main) | Host container | Container line sent |
| --- | --- | --- | --- |
| List (CR-448) | `ul`, `ol`, `li` | the `li` (CR-448, point 5) | `itemLine` (unchanged) |
| Quote | `blockquote` | the `blockquote` | none |
| GitHub alert | `aside[data-okf-github-alert]` | the `aside` | none |
| Admonition | `aside.admonition`, `details.admonition` (every admonition kind, `{admonition}`, `:class: dropdown`), not `.myst-context-admonition` | the element | its line (the opening fence line) |
| Figure | `figure` mapped by the `{figure}` directive (caption and legend) | the `figure` | its line |
| Card | `div.myst-card` (`{card}`) | the `div.myst-card` | its line |
| Grid item | `div.myst-grid-item` (`{grid-item}`); `div.myst-grid` holds grid items only | the grid item; a run held by the grid and by no grid item shows nothing | the grid item's line |
| Definition list | `dl`, through its `dd` | the `dd` (rule below) | the `dd`'s line (rule below) |
| Footnote | `section[data-footnotes] li` (not a holder: rule below) | the `li` | its first block's line |

Holders are collected as CR-448 does (the top-level body block that holds the run, then
`rt.blocks.mappedChildren` recursively), from the same file and document, never an included block
(`isIncludedBlock`). The deepest one is the host container, with the exceptions of the table.

**Quotes hold a quote run up to their edges.** For a `blockquote` or an alert, the holder test also
takes a run that starts on the quote's first line or ends on its last line
(`line <= run.line && run.endLine <= endLine`). A quote run at the start of a quote (`>`, `>`,
`> b`) or at the end of a file (`> a`, `>`, `>` with nothing after) is then inside its quote. A
plain run can never be within a quote's range: a quote's range ends at most on one blank line after
it (`> a`, `>`, `>`, blank renders as `<blockquote data-line="3" data-end-line="6">`). Every other
container keeps the strict test.

**Definitions.** A `dd` carries no source line on origin/main, and the paragraph of a tight
definition is not mapped (`<dd>d1</dd>`), so the page cannot place a run in it from the mapped
blocks alone.
- The render gives each `dd` a page-only attribute with its first source line (the definition's
  marker line), for example `data-okf-definition-line`, in `src/core/render/mystNormalize.ts` (a
  rule for the `definitionDescription` node, `mergeProperties` with the node's start line). It is
  never `data-line`, so the `dd` does not become a mapped block, and never `data-okf-line`, which
  `src/page/modules/incomingChanges.ts` reads for the properties table. The sanitizer keeps
  `data-okf-*` attributes (`ALLOWED_ATTRIBUTE_PREFIXES`); `src/core/export/exportContent.ts` adds
  it to the attributes it strips (the list beside `data-okf-line`, line 53).
- When the deepest holder is a `dl`, the host container is its last `dd` whose line is before
  `run.line`. With none, the run shows nothing.
- A run between two entries (after a definition, before the next term) therefore goes at the end
  of the definition above, as a run between two items goes at the end of the item above (CR-448).

**Footnotes.** A footnote is not a holder (no source line). A run held by no top-level block whose
nearest top-level block above (by line) and nearest top-level block below are both inside the same
footnote `li` is inside that footnote: the `li` is its host container, and its container line is
the line of the `li`'s first mapped descendant. Any other run held by no block keeps CR-444's
top-level rule, unchanged. A run held by a top-level block inside a footnote (a list or a quote in
the footnote) follows the rules above, through that block.

**Position.** The block goes inside the host container, right after its last child element that
starts before the run (`lineOf(child) < run.line`), else right before its first child that starts
after the run, else as its last child, as `placeInItem` does today. Children without a line (an
admonition's title, a footnote's back link) are skipped by that rule, so a run right after an
admonition's or alert's title line shows after the title, before the first block. A card's
paragraphs sit in an unmapped body `div`: there the position is taken among the host container's
mapped children (`rt.blocks.mappedChildren`), right after the one that starts last before the run,
as its next sibling. The Driver may use that mapped-children rule for every container if CR-448's
list tests still pass.

**Folded and closed.** A run whose top-level holder carries `data-okf-folded` shows nothing, as in
CR-448. For a run inside a closed dropdown (`details.admonition` without `open`), see Open
question 1.

**What the page keeps with the run.** The `Run` of `blankLines.ts` keeps, besides `line` and
`endLine`:
- `itemLine` when the host container is a list item (unchanged);
- `containerLine` when the host container is an admonition, a figure, a card, a grid item, a
  definition or a footnote (the "Container line sent" column);
- that the run is held by a container (quote runs carry neither line), for the selection after a
  removal (section 5) and for `attached` (below). The Driver names the field.

The key of the `existing` map includes `containerLine`, as it includes `itemLine`. At most one of
`itemLine` and `containerLine` is ever set: the one of the host container.

**Refresh.** CR-448's rules (point 8) apply to every run inside a container, not only to runs with
an `itemLine`: `attached` tests document containment (`inContent`) for every held run, since a
quote run has no `itemLine` and its block keeps its `parentNode` when the content morph detaches
the old quote. When the open editor's block is no longer in the document, it goes back inside its
host container of the new content by the position rule, with the editor frame after it.

### 3. The host's run checks and the removal (bq-Q2, CoS: format kept)

**The check.** `checkBlankRun(text, line, endLine)` in `blockRange.ts` accepts either kind:
- a plain run: today's rule, unchanged;
- a quote run: every line from `line` to `endLine` is an empty quote line of the same depth and
  marker columns (`emptyQuoteLine`), `line` is after the frontmatter, and neither line `line - 1`
  (when it exists and is not the frontmatter's last line) nor line `endLine + 1` (when it exists)
  is an empty quote line of that same depth and columns.

The host reads the kind from the text; no message carries it. Every caller (`handleEditOpen` and
the re-created save of `src/session/features/blockEdits.ts`, `planBlankRunPaste`,
`planBlankRunRemoval`) gets the quote runs through it.

**The removal.** `planBlankRunRemoval` (and `planBlankRunDelete` in `src/core/edits/sourceEdits.ts`,
through `handleBlankRunDelete` in `src/session/features/sourceEdits.ts`) removes, in one text edit
and one undo step:
- a plain run: today's rule (lines `line + 1`..`endLine`, or all lines at the start of a file
  without frontmatter and at the end of the body);
- a quote run: always lines `line + 1`..`endLine`, wherever the run is, so line `line` stays byte
  for byte, its spaces included (bq-Q2: "Delete keeps one empty `>` line"). At the end of the text,
  the removal runs from the end of line `line` (before its line break) to the end of the text, so
  the document's final line break, or its absence, is kept (BLOCK-234).
- A plain run inside a directive container, a definition or a footnote: lines `line + 1`..`endLine`
  go, line `line` stays (today's middle-of-body rule, which already applies: such a run always has
  a block above and below).

No other line of the file changes (CoS: "Markdown keeps its original format"; only the removed lines
change). `previewBlankRunDelete` carries no container line. A stale run is refused as today.

### 4. Typing and pasting in a run inside a container (bq-Q2, CoS: content indent)

The owner's answer (bq-Q2): "Reste dans la citation": a block typed or pasted in place of the run
gets the quote's `>` prefix, and the item or content indent when nested, as CR-448's br-Q5. The
Chief of Staff settled (02-answers): inside an admonition, a definition or a footnote, a typed block
takes the content indent of that container.

**The message.** `replaceBlankRun` gains an optional field `containerLine`, sent by the page when
the host container is an admonition, a figure, a card, a grid item, a definition or a footnote
(section 2). It is carried on `previewEditOpen`, `previewEditSave`, `previewEditCancel` and
`previewBlocksPaste`, like `itemLine`.
- Add it to the `replaceBlankRun` type in `src/core/protocol/pageToHostMessages.ts` and to the
  page's types in `src/page/features/pageRuntime.ts` (`replaceBlankRun`, `runOf`).
- Add it to `isBlankRunFields` in `src/core/protocol/pageToHost.ts`: valid only when it is
  `isSourceLine` and below `line`, and never together with `itemLine`.
- A quote run with no list item, admonition, definition or footnote inside the quote sends neither
  field. A top-level plain run sends neither and behaves exactly as today.

**The container indent (core).** Add pure functions in a new file, for example
`src/core/mapping/blankRunContainer.ts` (`listItemIndent.ts` and `insertion.ts` stay as they are
where they can). For a run `line`..`endLine` with an optional `itemLine` or `containerLine`:

1. **Quote prefix.** For a quote run, the quote part is the quote prefix of line `line`, followed by
   one space. For a plain run there is none.
2. **The container's own line, without the quote prefix.** When `itemLine` or `containerLine` is
   given and the run is a quote run, that line must start with quote markers at the same depth and
   columns as the run; they are removed from it with the one optional space or tab after the last
   marker, as CommonMark reads a quote's content. Otherwise the line is read as it is. When the
   markers do not match, the line is refused (stale).
3. **The inner indent**, from that line:
   - **list item** (`itemLine`): CR-448's `listItemIndent` (item indent and content indent), and
     CR-448's choice between them, where the line after the run is also read without its quote
     prefix (`startsSiblingItem`);
   - **directive** (`containerLine` is an opening fence: `` ``` ``, `~~~` or `:::` of three or more,
     then `{name}`): the fence line's leading spaces and tabs, copied as they are. A fence keeps its
     content until its closing fence, so this keeps the block inside, nested in a list item too;
   - **definition** (`containerLine` starts, after its leading spaces and tabs, with `:` or `~`
     followed by a space or a tab and some text): the line's leading spaces and tabs, then two
     spaces. That is the definition list's own content indent (`markdown-it-deflist`:
     `blkIndent = sCount[ddLine] + 2`; checked on origin/main: `: d1` then `  two` stays in the
     definition);
   - **footnote** (`containerLine` starts, after at most three spaces, with `[^label]:`, or the
     lines between it and the nearest non-blank line above it are blank and that line is one, for
     a footnote whose first block is not on its label line): the label line's leading spaces and
     tabs, then four spaces (checked on origin/main: two spaces leave the footnote, four stay);
   - any other line: refused (stale).
4. **The container indent** is the quote part followed by the inner indent. The line is also
   refused when it is in the frontmatter or not before the run.

Examples, with "More" typed:

| Text around the run | Written |
| --- | --- |
| `> a`, `>`, `>`, `> b` | `> a`, `>`, `> More`, `>`, `> b` |
| `> [!NOTE]`, `>`, `>`, `> x` (alert) | `> [!NOTE]`, `>`, `> More`, `>`, `> x` |
| `> > c`, `> >`, `> >`, `> > d` | `> > More` between `> >` separators |
| `- item`, blank, `  > q`, `  >`, `  >`, `  > r` | `  > More` between `  >` separators |
| `> - x`, `>`, `>`, `>   more` (item line `> - x`) | `>   More` |
| `> - x`, `>`, `>`, `> - y`, typed `- c` | `> - c` (a sibling item, CR-448) |
| ```` ```{note} ````, `a`, blank, blank, `b` | `More` |
| `- i`, blank, ```` ```{note} ```` indented 2, `  a`, blank, blank, `  b` | `  More` |
| `Term`, `: d1`, blank, blank, `  two` | `  More` |
| `[^a]: f1`, blank, blank, `    more` | `    More` |

**What is written.**
- Each line of the block that is not blank gets the container indent before it, after the writer's
  own indentation is kept (`insertionText` keeps the first line's indentation as typed). A line
  typed as `> x` in a quote becomes `> > x`, a nested quote, as Markdown reads it.
- A blank line of the block: inside a quote run, a copy of line `line` (an empty quote line, so the
  quote does not end); otherwise nothing is added (CR-448).
- **The separators.** CR-444's rule stays: one separator before the block (none at the start of
  the file) and one after it (none at the end of the text, where the final line break is kept, or
  kept absent). For a quote run, each separator is a copy of line `line`, byte for byte, instead of
  an empty line; for a plain run it stays an empty line.
- The block's line endings are the document's (BLOCK-094, BLOCK-234). Nothing else in the file
  changes (CoS: format kept). An empty Done writes nothing. Cancel after an autosave restores the
  run byte for byte (the held `blankRunRegion`). The page-facing `originalText` stays `""`.

**Where it goes in the plan.** `planBlankRunInsertion(text, line, endLine, itemLine?,
containerLine?)` (or one options object; the Driver names the shape) computes, once, against the
document of that moment, everything `insertionText` needs: the quote part, the blank-line copy, the
list indents and the between-items choice (CR-448), or the container indent. `insertionText`
applies it. `planBlankRunPaste(..., containerLine?)` and its caller `planBlocksPaste`
(`src/core/edits/sourceEdits.ts`, the `blankRun` argument) pass `containerLine` on, as they pass
`itemLine`. An autosave and each later save reuse the held edit's plan (`ActiveBlockEdit.insertion`
in `blockEdits.ts`), so every save of that editor writes with the same prefix.

**The host's checks.** The host never trusts `containerLine` or `itemLine` without checking it.
`itemLineHolds` in `blockEdits.ts` becomes one core check of the container line (step 2 and 3
above), used on open (`handleEditOpen`, beside `checkBlankRun`), on the re-created save of
`handleEditSave`, and on the paste (`planBlankRunPaste`). A refused line gets that path's existing
stale message: "The preview is stale. Refresh it before editing this block." on open, "The preview
is stale. Reopen the block before saving." on a re-created save, and the out-of-date reason on a
paste. `sameBlankRun` (and the held `blankRunRegion`) compares `containerLine` too, so a save or
cancel for a different container is refused with the held-edit stale reason. `blockEdits.ts` is 727
lines: the new logic goes in core, and the session file only passes the field on.

### 5. Keyboard, pointer and selection

The keys are CR-444's and CR-448's. Two things change in `blockSelectionView.ts`:
- **The selection after a removal (`requestDeleteBlankLines`).** Today `targetIndex` subtracts 1
  only for a run with an `itemLine`. It does so for every run held by a container (section 2,
  "What the page keeps"), so the top-level block that held the run is selected: the quote, the
  alert, the admonition, the definition list, the figure, the card, the grid or the list. A
  footnote run (held by no top-level block) keeps the top-level rule: the block that follows it.
- **Paste.** `Ctrl/Cmd+V` on a selected one posts `previewBlocksPaste` with the run's
  `containerLine`, as it posts `itemLine` today (around line 609).

Unchanged, and to keep: a click on a blank-lines block inside an admonition, an alert, a quote, a
definition or a footnote opens its insertion editor, never the container's own editor (today a
click inside an alert or admonition body opens the whole container, `editingElementFor` in
`src/page/features/mappedBlocks.ts`; the block's click handler stops propagation). Shift+click does
nothing. Delete and Backspace act only on a selected one. Alt+Up/Down moves nothing. Escape clears
it. Ctrl/Cmd+C and +X do nothing. The structural navigation (BLOCK-254) never stops on it.

### 6. Look

Same element and CSS as CR-444 (`.sphinx-preview-blank-lines`). Inside a container it is as wide as
the container's content box. Its Delete block button stays at its left edge and must not overlap a
quote's left border, an admonition's or alert's icon and title, or the list item handles; the
visual captures check it. `editModeStyles.ts` is 792 lines: new CSS goes in a style module of its
own, as CR-448 says, rather than raising the cap.

### 7. Requirements

Follow the project's requirements guidelines: markers move with the code; run
`just requirements-update`; add a dated entry in `requirements/tiers/log.md`. All of it is in scope
`block-editing`. Update the four SwRS of CR-444 and CR-448 (all `proposed`); the log entry gives
the reason (they said runs inside a quote, an alert or an admonition show nothing):

- **SwRS-MDOKFSTUDIO-BLOCK-266** (where a run shows): the title and the normative text add runs
  inside a quote or an alert (its empty `>` lines), an admonition or another Markdown directive of
  the list, a definition and a footnote, shown inside that container. The "Nothing is shown"
  scenario drops "a quote, an alert or an admonition" and keeps a fence, an HTML block, a table and
  the directives outside the list. Add a scenario "Runs inside quotes and containers are shown".
- **SwRS-MDOKFSTUDIO-BLOCK-267** (arrows, Enter, click): add a scenario: Down from a selected quote
  or admonition stops on each blank-lines block inside it, then on the block after it; a click on
  one opens its insertion editor, not the container's editor.
- **SwRS-MDOKFSTUDIO-BLOCK-268** (typing or pasting): the normative text adds that a block written
  in place of a run inside a container takes the container indent (the quote prefix, then the
  item, directive, definition or footnote indent), that inside a quote its blank lines and
  separators are copies of the run's first line, and that the host checks the container line and
  refuses it as stale. Add a scenario "A block typed in a quote or a container stays in it".
- **SwRS-MDOKFSTUDIO-BLOCK-269** (removal): the normative text adds that a quote run keeps its
  first empty `>` line wherever it is. Add a scenario covering a quote, an admonition, a definition
  and a footnote; the selection goes to the top-level block that held the run.
- No new StRS. `derives_from` stays StRS BLOCK-011 and BLOCK-025, whose text is unchanged.
- New tests carry `@tests_req` for the SwRS they check. The changed code in `blankRuns.ts`,
  `blankRunContainer.ts`, `blockRange.ts`, `insertion.ts`, `renderPipeline.ts`, `mystNormalize.ts`,
  `exportContent.ts`, `pageToHost.ts`, `blankLines.ts` (and any file split from it),
  `blockSelectionView.ts`, `src/core/edits/sourceEdits.ts` and `blockEdits.ts` keeps or gains its
  `@implements_req` markers, with at most 3 IDs per marker block.

### 8. Shared vocabulary and docs

- `.agents/glossary/common.md`:
  - "Blank run": add "inside a quote or an alert (two or more empty `>` lines of the same depth),
    an admonition or another Markdown directive, a definition or a footnote".
  - "Blank-lines block": add that inside a container it shows in that container, and that a block
    typed in it takes the container's `>` prefix and content indent.
  - Add "Empty quote line" and "Quote run" (see "Words"), and "Container indent" if the code uses
    the word.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes (the `dd` attribute is page-only and stripped from the export), and the
  blank-lines block is edit-mode chrome.
- The release notes are written when the release is prepared, not in this PR.

## Out of scope

- Directives whose content is not Markdown: code blocks, math, mermaid, PlantUML, list-table and
  the other tables, unresolved directives (shown as `pre`): their blank lines are their content
  (CR-444, BLOCK-256 unchanged). A fence, an HTML block or a table inside a container likewise.
- Directives that render their body without a mapped wrapper (`{topic}`, `{sidebar}`, `{margin}`,
  `{div}`, `{aside}`: an unmapped `div` around mapped paragraphs): their paragraphs are top-level
  blocks (or blocks of a list item), so their runs already follow CR-444's and CR-448's rules, and a
  block typed there stays in the fence. Unchanged; one page check and one host check confirm it.
- Collapsing runs by itself, on save, on render or on any other edit. Re-indenting or re-prefixing
  any line but those of the block the writer types or pastes. Normalising `>` spacing.
- Making the `dd`, the footnote `li` or any other element a mapped block.
- Runs in an included file, in the frontmatter or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks onto it.
- The questions below, until answered.

## Evidence

The checks read the shipped files at the head under test: the real render pipeline, the real page
bundle and the real stylesheet, never a prepared copy. Each new check fails on the code before the
change (constitution, section 3). The CR-444 and CR-448 tests keep their intent; an assertion that
expected nothing for a run inside a quote, an alert or an admonition (for example "a run inside a
list of an admonition shows no blank-lines block" in `test/page/runtimeBlankLines.test.ts`, line
471, and the admonition run of `test/core/render/blankRunsInLists.test.ts`) is changed only for that
reason, and the commit says so.

**Core, `test/core/mapping/`** (each in LF, CR LF and lone CR):
- `emptyQuoteLine` and `quoteBlankRuns`: `>`, `> `, `>\t`, `> >`, `>>`, `  >` (in a list item) are
  empty quote lines with their depth; `> a`, `>a` and a blank line are not; runs of 2 and 3 `>`
  lines; a single `>` gives nothing; `> >`, `>` (two depths) gives nothing; `> >`, `> >`, `>`, `>`
  gives two runs; a run at the start of a quote and at the end of the text; frontmatter excluded.
- `checkBlankRun` on quote runs: accepted; refused when a line is not an empty quote line, when the
  line above or below is one of the same depth, or when depths or columns differ.
- `planBlankRunRemoval` on quote runs: lines `line + 1`..`endLine` go and line `line` stays byte for
  byte (`> ` with its space) in the middle, at the start of the file, at the start of a quote after
  a blank line, and at the end of the text with and without a final line break; no bare LF in CR
  LF, no CR in LF. Plain runs inside a directive, a definition and a footnote keep line `line`.
- The container indent function: each row of the examples table of section 4 gives its indent; a
  tab before a fence, a definition marker or a footnote label is kept as is; `itemLine` `> - x`
  with a run at depth 1 gives `>   `; refused for a paragraph line, a fence without `{name}`, `:`
  with no text after, a label line at or after the run, a frontmatter line, and quote markers at
  another depth.
- `planBlankRunInsertion` and `planBlankRunPaste` (and `planBlocksPaste`, `test/core/edits/`)
  through `insertionText`: every row of the examples table; a two-line "More\n\nText" in a quote
  gives `> More`, a copy of line `line`, `> Text`; "> x" in a quote gives `> > x`; "- c" between
  `> - x` and `> - y` gives `> - c`; without `itemLine` or `containerLine` the output of a plain
  run is identical to today.
- **Rendered result.** Each insertion and paste case above applies its plan to the text and renders
  the result with `renderPreviewSource`. It asserts one top-level quote (or alert, admonition,
  definition list, footnote) and the new paragraph inside the expected container.

**Protocol, `test/core/protocol/pageToHost.test.ts`:** `replaceBlankRun.containerLine` is accepted
when it is a source line below `line`; rejected at or after `line`, when not an integer, together
with `itemLine`, or on a message type that does not take `replaceBlankRun`.

**Render and export, `test/core/render/`, `test/core/export/`.** Take a text with a quote run, an
alert run, a run in an admonition, a run in a `{figure}`, a run in a `{card}`, a run in a definition
(loose) and between two entries of a tight definition list, a run in a footnote, a run in a fence
inside a quote, and a quote run next to a plain run. `renderPreviewSource` gives:
- the run list with every run, sorted, the adjacent quote and plain runs both present;
- each `dd` with its page-only line attribute equal to its marker line, and no `data-line` on it;
- the containers' ranges as section 2 uses them (the quote holding its run up to its edges, the
  admonition and figure holding theirs, the footnote paragraphs as top-level mapped blocks).
- `exportContent` carries no `dd` line attribute.

**Page, `test/page/runtimeBlankLines.test.ts`** (runtime bundle, one check per rule; add shapes to
the harness for each container). The checks:
- a quote run makes one blank-lines block inside the `blockquote`, between its paragraphs; one at
  the start of a quote and one at its end make one each, inside it;
- an alert run makes one inside the alert, after its title, before its first block;
- a run in an admonition, a `{figure}`, a `{card}` (in its body, between the paragraphs) and a grid
  item makes one inside that container; a run held only by a grid makes none;
- a run in a loose definition makes one in its `dd`, between its paragraphs; a run between two
  entries of a tight definition list makes one at the end of the first `dd`;
- a run between two paragraphs of a footnote makes one inside the footnote `li`, and its message
  carries the footnote's `containerLine`; a run between two footnotes keeps CR-444's top-level rule;
- a run in a fence inside a quote, in a `pre`, in a table and in a context-tag panel makes none;
- adjacent quote and plain runs both show;
- a run inside a folded top-level quote makes none, and unfolding makes it;
- a content patch keeps the element of an unchanged quote run;
- an editor opened from a quote run stays open across a patch that replaces the whole quote (new
  elements, the old ones detached, the run gone): the block is back inside the new quote, with the
  editor frame after it, and Cancel posts `previewEditCancel` with the same `replaceBlankRun`;
- a click on one inside an admonition and inside an alert posts `previewEditOpen` with
  `replaceBlankRun` (with `containerLine` for the admonition, none for the alert) and opens no
  container editor;
- Ctrl/Cmd+V on a selected one posts `previewBlocksPaste` with the same `containerLine`;
- Down from a selected quote stops on each blank-lines block inside it, in line order, then on the
  block after it; Up walks back;
- Delete on a selected one posts `previewBlankRunDelete`; after the removal result and the render,
  the quote (or the admonition, the definition list) is selected.

**Session, `test/session/`** (a new file, for example `blankRunInContainerHost.test.ts`; the real
handlers, in LF and CR LF):
- `previewBlankRunDelete` on a quote run: lines `line + 1`..`endLine` go, the first `>` line stays
  byte for byte, one `applyWrittenEdits` call, the rest identical; the same on a run in an
  admonition, a definition and a footnote.
- A save of "More" in a quote run writes `> More` with `>` separators; a later autosave of "More
  text" replaces it; Cancel after the autosave restores the run byte for byte.
- A save of "More" with `containerLine` in an admonition nested in a list item, in a definition and
  in a footnote writes the indents of the examples table; a save of "- c" with `itemLine` in a list
  inside a quote writes `> - c` between items and `>   - c` inside an item.
- Each save and paste above renders the written text with `renderPreviewSource` and asserts the new
  block inside the expected container.
- A re-created save (no held edit) with `containerLine` writes the same indent.
- A stale `containerLine` (a paragraph line, a line that changed, quote markers at another depth)
  is refused with the stale message of open, of the re-created save and of the paste; the document
  does not change.
- A run inside a `{topic}` at the top level and in a list item: a save of "More" writes it inside
  the fence, as today.

**Visual (`just ci-visual`):** add a fixture `test/visual/fixtures/94-blank-lines-in-containers.md`
with a quote run, an alert run, a run in an admonition, a run in a definition and a run in a
footnote, and scenarios in `test/visual/blankLinesBlockScenarios.ts` with checks in
`test/visual/capture_blank_lines_block.py`:
- edit mode: one blank-lines block in each container, inside it, as wide as its content box;
- one selected in the quote and one in the alert: the Delete block button shows at the block's left
  edge and overlaps neither the quote's border nor the alert's icon or title;
- reading mode: none;
- typing: click the quote's blank-lines block, type "More" and wait past an autosave; the editor is
  still open inside the re-rendered quote.

The captures are attached to the PR, as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch).** In
`test/integration/blankLines.test.ts`, add a fixture, in LF and in CR LF, with a quote holding three
empty `>` lines between two paragraphs, an admonition in a list item with three blank lines between
two paragraphs, and a footnote with three blank lines between two paragraphs:
1. Send `previewBlankRunDelete` for the quote run: one `>` line is left, the rest unchanged, no bare
   LF in CR LF. One undo brings the run back.
2. Send `previewEditSave` with `replaceBlankRun` for the quote run, with `More`: `> More` with one
   `>` line on each side, line endings kept. One undo brings the run back.
3. The same for the admonition run with its `containerLine`: `  More`, inside the fence.
4. The same for the footnote run with its `containerLine`: `    More`, inside the footnote.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. The updated SwRS
carry their markers at the code and the tests above.

**Gate:** `just preflight` passes (on Windows, its static stage; CI runs the others).

## Open questions

The answers do not settle these; the spec's rules above leave them out until the owner answers.

1. **A run inside a closed dropdown** (`details.admonition` without `open`). Its blank-lines block
   would be out of sight, yet the arrows (`stops`) would select it. Options: (a) no blank-lines
   block while the dropdown is closed, made when it opens (a `toggle` listener calls `refresh`);
   (b) the arrows open the dropdown on reaching it; (c) the arrows pass over a hidden one. Proposed:
   (a), as the folded rule does.
2. **Tab items** (`{tab-item}` in a `{tab-set}`). Their blocks carry no source line by design (a
   block under a tab item is edited with the item, `sourcePositionProperties` in
   `src/core/render/mystNode.ts`), so a run cannot be placed between them. Options: show the run's
   blank-lines block at the end of the tab panel (the panel is mapped), or keep showing nothing (as
   today). Proposed: nothing, as today.
3. **Context-tag panels** (`<example>` ... `</example>`, rendered as an admonition panel,
   `.myst-context-admonition`). They are not directives. Include them (the block takes the tag
   line's indent) or keep showing nothing? Proposed: nothing, as today.
4. **Quote directives** (`{epigraph}`, `{pull-quote}`, `{blockquote}`). The quote they render is
   mapped to its first line only (`<blockquote data-line="22">`, no end line), so their runs are
   held by no block and, by the code read, show after the quote by CR-444's top-level rule, not
   between its paragraphs; a block typed there stays in the fence. Fix the placement (a renderer
   change: give that quote its end line) or leave it? Proposed: leave it.
5. **Footnote edges.** A run between the label line and the first block of a footnote (`[^a]:`
   alone, then blank lines, then an indented paragraph), and a run between two footnote
   definitions, keep CR-444's top-level rule: a block typed there is written at column 0, so it
   becomes a body paragraph. Keep that, or indent it into the footnote above? Proposed: keep.
