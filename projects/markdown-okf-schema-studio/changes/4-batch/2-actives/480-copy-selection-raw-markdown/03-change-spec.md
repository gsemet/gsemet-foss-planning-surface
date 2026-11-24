# Copy a selection as the exact raw Markdown under it

Short name: `copy-raw`. No tracker issue (origin: the owner, verbal, 2026-11-23). Destination:
the running batch, batch-09. This CR is the lower of two stacked CRs (copy-raw-Q17): it copies the
raw cut verbatim; the stacked CR `copy-raw-edge-balancing` (short name `copy-edges`, specified
apart) balances the cut's edges through the seam `balanceRawCut` named in section 2.3.

## Goal

The owner, 2026-11-23: "quand je sélectionne du texte ça copie pas exactement le texte dessous
(par exemple les triple tirets ou des tables etc). Le but c'est que du point de départ au point en
dessous le texte brut y compris le formatage est conservé."

When a writer selects text in Studio with the mouse or the keyboard and presses the platform copy
chord (Ctrl+C, Cmd+C on macOS), the clipboard's plain text holds the raw Markdown source from the
character under the selection's start to the character under its end, verbatim: thematic breaks,
tables, emphasis, links, directives and fences come along as they are written. Generated content
gives the source that produces it; the page's UI chrome is never copied. The clipboard's HTML
keeps the rendered selection, so pasting into a rich editor still gives formatted text.

In this CR the cut is exact and not repaired: a selection starting at "r" of `**world**` copies
`rld**`. Making a cut edge well formed again (`**rld**`, the container's fence, the table's
header, the list level, the heading marker, snapping an edge that cannot be placed) is the stacked
CR `copy-raw-edge-balancing`.

Today the page has no copy handler for a native selection: the browser copies the rendered text
(a table becomes tab-separated cells, `---` disappears, `**bold**` becomes `bold`). Only the edit
mode's block selection (Shift+click, whole blocks, SwRS-MDOKFSTUDIO-BLOCK-166) copies source lines,
through the host.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| Q1 | Character-precise. The added opening and closing characters go to `copy-raw-edge-balancing` (Q17). | 3.2; seam 2.3 |
| Q2 | Inline balancing: goes to `copy-raw-edge-balancing` (Q17). Here the inline cut is copied unbalanced. | seam 2.3, 3.2 |
| Q3 | text/plain carries the raw Markdown, text/html the rendered HTML. | 3.6 |
| Q4 | Everywhere in the page, read and edit mode, except inside a text input or a field being edited, which keeps the native copy. | 3.1 |
| Q5 | Generated content copies the source that produces it (a Mermaid diagram its fence, a generated table of contents its directive or marker, the frontmatter properties table its YAML); UI chrome (comment bubbles, buttons, line numbers, toolbars) is never copied. | 3.4, 3.6 |
| Q6, Q7, Q11, Q13, Q16 | Table header, list level, heading marker, snapping an unplaceable edge, list indentation: go to `copy-raw-edge-balancing` (Q17). | seam 2.3 |
| Q8 | Not grilled enough then; Q9 was the point left. | - |
| Q9 | okfreq requirements (one StRS, one SwRS per rule) and edge tests. This CR keeps the SwRS of its own rules (section 4) and the edge tests that need no balancing: nested containers copied whole, a selection across containers, the whole-document round trip; the balancing tests go to the stacked CR (Q17). | 4, E2, E3 |
| Q10 | Specified for the running batch, batch-09. | - |
| Q12 | A selection lying entirely in UI chrome: the native copy, as today. | 3.1 |
| Q14 | Ctrl+A (Cmd+A) then copy: the whole source exactly, trailing definitions, comments and the final line break included. | 3.5 |
| Q15 | Side by side, a selection touching an old-side card: the current source only; the old card's text is skipped; the native copy when an edge lies in an old card. | 3.1, 3.2, 3.6 |
| Q17 | Split into two stacked CRs in batch-09: this one (verbatim raw copy), and `copy-raw-edge-balancing` stacked on it. | whole spec; seam 2.3 |
| 18 (routine F4-F7) | F4: BLOCK-166 row and StRS-016 line reworded to the block-copy handler only. F5: E2 frames built from the real core renderer's output (tab items carry no source line). F6: the context menu's Copy is not claimed; text/html proved in Chromium only. F7: the table of contents source is `{contents}` or the bracket marker. | 4, E2, E4, 3.4 |

