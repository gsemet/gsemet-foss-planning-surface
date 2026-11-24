# Balance the edges of a raw Markdown copy

Short name: `copy-edges`. No tracker issue (origin: the owner, verbal, 2026-11-23, split off from
`copy-selection-raw-markdown` on copy-raw-Q17). Destination: the running batch, batch-09, stacked on
`copy-selection-raw-markdown` (short name `copy-raw`, "the base CR" below): this CR's branch starts
from the base CR's branch and needs its raw copy (the `previewSourceText` protocol, the page's copy
handler, the selection-to-source mapping, generated content, UI chrome, scope and clipboard
formats).

## Goal

The owner, 2026-11-23: "Au caractère prêt, et il faut éventuellement rajouter les caractères de
clôture ou d'ouverture (admonition, tables…) si on commence ou fini au milieu".

The base CR makes a native selection copy, as text/plain, the source between the character under
the selection's start and the character under its end, verbatim. When an edge falls in the middle
of a construct, that verbatim cut is broken Markdown: `rld** again`, an admonition's body without
its fence, table rows without their header, a sub-item still indented under a parent that is not
copied. This CR balances the cut: the text is still cut exactly at the character, and the
characters that open or close what the cut went through are added, so the pasted Markdown is well
formed and renders as the part the writer selected. A selection whose edges are clean (outside
any construct) copies exactly what the base CR copies.

## Decisions carried from `02-answers.md`

| Q | Decision | Where it lands below |
| --- | --- | --- |
| copy-edges-Q1 (= copy-raw-Q1) | Character-precise; the opening or closing characters of a container (admonition, table…) are added when the selection starts or ends inside it. | 3.3, 3.4 |
| copy-edges-Q2 (= copy-raw-Q2) | An inline construct cut at an edge is cut exactly there and its markers are added: starting at "r" of `**world**` copies `**rld**`. | 3.2 |
| copy-edges-Q3 (= copy-raw-Q6) | A table cut at an edge: the rows touched, whole, preceded by the header row and the delimiter row. | 3.4 |
| copy-edges-Q4 (= copy-raw-Q7, copy-raw-Q16) | A nested list cut at the start keeps the item's marker and the list is brought to level 0: every copied item is shifted by the indentation of the shallowest item selected, so relative depths are kept (Q16 B, against the recommendation). | 3.5 |
| copy-edges-Q5 (= copy-raw-Q11) | A heading cut at the start keeps its marker: `## llo`. | 3.6 |
| copy-edges-Q6 (= copy-raw-Q13) | An edge the alignment cannot place snaps to the whole source element. | 3.7 |
| copy-edges-Q7 (= copy-raw-Q9) | One okfreq SwRS per balancing rule, and tests at the edges: an admonition in an admonition, a list inside an admonition, an admonition inside a list item, a selection starting or ending at each nesting level, code fences inside containers, tables inside admonitions, a cut inside nested inline markers (bold inside a link), a selection across several containers. | 4, E2, E3 |
| copy-edges-Q8 (= copy-raw-Q17) | Specified for the running batch, batch-09, stacked on the base CR; spec critic yes, on the split's seams. | Header, 1 |

Carried from the base CR's critic run (copy-raw answers 14 to 18) where they touch the edges:

- copy-raw-Q14: Ctrl+A then copy gives the whole source exactly, final newline included. An edge
  at offset 0 or at the end of the source is clean (3.1), so balancing never changes that result.
- copy-raw-Q15: a selection with an edge in an old-side card of the side-by-side view stays a
  native copy (the base CR decides it before the seam); balancing never runs on it.
- copy-raw answer 18, F5: the frames of the core tests are taken from the real core renderer's
  output (a tab item carries no source line: `src/core/render/mystNode.ts` lines 90-97,
  `src/core/render/mystGridToctree.ts` line 491), and the nesting grid also runs in the real
  browser (E2, E3).
- copy-raw answer 18, F6: text/html is proved in Chromium only; this CR does not change text/html.

## 1. The seam with the base CR

