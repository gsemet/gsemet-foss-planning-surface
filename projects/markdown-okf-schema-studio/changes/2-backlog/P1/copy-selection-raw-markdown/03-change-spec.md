# Copy a selection as the exact raw Markdown under it

Short name: `copy-raw`. No tracker issue (origin: the owner, verbal, 2026-11-23). Destination:
the running batch, batch-09.

## Goal

The owner, 2026-11-23: "quand je sélectionne du texte ça copie pas exactement le texte dessous
(par exemple les triple tirets ou des tables etc). Le but c'est que du point de départ au point en
dessous le texte brut y compris le formatage est conservé."

When a writer selects text in Studio with the mouse or the keyboard and copies it (Ctrl+C, Cmd+C
on macOS, or the context menu's Copy), the clipboard's plain text holds the raw Markdown source
from the point under the selection's start to the point under its end, formatting included:
thematic breaks, tables, emphasis, links, directives, fences. The cut is exact to the character,
and the copied Markdown stays well formed: an inline marker, a container or a table cut at an edge
gets back the characters that open or close it. The clipboard's HTML keeps the rendered selection,
so pasting into a rich editor still gives formatted text.

Today the page has no copy handler for a native selection: the browser copies the rendered text
(a table becomes tab-separated cells, `---` disappears, `**bold**` becomes `bold`). Only the edit
mode's block selection (Shift+click, whole blocks, SwRS-MDOKFSTUDIO-BLOCK-166) copies source lines,
through the host.

## Decisions carried from `02-answers.md`

| Q | Decision | Where it lands below |
| --- | --- | --- |
| Q1 | Character-precise; when the selection starts or ends inside a container, its opening or closing characters are added. | 3.2, 3.4 |
| Q2 | An inline element cut at an edge is cut exactly there, and its closing (or opening) characters are added so the Markdown stays balanced: starting at "r" of `**world**` copies `**rld**`. | 3.3 |
| Q3 | text/plain carries the raw Markdown, text/html the rendered HTML. | 3.7 |
| Q4 | Everywhere in the page, read and edit mode, except inside a text input or a field being edited, which keeps the native copy. | 3.1 |
| Q5 | Generated content copies the source that produces it (a rendered Mermaid diagram gives its fence, a generated table of contents its directive, the frontmatter properties table its YAML); UI chrome (comment bubbles, buttons, line numbers, toolbars) is never copied. | 3.6, 3.7 |
| Q6 | A table cut at an edge: the rows touched, whole, preceded by the header row and the delimiter row. | 3.5 |
| Q7 | A nested list cut at the start: keep the item's marker and bring the first item to level 0; the next items keep their relative indentation. | 3.5 |
| Q9 | The behaviour is captured in okfreq requirements (one StRS use case, one SwRS per rule), and the tests cover the edges listed in "Evidence", section E2. | 4, Evidence |
| Q10 | Specified for the running batch, batch-09, provided the testing is planned as Q9 asks. | - |

Points the answers leave open are listed at the end ("Open questions"); the specification names
the default each one is written against, so the Driver can start, and the Chief of Staff confirms
or corrects them with the owner.

## 1. How it works (design)

The copy event of the browser is synchronous: `event.clipboardData.setData` must run inside the
handler, and the host's clipboard (`HostUi.writeClipboard`, `vscode.env.clipboard.writeText`) only
writes plain text, so it cannot carry the text/html that Q3 asks for. The page therefore computes
the Markdown itself, at copy time, from the source text of the render it shows:

1. The host sends the page the source text of the render the page shows (new message
   `previewSourceText`, section 2.1).
2. On a `copy` event, the page reads the selection's two edges from the DOM (the mapped elements
   that enclose each edge, the rendered text of the innermost one and the edge's offset in it) and
   calls a pure function of `src/core` with the source text and the two edges.
3. That function returns the raw Markdown (sections 3.2 to 3.6); the page sets it as text/plain,
   sets the rendered HTML of the selection (chrome removed) as text/html, and prevents the default
   copy.

No host round trip happens at copy time; the block selection's copy (BLOCK-166) keeps its own host
path unchanged.

## 2. What changes, area by area

### 2.1 Protocol: the source text of the shown render

- `src/core/protocol/hostToPage.ts`: a new message
  `PreviewSourceTextMessage extends RenderMessage<"previewSourceText">` with one field
  `text: string`, the full text of the active document of that render (frontmatter included, line
  breaks as in the document). Add it to `HostToPageMessage` and to the host-message filter table
  (near `previewCopyTextResult: ownId` and `sourceScroll: render`) with the `render` identity rule
  and a bounded-string check on `text`; reuse the bound of `MAX_COPY_TEXT_TRANSPORT_LENGTH`
  (20 000 000 characters) from `src/core/protocol/pageToHost.ts` (export it, or move it to a shared
  constant of `src/core/protocol`). A message over the bound is refused by the filter like any
  malformed message.
- `src/session/features/rendering.ts`, `onReady`: when the page reports ready for a render whose
  stage is the session's current stage (`preview.stage.requestId === value.requestId`), post
  `previewSourceText` addressed to that render with `preview.stage.sourceText`. This covers both a
  full load and a content patch (a patched page also reports ready, see
  `armContentPatchFallback` in `src/session/features/pageDocument.ts`). Put the posting in a small
  method of the feature that owns it (for example `postSourceText(preview)` next to
  `postShowComments`), so `rendering.ts` stays under its size limit.
- `src/page/features/hostHandlers.ts` (or the page's host-message dispatch): keep the text with
  the render identity it came with. The page uses it only while its shown render has that identity;
  a content patch or a reload drops it until the next `previewSourceText`.

### 2.2 Core: the raw Markdown of a selection

New pure module `src/core/mapping/rawCopy.ts` (no DOM, no host API, under 800 lines; split into a
second file, for example `rawCopyBalance.ts`, if it grows). Suggested shape, the Driver may refine
the names:

```ts
/** One mapped element enclosing an edge, outermost first. */
export interface RawCopyFrame {
  line: number;        // 1-based first source line (data-sphinx-source-line)
  endLine: number;     // 1-based last source line (data-sphinx-source-end-line, else line)
  atomic: boolean;     // generated content or an included block: copied whole (section 3.6)
}
export interface RawCopyEdge {
  frames: readonly RawCopyFrame[];  // the enclosing mapped elements, outermost first
  text: string;                     // rendered text of the innermost non-atomic frame, chrome removed
  offset: number;                   // the edge's offset in `text`
}
export function rawMarkdownForSelection(source: string, start: RawCopyEdge, end: RawCopyEdge): string | undefined;
```

It resolves each edge to a source offset (3.2), slices the source between them, then balances the
slice at both ends (3.3 to 3.5). It returns `undefined` when an edge cannot be placed at all (no
frame, lines outside the source); the page then leaves the copy native.

The existing `mapRenderedCaret` of `src/page/modules/textEditing.ts` (SwRS-MDOKFSTUDIO-BLOCK-026)
already projects a block's source onto its rendered text (markers skipped, whitespace collapsed);
the new alignment starts from that projection, moved to `src/core` and generalized to map a
rendered offset to a source offset. When the projection moves, its `@implements_req
SwRS-MDOKFSTUDIO-BLOCK-026` marker moves with it and `textEditing.ts` calls the moved function.

### 2.3 Page: the copy handler

New module `src/page/features/rawCopy.ts`, installed from `src/page/runtime.ts` (next to
`installCodeCopy`). It listens to `copy` on the document and:

- leaves the event alone (native copy) in the cases of 3.1;
- builds the two `RawCopyEdge` from `window.getSelection()`'s first range: for each edge, the
  chain of enclosing elements carrying `data-sphinx-source-line` inside the content container
  (`#sphinx-myst-preview-content`), their `data-sphinx-source-end-line`, whether each is atomic
  (3.6), the rendered text of the innermost non-atomic one with chrome nodes skipped, and the
  edge's offset in that text (the same tree-walker counting as `editMode.ts` uses for a click);
- calls `rawMarkdownForSelection`; on a result, sets text/plain to it and text/html to the
  serialized `cloneContents()` of the range with chrome elements removed, then
  `event.preventDefault()`.

The chrome definition is shared with the HTML export: move the lists `REMOVED_CLASSES` and
`REMOVED_BY_ATTRIBUTE` (and the comment-attribute rule of `isChrome`) of
`src/core/export/exportContent.ts` into an exported core module (for example
`src/core/export/chromeMarks.ts`) that both `exportContent.ts` and `rawCopy.ts` use; buttons and
form controls (`REMOVED_TAGS`) are chrome too. The export's behaviour and its markers
(SwRS-MDOKFSTUDIO-TOOLBAR-137) do not change.

### 2.4 Glossary

`.agents/glossary/common.md`: add **Raw copy**: the copy of a native text selection of the page as
the raw Markdown under it (`src/page/features/rawCopy.ts`, `src/core/mapping/rawCopy.ts`); not the
block selection's copy, nor the code block's Copy button.

### 2.5 Not touched

The writing skill (`skills/writing-for-markdown-okf-schema-studio/`) is not touched: no rendered
syntax changes. The code block's Copy button (`src/page/modules/codeCopy.ts`) and the block
selection's copy, cut and paste keep their behaviour.

## 3. Behaviour

### 3.1 Where the raw copy applies (Q4)

The page takes over the copy event in read mode and in edit mode, for a non-empty selection whose
range touches the content container, except:

- the selection or the focused element is inside a text control: a `textarea`, a text-like
  `input`, an element with `contenteditable`, an open block editor
  (`[data-sphinx-preview-block-editor]`), the table cell editor, the frontmatter editor
  (`[data-okf-frontmatter-editor]`), a comment compose box, the find bar: the native copy runs;
- a block selection is active (`blockSelection.isActive()`): the block copy of BLOCK-166 owns the
  chord and the raw copy does nothing;
- the page has no source text for the render it shows (not yet received, or dropped by a patch):
  the native copy runs (no error, no message);
- the selection lies entirely in chrome (a thread popover, the toolbar): the native copy runs (see
  open question 2).

An edge outside the content container (a Ctrl+A that also covers the toolbar) is clamped to the
first or last content position.

### 3.2 Each edge maps to a character of the source (Q1)

- An edge inside the text of a non-atomic element maps to the source character under it: the
  rendered text of the innermost mapped element is aligned with the source text of that element's
  lines, with markup characters skipped (emphasis and strike markers, backticks, link brackets and
  targets, list and heading markers, blockquote prefixes, table pipes, escapes `\*`, entities
  `&amp;`) and whitespace runs collapsed.
- Inside a code block (fenced or a `{code-block}` directive), the rendered code is the source text
  of the fence's content lines, so the edge maps to that exact character.
- An edge in a container's opening line (for example an admonition's title) maps to the start of
  that line (start edge) or the end of it (end edge): the opening line is copied whole.
- When the alignment cannot place an edge in the element (the rendered text has no unique match in
  its source), the edge snaps to the boundary of that element: its first source character for the
  start edge, the end of its last line for the end edge (see open question 3).
- The copied text is the source between the two offsets, verbatim: everything between the edges
  (blank lines, HTML comments, link reference definitions, line breaks, CR LF or LF as in the
  document) comes along. The characters added by 3.3 to 3.5 use the document's line break.

### 3.3 Inline balancing (Q2)

When an edge falls strictly inside an inline construct, the slice is cut exactly at the edge and
the construct's delimiters on the other side are added, innermost nearest the text:

| Source | Selection | Copied |
| --- | --- | --- |
| `Hello **world** again` | from "r" of world to the end of the line | `**rld** again` |
| `Hello **world** again` | from the start to "o" of world (included) | `Hello **wo**` |
| `a [link **bold** text](https://x.test) b` | from "ld" to "te" (included) | `[**ld** te](https://x.test)` |
| `` use `npm ci` here `` | from "ci" to the end | `` `ci` here `` |
| ``{kbd}`Ctrl+C` to copy`` | from "C" of Ctrl to the end | ``{kbd}`trl+C` to copy`` |
| `~~old~~ and *new*` | from "l" of old to "n" of new (included) | `~~ld~~ and *n*` |

The constructs: emphasis and strong (`*`, `_`, `**`, `__`), strikethrough (`~~`), inline code (a
backtick run), links (`[`…`](target "title")`, and reference links `[`…`][ref]`), autolinks
(`<`…`>`), MyST roles (``{name}` `` … `` ` ``), inline math (`$`…`$`) and inline HTML elements
(the opening tag, the closing tag). A construct whose rendered text is not in the source (an
image, a footnote reference `[^1]`, a role whose text is computed such as `{ref}`, `{numref}`,
`{doc}`, a citation) is atomic: an edge inside it copies it whole (3.6).

### 3.4 Containers cut at an edge (Q1)

A container is any mapped element whose source has an opening and, for some, a closing: a MyST
directive or admonition in a backtick or colon fence (```` ```{note} ````, `:::{note}`, with its
option lines `:key: value` or its YAML options block), a code fence, a GitHub alert
(`> [!NOTE]`), a blockquote (`>`), a list and a list item, a table (3.5), a tab set or a card grid.

- Start edge inside a container that opens before it: the container's opening lines (the fence
  line and its option lines, verbatim; for an alert its `> [!TYPE]` line) are added before the
  slice, outermost first. A blockquote or alert gives its `> ` prefix(es) to the first, partial
  line of the slice; the later lines already carry theirs.
- End edge inside a container that closes after it: the container's closing line (the fence line
  at its last source line, verbatim) is added after the slice, innermost first. A blockquote, an
  alert and a list have no closing line.
- Nested containers are each handled: an admonition in an admonition gives both opening lines and
  both closing lines, each verbatim (so a four-colon outer fence stays four colons).
- A selection across several containers balances each end on its own: starting inside admonition A
  and ending inside admonition B adds A's opening before and B's closing after; A's closing and B's
  opening are already in the slice.
- A code fence inside a container cut at an edge is itself a container: starting inside the code
  adds the code fence's opening line after the container's opening lines.

### 3.5 Tables and lists (Q6, Q7)

- Table (Q6): an edge inside a table copies the rows it touches, whole, and the copy of that
  table's part always starts with the table's header row and its delimiter row. Both edges in one
  table: header, delimiter, then the rows from the start row to the end row. Start edge in the
  header row: from the header row. A table inside an admonition cut at the start: the admonition's
  opening lines, then header, delimiter and the touched rows.
- List (Q7): the innermost list item enclosing the start edge keeps its marker (`-`, `*`, `+`, or
  its own number `3.` / `3)`, with its task box `[ ]` / `[x]` when it has one), brought to column 0;
  the text that follows the marker is what the other rules give (the cut text, or the opening lines
  of an inner container). Every later copied line loses the same indentation as that item's marker
  (clamped at column 0), so the next items keep their relative indentation. The enclosing outer
  items give nothing. Example, selecting from "rld" of the sub-item to the end of the list:

  Source:

  ```markdown
  - parent
    - child **world**
    - sibling
  - next
  ```

  Copied:

  ```markdown
  - **rld**
  - sibling
  - next
  ```

  (`- sibling` moves from column 2 to 0, `- next` stays at 0, clamped.)

- An admonition inside a list item cut at the start: the item's marker at column 0, then the
  admonition's opening line on the marker line, then its content indented by the marker's width.

### 3.6 Generated content and included blocks (Q5)

An atomic element is copied whole, as the source lines of its mapped range, whichever part of it
the selection touches; an edge inside it moves to its first line (start edge) or the end of its
last line (end edge):

- a rendered Mermaid diagram (`.myst-mermaid-diagram`), PlantUML diagram
  (`.myst-plantuml-diagram`), chart (`.myst-vega-diagram`): its fence or directive;
- a generated table of contents: its directive;
- the frontmatter properties table (`[data-okf-properties]`): the frontmatter block, its `---`
  delimiter lines included;
- display math, an image or a figure: its source construct;
- a block that comes from an included file (`rt.blocks.isIncludedBlock`, whose lines are mapped to
  the `{include}` directive, see `setIncludedSourceLine` in `src/core/render/mystRenderer.ts`): the
  `{include}` directive of the active document (the source that produces it in this document);
- the inline atomic constructs of 3.3: the whole construct.

### 3.7 Clipboard formats and chrome (Q3, Q5)

- text/plain: the raw Markdown of 3.2 to 3.6, with no chrome text (comment chips and thread text,
  buttons, the code Copy button, insert points and their bars, row and column handles, fold
  toggles, line numbers, toolbars, the find bar, the selection status).
- text/html: the rendered HTML of the selection's range, with the same chrome elements removed.
- A whole-document selection (Ctrl+A or Cmd+A, then copy) copies the document's source from its
  first character to the end of its last rendered block: with a frontmatter and a body ending in a
  paragraph, exactly the source text without its final line break.

## 4. Requirements (okfreq)

Rules: `requirements/guidelines/project.guidelines.md`
("During a change") and the okfreq baseline it links to; run okfreq as
`uv run --no-sync --group requirements okfreq`.

- New StRS in scope `block-editing` (token BLOCK), created with `okfreq new … --lifecycle
  proposed`: "A reader copies a selection as the exact Markdown under it". User need, in the
  owner's terms: from the point under the selection's start to the point under its end, the raw
  text with its formatting. Optional `### Main paths`: one path (select, copy, paste into a
  Markdown editor gives the source).