## 1. How it works (design)

The browser's copy event is synchronous: `event.clipboardData.setData` must run inside the handler,
and the host's clipboard (`HostUi.writeClipboard`, `vscode.env.clipboard.writeText`) only writes
plain text, so it cannot carry the text/html that Q3 asks for. The page therefore computes the
Markdown itself, at copy time, from the source text of the render it shows:

1. The host sends the page the source text of the render the page shows (new message
   `previewSourceText`, section 2.1).
2. On a `copy` event, the page reads the selection's two edges from the DOM (the mapped elements
   enclosing each edge, outermost first, the rendered text of the innermost non-atomic one and the
   edge's offset in it) and calls the pure function `rawMarkdownForSelection` of `src/core` with
   the source text and the two edges.
3. That function resolves each edge to a source offset (3.2, 3.4, 3.5), then hands the two
   resolved edges to the seam `balanceRawCut` (2.3), which in this CR returns the verbatim slice.
4. On a result, the page sets it as text/plain, sets the rendered HTML of the selection (chrome
   removed) as text/html, and prevents the default copy. On `undefined`, the copy stays native.

No host round trip happens at copy time; the block selection's copy (BLOCK-166) keeps its own host
path unchanged.

## 2. What changes, area by area

### 2.1 Protocol: the source text of the shown render

- `src/core/protocol/hostToPage.ts`: a new message
  `PreviewSourceTextMessage extends RenderMessage<"previewSourceText">` with one field
  `text: string`, the full text of the active document of that render (frontmatter included, line
  breaks as in the document). Add it to `HostToPageMessage` and to the host-message filter table
  (near `previewCopyTextResult` and `sourceScroll`) with the `render` identity rule and a
  bounded-string check on `text`. Reuse the bound `MAX_COPY_TEXT_TRANSPORT_LENGTH` (20 000 000
  characters, today a private constant at `src/core/protocol/pageToHost.ts:62`): export it, or
  move it to a shared constant of `src/core/protocol`. A message over the bound is refused by the
  filter like any malformed message.
- `src/session/features/rendering.ts`, `onReady` (line 557): when the page reports ready for a
  render whose stage is the session's current stage (`preview.stage.requestId ===
  value.requestId`), post `previewSourceText` addressed to that render with
  `preview.stage.sourceText`. This covers a full load and a content patch (a patched page also
  reports ready, see `armContentPatchFallback` in `src/session/features/pageDocument.ts`). Put the
  posting in a small method of the feature that owns it (for example `postSourceText(preview)` next
  to `postShowComments`, called at line 593), so `rendering.ts` stays under its size limit.
- `src/page/features/hostHandlers.ts` (or the page's host-message dispatch): keep the text with
  the render identity it came with. The page uses it only while its shown render has that identity;
  a content patch or a reload drops it until the next `previewSourceText`.

### 2.2 Core: resolving the selection's edges

New pure module `src/core/mapping/rawCopy.ts` (no DOM, no host API, under the file size limit).
Suggested shape; the Driver may refine names but keeps the seam of 2.3:

```ts
/** One mapped element enclosing an edge, outermost first. */
export interface RawCopyFrame {
  line: number;        // 1-based first source line (data-sphinx-source-line)
  endLine: number;     // 1-based last source line (data-sphinx-source-end-line, else line)
  atomic: boolean;     // generated content or an included block: copied whole (3.4)
}
export interface RawCopyEdge {
  frames: readonly RawCopyFrame[];  // enclosing mapped elements, outermost first; empty when clamped
  clamp?: "start" | "end";          // the edge lies before the first / after the last mapped element (3.5)
  text: string;                     // rendered text of the innermost non-atomic frame, chrome removed
  offset: number;                   // the edge's offset in `text`
}
export function rawMarkdownForSelection(source: string, start: RawCopyEdge, end: RawCopyEdge): string | undefined;
```

It resolves each edge to a `ResolvedRawEdge` (2.3) by the rules of 3.2, 3.4 and 3.5, then returns
`balanceRawCut(...)`. Line ranges become offsets with the existing `sourceRangeForLines` of
`src/core/mapping/sourceMapping.ts`.

The existing `mapRenderedCaret` of `src/page/modules/textEditing.ts` (line 203,
SwRS-MDOKFSTUDIO-BLOCK-026) already projects a block's source onto its rendered text (markers
skipped, whitespace collapsed); the new alignment starts from that projection, moved to `src/core`
and generalized to map a rendered offset to a source offset. When the projection moves, its
`@implements_req SwRS-MDOKFSTUDIO-BLOCK-026` marker moves with it and `textEditing.ts` (and its
caller `src/page/features/textControls.ts:288`) call the moved function; the behaviour and the
tests of BLOCK-026 do not change.

### 2.3 The seam the stacked CR fills: `balanceRawCut`

New pure module `src/core/mapping/rawCopyEdges.ts`, holding one exported function and its types:

```ts
export interface ResolvedRawFrame extends RawCopyFrame {
  start: number;  // source offset of the frame's first line
  end: number;    // source offset of the end of the frame's last line (before its line break)
}
export type ResolvedRawEdge =
  | { kind: "placed"; offset: number; frames: readonly ResolvedRawFrame[] }
  | { kind: "unplaced"; frames: readonly ResolvedRawFrame[] };