The base CR's pure function (`rawMarkdownForSelection` in `src/core/mapping/rawCopy.ts`, as the
joint specification named it) resolves each edge to a source offset, then produces the verbatim
cut `source.slice(startOffset, endOffset)` in one step. That step is the seam. This CR replaces it
with a call to a new pure function, and changes nothing before it (scope, native cases, the
`previewSourceText` message, the alignment of a placed edge, atomic generated content, chrome,
text/html) nor after it (setting text/plain, `preventDefault`).

```ts
// src/core/mapping/rawCopyBalance.ts
/** One edge of the cut, resolved by the base CR's mapping. */
export interface RawCutEdge {
  offset: number;                   // the source offset of the edge (UTF-16 index in `source`)
  frames: readonly RawCopyFrame[];  // the mapped elements enclosing the edge, outermost first
  placed: boolean;                  // false when the alignment could not place the edge (3.7)
}
export function balanceRawCut(source: string, start: RawCutEdge, end: RawCutEdge): string;
```

`RawCopyFrame` is the base CR's type (`line`, `endLine`, `atomic`). If the base CR names the seam,
the frame type or the unplaceable case differently, the Driver uses the base CR's names and keeps
the behaviour below; if the base CR's edge carries no frames past the mapping, this CR passes them
through (the page's edge builder already reads them for the mapping). If the base CR's mapping
returns `undefined` for an unplaceable edge (native copy), this CR changes that branch to call
`balanceRawCut` with `placed: false` (3.7).

`balanceRawCut` returns exactly `source.slice(start.offset, end.offset)` when both edges are clean
(3.1). Every added character uses the document's line break (CR LF or LF, as the source's first
line break; LF for a source without one).

## 2. What changes, area by area

### 2.1 Core

