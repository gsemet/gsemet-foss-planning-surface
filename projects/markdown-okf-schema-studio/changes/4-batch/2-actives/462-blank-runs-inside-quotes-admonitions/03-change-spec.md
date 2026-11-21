# Show blank-line runs inside quotes, alerts, admonitions, definitions and footnotes

In edit mode, a run of two or more blank lines can sit inside a container:
- a quote or a GitHub alert (its empty `>` lines);
- a MyST admonition, a context-tag panel or another directive that holds Markdown;
- a definition of a definition list;
- a footnote definition.

Such a run shows as the same blank-lines block CR-444 and CR-448 show, placed inside the container
that holds the run. The writer reaches it, types in it or removes it as with any blank-lines block:
- A block typed there takes the container's `>` prefix and content indent, so it stays inside.
- Removing the run keeps one line (one empty `>` line in a quote), and nothing else in the file
  changes.

Origin: verbal. It was split off from CR-448 blank-runs-inside-lists on 2026-11-21. The owner gave
the goal on 2026-11-20 and answered on 2026-11-21. No issue.

## Goal

The owner's goal (2026-11-20) is that blank lines beyond the one separator are always reachable in
edit mode. CR-444 (PR #453) made the runs between top-level blocks reachable, and CR-448 (PR #463)
the runs inside lists. A run inside any other container is still unreachable, or reachable with a
wrong result:

- **Quotes and alerts.** Their empty lines are `>` lines. They are not CommonMark blank lines, so
  `blankRuns` never lists them.
- **Admonitions, context-tag panels, definition lists, other directive containers.** Each is a
  top-level block that holds the run, and the page skips every run held by a block that is not a
  list.
- **Quote directives.** The quote that `{epigraph}`, `{pull-quote}` and `{blockquote}` render is
  mapped to its first line only, so it holds no run.
- **Footnotes.** A footnote's paragraphs are top-level mapped blocks: the footnotes `section`, its
  `ol` and its `li` carry no source line. They sit at the end of the page's content, while their
  source lines can be anywhere, so a run near a footnote is placed by the nearest block in an order
  that is not the page's.
  - A block typed between two paragraphs of a footnote is written at column 0, and it leaves the
    footnote. `renderPreviewSource` reads a paragraph indented 2 spaces after `[^a]: f1` as a body
    paragraph; one indented 4 spaces stays in the footnote.
  - After a label line alone (`[^b]:`), a block written at column 0 would also turn the indented
    body under it into a code block.

This CR covers all of them at once (bq-Q1, "Tout d'un coup") and reuses everything CR-444 and
CR-448 built. Their specifications are in the planning folder:
- `4-batch/3-done/444-empty-block-blank-lines-block/03-change-spec.md`;
- `4-batch/3-done/448-blank-runs-inside-lists/03-change-spec.md`.

This file restates what a Driver needs from them.

**Base.** `origin/main` of markdown-okf-schema-studio, at or after `2d3187b6` (version 1.11.0). It
holds CR-444 (`399f1d05`) and CR-448 (`3eca44a4`). The code references below are read from that
commit, and the rendered HTML quoted below comes from its `renderPreviewSource`.

**Project rules.** This change follows the project's constitution (`.agents/constitution.md`), its
`AGENTS.md` (requirements, completion gate `just preflight`) and the requirements guidelines named
there. This specification restates none of them.

**Batch.** Once specified, this CR joins the running batch-07, in the stack shape (owner,
2026-11-21).

## Words

**Terms from CR-444 and CR-448**, used here with the same meaning:
- **Blank run**, **Blank-lines block**, **Separator**, **CommonMark blank line**: as in CR-444 and
  `.agents/glossary/common.md`.
- **Holder**, **Host item**, **Item line**, **Columns**, **List marker**, **Item indent**,
  **Content indent**: as in CR-448 ("Words").

**Quote terms.**
- **Quote marker**: a `>` that opens or continues a quote level, as CommonMark reads it. It comes
  after the line's leading spaces and tabs, or after the previous quote marker and the spaces and
  tabs after it.
- **Empty quote line**: a line made only of spaces, tabs and one or more quote markers, with only
  spaces and tabs after the last marker (`>`, `> `, `>\t`, `> >`, `  >`).
  - Its **depth** is its number of quote markers.
  - Its **marker columns** are the columns of its markers, counted as CR-448 counts columns (a tab
    goes to the next stop of 4).
  - Its **quote prefix** is its text up to and including its last quote marker.
- **Quote run**: a maximal sequence of two or more consecutive empty quote lines of the same depth
  and marker columns, after the frontmatter.
  - "Maximal": the line above and the line below are not empty quote lines of that same depth and
    columns.
  - Lines of another depth do not join it. In `> > c`, `> >`, `>`, `> > d`, the `> >` line belongs
    to the inner quote and the `>` line closes it, so keeping one of them would merge or split
    quotes (bq-Q2: "the quote stays one quote"). Such a mix is no run.
- **Plain run**: a blank run as CR-444 defines it (CommonMark blank lines).
  - Every run is either a plain run or a quote run.
  - A plain run and a quote run can be next to each other (`> a`, `>`, `>`, blank, blank, `b`).

**Container terms.**
- **Container**: an element of the page that holds Markdown blocks. The closed list is in section
  2.
  - A **quote container** is a quote or an alert.
  - A **definition** is a `dd` of a definition list.
  - A **footnote** is an `li` of the footnotes section (`section[data-footnotes] li`).
- **Host container** of a run: the container whose blank-lines block shows the run (section 2).
- **Container line**: the source line the host reads a container's indent from:
  - a directive's opening fence line;
  - a context-tag panel's opening tag line;
  - a definition's marker line (`:` or `~`);
  - a footnote's label line (`[^label]:`).

  A list item's container line is its item line (CR-448). A quote has none: its prefix is read from
  the run's own lines.
- **Container indent**: the text a block typed in place of a run takes before each of its lines,
  so it stays in the host container (section 4).

## What CR-444 and CR-448 already give, unchanged

- **The page reads only the host's run list.** `readRuns` in `src/page/features/blankLines.ts`
  reads the last element of the content, `<div hidden data-okf-blank-runs="L-E ...">`, and the page
  builds every blank-lines block itself (`create`). CR-444's guard against an authored attribute
  holds.
- **The block's look and label.** A dashed bar with the CSS label "Blank lines (N)",
  `role="button"`, `tabindex="0"`, and the Delete block button at its left edge.
- **The block's keys.** Enter or a click opens the insertion editor (`open`). Delete and Backspace
  act on a selected block (`deleteSelection`).
- **The messages.** `previewBlankRunDelete`, `previewEditOpen`/`Save`/`Cancel` and
  `previewBlocksPaste` with `replaceBlankRun`. The editor stays open across an autosave's
  re-render.
- **Plain runs keep every rule.** `blankRuns`, `isCommonMarkBlank`, today's branch of
  `checkBlankRun` and of `planBlankRunRemoval` (`src/core/mapping/blockRange.ts`), and the
  separators of `planBlankRunInsertion` (`src/core/mapping/insertion.ts`) are unchanged.
  - The host already lists plain runs inside a directive container, a definition or a footnote (the
    hidden list of origin/main shows them), and they pass the run checks.
  - Only their placement on the page and the indent of a typed block change for them.
- **Lists keep CR-448's rules.** Placement in the host item, `itemLine`, `listItemIndent`
  (`src/core/mapping/listItemIndent.ts`), the item indent for a list marker typed between items,
  and the content indent otherwise. This CR also applies them to a list inside a quote, reading the
  item line and the line after the run without their quote prefix (section 4).

## What changes

### 1. The host lists quote runs (bq-Q1)

- **Finder.** Add a pure function `quoteBlankRuns(text): BlankRun[]` (the name is an example) in
  `src/core/mapping/blankRuns.ts`, beside `blankRuns`.
  - It returns every quote run (see "Words") as 1-based document lines, in document order.
  - It uses `splitLines`, skips the frontmatter (`frontmatterLineCount`) and works the same in LF,
    CR LF and lone CR.
- **Reader of one line.** Add a helper that reads an empty quote line, for example
  `emptyQuoteLine(text): { depth: number; columns: number[]; prefix: string } | undefined`. It is
  exported for the run checks and the plan (sections 3 and 4), which are its only callers.
- **Where it looks.** Like `blankRuns`, it lists runs wherever they are, including inside a fence
  held by a quote (`> ```` ... `> ````) or an indented code block (`    >`). The page decides where
  a run shows (section 2); a run inside a fence or a code block shows nothing.
- **The run list.** `blankRunsMarker` (`src/core/render/renderPipeline.ts`) writes the plain runs
  and the quote runs in one list, sorted by line, in the same `L-E` format. The element does not
  change otherwise.
- **The page accepts runs next to each other.** `parseRuns` in `blankLines.ts` drops a run today
  unless `run.line > last.endLine + 1`. The test becomes `run.line > last.endLine`: runs in order,
  never overlapping. A plain run right after a quote run is kept.

### 2. Placement inside a container (bq-Q1, bq-Q2, bq-Q3, bq-Q4, bq-Q6)

All of this is in `refresh()` of `src/page/features/blankLines.ts` (`spotOf`, `aboveOf`,
`hostItemOf`, `placeInItem`). `blankLines.ts` is 290 lines, so the Driver may move the container
rules to a new file of `src/page/features/` (for example `blankRunHosts.ts`) to keep it readable.
Every file stays under the 800-line limit.

**The containers.** Each row is recognised on the page element:

| Container | Element (as rendered on origin/main) | Host container | Container line sent |
| --- | --- | --- | --- |
| List (CR-448) | `ul`, `ol`, `li` | the `li` (CR-448, point 5) | `itemLine` (unchanged) |
| Quote | `blockquote` from `>` lines | the `blockquote` | none |
| Quote directive | the `blockquote` of `{epigraph}`, `{pull-quote}`, `{blockquote}` (inside an unmapped `figure`), once it has an end line (below) | the `blockquote` | its line (the opening fence line) |
| GitHub alert | `aside[data-okf-github-alert]` | the `aside` | none |
| Admonition | `aside.admonition` and `details.admonition`, for every admonition kind, `{admonition}` and `:class: dropdown`, without `.myst-context-admonition` | the element | its line (the opening fence line) |
| Context-tag panel | `aside.admonition.myst-context-admonition` (bq-Q3) | the `aside` | its line (the opening tag line, `<example>`) |
| Figure | a mapped `figure` from the `{figure}` directive (caption and legend) | the `figure` | its line |
| Card | `div.myst-card` (`{card}`) | the `div.myst-card` | its line |
| Grid | `div.myst-grid` (`{grid}`), which holds grid items only | none: a pass-through holder (see "Holder chain" below) | none |
| Grid item | `div.myst-grid-item` (`{grid-item}`) | the grid item | its line |
| Definition list | `dl` | none: a pass-through holder; the host is one of its `dd` (see "Definitions" below) | the `dd`'s line |
| Footnote | `section[data-footnotes] li` (not a holder: see "Footnotes" below) | the `li` | its label line |

The table separates a quote from a quote directive by the run's kind:
- A `blockquote` that holds a quote run is a quote.
- One that holds a plain run is a quote directive, whose line is its opening fence line. A
  Markdown quote never holds a plain run strictly.

**The holder chain.** Holders are collected as CR-448 does:
- The chain starts at the top-level body block that holds the run (CR-448:
  `line < run.line && run.endLine < endLine`), then follows `rt.blocks.mappedChildren` recursively.
- Each holder comes from the same file and document; an included block (`isIncludedBlock`) is
  never a holder.
- **Every holder in the chain must be a container of the table**, the grid and the `dl` included.
  If any holder is something else, the run shows nothing, as `hostItemOf` refuses a non-list
  holder today. That covers a table, a `pre`, an unresolved directive, a tab panel, an included
  block, and a `figure` that is not a `{figure}`.
- The host container is the deepest holder, with three named exceptions:
  - **Grid:** when the deepest holder is a grid, the run shows nothing.
  - **Definition list:** when the deepest holder is a `dl`, the host is one of its `dd`.
  - **Footnote:** a footnote is never a holder and has its own rule.

**Quotes hold a quote run up to their edges.** For a `blockquote` or an alert holding a quote run,
the holder test also takes a run that starts on the quote's first line or ends on its last line
(`line <= run.line && run.endLine <= endLine`).
- So a quote run at the start of a quote (`>`, `>`, `> b`) or at the end of the text (`> a`, `>`,
  `>`, rendered `<blockquote data-line="1" data-end-line="3">`) is inside its quote.
- Plain runs and every other container keep the strict test.

**Definitions.** On origin/main a `dd` carries no source line, and the paragraph of a tight
definition is not mapped (`<dd>d1</dd>`), so the page cannot place a run in it from the mapped
blocks alone.
- **New render attribute.** The render gives each `dd` a page-only attribute with its first source
  line (the definition's marker line), for example `data-okf-definition-line`.
  - It is set in `src/core/render/mystNormalize.ts`: a rule for the `definitionDescription` node,
    `mergeProperties` with the node's start line.
  - It is never `data-line`, so the `dd` does not become a mapped block.
  - It is never `data-okf-line`, which `src/page/modules/incomingChanges.ts` reads for the
    properties table.
  - The sanitizer keeps `data-okf-*` attributes (`ALLOWED_ATTRIBUTE_PREFIXES`).
  - `src/core/export/exportContent.ts` adds it to the attributes it strips (the list beside
    `data-okf-line`, line 53).
- **Which `dd`.** When the deepest holder is a `dl`, the host container is its last `dd` whose line
  is before `run.line`. With none, the run shows nothing.
- **Between entries.** A run between two entries (after a definition, before the next term) goes
  at the end of the definition above, as a run between two items goes at the end of the item above
  (CR-448). Section 4 says what a block typed there becomes (bq-Q5).

**Footnotes.**
- **New render attribute.** The render gives each footnote `li` a page-only attribute with its
  label line, for example `data-okf-footnote-line`.
  - The value is the start line of the `footnoteDefinition` node whose identifier matches the
    `li`'s `id` (`user-content-fn-<identifier>`).
  - The Driver finds the render step where the footnotes section is built from the definitions;
    it is in the MyST-to-HTML conversion of `src/core/render/`.
  - It is never `data-line`; it is stripped from the export like the `dd` attribute.
- **The rule.** A footnote is not a holder, since it has no source line. Take a run held by no
  top-level block. Let "below" be the nearest top-level mapped block after it (the one with the
  smallest line greater than `run.endLine`), and "above" the nearest one before it (the largest
  line less than `run.line`). Both are found by comparing lines. The run is inside footnote F in
  two cases:
  - **In F's body:** "below" is inside F, and F's label line is before `run.line`.
  - **Between two footnotes (bq-Q5):** "above" is inside F, and "below" is inside another footnote
    G whose label line is after the run. Like a run between two items (CR-448) or between two
    definition entries, the run belongs to the footnote above.

  F is then the host container, and its container line is F's label line. The first case is
  tested first.
- **What the rule covers.**
  - A run between two paragraphs of a footnote.
  - A run right after a label line alone (`[^b]:`, a run, then the indented body). This one shows
    at the start of F, before its first block (settled by the Chief of Staff, critic F2).
  - A run between two footnote definitions. It shows at the end of the footnote above, after its
    last block. Section 4 says what a block typed there becomes.
  - A run between the last footnote definition and the body text after it is not between two
    footnotes. It is a top-level run (below).
- **Footnotes nested in a container.** When the run is held by a top-level block, the chain rules
  apply. A footnote definition written inside a quote, a list item or a directive has its
  paragraphs outside that container on the page, at the end of the content. So a run whose holder
  chain is not empty, and whose nearest mapped blocks above and below by line are both inside a
  footnote `li`, shows nothing.

**Top-level runs near footnotes (CR-444's rule, amended).** The footnotes section is at the end of
the content, but its blocks' lines can sit anywhere in the source.
- `aboveOf` picks, among the top-level body blocks that are not inside `section[data-footnotes]`,
  the one with the largest line before `run.line`. It compares lines; it never relies on the
  array's order. With none, it picks the properties section or the start, as today.
- So a run between a footnote definition and the body that follows it shows in the body, right
  after that block, where a paragraph typed there at column 0 renders.
- Folding: the "below" neighbour that the folded check reads is, likewise, the body block outside
  the footnotes with the smallest line after the run.

**Position.** The block goes inside the host container:
- right after its last child element that starts before the run (`lineOf(child) < run.line`);
- else right before its first child that starts after the run;
- else as its last child.

This is what `placeInItem` does today. Some details of that rule:
- Children without a line are skipped: an admonition's title, an alert's title, a footnote's back
  link. So a run right after an admonition's or alert's title line shows after the title, before
  the first block. A run that starts on a quote's own first line shows before the quote's first
  child.
- A card's paragraphs sit in an unmapped body `div`. There the position is taken among the host
  container's mapped children (`rt.blocks.mappedChildren`): the block goes right after the one
  that starts last before the run, as its next sibling. The Driver may use that mapped-children
  rule for every container if CR-448's list tests still pass.
- In a definition, the same rule applies among the `dd`'s children; a tight `dd` has none, so the
  block is appended to it.

**Folded and closed dropdowns (bq-Q4).**
- **Folded.** A run whose top-level holder carries `data-okf-folded` shows nothing, as in CR-448.
- **Closed dropdown.** A run with a `details` element without `open` in its holder chain (a
  `:class: dropdown` admonition, or a closed `details` above it) shows nothing.
- **Opening and closing.** A `toggle` listener, in capture phase on the content (`toggle` does not
  bubble), calls `refresh()`, so the block appears when the dropdown opens and goes when it closes.
  This mirrors the existing `details` toggle listener in `src/page/features/contentPatch.ts`, line
  153.
- **An open editor stays.** A blank-lines block whose insertion editor is open is kept when its
  dropdown closes, like every edited block in `refresh()` today (`editing` is always kept).

**What the page keeps with the run.** The `Run` of `blankLines.ts` keeps, besides `line` and
`endLine`:
- `itemLine` when the host container is a list item (unchanged);
- `containerLine` for a quote directive, an admonition, a context-tag panel, a figure, a card, a
  grid item, a definition or a footnote (the "Container line sent" column);
- the top-level holder, or a mark that the run is held. A quote run carries neither line, so the
  held mark is what tells a held run apart. It is used for the selection after a removal
  (section 5) and for `attached` (below). The Driver names the field.

The key of the `existing` map includes `containerLine`, as it includes `itemLine`. At most one of
`itemLine` and `containerLine` is ever set: the one of the host container.

**Refresh.** CR-448's rules (point 8) apply to every run inside a container, not only to runs with
an `itemLine`:
- `attached` tests document containment (`inContent`) for every held run, including footnote runs.
  A quote run has no `itemLine`, and its block keeps its `parentNode` when the content morph
  detaches the old quote.
- When the open editor's block is no longer in the document, it goes back inside its host container
  in the new content by the position rule, with the editor frame after it.

**The quote directive's end line (bq-Q6).** The `blockquote` that `{epigraph}`, `{pull-quote}` and
`{blockquote}` render gets the directive's end line. On origin/main it is
`<figure class="numbered epigraph"><blockquote data-line="13">`, with no end line.
- The fix is a tree pass in `src/core/render/` (beside `normalizeFigureCaptions` in
  `mystBlockTransforms.ts`, or in `mystNormalize.ts`). It gives that `blockquote` node the end
  position of its directive (the closing fence line), so `sourcePositionProperties`
  (`src/core/render/mystNode.ts`) writes its `data-end-line`.
- The Driver confirms where the directive's position is still available.
- With it, the quote holds the plain runs between its paragraphs, and the editor range of that
  quote (`blockRange`) becomes the whole directive. The tests of those directives keep their
  intent.

### 3. The host's run checks and the removal (bq-Q2, CoS: format kept)

**The check.** `checkBlankRun(text, line, endLine)` in `blockRange.ts` accepts either kind:
- **A plain run:** today's rule, unchanged.
- **A quote run:** all of these hold:
  - every line from `line` to `endLine` is an empty quote line of the same depth and marker columns
    (`emptyQuoteLine`);
  - `line` is after the frontmatter;
  - line `line - 1`, when it exists and is not the frontmatter's last line, is not an empty quote
    line of that same depth and columns;
  - line `endLine + 1`, when it exists, is not one either.

The host reads the kind from the text; no message carries it. Every caller gets the quote runs
through `checkBlankRun`: `handleEditOpen` and the re-created save of
`src/session/features/blockEdits.ts`, `planBlankRunPaste` and `planBlankRunRemoval`.

**The removal.** `planBlankRunRemoval` removes the lines in one text edit and one undo step. It is
also reached through `planBlankRunDelete` in `src/core/edits/sourceEdits.ts`, called by
`handleBlankRunDelete` in `src/session/features/sourceEdits.ts`.
- **A plain run:** today's rule. Lines `line + 1`..`endLine` go, or all of the run's lines at the
  start of a file without frontmatter and at the end of the body.
  - A plain run inside a directive container, a definition or a footnote always has a block above
    and below it, so today's middle-of-body rule already applies: lines `line + 1`..`endLine` go
    and line `line` stays.
- **A quote run:** lines `line + 1`..`endLine` always go, wherever the run is, so line `line` stays
  byte for byte, its spaces included (bq-Q2: "Delete keeps one empty `>` line").
  - When a line follows the run, the edit runs from the start of line `line + 1` to the start of
    line `endLine + 1`.
  - At the end of the text (`endLine` is the last line), the edit mirrors `keepsFinalBreak` of the
    plain branch (`blockRange.ts`, line 265):
    - when the text ends with a line break, it runs from the start of line `line + 1` to the end of
      the text, so line `line` keeps its line break and the text still ends with one;
    - when it does not, it runs from the end of line `line`'s text (before its line break) to the
      end of the text, so the text still ends without one (BLOCK-234).

No other line of the file changes (CoS: "Markdown keeps its original format"; only the removed lines
change). `previewBlankRunDelete` carries no container line. A stale run is refused as today.

### 4. Typing and pasting in a run inside a container (bq-Q2, bq-Q3, bq-Q5, CoS: content indent)

**The decisions.**
- **bq-Q2:** the owner answered "Reste dans la citation". A block typed or pasted in place of the
  run gets the quote's `>` prefix, plus the item or content indent when nested, as in CR-448's
  br-Q5.
- **CoS:** the Chief of Staff settled that inside an admonition, a definition or a footnote, a typed
  block takes the content indent of that container.
- **bq-Q3:** in a context-tag panel, a typed block takes the tag line's leading whitespace.
- **bq-Q5:** a new entry typed between two entries of a definition list goes at the list's indent.

**The message.** `replaceBlankRun` gains an optional field `containerLine`. The page sends it for
the containers of section 2's "Container line sent" column, and it is carried on
`previewEditOpen`, `previewEditSave`, `previewEditCancel` and `previewBlocksPaste`, like `itemLine`.
- Add it to the `replaceBlankRun` type in `src/core/protocol/pageToHostMessages.ts` and to the
  page's types in `src/page/features/pageRuntime.ts` (`replaceBlankRun`, `runOf`).
- Add it to `isBlankRunFields` in `src/core/protocol/pageToHost.ts`. It is valid only when it is
  `isSourceLine` and below `line`, and never together with `itemLine`.
- A quote run with no list item, directive, definition or footnote inside the quote sends neither
  field. A top-level plain run sends neither field and behaves exactly as today.

**The container indent (core).** Add pure functions in a new file, for example
`src/core/mapping/blankRunContainer.ts`; `listItemIndent.ts` and `insertion.ts` stay as they are
where they can. The input is a run `line`..`endLine`, with an optional `itemLine` or
`containerLine`.

1. **The quote part.** For a quote run, the quote part is the quote prefix of line `line`, then one
   space. A plain run has none.
2. **The container line, without its quote prefix.** When `itemLine` or `containerLine` is given
   and the run is a quote run, the line must start with quote markers at the same depth and marker
   columns as the run. Otherwise it is refused as stale.
   - The markers are removed with the one optional space after the last marker, as CommonMark
     reads a quote's content.
   - **A tab right after the last marker keeps its columns.** It counts as the one optional space
     for one column, and the rest of its width stays as leading spaces of the line read. So
     `>\t- x` is read as `  - x` (critic F6; CommonMark's partial tab).
   - The line after the run (CR-448's `startsSiblingItem`, and the between-entries test below) is
     read the same way.
   - For a plain run, the line is read as it is.
3. **The inner indent**, from that line:
   - **List item** (`itemLine`): CR-448's `listItemIndent` (item indent and content indent), and
     CR-448's choice between them.
   - **Directive** (`containerLine` is an opening fence: three or more `` ` ``, `~` or `:`, then
     `{name}`): the fence line's leading spaces and tabs, copied as they are. A fence keeps its
     content until its closing fence, so this keeps the block inside, also when nested in a list
     item. This covers the quote directives, the admonitions, the figure, the card and the grid
     item.
   - **Context-tag panel** (`containerLine`, trimmed of its leading spaces and tabs, matches
     `CONTEXT_TAG_OPEN` of `src/core/render/mystContextTags.ts` with a name that is not an HTML tag
     name): the tag line's leading spaces and tabs (bq-Q3).
   - **Definition** (`containerLine` starts, after its leading spaces and tabs, with `:` or `~`,
     then a space or a tab, then some text):
     - the line's leading spaces and tabs, then two spaces. That is the definition list's own
       content indent (`markdown-it-deflist`: `blkIndent = sCount[ddLine] + 2`). Checked on
       origin/main: `: d1` then `  two` stays in the definition;
     - except for a new entry between two entries (bq-Q5): the line's leading spaces and tabs only
       (the list's indent). That applies when both of these hold:
       - **between two entries:** the line after the run starts at the marker line's column and is
         not a definition marker line;
       - **the typed block is a new entry:** its first line is not blank and is not a definition
         marker line, and its next line that is not blank, after at most one blank line, is a
         definition marker line (a term, then its definition).

       Any other text typed there takes the content indent.
   - **Footnote** (`containerLine` starts, after at most three spaces, with `[^label]:`):
     - the label line's leading spaces and tabs, then four spaces. Checked on origin/main: two
       spaces leave the footnote, four stay;
     - except for a new footnote between two footnotes (bq-Q5): the label line's leading spaces and
       tabs only (the footnote list's indent). That applies when both of these hold:
       - **between two footnotes:** the line after the run is a footnote label line
         (`[^label]:`) at the container line's column;
       - **the typed block is a new footnote:** its first line starts with `[^label]:`.

       Any other text typed there takes the four-space indent and stays in the footnote above.
   - **Any other line** is refused as stale.
4. **The container indent** is the quote part followed by the inner indent. The line is also
   refused when it is in the frontmatter or not before the run.

**Lines of a forged shape are accepted.** The host checks the shape of the container line, its
place before the run and its quote markers. It does not check that the run is really inside that
container: a well-formed line of another container gives that line's indent. This is what CR-448
accepts for an item line (critic F6).

**The same rule for definitions and footnotes (bq-Q5).** The owner's answer: "un terme suivi
d'une ligne « : » devient une entrée au même niveau ; tout autre texte reste dans la définition du
dessus. Même règle pour une note [^x]: tapée entre deux notes." So, in a run between two entries of
a definition list, or between two footnote definitions:
- a new entry (a term with its `:` line, or a `[^x]:` definition) is written at the list's indent,
  as a sibling;
- any other text takes the content indent and stays in the entry above.

Examples, with "More" typed unless the row says otherwise:

| Text around the run | Written |
| --- | --- |
| `> a`, `>`, `>`, `> b` | `> a`, `>`, `> More`, `>`, `> b` |
| `>`, `>`, `> b` (at the start of the file) | `> More`, `>`, `> b` |
| `> [!NOTE]`, `>`, `>`, `> x` (alert) | `> [!NOTE]`, `>`, `> More`, `>`, `> x` |
| `> > c`, `> >`, `> >`, `> > d` | `> > More` between `> >` separators |
| `- item`, blank, `  > q`, `  >`, `  >`, `  > r` | `  > More` between `  >` separators |
| `> - x`, `>`, `>`, `>   more` (item line `> - x`) | `>   More` |
| `>\t- x`, `>`, `>`, `>   more` (item line `>\t- x`) | `>   More` |
| `> - x`, `>`, `>`, `> - y`, with `- c` typed | `> - c` (a sibling item, CR-448) |
| ```` ```{note} ````, `a`, blank, blank, `b` | `More` |
| `- i`, blank, ```` ```{note} ```` indented 2, `  a`, blank, blank, `  b` | `  More` |
| ```` ```{epigraph} ````, `q1`, blank, blank, `q2` | `More` |
| `<example>`, blank, `alpha`, blank, blank, `beta` | `More` |
| `Term`, `: d1`, blank, blank, `  two` | `  More` |
| `Term`, `: d1`, blank, blank, `Other`, `: d2` | `  More` |
| `Term`, `: d1`, blank, blank, `Other`, `: d2`, with `New`, `: dn` typed | `New`, `: dn` |
| `[^a]: f1`, blank, blank, `    more` | `    More` |
| `[^b]:`, blank, blank, `    body` | `    More` |
| `[^a]: f1`, blank, blank, `[^b]: f2` | `    More` (in footnote a) |
| `[^a]: f1`, blank, blank, `[^b]: f2`, with `[^c]: f3` typed | `[^c]: f3` (a sibling footnote) |

**What is written.**
- **Lines with text.** Each line of the block that is not blank gets the container indent before
  it, in front of the writer's own indentation (`insertionText` keeps the first line's indentation
  as typed). A line typed as `> x` in a quote becomes `> > x`, a nested quote, as Markdown reads
  it.
- **Blank lines of the block.** Inside a quote run, each one becomes a copy of line `line` (an empty
  quote line, so the quote does not end). Otherwise nothing is added (CR-448).
- **The separators.** CR-444's rule stays:
  - one separator before the block, none at the start of the file;
  - one separator after the block, none at the end of the text, where the final line break is
    kept, or kept absent.

  For a quote run, each separator is a copy of line `line`, byte for byte, instead of an empty
  line. For a plain run it stays an empty line.
- **Unchanged rules.** The block's line endings are the document's (BLOCK-094, BLOCK-234). Nothing
  else in the file changes (CoS: format kept). An empty Done writes nothing. Cancel after an
  autosave restores the run byte for byte (the held `blankRunRegion`). The page-facing
  `originalText` stays `""`.

**Where it goes in the plan.**
- `planBlankRunInsertion(text, line, endLine, itemLine?, containerLine?)` computes, once, against
  the document of that moment, everything `insertionText` needs. The Driver chooses the shape,
  positional arguments or one options object. What it computes:
  - the quote part and the blank-line copy;
  - the list indents and the between-items choice (CR-448);
  - or the container indent, with the definition's between-entries flag.
- `insertionText` applies the plan. The choices that depend on the typed text (CR-448's list
  marker, bq-Q5's new entry) are made there.
- `planBlankRunPaste(..., containerLine?)` and its caller `planBlocksPaste`
  (`src/core/edits/sourceEdits.ts`, the `blankRun` argument) pass `containerLine` on, as they pass
  `itemLine`.
- An autosave and each later save reuse the held edit's plan (`ActiveBlockEdit.insertion` in
  `blockEdits.ts`), so every save of that editor writes with the same prefix.

**The host's checks.** The host never uses `containerLine` or `itemLine` without checking it.
- `itemLineHolds` in `blockEdits.ts` becomes one core check of the container line (steps 2 to 4
  above). It is used on open (`handleEditOpen`, beside `checkBlankRun`), on the re-created save of
  `handleEditSave`, and on the paste (`planBlankRunPaste`).
- A refused line gets that path's existing stale message:
  - on open: "The preview is stale. Refresh it before editing this block.";
  - on a re-created save: "The preview is stale. Reopen the block before saving.";
  - on a paste: the out-of-date reason.
- `sameBlankRun` (and the held `blankRunRegion`) compares `containerLine` too, so a save or cancel
  for a different container is refused with the held-edit stale reason.
- `blockEdits.ts` is 727 lines, so the new logic goes in core; the session file only passes the
  field on.

### 5. Keyboard, pointer and selection (critic F1, F4)

The keys are CR-444's and CR-448's. Three things change in `src/page/features/blockSelectionView.ts`.

**The order of the stops (`stops`, `neighbourStop`).** Today `stops` sorts by first line only, and
`neighbourStop` looks for the first stop whose line is strictly greater (or smaller) than the
current one. A quote run that starts on the quote's own first line has the quote's line, so Down
from the quote skips it, and Up from it skips the quote.
- **New order.** `stops` sorts by first line. On equal lines, a container comes before the
  blank-lines blocks it holds, then the others in their current order. Any stable tie-break that
  puts a body block before a blank-lines block of the same line does it.
- **New step.** `neighbourStop` finds the current stop's place in that sorted list and returns the
  next or previous stop by position, passing over blank-lines blocks when `skipBlank` is set. The
  current stop is the selected blank-lines block, or the stop of the block at the free end of the
  block selection. It no longer compares lines.
- **Result.** Down from a selected top-level block reaches each blank-lines block inside it, in line
  order, then the block after it. Up walks the same stops back. Shift+Up/Down from a blank-lines
  block starts the block selection on the nearest body block in that direction (CR-448 section 3).
  This holds for every container, and for a run on the container's first line.

**The selection after a removal (`requestDeleteBlankLines`).** Today `targetIndex` counts the blocks
that start before the run, minus 1 for a run with an `itemLine`. That count misses a holder that
starts on the run's first line, and it is wrong for footnotes, whose blocks are not next to the
body in the page. It becomes an index:
- **A held run** (any run with a top-level holder, section 2): the index in `blocks` (the selectable
  blocks) of that top-level holder itself, `blocks.indexOf(holder)`. That holder is the quote, the
  alert, the admonition, the panel, the definition list, the figure, the card, the grid, the quote
  directive or the list.
- **Any other run** (top-level or footnote): the index of the selectable block with the smallest
  line greater than `run.endLine`. With none, the index of the one with the largest line before
  `run.line`. Both are found by comparing lines.

**Paste.** `Ctrl/Cmd+V` on a selected block posts `previewBlocksPaste` with the run's
`containerLine`, as it posts `itemLine` today (around line 609).

**Unchanged, and kept:**
- A click on a blank-lines block inside an admonition, an alert, a context-tag panel, a quote, a
  definition or a footnote opens its insertion editor, never the container's own editor. Today a
  click inside an alert or admonition body opens the whole container (`editingElementFor` in
  `src/page/features/mappedBlocks.ts`); the block's click handler stops propagation.
- Shift+click does nothing. Delete and Backspace act only on a selected block. Alt+Up/Down moves
  nothing. Escape clears the selection. Ctrl/Cmd+C and +X do nothing.
- The structural navigation (BLOCK-254) never stops on a blank-lines block.

### 6. Look

The block uses the same element and CSS as CR-444 (`.sphinx-preview-blank-lines`).
- Inside a container it is as wide as the container's content box.
- Its Delete block button stays at its left edge. It must not overlap a quote's left border, an
  admonition's or alert's icon and title, or the list item handles; the visual captures check it.
- `editModeStyles.ts` is 792 lines, so new CSS goes in a style module of its own, as CR-448 says,
  rather than raising the cap.

### 7. Requirements

Follow the project's requirements guidelines: markers move with the code, run
`just requirements-update`, and add a dated entry in `requirements/tiers/log.md`. Everything is in
scope `block-editing`.

Update the four SwRS of CR-444 and CR-448, all `proposed`. The log entry gives the reason: they said
runs inside a quote, an alert or an admonition show nothing.

- **SwRS-MDOKFSTUDIO-BLOCK-266** (where a run shows):
  - The title and the normative text add runs inside a quote or an alert (its empty `>` lines), a
    directive of section 2's list (quote directives included), a context-tag panel, a definition
    and a footnote, shown inside that container.
  - They add that a run inside a closed dropdown shows only while the dropdown is open.
  - They add that a run between two footnote definitions shows at the end of the footnote above.
    A run between a footnote definition and the body after it shows in the body, after the body
    block above it.
  - The "Nothing is shown" scenario drops "a quote, an alert or an admonition". It keeps a fence,
    an HTML block, a table, a tab item and every holder outside the list.
  - Add the scenarios "Runs inside quotes and containers are shown" and "A run in a closed dropdown
    shows when it opens".
- **SwRS-MDOKFSTUDIO-BLOCK-267** (arrows, Enter, click):
  - The normative text adds the order on equal lines (a container before the blank-lines blocks it
    holds).
  - Add a scenario: Down from a selected quote whose run starts on its first line stops on that
    run, then on the next blank-lines block inside it, then on the block after it.
  - Add a scenario: a click on a blank-lines block opens its insertion editor, not the container's
    editor.
- **SwRS-MDOKFSTUDIO-BLOCK-268** (typing or pasting):
  - The normative text adds that a block written in place of a run inside a container takes the
    container indent: the quote prefix, then the item, directive, panel, definition or footnote
    indent.
  - It adds that inside a quote the block's blank lines and separators are copies of the run's
    first line.
  - It adds that a new entry typed between two entries goes at the list's indent: a term with its
    `:` line between two definition entries, or a `[^x]:` definition between two footnotes. Any
    other text typed there stays in the entry above.
  - It adds that the host checks the shape of the container line and refuses it as stale.
  - Add the scenarios "A block typed in a quote or a container stays in it" and "A new entry typed
    between two definitions or two footnotes is a sibling entry".
- **SwRS-MDOKFSTUDIO-BLOCK-269** (removal):
  - The normative text adds that a quote run keeps its first empty `>` line wherever it is, with
    the final line break kept or kept absent.
  - It adds that the selection goes to the top-level block that held the run.
  - Add a scenario covering a quote, an admonition, a definition and a footnote.
- **StRS:** none is added. `derives_from` stays StRS BLOCK-011 and BLOCK-025, whose text is
  unchanged.
- **Markers:**
  - New tests carry `@tests_req` for the SwRS they check.
  - The changed code keeps or gains its `@implements_req` markers, with at most 3 IDs per marker
    block: `blankRuns.ts`, `blankRunContainer.ts`, `blockRange.ts`, `insertion.ts`,
    `renderPipeline.ts`, `mystNormalize.ts`, the footnote and quote-directive render passes,
    `exportContent.ts`, `pageToHost.ts`, `blankLines.ts` and any file split from it,
    `blockSelectionView.ts`, `src/core/edits/sourceEdits.ts` and `blockEdits.ts`.

### 8. Shared vocabulary and docs

- **Glossary** (`.agents/glossary/common.md`):
  - "Blank run": add "inside a quote or an alert (two or more empty `>` lines of the same depth), an
    admonition, a context-tag panel or another Markdown directive, a definition or a footnote".
  - "Blank-lines block": add that inside a container it shows in that container, and that a block
    typed in it takes the container's `>` prefix and content indent.
  - Add "Empty quote line" and "Quote run" (see "Words"), and "Container indent" if the code uses
    that word.
- **Writing skill.** The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not
  concerned. No rendered syntax changes: the `dd` and footnote attributes are page-only and
  stripped from the export, and the quote directive's end line changes only mapping. The
  blank-lines block is edit-mode chrome.
- **Release notes.** They are written when the release is prepared, not in this PR.

## Out of scope

- **Directives whose content is not Markdown:** code blocks, math, mermaid, PlantUML, list-table and
  the other tables, and unresolved directives (shown as `pre`). Their blank lines are their content
  (CR-444, BLOCK-256 unchanged). The same goes for a fence, an HTML block or a table inside a
  container.
- **Tab items** (`{tab-item}` in a `{tab-set}`). Their blocks carry no source line by design, since
  they are edited with the item (settled by the Chief of Staff). Nothing is shown.
- **Wrapper directives.** `{topic}`, `{sidebar}`, `{margin}`, `{div}` and `{aside}` render an
  unmapped `div` around mapped paragraphs. Those paragraphs are top-level blocks (or blocks of a
  list item), so their runs already follow CR-444's and CR-448's rules, and a block typed there
  stays in the fence. This is unchanged; one page check and one host check confirm it.
- **Footnote definitions nested in a quote, a list item or a directive.** On the page, their
  paragraphs are not inside that container (section 2). Nothing is shown for a run in their body.
- **Changing other lines.** Collapsing runs by itself, on save, on render or on any other edit.
  Re-indenting or re-prefixing any line other than those of the block the writer types or pastes.
  Normalising `>` spacing.
- **New mapped blocks.** The `dd`, the footnote `li` and every other element stay unmapped.
- **Other places.** Runs in an included file, in the frontmatter or in a cell of the properties
  table.
- **Moving.** Moving a blank-lines block, or dragging blocks onto it.

## Evidence

**The ground rules.**
- The checks read the shipped files at the head under test: the real render pipeline, the real page
  bundle and the real stylesheet, never a prepared copy.
- Each new check fails on the code before the change (constitution, section 3).
- The CR-444 and CR-448 tests keep their intent. Some assertions expected nothing for a run inside a
  quote, an alert or an admonition: "a run inside a list of an admonition shows no blank-lines
  block" in `test/page/runtimeBlankLines.test.ts` (line 471), and the admonition run of
  `test/core/render/blankRunsInLists.test.ts`. Such an assertion is changed only for that reason,
  and the commit says so.

**Core, `test/core/mapping/`.** Each check runs in LF, CR LF and lone CR.
- **`emptyQuoteLine` and `quoteBlankRuns`:**
  - `>`, `> `, `>\t`, `> >`, `>>` and `  >` (in a list item) are empty quote lines, with their
    depth.
  - `> a`, `>a` and a blank line are not.
  - Runs of 2 and of 3 `>` lines are found. A single `>` gives nothing.
  - `> >`, `>` (two depths) gives nothing. `> >`, `> >`, `>`, `>` gives two runs.
  - A run at the start of a quote and one at the end of the text are found. The frontmatter is
    excluded.
- **`checkBlankRun` on quote runs:** accepted. Refused when a line is not an empty quote line, when
  the line above or below is one of the same depth, or when depths or columns differ.
- **`planBlankRunRemoval` on quote runs:** lines `line + 1`..`endLine` go and line `line` stays byte
  for byte (`> ` with its space). Checked in these places:
  - in the middle of the text;
  - at the start of the file;
  - at the start of a quote after a blank line;
  - at the end of the text, with a final line break (the result still ends with one) and without
    one (the result still ends without one).

  No bare LF appears in CR LF, and no CR in LF. Plain runs inside a directive, a definition and a
  footnote keep line `line`.
- **The container indent function:**
  - Each row of the examples table in section 4 gives its indent.
  - A tab before a fence, a context tag, a definition marker or a footnote label is kept as is.
  - Item line `> - x` with a run at depth 1 gives `>   `. Item line `>\t- x` gives the same
    columns.
  - A forged but well-formed fence line before the run is accepted.
  - Refused: a paragraph line, a fence without `{name}`, an HTML tag line (`<div>`), `:` with no
    text after it, a label line at or after the run, a frontmatter line, and quote markers at
    another depth.
- **`planBlankRunInsertion` and `planBlankRunPaste` through `insertionText`** (and `planBlocksPaste`
  in `test/core/edits/`):
  - Every row of the examples table.
  - A two-line "More\n\nText" in a quote gives `> More`, a copy of line `line`, `> Text`.
  - "> x" typed in a quote gives `> > x`.
  - "- c" between `> - x` and `> - y` gives `> - c`.
  - "New\n: dn" between two definition entries gives `New`, `: dn`; between two paragraphs of one
    definition it gives `  New`, `  : dn`.
  - "[^c]: f3" between two footnote definitions gives `[^c]: f3`; "More" there gives `    More`;
    "[^c]: f3" between two paragraphs of one footnote gives `    [^c]: f3`.
  - Without `itemLine` or `containerLine`, the output for a plain run is identical to today.
- **Rendered result.** Each insertion and paste case above applies its plan to the text and renders
  the result with `renderPreviewSource`. It asserts one top-level container (quote, alert,
  admonition, panel, quote directive, definition list or footnote) and the new block inside the
  expected container. For the new definition entry, it asserts one `dl` with three terms; for the new footnote, three
  footnotes, and for "More" between two footnotes, a second paragraph in the first one.

**Protocol, `test/core/protocol/pageToHost.test.ts`.** `replaceBlankRun.containerLine` is accepted
when it is a source line below `line`. It is rejected when at or after `line`, when not an integer,
when sent together with `itemLine`, and on a message type that does not take `replaceBlankRun`.

**Render and export, `test/core/render/` and `test/core/export/`.** The input text holds all of
these:
- a quote run, an alert run, and a quote run that starts on the quote's first line;
- a run in an admonition, in a closed dropdown, in a context-tag panel, in an `{epigraph}`, in a
  `{figure}` and in a `{card}`;
- a run in a loose definition, and one between two entries of a tight definition list;
- a run in a footnote, one after a label line alone, and one between two footnote definitions;
- a run in a fence inside a quote, and a quote run next to a plain run.

`renderPreviewSource` gives:
- the run list with every run, sorted, the adjacent quote and plain runs both present;
- each `dd` with its page-only line attribute equal to its marker line, and no `data-line` on it;
- each footnote `li` with its page-only label line attribute, equal to its label line, the label
  line alone included;
- the `{epigraph}` quote with a `data-end-line` equal to the closing fence line;
- the ranges section 2 relies on: the quote holding its run up to its edges, the admonition, panel,
  quote directive and figure holding theirs, and the footnote paragraphs as top-level mapped
  blocks.

`exportContent` carries neither the `dd` attribute nor the footnote attribute.

**Page, `test/page/runtimeBlankLines.test.ts`.** The checks run on the runtime bundle, one check
per rule; add shapes to the harness for each container.
- **Quotes and alerts:**
  - A quote run makes one blank-lines block inside the `blockquote`, between its paragraphs.
  - A run at the start of a quote and one at its end make one block each, inside the quote. The
    start one sits before the quote's first child.
  - An alert run makes one block inside the alert, after its title, before its first block.
- **Directives:**
  - A run in an admonition, a context-tag panel, an `{epigraph}`, a `{figure}`, a `{card}` (in its
    body, between the paragraphs) and a grid item makes one block inside that container.
  - A run held only by a grid makes none.
- **Definitions:** a run in a loose definition makes one block in its `dd`, between its paragraphs.
  A run between two entries of a tight definition list makes one at the end of the first `dd`.
- **Footnotes:**
  - A run between two paragraphs of a footnote makes one block inside the footnote `li`, and its
    message carries the footnote's label line as `containerLine`.
  - A run after a label line alone makes one block at the start of that `li`, with that label line.
  - A run between two footnote definitions makes one block at the end of the first footnote's
    `li`, with that footnote's label line as `containerLine`.
  - A run between a footnote definition and the body after it makes one block in the body, right
    after the body block with the largest line before it, even when footnote blocks have larger
    lines.
  - A run in the body of a footnote written inside a quote makes none.
- **Nothing shown:** a run in a fence inside a quote, in a `pre`, in a table, in a tab panel, and in
  a table inside an admonition (a non-container in the chain) makes none.
- **Adjacent runs:** a quote run and a plain run next to each other both show.
- **Folding and dropdowns:**
  - A run inside a folded top-level quote makes none, and unfolding makes one.
  - A run in a closed dropdown makes none. Opening it (setting `open` and firing `toggle`) makes
    one, and closing it removes it.
  - An insertion editor opened in an open dropdown stays open, with its block, when the dropdown
    closes.
- **Patches:**
  - A content patch keeps the element of an unchanged quote run.
  - An editor opened from a quote run stays open across a patch that replaces the whole quote (new
    elements, the old ones detached, the run gone). The block is back inside the new quote with the
    editor frame after it, and Cancel posts `previewEditCancel` with the same `replaceBlankRun`.
- **Click and paste:**
  - A click on a block inside an admonition, a context-tag panel and an alert posts
    `previewEditOpen` with `replaceBlankRun`: with `containerLine` for the admonition and the
    panel, none for the alert. It opens no container editor.
  - Ctrl/Cmd+V on a selected block posts `previewBlocksPaste` with the same `containerLine`.
- **Arrows (F1):**
  - Down from a selected quote stops on each blank-lines block inside it, in line order, then on
    the block after it; Up walks back.
  - With a run that starts on the quote's first line, Down from the quote stops on that run first,
    and Up from that run selects the quote.
- **Delete:**
  - Delete on a selected block posts `previewBlankRunDelete`. After the removal result and the
    render, the quote is selected; the same holds for the admonition and the definition list.
  - It also holds for a run on the quote's first line, with blocks above the quote.
  - For a footnote run, the selection goes to the footnote paragraph after it, not to a body block.

**Session, `test/session/`.** Use a new file, for example `blankRunInContainerHost.test.ts`, with
the real handlers, in LF and CR LF.
- **Delete:**
  - `previewBlankRunDelete` on a quote run removes lines `line + 1`..`endLine` and keeps the first
    `>` line byte for byte. It makes one `applyWrittenEdits` call and leaves the rest identical.
  - The same holds at the end of the text with and without a final line break, and on a run in an
    admonition, a definition and a footnote.
- **Save in a quote:** a save of "More" in a quote run writes `> More` with `>` separators. A later
  autosave of "More text" replaces it. Cancel after the autosave restores the run byte for byte.
- **Save with a container line:**
  - A save of "More" with `containerLine` writes the indents of the examples table for: an
    admonition nested in a list item, a context-tag panel, an `{epigraph}`, a definition, a footnote
    and a footnote label line alone.
  - A save of "New\n: dn" between two definition entries writes a sibling entry.
  - Between two footnote definitions, a save of "[^c]: f3" writes a sibling footnote at column 0,
    and a save of "More" writes `    More` in the footnote above.
  - A save of "- c" with `itemLine` in a list inside a quote writes `> - c` between items and
    `>   - c` inside an item.
- **Rendered result:** each save and paste above renders the written text with
  `renderPreviewSource` and asserts the new block inside the expected container.
- **Re-created save:** a save with `containerLine` and no held edit writes the same indent.
- **Stale line:** a stale `containerLine` is refused with the stale message of open, of the
  re-created save and of the paste, and the document does not change. Stale cases: a paragraph line,
  a line that changed, quote markers at another depth.
- **Wrapper directive:** for a run inside a `{topic}`, at the top level and in a list item, a save
  of "More" writes it inside the fence, as today.

**Visual (`just ci-visual`).** Add the fixture `test/visual/fixtures/94-blank-lines-in-containers.md`
with a quote run, an alert run, a run in an admonition, a run in a context-tag panel, a run in a
definition and a run in a footnote. Add scenarios in `test/visual/blankLinesBlockScenarios.ts`,
with checks in `test/visual/capture_blank_lines_block.py`:
- In edit mode there is one blank-lines block in each container, inside it, as wide as its content
  box.
- With one block selected in the quote and one in the alert, the Delete block button shows at the
  block's left edge and overlaps neither the quote's border nor the alert's icon or title.
- In reading mode there is none.
- Typing: click the quote's blank-lines block, type "More" and wait past an autosave. The editor is
  still open inside the re-rendered quote.

The captures are attached to the PR, as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch).** In
`test/integration/blankLines.test.ts`, add a fixture, in LF and in CR LF, with three parts:
- a quote holding three empty `>` lines between two paragraphs;
- an admonition in a list item, with three blank lines between two paragraphs;
- a footnote with three blank lines between two paragraphs.

The test does this:
1. Send `previewBlankRunDelete` for the quote run. One `>` line is left, the rest is unchanged, and
   no bare LF appears in CR LF. One undo brings the run back.
2. Send `previewEditSave` with `replaceBlankRun` for the quote run, with `More`. The file gets
   `> More` with one `>` line on each side, and the line endings are kept. One undo brings the run
   back.
3. The same for the admonition run with its `containerLine`: `  More`, inside the fence.
4. The same for the footnote run with its `containerLine`: `    More`, inside the footnote.

**Requirements.** `just requirements-lint` and `just requirements-update` pass. The updated SwRS
carry their markers at the code and the tests above.

**Gate.** `just preflight` passes (on Windows, its static stage; CI runs the others).