export interface RawCut {
  source: string;
  lineBreak: "\n" | "\r\n";   // the document's line break (the first one found, else "\n")
  start: ResolvedRawEdge;
  end: ResolvedRawEdge;
}
/** The Markdown copied for a resolved cut; undefined leaves the copy native. */
export function balanceRawCut(cut: RawCut): string | undefined;
```

In this CR `balanceRawCut` returns `undefined` when either edge is `unplaced` or when the start
offset is after the end offset, and otherwise `cut.source.slice(start.offset, end.offset)`,
verbatim, with nothing added. Its doc comment names the stacked CR: "the edges are balanced by
copy-raw-edge-balancing". The stacked CR replaces the body of this function (and may add modules
it calls); it does not change `rawMarkdownForSelection`, the page handler or the protocol. The
frames carry everything balancing needs (each enclosing element's line range and source offsets,
outermost first), so the stacked CR reads no more DOM.

The seam's unit tests (E2, "seam cases") pin the unbalanced output on purpose; the stacked CR
changes their expected values.

### 2.4 Page: the copy handler

New module `src/page/features/rawCopy.ts`, installed from `src/page/runtime.ts` (next to
`installCodeCopy`, line 211). It listens to `copy` on the document and:

- leaves the event alone (native copy) in the cases of 3.1;
- builds the two `RawCopyEdge` from `window.getSelection()`'s first range: for each edge, the chain
  of enclosing elements carrying `data-sphinx-source-line` inside the content container
  (`#sphinx-myst-preview-content`), their `data-sphinx-source-end-line`, whether each is atomic
  (3.4), the rendered text of the innermost non-atomic one with chrome nodes skipped, and the
  edge's offset in that text (the same tree-walker counting as `editMode.ts` uses for a click); an
  edge with no mapped element before it (start) or after it (end) in the content gets `clamp`
  (3.5);
- for an edge in a side-by-side card (3.2, Q15), resolves it as 3.2 says or leaves the copy native;
- calls `rawMarkdownForSelection`; on a string, sets text/plain to it and text/html to the
  serialized `cloneContents()` of the range with chrome elements and old-side card content removed
  (3.6), then `event.preventDefault()`.

The chrome definition is shared with the HTML export: move `REMOVED_TAGS`, `REMOVED_CLASSES`,
`REMOVED_BY_ATTRIBUTE` and the rule of `isChrome` of `src/core/export/exportContent.ts` (lines
26-138) into an exported core module (for example `src/core/export/chromeMarks.ts`) that both
`exportContent.ts` and `src/page/features/rawCopy.ts` use. The export's behaviour and its markers
(SwRS-MDOKFSTUDIO-TOOLBAR-137) do not change.

The handler listens to the `copy` event itself, whatever fires it; this CR claims and proves only
the keyboard chord (F6): the context menu's Copy is not claimed.