- New `src/core/mapping/rawCopyBalance.ts`: `balanceRawCut` and the block rules (3.3 to 3.7). New
  `src/core/mapping/rawCopyInline.ts`: the inline scan of 3.2 (the delimiters of the constructs
  that enclose an offset inside one block's source). Both pure (no DOM, no host API, no `vscode`),
  each under the project's file size limit (`just check`); split further if one grows.
- Reuse, do not duplicate: `listItemIndentOfLine` and `startsWithListMarker` of
  `src/core/mapping/listItemIndent.ts` for list markers and content columns,
  `frontmatterLineCount` of `src/core/mapping/blockRange.ts` for the frontmatter, the quote-prefix
  reading of `src/core/mapping/quoteLine.ts` where it fits.
- `src/core/mapping/rawCopy.ts` (the base CR's): the seam calls `balanceRawCut`; its unplaceable
  branch is changed as section 1 says.

### 2.2 Page

No new page module. Only if the base CR's page code drops an edge's frames or turns an
unplaceable edge into a native copy before the core call, `src/page/features/rawCopy.ts` (the base
CR's) is changed to pass them on. Scope, native cases and chrome stay the base CR's.

### 2.3 Glossary

`.agents/glossary/common.md`, next to the base CR's **Raw copy** entry: add **Edge balancing**:
the characters a raw copy adds at a cut edge so the copied Markdown stays well formed (inline
markers, container fence lines, a table's header and delimiter rows, a list item's marker brought
to level 0, a heading marker), `balanceRawCut` in `src/core/mapping/rawCopyBalance.ts`.

### 2.4 Not touched

The writing skill (`skills/writing-for-markdown-okf-schema-studio/`): no rendered syntax changes.
The block selection's copy (SwRS-MDOKFSTUDIO-BLOCK-166), the code block's Copy button, the
`previewSourceText` protocol and text/html.

## 3. Behaviour

### 3.1 Clean and cut edges

- An edge is **clean** when it is at offset 0, at the end of the source, between two top-level
  blocks, or in a top-level paragraph's text outside every inline construct. A clean edge adds
  nothing.
- Otherwise the edge **cuts** the constructs that enclose it: the inline constructs of its block
  (3.2), and the block constructs of its frames (3.3 to 3.6). Each cut construct adds its opening
  characters before the copy (start edge) or its closing characters after it (end edge). The
  added characters come from the source, verbatim (the same fence length, option lines, link
  target), never rebuilt.
- Each end is balanced on its own: a construct both edges are inside (a selection within one bold
  word, one admonition, one table) gets its opening before and its closing after; a construct the
  selection fully covers, or whose opening and closing are both in the cut, adds nothing.
- Order: before the cut, the openings outermost first (the outermost block container's opening
  line first, the innermost inline marker last, nearest the text); after the cut, the closings
  innermost first.

### 3.2 Inline constructs (copy-edges-Q2)

When an edge falls strictly inside an inline construct of its block, the cut stays at the edge
and the construct's delimiters on the other side are added:

| Source | Selection | Copied |
| --- | --- | --- |
| `Hello **world** again` | from "r" of world to the end of the line | `**rld** again` |
| `Hello **world** again` | from the start to "o" of world (included) | `Hello **wo**` |
| `Hello **world** again` | from "o" to "l" of world (included) | `**orl**` |
| `a [link **bold** text](https://x.test) b` | from "ld" to "te" (included) | `[**ld** te](https://x.test)` |
| `` use `npm ci` here `` | from "ci" to the end | `` `ci` here `` |
| ``{kbd}`Ctrl+C` to copy`` | from "t" of Ctrl to the end | ``{kbd}`trl+C` to copy`` |
| `~~old~~ and *new*` | from "l" of old to "n" of new (included) | `~~ld~~ and *n*` |
| `see <span class="k">key word</span> here` | from "w" to the end | `<span class="k">word</span> here` |

- The constructs: emphasis and strong (`*`, `_`, `**`, `__`, `***`), strikethrough (`~~`), inline
  code (its backtick run), links (opening `[`, closing `](target "title")` verbatim), reference
  links (closing `][ref]`, `][]` or `]` verbatim), autolinks (`<` … `>`), MyST roles (opening
  ``{name}` `` plus its backtick run, closing the backtick run), inline math (`$` … `$`) and inline
  HTML elements (the opening tag verbatim, the matching closing tag).
- A start edge on the first content character of a construct, or an end edge after its last one,
  gives the whole construct (`**world**`), not a cut.
- An inline construct whose rendered text is not its source (an image, a footnote reference
  `[^1]`, a role whose text is computed such as `{ref}`, `{numref}`, `{doc}`, a citation) is
  atomic: an edge inside it moves before it (start edge) or after it (end edge), so it is copied
  whole. If the base CR already does this, nothing changes.
- An inline construct cut inside a table row gives nothing of its own: the row is copied whole
  (3.4).

### 3.3 Containers (copy-edges-Q1)

A container is a mapped element whose source has an opening and, for some, a closing: a MyST
directive or admonition in a backtick, tilde or colon fence (```` ```{note} ````, `:::{note}`),
with its option lines (`:key: value`) or its YAML options block; a code fence (backtick, tilde, or
a `{code-block}` / `{code}` directive); a GitHub alert (`> [!NOTE]`); a blockquote (`>`); a tab set,
a tab item, a card, a grid and a grid item (all fenced directives).

- Start edge inside a container that opens before it: the container's opening lines (the fence
  line and its option lines or options block, verbatim; for an alert its `> [!TYPE]` line) are
  added before the cut. A blockquote or an alert gives its `> ` prefix(es), verbatim, to the
  first, partial line of the cut; the later lines carry theirs already.
- End edge inside a container that closes after it: the container's closing line (its fence line,
  verbatim) is added after the cut, on a new line. A blockquote, an alert and a list have no
  closing line. A fenced container left unclosed in the source (it runs to the end of the
  document) has none either: nothing is added.
- An edge in a container's opening line (an admonition's title, a tab item's label): the start
  edge moves to the start of that line, the end edge to its end, so the opening line is copied
  whole; then the rule above applies (an end edge there adds the closing line).
- Nested containers each add theirs: an admonition in an admonition cut at both ends gives both
  opening lines and both closing lines, each verbatim (a four-colon outer fence stays four
  colons).
- Across containers: starting inside admonition A and ending inside admonition B adds A's opening
  before and B's closing after; A's closing and B's opening are in the cut already.
- A code fence inside a container is itself a container: starting in the code adds the outer
  opening lines, then the code fence's opening line, then the code from the edge; an end inside
  the code adds the code fence's closing line, then the outer closings.
- Fenced containers are found in the source, not only from the frames: a fence scan of the source
  (fence character, length, nesting, the matching closing fence; inside list items, at the item's
  content column) gives every fenced container enclosing an offset, so a tab item, which carries
  no source line in the page (copy-raw answer 18, F5), still gets its fence lines. Lists, list
  items, tables, headings, blockquotes and alerts come from the frames and the source lines they
  name.

### 3.4 Tables (copy-edges-Q3)

- An edge inside a table copies the rows it touches whole: the start edge moves to the start of
  its row's line, the end edge to the end of its row's line.
- The copied part of a table that the start edge is inside begins with that table's header row
  and its delimiter row, verbatim, then the rows from the start row on. A start edge in the header
  row or the delimiter row starts at the header row (nothing added).
- Both edges in one table: header, delimiter, then the rows from the start row to the end row.
- Start before the table, end inside it: the header and delimiter are in the cut already; the end
  row is completed.
- A table inside an admonition cut at the start: the admonition's opening lines, then header,
  delimiter and the touched rows, then (end inside the admonition) its closing line.
- A table inside a blockquote or a list item keeps its prefix or indentation on the added header
  and delimiter rows, as in the source (then 3.5 shifts list lines).

### 3.5 Lists (copy-edges-Q4)

Applies when the start edge is inside a list item.

- The innermost list item enclosing the start edge keeps its marker (`-`, `*`, `+`, or its own
  number `3.` / `3)`, with its task box `[ ]` / `[x]` when it has one), followed by one space and
  what the other rules give: the cut text, or the opening line of a container inside the item
  (then that container's other opening lines on the next lines, at the item's content column).
  The outer items enclosing it give no marker and no text.
- The shift: among the list items whose marker is copied (the start item and every later item of
  the same top-level list whose marker line is in the cut), take the smallest marker column `m`,
  counted after the prefix of the containers kept in the copy (a blockquote's `> `, the content
  column of a kept enclosing container). Every copied line of that top-level list, the start
  item's marker line included, loses `m` columns of leading whitespace, clamped at column 0 (a
  lazy continuation line with less indentation keeps its text). Lines after that list's last line
  are not shifted. The shallowest item selected lands at column 0; the others keep their depth
  relative to it.