- New SwRS, `proposed`, each deriving from that StRS, one per rule (the Driver may merge two only
  when one test file proves both):
  1. The host sends the shown render's source text to the page on every page ready
     (`previewSourceText`); the page keeps it for that render only.
  2. Scope: read and edit mode; native copy in text controls, with a block selection, without
     source text, or for a selection only in chrome (3.1).
  3. Character-precise cut: each edge maps to the source character under it; code blocks exactly;
     opening-line edges; the alignment fallback (3.2).
  4. Inline balancing (3.3).
  5. Container fences, nested and across containers, code fences inside containers (3.4).
  6. Table header and delimiter rows with whole touched rows (3.5).
  7. List item marker at level 0 and relative indentation (3.5).
  8. Generated content and included blocks give their source (3.6).
  9. UI chrome is never copied (3.7).
  10. Clipboard formats: text/plain Markdown, text/html rendered (3.7).
- Changed SwRS: `SwRS-MDOKFSTUDIO-BLOCK-166` (`proposed`, not approved): its refusal row "Copy, cut
  or paste chord in reading mode (edit mode off, a selection left over) | The page does nothing and
  the browser copies" now says the block-copy handler does nothing and the copy event goes to the
  raw copy (new SwRS 2). The statement and the other rows do not change. `SwRS-MDOKFSTUDIO-BLOCK-026`
  (`mapRenderedCaret`) changes only if its implementation moves: the marker moves, the behaviour
  and its tests stay.