### 2.5 Glossary

`.agents/glossary/common.md`: add **Raw copy**: the copy of a native text selection of the page as
the raw Markdown under it (`src/page/features/rawCopy.ts`, `src/core/mapping/rawCopy.ts`); not the
block selection's copy, nor the code block's Copy button.

### 2.6 Not touched

The writing skill (`skills/writing-for-markdown-okf-schema-studio/`): no rendered syntax changes.
The code block's Copy button (`src/page/modules/codeCopy.ts`) and the block selection's copy, cut
and paste keep their behaviour.

## 3. Behaviour

### 3.1 Where the raw copy applies (Q4, Q12, Q15)

The page takes over the copy event in read mode and in edit mode, for a non-empty selection whose
range touches the content container, except in these cases, where the native copy runs:

- the selection or the focused element is inside a text control: a `textarea`, a text-like
  `input`, an element with `contenteditable`, an open block editor
  (`[data-sphinx-preview-block-editor]`), the table cell editor, the frontmatter editor
  (`[data-okf-frontmatter-editor]`), a comment compose box, the find bar;
- a block selection is active (`blockSelection.isActive()`): the block copy of BLOCK-166 owns the
  chord and the raw copy does nothing;
- the page has no source text for the render it shows (not yet received, or dropped by a patch):
  no error, no message;
- the selection lies entirely in UI chrome (a thread popover, the toolbar), Q12;
- side by side, an edge lies in an old-side card (`[data-okf-sbs-side="base"]` inside
  `[data-okf-sbs-card]`), Q15;
- `rawMarkdownForSelection` returns `undefined` (an edge that cannot be placed, 3.2).

### 3.2 Each edge maps to a character of the source (Q1)

- An edge inside the text of a non-atomic element maps to the source character under it: the
  rendered text of the innermost mapped element is aligned with the source text of that element's
  lines, with markup characters skipped (emphasis and strike markers, backticks, link brackets and
  targets, list and heading markers, blockquote prefixes, table pipes, escapes `\*`, entities
  `&amp;`) and whitespace runs collapsed.
- Inside a code block (fenced or a `{code-block}` directive), the rendered code is the source text
  of the fence's content lines, so the edge maps to that exact character.
- An edge in a container's opening line (for example an admonition's title, written or the default
  "Note") maps to the start of that line (start edge) or the end of it (end edge).
- A block under a tab item carries no source line of its own (`src/core/render/mystNode.ts:90-97`,
  `src/core/render/mystGridToctree.ts:491`): its innermost frame is the nearest enclosing element
  that has one, and the alignment runs against that element's whole line range.
- Side by side (Q15), an edge in the current side of a card (`[data-okf-sbs-side="current"]`) is
  resolved through the page block that card side copies (the card's blocks are copies stripped of
  their source attributes; the shown original carries `data-okf-sbs-replaced`, see
  `src/page/modules/sideBySide.ts`): same child order, same rendered text. When it cannot be
  resolved so, the edge is unplaced.
- When the alignment cannot place an edge (the rendered text has no unique match in its element's
  source), the edge is `unplaced`. In this CR an unplaced edge leaves the whole copy native; the
  stacked CR snaps it to its element (Q13).
- The copied text is the source between the two offsets, verbatim: everything between the edges
  (blank lines, HTML comments, link reference definitions, other containers' fences, line breaks
  CR LF or LF as in the document) comes along, and nothing is added at either edge.

Examples of the verbatim cut (the seam cases of E2; the stacked CR changes these outputs):

| Source | Selection | Copied in this CR |
| --- | --- | --- |
| `Hello **world** again` | from "r" of world to the end of the line | `rld** again` |
| `## Hello` | from "llo" to the end | `llo` |
| two colon-fenced admonitions A then B | from A's paragraph to B's paragraph | from the edge in A, A's closing fence, the lines between, B's opening fence, to the edge in B |

### 3.3 Nested and adjacent containers copied whole