- Example, selecting from "rld" of the sub-item to the end of the list:

  Source:

  ```markdown
  - parent
    - child **world**
    - sibling
  - next
  ```

  Copied (`m` = 0, from `- next`):

  ```markdown
    - **rld**
    - sibling
  - next
  ```

  Selecting from "rld" to the end of `sibling` only (`m` = 2):

  ```markdown
  - **rld**
  - sibling
  ```

- An admonition inside a list item, start in the admonition's paragraph: the item's marker
  (shifted), then the admonition's opening line on the marker line, then the cut text and the
  later lines at the item's content column minus `m`, then (end inside it) the closing line at
  the same column.
- An end edge inside a list item adds nothing for the list (a list has no closing line); the
  containers inside the item close as 3.3 says, at their source column minus `m` when the start
  edge is in the same top-level list.

### 3.6 Headings (copy-edges-Q5)

- A start edge inside an ATX heading's text adds its marker verbatim (the `#` run and the space
  after it, with the heading's indentation): `## Hello` from "llo" copies `## llo`.
- A start edge inside a setext heading (`Hello` over a `===` or `---` line) adds nothing before;
  an end edge inside it adds its underline line on a new line, verbatim, so it stays a heading.
  (Written against an open point: open question 2.)
- An end edge inside an ATX heading adds nothing (closing `#`s are optional).

### 3.7 An edge the alignment cannot place (copy-edges-Q6)

When the base CR's alignment cannot place an edge in its innermost non-atomic mapped element (the
rendered text has no unique match in that element's source), the edge snaps to that whole
element: the start edge to the first character of its first source line, the end edge to the end
of its last source line. The element is then copied whole and adds nothing of its own; the
containers enclosing it are balanced as 3.3 to 3.6 say. The copy is never left native for this
reason.

## 4. Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md`, the okfreq baseline it links to and
`requirements/guidelines/project.guidelines.md` ("During a change"); run okfreq as
`uv run --no-sync --group requirements okfreq`.