- Approved requirements changed: none. The change touches no `approved` requirement (checked: none
  of the 15 approved StRS covers copying a native selection); the owner's agreement is therefore
  not needed. If the Driver finds one it would alter, it stops and asks.
- Markers: `@implements_req` at the code point of each rule (`rawCopy.ts` functions, the page
  handler, the session posting, the filter rule), `@tests_req` at each test; at most 3 IDs per
  marker block (`just check-markers`).
- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` under
  `## 2026-11-24` (or the day of the change), topic in a `### Raw copy of a selection` sub-heading.

## 5. Out of scope

- Cut (Ctrl+X) of a native selection and any edit made from a native selection.
- A change to the block selection's copy, cut and paste (BLOCK-166, -169, -174) or to the code
  block's Copy button.
- Copy from the side-by-side diff view's old side, the export, or any page other than the Studio
  preview page.
- Rewriting the copied Markdown (no normalization of markers, no reflow, no conversion of relative
  links or image paths).
- A new setting to turn the raw copy off.
- The writing skill (no rendered syntax change).

## Evidence

No host and default matrix: the change depends on neither a chantier host nor a shipped default
versus a configured value. The copy path differs between the simulated page (Chromium, a
constructed `ClipboardEvent`) and a real VS Code window (VS Code's own copy command on the
webview); E3 and E4 prove each.