A selection that starts before a container's opening line and ends after its closing line copies
the container verbatim, whatever it nests: an admonition in an admonition (a four-colon outer fence
stays four colons), a list inside an admonition, an admonition inside a list item, a code fence or
a table inside an admonition, a tab set. A selection across several containers copies every fence
between its edges as written (3.2's last example).

### 3.4 Generated content and included blocks (Q5)

An atomic element is copied whole, as the source lines of its mapped range, whichever part of it
the selection touches: an edge inside it moves to its first line's start (start edge) or the end of
its last line (end edge). This is part of the mapping, not of balancing.

- a rendered Mermaid diagram (`.myst-mermaid-diagram`), PlantUML diagram
  (`.myst-plantuml-diagram`), chart (`.myst-vega-diagram`): its fence or directive;
- a generated table of contents: its `{contents}` directive, or its bracket marker paragraph
  (`[TOC]`, `[[_TOC_]]`), see `expandTocMarkers` in `src/core/render/mystToc.ts:164-169` (F7);
- the frontmatter properties table (`[data-okf-properties]`): the frontmatter block, its `---`
  delimiter lines included;
- display math, an image or a figure: its source construct;
- a block that comes from an included file (`data-sphinx-preview-included`, whose lines are mapped
  to the `{include}` directive, see `setIncludedSourceLine` in `src/core/render/mystRenderer.ts`):
  the `{include}` directive of the active document;
- an inline construct whose rendered text is not in the source (an image, a footnote reference
  `[^1]`, a role whose text is computed such as `{ref}`, `{numref}`, `{doc}`, a citation): the whole
  construct.

### 3.5 The whole document (Q14)

A start edge with no mapped element before it in the content (for example the range of Ctrl+A or
Cmd+A, which starts before the content container) resolves to offset 0; an end edge with no mapped
element after it resolves to the source's length. So Ctrl+A then copy copies the whole source
exactly: the frontmatter, trailing link definitions and comments, and the final line break
included.

### 3.6 Clipboard formats and chrome (Q3, Q5, Q15)

- text/plain: the raw Markdown of 3.2 to 3.5. It never holds chrome text (comment chips and thread
  text, buttons, the code Copy button, insert points and their bars, row and column handles, fold
  toggles, line numbers, toolbars, the find bar, the selection status) nor an old-side card's text:
  it is cut from the source, which holds none of them.
- text/html: the rendered HTML of the selection's range, with the same chrome elements and the
  old-side card content (`[data-okf-sbs-side="base"]`) removed.

## 4. Requirements (okfreq)

Rules: `requirements/guidelines/project.guidelines.md` ("During a change") and the okfreq baseline
it links to; run okfreq as `uv run --no-sync --group requirements okfreq`.

- New StRS in scope `block-editing` (token BLOCK), created with `okfreq new … --lifecycle
  proposed`: "A reader copies a selection as the exact Markdown under it". User need, in the
  owner's terms: from the point under the selection's start to the point under its end, the raw
  text with its formatting. Optional `### Main paths`: one path (select, copy, paste into a
  Markdown editor gives the source). The stacked CR adds its balancing SwRS under this StRS.
- New SwRS, `proposed`, each deriving from that StRS, one per rule (the Driver may merge two only
  when one test file proves both):
  1. The host sends the shown render's source text to the page on every page ready
     (`previewSourceText`); the page keeps it for that render only (2.1).
  2. Scope: read and edit mode; native copy in text controls, with a block selection, without
     source text, for a selection only in chrome, with an edge in an old-side card, or when an
     edge cannot be placed (3.1).
  3. Character-precise verbatim cut: each edge maps to the source character under it; code blocks
     exactly; opening-line edges; tab items; the current side of a card; nothing added at the
     edges (3.2, 3.3).
  4. Generated content and included blocks give their source (3.4).
  5. The whole document: Ctrl+A then copy gives the whole source exactly (3.5).
  6. UI chrome and old-side card text are never copied (3.6).
  7. Clipboard formats: text/plain Markdown, text/html rendered (3.6).
- Changed requirements, both `proposed` (F4):
  - `SwRS-MDOKFSTUDIO-BLOCK-166`, the refusal row at line 77, "Copy, cut or paste chord in reading
    mode (edit mode off, a selection left over) | The page does nothing and the browser copies":
    reworded to the block-copy handler only, for example "| The block-copy handler does nothing;
    a copy goes to the raw copy (<new SwRS 2>)". The statement and the other rows do not change.
  - `StRS-MDOKFSTUDIO-BLOCK-016`, line 59, "The clipboard keys stay native in a text box, a field,
    the properties table and in reading mode.": reworded to the block selection's handler only,
    for example "The block selection does not take the clipboard keys in a text box, a field, the
    properties table or in reading mode (a native selection is copied by the raw copy, <new
    StRS>)."
  - `SwRS-MDOKFSTUDIO-BLOCK-026` (`mapRenderedCaret`) changes only if its implementation moves: the
    marker moves, the behaviour and its tests stay.
- Approved requirements changed: none (checked: none of the approved StRS covers copying a native
  selection, and both changed requirements are `proposed`); the owner's agreement is therefore not
  needed. If the Driver finds an approved one it would alter, it stops and asks.
- Markers: `@implements_req` at the code point of each rule (`rawCopy.ts` functions, `balanceRawCut`
  for SwRS 3, the page handler, the session posting, the filter rule), `@tests_req` at each test;
  at most 3 IDs per marker block (`just check-markers`).
- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` under
  `## 2026-11-24` (or the day of the change), topic in a `### Raw copy of a selection` sub-heading.

## 5. Out of scope

- Everything of the stacked CR `copy-raw-edge-balancing`: inline closing and opening markers,
  container fences added at a cut edge, table header and delimiter rows, list level and
  indentation, heading marker, snapping an unplaceable edge; and their tests.
- Cut (Ctrl+X) of a native selection and any edit made from a native selection.
- A change to the block selection's copy, cut and paste (BLOCK-166, -169, -174) or to the code
  block's Copy button.
- The context menu's Copy as a claimed path (F6), the export, and any page other than the Studio
  preview page.
- Rewriting the copied Markdown (no normalization of markers, no reflow, no conversion of relative
  links or image paths).
- A new setting to turn the raw copy off.
- The writing skill (no rendered syntax change).

## Evidence

No host and default matrix: the change depends on neither a chantier host nor a shipped default
versus a configured value. The copy path differs between the simulated page (Chromium, a
constructed `ClipboardEvent`) and a real VS Code window (VS Code's copy on the webview); E3 and E4
prove each. text/html is proved in Chromium only (E3): the VS Code clipboard API of E4 reads plain
text only (F6).

### E1. Static and unit gates

- `just check` passes (formatting, TypeScript, import boundaries: `src/page` and `src/session` may
  import the new core modules, `src/core` imports no layer above it; file size; unused exports;
  markers; unit and contract tests).
- `just requirements-lint` and `just requirements-update` pass with the new StRS and SwRS, every
  new SwRS with a source marker and a test marker.
- `just preflight` passes (on Windows the static stage; CI runs the others), constitution
  section 4.

### E2. Core unit tests: `test/core/mapping/rawCopy.test.ts`

Each case is a source text written in the test, two edges and the exact expected string. The
frames are not written by hand (F5): a test helper (for example `test/core/mapping/rawCopyFrames.ts`)
renders the source through the real core pipeline (`renderMyst` of
`src/core/render/mystRenderer.ts`, then the sanitizer that writes `data-sphinx-source-line`, as the
page receives it), parses the HTML with `parse5`, finds the element holding the named rendered
text, and builds the `RawCopyEdge` from its mapped ancestors, the same way the page handler does.
So a block under a tab item (no source line) gets the frames the page would see. Cases, at least:

- a thematic break `---` and a table in the middle of a selection, copied verbatim (the owner's
  examples);
- nested containers copied whole (3.3): an admonition in an admonition (colon fences of 4 and 3
  colons) holding a list and a code fence, selected from before the outer opening to after the
  outer closing; a table inside an admonition; an admonition inside a list item; a tab set with a
  block inside a tab item;
- edges inside a code block inside an admonition: the exact code characters;
- an edge in an admonition's title (written, and the default title): the opening line's start or
  end;
- an edge inside a tab item's block (its frame is the tab set);
- atomic frames, each with an edge inside: a Mermaid fence, the frontmatter, a `{contents}`
  directive, a `[TOC]` marker, an `{include}` directive, an image, a `{ref}` role;
- an alignment that cannot be placed (the rendered text absent from the element's source):
  `undefined`;
- a CR LF document: the slice keeps CR LF;
- the whole document (3.5): clamped edges on a document with frontmatter, admonitions, a table, a
  list, code, a Mermaid fence, a trailing link definition, a trailing comment and a final line
  break return the source exactly;
- seam cases on `balanceRawCut` (2.3), pinned unbalanced: the three rows of 3.2's table; an
  unplaced edge gives `undefined`; a start after the end gives `undefined`.

### E3. Real browser: `test/visual/capture_raw_copy.py`

A capture check in the Playwright harness (registered in `test/visual/capture.py` like
`check_table_grid_paste`, its scenario in a new `test/visual/rawCopyScenarios.ts` with a
`rawCopyChecks` flag), on a new fixture `test/visual/fixtures/97-raw-copy.md` (or the next free
number) holding nested admonitions with a list and a code fence, a table in an admonition, a
nested list, bold inside a link, a thematic break, a Mermaid fence, a frontmatter, a trailing link
definition and comment. The fixture is rendered by the real pipeline (the harness's
`renderFixtures`), the page runs the shipped page bundle, and the check:

- posts `previewSourceText` with the fixture's text read from the repository file, as the host
  does;
- for each case, sets the selection with a DOM `Range` on the rendered text (the start and end
  characters named in the case), dispatches
  `new ClipboardEvent('copy', { clipboardData: new DataTransfer(), bubbles: true, cancelable: true })`
  on the selection's container, and asserts `defaultPrevented`, the exact text/plain, and that
  text/html holds the rendered element (for example `<strong>`) and no chrome (no
  `data-okf-comment`, no `button`);
- covers, at least: a selection over the thematic break and the table (verbatim), the nested
  admonitions selected whole, a selection from inside one admonition to inside the next (verbatim
  fences between), an edge inside the Mermaid diagram, a selection over the properties table, and
  `selectAll` over the whole page returning the fixture's text exactly, final line break included;
- side by side (Q15): with the side-by-side view on and a changed block, a selection from before a
  card to after it copies the current source only and its text/html holds no old-side text; a
  selection with an edge in the old side is not prevented;
- covers the native cases: a selection inside an open block editor's textarea and in a field, a
  selection only in a comment thread popover, and no `previewSourceText` posted: the event is not
  prevented.

### E4. Real VS Code window: `test/integration/realInput/rawCopy.ts`

A real-input scenario registered in `test/integration/realInput/run.ts`, like
`scenarioCutCopyListBeforeBlankLines` in `test/integration/realInput/blockKeys.ts`: it opens a
fixture in Studio, saves the clipboard and writes a sentinel, selects text in the webview frame (a
Range from a paragraph before a table inside an admonition to the end of that table's row), presses
the platform copy chord as real input, and waits until `vscode.env.clipboard.readText()` holds the
expected raw Markdown; then the same in edit mode; then Ctrl+A (Cmd+A) and the chord give the whole
fixture text; then a selection inside an open block editor copies the textarea's text natively;
the clipboard is restored at the end. The context menu's Copy is not exercised and not claimed
(F6). It runs in `just ci-integration` (a push to `main`, or
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
- `test/core/export/`: the HTML export's tests still pass unchanged after the chrome lists move.
- Each test that checks a rule carries its `@tests_req`; per constitution section 3, at least one
  test fails on the previous code (today no handler: every prevented E3 case fails before the
  change).

### E6. Pull request

The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and
`.agents/guidelines/pull-request.guidelines.md`: the Tests section lists the new and changed
requirement IDs with their source and test files, a short before/after of a copied table and
admonition, the CHANGELOG line; it names `balanceRawCut` as the seam the stacked
`copy-raw-edge-balancing` PR fills. Commit scope per `git-commit-allowed-scopes.md`
(`feat(vscode)` or `feat(render)`).

## Open questions

1. This PR alone (before the stacked edge PR merges): an edge the alignment cannot place leaves the
   whole copy native (written against), since snapping it (Q13) belongs to the stacked CR. The
   other option: move the snapping into this CR's resolution step and keep only marker balancing
   in the stacked CR.