- New SwRS in scope `block-editing` (token BLOCK), created with `okfreq new … --lifecycle
  proposed`, each deriving from the StRS the base CR creates ("A reader copies a selection as the
  exact Markdown under it"), one per balancing rule (the Driver may merge two only when one test
  file proves both):
  1. Inline balancing, atomic inline constructs, clean edges unchanged (3.1, 3.2).
  2. Container opening and closing lines: nested, across containers, opening-line edges, code
     fences inside containers, blockquote and alert prefixes, unclosed fences (3.3).
  3. Table header and delimiter rows with whole touched rows (3.4).
  4. List item marker and the shift by the shallowest item selected (3.5).
  5. Heading marker at a cut heading (3.6).
  6. An unplaceable edge snaps to the whole element (3.7).
- Changed SwRS: the base CR's SwRS of the character-precise cut (and of the unplaceable edge, if
  the base CR states one) gets one line: the verbatim cut is then balanced as the six SwRS above
  say. They are `proposed` in the same batch: no owner approval needed. No `approved` requirement
  is touched (none of the approved StRS covers copying a native selection); if the Driver finds
  one, it stops and asks.
- Markers: `@implements_req` at each rule's code point in `rawCopyBalance.ts` and
  `rawCopyInline.ts` (the inline scan, the container rule, the table rule, the list shift, the
  heading rule, the snap), `@tests_req` at each test; at most 3 IDs per marker block
  (`just check-markers`).
- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` under the day of
  the change, in a `### Raw copy: edge balancing` sub-heading.

## 5. Out of scope

- Everything the base CR owns: scope and native cases, the `previewSourceText` protocol, the
  alignment of a placed edge, generated content and included blocks, chrome, text/html, Ctrl+A.
- Adding a link reference definition, a footnote definition or a label target that a copied
  construct points to.
- Rewriting the copied Markdown beyond the added characters: no marker normalization, no reflow,
  no renumbering of an ordered list, no path conversion.
- Balancing a cut (Ctrl+X) or any edit from a native selection.
- A setting to turn balancing off.

## Evidence

No host and default matrix: the change depends on neither a chantier host nor a shipped default
versus a configured value. Balancing is pure core code; the browser and the real VS Code window
only prove that the page's copy reaches it (E3, E4).

### E1. Static and unit gates

- `just check` passes (formatting, TypeScript, import boundaries: the new modules are `src/core`
  and import nothing above it; file size; unused exports; markers; unit and contract tests).
- `just requirements-lint` and `just requirements-update` pass, each new SwRS with a source marker
  and a test marker.
- `just preflight` passes (on Windows the static stage; CI runs the others), constitution
  section 4.

### E2. Core unit tests: `test/core/mapping/rawCopyBalance.test.ts`

Each case is a source written in the test, the selection's start and end named as rendered
characters, and the exact expected string. The frames are not written by hand: the test renders
the source with `renderMyst` of `src/core/render/mystRenderer.ts` and reads the mapped elements
(`data-line`, `data-end-line`) with the helpers of `test/core/render/dom.ts`, as
`test/core/render/alertSourceLines.test.ts` does, then calls the base CR's mapping and
`balanceRawCut` (copy-raw answer 18, F5). Cases, at least:

- every row of the 3.2 table, and bold inside a link cut on both sides;
- clean edges: a selection between blocks and one in a top-level paragraph outside any construct
  give exactly `source.slice(start, end)`; a whole-document selection (offset 0 to the end) gives
  the source exactly, final newline included (copy-raw-Q14);
- an inline atomic construct (`{ref}`, an image, `[^1]`) with an edge inside: copied whole;
- an admonition in an admonition (colon fences of 4 and 3 colons): start in the inner one and end
  after both; start before both and end in the inner one; both edges in the inner one;
- a list inside an admonition, start in the second item: the admonition's opening, the item's
  marker at column 0, the closing fence after;
- an admonition inside a list item, start in the admonition's paragraph (3.5);
- the nesting grid: an admonition > list item > admonition, a start at each level (0 to 3) by an
  end at each level (0 to 3), the 16 expected strings written out;
- a code fence inside an admonition, start in the code: admonition opening, code fence opening,
  the code from the edge; with the end in the code: the code fence's closing, then the
  admonition's;