### E1. Static and unit gates

- `just check` passes (formatting, TypeScript, import boundaries: `src/page` and `src/session` may
  import the new core modules, `src/core` imports no layer above it; file size; unused exports;
  markers; unit and contract tests).
- `just requirements-lint` and `just requirements-update` pass with the new StRS and SwRS, every
  new SwRS with a source marker and a test marker.
- `just preflight` passes (on Windows the static stage; CI runs the others), constitution section 4.

### E2. Core unit tests: `test/core/mapping/rawCopy.test.ts`

Each case is a source text, two edges (frames, rendered text, offset) and the exact expected
string; the source texts are written in the test, the frames are the line ranges the real renderer
gives (checked once against the renderer's output in E3). Cases, at least:

- the rows of the 3.3 table (inline balancing, including bold inside a link cut on both sides);
- a thematic break `---` and a table in the middle of a selection copied verbatim (the owner's
  examples);
- an admonition in an admonition (colon fences of 4 and 3 colons), the start in the inner one and
  the end after both; the start before both and the end in the inner one;
- a list inside an admonition, the start in the second item: the admonition's opening, `- ` at
  column 0, the closing fence after;
- an admonition inside a list item, the start in the admonition's paragraph (3.5 last bullet);
- a selection starting at each nesting level of an admonition > list > admonition and ending at
  each level (a small grid: start level 0 to 3 by end level 0 to 3 that the test loops over);
- a code fence inside an admonition, the start in the code: admonition opening, code fence
  opening, the code from the edge, closings when the end is inside;
- a table inside an admonition, both edges in the table (header, delimiter, touched rows, closing
  fence);
- a table with the start in the header row, and with the end in the last row;
- the nested-list example of 3.5, an ordered list keeping its own number, a task item keeping
  `[x]`;
- a selection from inside admonition A to inside admonition B (two containers);
- a GitHub alert and a blockquote cut at the start (`> [!NOTE]` and `> ` prefixes);
- an edge in an admonition's title (opening line copied whole);
- atomic frames: a Mermaid fence, the frontmatter, a `{toc}`-like directive, an `{include}`
  directive, an image and a `{ref}` role, each with an edge inside;
- an alignment that cannot be placed (the rendered text absent from the source): the edge snaps
  to the element's boundary;
- a CR LF document: the slice keeps CR LF and the added fence lines use CR LF;
- a whole-document selection of a document with frontmatter, admonitions, a table, a list, code
  and a Mermaid fence returns the source exactly (without its final line break).

### E3. Real browser: `test/visual/capture_raw_copy.py`

A capture check in the Playwright harness (registered in `test/visual/capture.py` like
`check_table_grid_paste`, its scenario in a new `test/visual/rawCopyScenarios.ts` with a
`rawCopyChecks` flag), on a new fixture `test/visual/fixtures/<next number>-raw-copy.md` that holds
the constructs of E2 (nested admonitions with a list and a code fence, a table in an admonition, a
nested list, bold inside a link, a thematic break, a Mermaid fence, a frontmatter). The fixture is
rendered by the real pipeline (`renderFixtures`), the page runs the shipped page bundle, and the
check:

- posts `previewSourceText` with the fixture's text read from the repository file, as the host
  does;
- for each case, sets the selection with a DOM `Range` on the rendered text (the start and end
  characters named in the case), dispatches
  `new ClipboardEvent('copy', { clipboardData: new DataTransfer(), bubbles: true, cancelable: true })`
  on the selection's container, and asserts `defaultPrevented`, the exact text/plain, and that
  text/html holds the rendered element (for example `<strong>`) and no chrome (no
  `data-okf-comment`, no `button`);
- covers, at least: `**rld**`, the nested admonition with a list started in the list, a table row
  inside an admonition, the nested list example, a selection across two admonitions, an edge
  inside the Mermaid diagram, a selection over the properties table, and Ctrl+A over the whole
  page returning the fixture's text (without its final line break);
- covers the native cases: a selection inside an open block editor's textarea and in a field: the
  event is not prevented; no `previewSourceText` posted: not prevented.

### E4. Real VS Code window: `test/integration/realInput/rawCopy.ts`

A real-input scenario registered in `test/integration/realInput/run.ts`, like
`scenarioCutCopyListBeforeBlankLines` in `blockKeys.ts`: it opens a fixture in Studio, saves the
clipboard and writes a sentinel, selects text in the webview frame (a Range from "r" of a bold word
to the end of a table row inside an admonition), presses the platform copy chord as real input, and
waits until `vscode.env.clipboard.readText()` holds the expected raw Markdown; then the same in edit
mode; then a selection inside an open block editor copies the textarea's text natively; the
clipboard is restored at the end. It runs in `just ci-integration` (a push to `main`, or
`gh workflow run ci.yml --ref <branch> -f heavy=true` on the branch, which the Driver runs before
asking for a merge).

### E5. Session and page wiring

- `test/session/`: on `previewReady` for the current stage the host posts `previewSourceText` with
  the stage's source text, addressed to that render; for an older render it posts nothing.
- `test/core/protocol/`: the host-message filter accepts `previewSourceText` with a bounded string
  and refuses one without `text` or over the bound.
- `test/page/runtimeRawCopy.test.ts` (the node:vm harness of `runtimeHarness.ts`), where the fake
  DOM allows it: the page keeps the source text only for its shown render and drops it on a content
  patch; with a block selection active the copy event is not taken. What the fake DOM cannot hold
  (a real Selection) is proved in E3.
- Each test that checks a rule carries its `@tests_req`; one test per constitution section 3 fails
  on the previous code (today no handler: every E3 case fails before the change).

### E6. Pull request

The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and
`.agents/guidelines/pull-request.guidelines.md`:
the Tests section lists the new and changed requirement IDs with their source and test files, a
short before/after of a copied table and admonition, the CHANGELOG line. Commit scope per
`git-commit-allowed-scopes.md` (`feat(vscode)` or `feat(render)`).

## Open questions

1. A heading cut at the start: the slice starts inside `## Hello` at "llo". Written against: keep
   the heading marker, `## llo`, like the list marker of Q7. The other option: `llo` alone.
2. A selection that lies entirely in UI chrome (the text of a comment thread popover, the
   toolbar): written against "the native copy runs" (the user can still copy a comment's text).
   The other option: nothing is copied.
3. An edge the alignment cannot place (rendered text with no unique match in its element's
   source): written against "the edge snaps to the whole element" (the copy stays well formed but
   loses character precision there). The other option: fall back to the native copy for the whole
   selection.