- a table inside an admonition, both edges in the table: opening, header, delimiter, touched rows,
  closing;
- a table with the start in the header row, with the start in a body row cell's bold text, and
  with the end in the last row;
- the two list examples of 3.5 (`m` = 0 and `m` = 2), a later item shallower than the start item
  three levels deep, an ordered list keeping its own number, a task item keeping `[x]`, a list in
  a blockquote (the shift counted after `> `);
- a selection from inside admonition A to inside admonition B;
- a GitHub alert and a blockquote cut at the start (`> [!NOTE]` line and `> ` prefixes);
- an edge in an admonition's title, start and end;
- a tab set with two tab items, start in the second item's paragraph: the tab set's and the tab
  item's opening lines (the tab item has no frame);
- an unclosed colon fence, end inside it: nothing added;
- an ATX heading cut at the start (`## llo`) and a setext heading cut at the end;
- an unplaceable edge (rendered text absent from the element's source): snapped to the element,
  its enclosing admonition still balanced;
- a CR LF document: the cut keeps CR LF and every added line uses CR LF.

### E3. Real browser: the base CR's `test/visual/capture_raw_copy.py`

The base CR's capture check (its scenario file `test/visual/rawCopyScenarios.ts` and its fixture
under `test/visual/fixtures/`) gets balancing cases; the fixture gains the constructs it lacks (an
admonition > list > admonition nest, a tab set, a heading, a table in an admonition). The fixture
is the repository file rendered by the real pipeline, the page runs the shipped page bundle, and
`previewSourceText` carries the fixture's text read from the repository, as the base CR's check
does. For each case the check sets a DOM `Range` on the rendered characters named in the case,
dispatches the `copy` `ClipboardEvent` the base CR's check uses, and asserts the exact text/plain:

- `**rld**` and bold inside a link cut on both sides;
- the nesting grid of E2 (16 cases), in the real DOM (copy-raw answer 18, F5);
- a table row inside an admonition, from a bold word in the row;
- the nested list example with `m` = 0;
- a selection across two admonitions;
- the tab set case;
- `## llo`;
- a clean selection (two whole paragraphs) equal to the verbatim slice.

Each case fails before this CR (the base CR alone gives the unbalanced cut), which is the failing
test constitution section 3 asks for.

### E4. Real VS Code window: the base CR's `test/integration/realInput/rawCopy.ts`

One more step in the base CR's real-input scenario: in the opened fixture, a Range from "r" of a
bold word inside an admonition to the middle of a table row in the same admonition, the platform
copy chord as real input, then `vscode.env.clipboard.readText()` waited until it holds the
admonition's opening line, `**rld**`, the rest of the line, the table's header and delimiter rows,
the touched rows whole and the closing fence; the clipboard restored at the end. It runs in
`just ci-integration` (a push to `main`, or
`gh workflow run ci.yml --ref <branch> -f heavy=true` on the branch, which the Driver runs before
asking for a merge).

### E5. Pull request

The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and
`.agents/guidelines/pull-request.guidelines.md`, stacked on the base CR's PR per
`.agents/guidelines/stacked-prs.guidelines.md`: the Tests section lists the new and changed
requirement IDs with their source and test files, a short before/after of a copy starting inside
a bold word of an admonition's table, the CHANGELOG line. Commit scope per
`.agents/guidelines/git-commit-allowed-scopes.md` (`feat(vscode)` or `feat(render)`, as the base
CR).

## Open questions

1. Q4 B shifts every copied item by the shallowest item selected. When the start item ends up 4 or
   more columns right of column 0 (it was three levels deep and a top-level item is selected
   after it), the pasted first line is, in CommonMark, an indented code block, not a list item.
   Written against Q4 as answered (the shift alone). The other option: when the start item would
   land at 4 columns or more, clamp its marker line to 3 columns.
2. A setext heading (`Hello` over `---`) cut at the end: written against "its underline line is
   added", like the heading marker of Q5. The other option: nothing is added (the copy becomes a
   paragraph).
3. A selection entirely inside one code block (a word of a code line): written against Q1 as
   answered, so the code fence's opening and closing lines are added around the word. The other
   option: inside a single code block, copy the code text alone.
