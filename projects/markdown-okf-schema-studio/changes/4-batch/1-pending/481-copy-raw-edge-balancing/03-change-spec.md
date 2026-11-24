# Balance the edges of a raw Markdown copy, behind an opt-in setting

Short name: `copy-edges`. No tracker issue (origin: the owner, verbal, 2026-11-23, split off from
`copy-selection-raw-markdown` on copy-raw-Q17). Destination: the running batch, batch-09, stacked on
CR-480 `copy-selection-raw-markdown` (short name `copy-raw`, "the base CR" below, spec
`changes/4-batch/2-actives/480-copy-selection-raw-markdown/03-change-spec.md`): this CR's branch
starts from the base CR's branch and needs its raw copy (the `previewSourceText` protocol, the
page's copy handler, the selection-to-source mapping, generated content, UI chrome, scope and
clipboard formats). It fills the base CR's seam `balanceRawCut` (base spec, section 2.3) and adds
one option to the seam's call (section 1).

## Goal

The owner, 2026-11-23: "Au caractère prêt, et il faut éventuellement rajouter les caractères de
clôture ou d'ouverture (admonition, tables…) si on commence ou fini au milieu". Then, 2026-11-24
(copy-edges-Q12): "Mais c'est pareil pour une sélection entièrement dans un admonition: on recopie
pas l'admonition. C'est que quand on casse le bordure et que le résultat risque d'être inconsistant
que l'on rajoute les delimiteurs manquants. Met une option opt-in pour ça et pense à faire une req
et des tests claire sur ces cas."

The base CR copies, as text/plain, the source between the character under the selection's start
and the character under its end, verbatim. When the selection crosses the boundary of a construct
(it starts inside a bold word and ends after it, starts inside an admonition and ends after it),
that verbatim cut is broken Markdown: `rld** again`, an admonition's body followed by a closing
fence with no opening, table rows without their header, a sub-item still indented, `llo` without
its heading marker.

This CR adds a setting, **off by default**, `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`.
With it on:

- a selection **entirely inside** a construct (one admonition, one code block, one table cell, one
  list item, one bold word) copies that construct's **content only**, never its delimiters: a word
  of a code line copies the word, a paragraph of an admonition copies the paragraph;
- a selection that **crosses** a construct's boundary keeps the exact character cut and gets the
  construct's **missing delimiters** added (closing or opening inline markers, container fence
  lines, a table's header and delimiter rows, a list item's marker brought to level 0, a heading
  marker or setext underline), so the pasted Markdown is well formed and renders as the part the
  writer selected.

With it off (the default), the copy is the base CR's verbatim cut. In both, an edge the base CR's
alignment cannot place snaps to its whole element instead of leaving the copy native (answer 13).

## Decisions carried from `02-answers.md`

| Q | Decision | Where it lands below |
| --- | --- | --- |
| copy-edges-Q1 (= copy-raw-Q1) | Character-precise; the opening or closing characters of a container are added when the selection starts or ends inside it. Narrowed by Q12: only when the selection crosses that container's boundary, setting on. | 3.2, 3.4 |
| copy-edges-Q2 (= copy-raw-Q2) | An inline construct cut at an edge is cut exactly there and its markers are added (`**rld**`). Narrowed by Q12: a selection inside the construct copies its text only. | 3.3 |
| copy-edges-Q3 (= copy-raw-Q6) | A table cut at an edge: the rows touched, whole, preceded by the header row and the delimiter row. | 3.6 |
| copy-edges-Q4 (= copy-raw-Q7, copy-raw-Q16) | A nested list cut at the start keeps the item's marker; every copied item is shifted by the indentation of the shallowest item selected, so relative depths are kept (Q16 B). | 3.7 |
| copy-edges-Q5 (= copy-raw-Q11) | A heading cut at the start keeps its marker: `## llo`. | 3.8 |
| copy-edges-Q6 (= copy-raw-Q13) | An edge the alignment cannot place snaps to the whole source element. | 3.11 |
| copy-edges-Q7 (= copy-raw-Q9) | One okfreq SwRS per balancing rule, and tests at the edges: admonition in admonition, list in admonition, admonition in list item, a start or end at each nesting level, code fences in containers, tables in admonitions, bold inside a link, a selection across several containers. | 4, E2, E3 |
| copy-edges-Q8 (= copy-raw-Q17) | Specified for batch-09, stacked on the base CR; spec critic on the split's seams. | Header, 1 |
| copy-edges-Q9 | The first copied item's marker line is capped at 3 columns so it stays a list item; the other lines follow Q4. | 3.7 |
| copy-edges-Q10 | A setext heading cut at the end: its underline line is added. | 3.8 |
| copy-edges-Q11 | A selection entirely inside one code block copies the code text alone; a selection leaving the code block gets the fences. | 3.5 |
| copy-edges-Q12 | Inside a construct: content only, never its delimiters. Delimiters only when the selection crosses a boundary. Opt-in setting, off by default; off is the base CR's verbatim cut; through the settings registry and docs. An SwRS for the setting and one per rule with "inside only" and "boundary crossed" rows; tests with the setting off and on. | 3.1, 3.2, 2.2, 2.4, 4, E2 to E5 |
| 13 (Chief of Staff routine, on Q12) | Snapping an unplaceable edge (Q6) is placement, not a delimiter: it applies with the setting off or on. | 1, 3.11 |
| copy-edges-Q14 | A list, table or heading inside a tab item: the rules read them from a scan of the tab item's source lines, as the fence scan does. | 3.10 |
| copy-edges-Q15 | A definition list, a raw HTML block, a footnote definition cut inside: balanced too (term line and `: ` marker, the HTML block's opening or closing tag, the `[^n]: ` label). | 3.9 |
| copy-edges-Q16 | A selection entirely inside a code block in a list item, blockquote or admonition: the code text alone, the container's indentation or `> ` prefix removed from every line. | 3.5 |
| 17 (Chief of Staff routine, critic F2-F4, F6, setting) | F6: inside one inline code span its text alone, leaving it its backticks. F2: the innermost frame in a tab item is the tab item (its panel is mapped). F3: inline math is whole, out of the inline list. F4: the base CR's tests whose values change with the setting on are listed. Off is the pure verbatim cut; Q16's prefix removal and every addition happen with the setting on only; snapping in both. | 3.3, 3.4, 3.10, E2 ("Base CR tests"), 3.1 |
| copy-edges-Q18 | A selection entirely inside a blockquote or list item, setting on: the container's prefix is removed from every copied line, not only in a code block (the general reading of 3.2). Setting off: the verbatim cut. | 3.2, 3.5 |

Carried from the base CR's critic run (copy-raw answers 14 to 18) where they touch the edges:

- copy-raw-Q14: Ctrl+A then copy gives the whole source exactly, final line break included. The
  base CR resolves those clamped edges to offset 0 and the source's length; no construct encloses
  them, so neither the setting nor balancing changes that result.
- copy-raw-Q15: an edge in an old-side card of the side-by-side view leaves the copy native,
  decided by the base CR's page handler before the seam; balancing never sees it.
- copy-raw answer 18, F5: the frames of the core tests come from the real core renderer's output
  through the base CR's test helper, and the nesting grid also runs in the real browser (E2, E3).
- copy-raw answer 18, F6: text/html is proved in Chromium only; this CR does not change text/html.

## 1. The seam with the base CR

The base CR resolves each edge in `rawMarkdownForSelection` (`src/core/mapping/rawCopy.ts`), then
returns `balanceRawCut(cut)` of `src/core/mapping/rawCopyEdges.ts`, whose types it defines:
`RawCut { source, lineBreak, start, end }`, each edge a `ResolvedRawEdge`, either
`{ kind: "placed"; offset; frames }` or `{ kind: "unplaced"; frames }`, each frame a
`ResolvedRawFrame` (`line`, `endLine`, `atomic`, and the source offsets `start` of its first line
and `end` of the end of its last line), outermost first. In the base CR `balanceRawCut` returns
`undefined` when an edge is unplaced or the start is after the end, else the verbatim slice.

The setting must reach the seam, so this CR changes the seam's call by one option, and nothing
else of the base CR's resolution:

- `RawCut` gains `balanceEdges: boolean`.
- `rawMarkdownForSelection(source, start, end, options?: { balanceEdges?: boolean })`: it copies
  `options?.balanceEdges === true` into the cut; absent means off, so every base CR call and test
  keeps its meaning.
- The page handler `src/page/features/rawCopy.ts` (`installRawCopy`, or the name the base CR gave
  it) reads `readPreviewBootSettings(context)["rawCopy.balanceEdges"]` once when it is installed
  from `src/page/runtime.ts` (a startup setting, 2.2) and passes it on every copy. The protocol,
  the edge building, the native cases and text/html do not change.

`balanceRawCut` keeps its signature; its body becomes:

1. An `unplaced` edge is snapped (3.11), setting off or on; it becomes a placed edge.
2. A start offset after the end offset still returns `undefined` (native copy).
3. Setting off: `cut.source.slice(start.offset, end.offset)`, the base CR's verbatim cut.
4. Setting on: the constructs enclosing each edge are found (3.2); those enclosing both edges add
   nothing and their line prefix is removed (3.2); those enclosing one edge add their delimiters on
   that side (3.3 to 3.9); the table rule moves the edges to whole rows (3.6). Every added line
   break is `cut.lineBreak`. When no construct encloses either edge, the result is the verbatim
   slice.

Its doc comment, which names this CR in the base CR, is replaced by one that states what it does
and names the setting.

## 2. What changes, area by area

### 2.1 Core

- `src/core/mapping/rawCopyEdges.ts` (the base CR's): `RawCut.balanceEdges`, and the body of
  `balanceRawCut` as section 1 says; it stays a thin entry point.
- `src/core/mapping/rawCopy.ts` (the base CR's): the `options` parameter of
  `rawMarkdownForSelection`, copied into the cut. Nothing else.
- New `src/core/mapping/rawCopyScan.ts`: the source scans the rules read: the fence scan (fence
  character, length, nesting, matching closing fence; inside a list item at the item's content
  column), and the line scan of a frame's source lines for list items, tables, ATX and setext
  headings, blockquotes and alerts, definition lists, HTML blocks and footnote definitions (used
  where no frame names those blocks: inside a tab item, 3.10). It returns, for an offset, the
  constructs enclosing it, outermost first, each with its opening lines, its closing line (if
  any), its line prefix and its source range.
- New `src/core/mapping/rawCopyBalance.ts`: the block rules (3.2, 3.4 to 3.9, 3.11): enclosing one
  edge or both, the prefix removal, the container openings and closings, the code block content,
  the table rows, the list shift with the 3-column cap, the heading marker and underline, the
  definition list, HTML block and footnote rules, the snap.
- New `src/core/mapping/rawCopyInline.ts`: the inline scan of 3.3 (the delimiters of the inline
  constructs enclosing an offset inside one block's source).
- All pure (no DOM, no host API, no `vscode`), each under the project's file size limit
  (`just check`); split further if one grows.
- Reuse, do not duplicate: `listItemIndentOfLine` and `startsWithListMarker` of
  `src/core/mapping/listItemIndent.ts`, the quote-prefix reading of `src/core/mapping/quoteLine.ts`
  where it fits, `sourceRangeForLines` of `src/core/mapping/sourceMapping.ts`.

### 2.2 The setting (settings registry)

Per CONTRIBUTING.md, "Add a setting":

- `src/core/configuration/settingsRegistry.ts`, in `PREVIEW_SETTINGS` (the only section whose
  settings reach the page's boot context), a `startupSetting<boolean>` keyed
  `"rawCopy.balanceEdges"`, with `@implements_req <new SwRS 1>` above it:
  - `type: "boolean"`, `default: false`, `order: 26` (free; next to `listItemsInToc`'s 25), no
    `scope` (window, like `markEditorSelection`);
  - `normalize`: `asStored`; page read: `bootFlag(false)` (only a real `true` is on);
  - `markdownDescription`: "Balances the edges of a copied selection. Copying a selection in the
    preview (Ctrl+C, Cmd+C) puts the raw Markdown under it on the clipboard. **On**: a selection
    entirely inside a construct (an admonition, a code block, a table cell, a list item, a bold
    word) copies its content only, and a selection that starts or ends inside a construct and
    crosses its boundary gets the missing delimiters added (closing `**`, the admonition's fence
    lines, the table's header rows, the list marker, the heading marker), so the pasted Markdown
    stays well formed. **Off** (default): the exact source between the two edges, nothing added or
    removed." (The Driver may tighten the wording; it keeps the on and off behaviours.)
- `just generate-settings` writes `package.json`'s `contributes.configuration` (never by hand;
  `just check-settings`).
- The boot context carries it with no more code (`previewBootSettings` /
  `readPreviewBootSettings`); being a startup setting, a change reloads the page content (the
  content patch compares startup settings, `runtimeContextKey`).
- The tests that list the preview keys and defaults are updated:
  `test/core/configuration/settingsRegistry.test.ts`,
  `test/core/configuration/previewConfiguration.test.ts`, and the setting names list of
  `test/security/package-contract.test.ts`.

### 2.3 Page

`src/page/features/rawCopy.ts` (the base CR's): reads the boot setting and passes it, section 1.
Nothing else in the page, the session or the protocol.

### 2.4 Documentation

- `docs/user/settings.md`: a `preview.rawCopy.balanceEdges` (default off) entry in the preview list,
  in the style of `preview.listItemsInToc`: what a copy holds off (the exact source between the
  edges) and on (content only inside a construct, delimiters added when the selection crosses a
  boundary), with the `**world**` example (from "r" to the end of the line: `rld** again` off,
  `**rld** again` on; from "o" to "l": `orl` both).
- If the base CR adds a user page or section on the raw copy, it gets one paragraph naming the
  setting and linking to `docs/user/settings.md`.
- `CHANGELOG.md`: one line under the unreleased section (opt-in edge balancing of the raw copy).
- `.agents/glossary/common.md`, next to the base CR's **Raw copy** entry: **Edge balancing**: with
  `preview.rawCopy.balanceEdges` on, a raw copy copies a construct's content only when the selection
  is inside it, and adds the delimiters a construct is missing when the selection crosses its
  boundary (inline markers, container fence lines, a table's header and delimiter rows, a list
  item's marker at level 0, a heading marker or underline); `balanceRawCut` in
  `src/core/mapping/rawCopyEdges.ts`, rules in `rawCopyBalance.ts`, `rawCopyInline.ts`,
  `rawCopyScan.ts`.

### 2.5 Test harnesses

- `test/visual/renderOptions.ts`: a `rawCopyBalanceEdges?: true` option ("`true`: the raw copy
  balances its edges (`preview.rawCopy.balanceEdges` on). Default off."), added to `OPTION_ORDER`
  (part of the page identity).
- `test/visual/renderFixtures.ts`: `...(options.rawCopyBalanceEdges === true ?
  { "rawCopy.balanceEdges": true } : {})` in `runtimeContext`, like `codeBlocks.lineNumbers`.
- `test/integration/realInput/`: a `withRawCopyBalanceEdges(enabled, body)` helper like
  `withIncrementalUpdates` of `renderPatching.ts` (Workspace target, original value restored).

### 2.6 Not touched

The writing skill (`skills/writing-for-markdown-okf-schema-studio/`): no rendered syntax changes.
The block selection's copy (SwRS-MDOKFSTUDIO-BLOCK-166), the code block's Copy button, the
`previewSourceText` protocol, the base CR's edge resolution (alignment, opening-line edges, tab
items, atomic generated content, side by side, the whole document) and text/html.

## 3. Behaviour

### 3.1 The setting (copy-edges-Q12, answers 13 and 17)

| Setting | What the copy holds |
| --- | --- |
| off (default, unset, `false`, or any non-boolean value) | The base CR's verbatim cut, nothing added or removed. An unplaced edge is snapped (3.11). |
| on (`true`) | 3.2 to 3.10: content only inside a construct, delimiters added at a crossed boundary, the shared line prefix removed. An unplaced edge is snapped (3.11). |

The page reads it once at startup; a change reloads the page content, and the next copy follows
the new value.

### 3.2 Inside only, boundary crossed (setting on)

- A construct **encloses** an edge when the edge's offset lies strictly inside it: after its first
  character and before the end of its last line (for an inline construct, after its opening
  delimiter's first character and before its closing delimiter's end). An edge at offset 0, at the
  end of the source, or between two top-level blocks is enclosed by nothing.
- A construct enclosing **both** edges (the selection is inside it): **inside only**. It adds no
  delimiter, and its line prefix (a blockquote's or alert's `> `, a list item's content-column
  indentation, the indentation of a container nested in a list item, an indented code block's four
  columns) is removed from every line of the copy after the first; the first line starts at the
  edge and holds no prefix. So the copy is that construct's content as it reads at column 0.
- A construct enclosing **one** edge (the selection crosses its boundary): **boundary crossed**. A
  start edge inside it adds its opening (before the copy); an end edge inside it adds its closing
  (after the copy), per 3.3 to 3.9. A construct with no opening or closing for that side adds
  nothing there.
- A construct enclosing neither edge is whole in the cut or out of it: nothing changes.
- The added characters are read from the source, verbatim (the same fence length, option lines,
  link target, tag), never rebuilt.
- Order: before the cut, the openings outermost first (the outermost crossed block's opening line
  first, the innermost inline marker last, nearest the text); after the cut, the closings innermost
  first. The added opening lines carry the prefix of the crossed constructs that enclose them, not
  of the inside-only ones (which is removed).

### 3.3 Inline constructs (copy-edges-Q2, Q12, answer 17 F3 and F6)

| Source | Selection | Off | On | Case |
| --- | --- | --- | --- | --- |
| `Hello **world** again` | from "r" of world to the end of the line | `rld** again` | `**rld** again` | crossed (start) |
| `Hello **world** again` | from the start to "o" of world (included) | `Hello **wo` | `Hello **wo**` | crossed (end) |
| `Hello **world** again` | from "o" to "l" of world (included) | `orl` | `orl` | inside only |
| `a [link **bold** text](https://x.test) b` | from "ld" to "te" (included) | `ld** te` | `**ld** te` | bold crossed, link inside only |
| `a [link **bold** text](https://x.test) b` | from "ld" to the end of the line | `ld** text](https://x.test) b` | `[**ld** text](https://x.test) b` | bold and link crossed |
| `` use `npm ci` here `` | from "ci" to the end | `` ci` here `` | `` `ci` here `` | crossed |
| `` use `npm ci` here `` | from "n" to "p" (included) | `np` | `np` | inside only (F6) |
| ``{kbd}`Ctrl+C` to copy`` | from "t" of Ctrl to the end | ``trl+C` to copy`` | ``{kbd}`trl+C` to copy`` | crossed |
| `~~old~~ and *new*` | from "l" of old to "n" of new (included) | `ld~~ and *n` | `~~ld~~ and *n*` | both crossed |
| `see <span class="k">key word</span> here` | from "w" to the end | `word</span> here` | `<span class="k">word</span> here` | crossed |

- The constructs: emphasis and strong (`*`, `_`, `**`, `__`, `***`), strikethrough (`~~`), inline
  code (its backtick run), links (opening `[`, closing `](target "title")` verbatim), reference
  links (closing `][ref]`, `][]` or `]` verbatim), autolinks (`<` … `>`), MyST roles (opening
  ``{name}` `` with its backtick run, closing the backtick run) and inline HTML elements (the
  opening tag verbatim, the matching closing tag).
- A start edge on the first content character of a construct with the end after the construct,
  or an end edge right after its last content character with the start before it, gives the whole
  construct (`**world**`).
- Inline math (`$` … `$`), like an image, `[^1]` or `{ref}`, is a construct whose rendered text is
  not its source: the base CR moves an edge inside it to its boundary (base spec 3.4; the Chief of
  Staff asks the base CR to name inline math in its whole-construct list, answer 17 F3). It is
  whole in the cut and adds nothing here.
- Inside a table row: an inline construct in one cell follows this rule on that cell's text when
  both edges are in that cell (3.6); otherwise the row is copied whole and the construct adds
  nothing of its own.

### 3.4 Containers (copy-edges-Q1, Q12)

A container: a MyST directive or admonition in a backtick, tilde or colon fence
(```` ```{note} ````, `:::{note}`), with its option lines (`:key: value`) or YAML options block; a
GitHub alert (`> [!NOTE]`); a blockquote (`>`); a tab set, a tab item, a card, a grid and a grid
item (fenced directives). Code blocks are 3.5.

| Selection | Off | On |
| --- | --- | --- |
| both edges in one admonition's body | verbatim | the body text between the edges, no fence line (inside only) |
| start in admonition A, end after A | verbatim (A's closing fence, no opening) | A's opening lines, then the cut (crossed) |
| start before admonition A, end in A | verbatim (A's opening, no closing) | the cut, then A's closing line (crossed) |
| start in A, end in the next admonition B | verbatim | A's opening lines, the cut, B's closing line |

- Opening: the fence line and its option lines or options block, verbatim; for an alert its
  `> [!TYPE]` line. A blockquote or an alert crossed at the start gives its `> ` prefix(es),
  verbatim, to the first, partial line of the cut; the later lines carry theirs already.
- Closing: the fence line, verbatim, on a new line. A blockquote, an alert and a list have no
  closing line. A fenced container left unclosed in the source has none either: nothing is added.
- Inside only: both edges in one blockquote or alert copy its content with the `> ` prefix removed
  from every line after the first (3.2).
- An edge in a container's opening line: the base CR moves it to the start (start edge) or the end
  (end edge) of that line, so the line is whole in the cut. A start edge moved to the line's start
  is not inside the container (3.2). An end edge moved to the line's end is: with the start before
  the container, its closing line is added (a title alone copies as an empty admonition); with
  both edges in the title, the start is at the container's first character, so the container
  encloses only the end and its closing line is added too.
- Nested containers each follow 3.2 on their own: an admonition in an admonition, start in the
  inner one and end after both, gives both opening lines (each verbatim, a four-colon outer fence
  stays four colons); start in the inner one and end in the outer one after the inner one, gives
  the inner opening only (the outer one is inside only).
- Fenced containers are found by the fence scan (`rawCopyScan.ts`), not only from the frames.
  Lists, list items, tables, headings, blockquotes and alerts come from the frames (`start`, `end`,
  `line`, `endLine`) and the source lines they name, or from the line scan where no frame names them
  (3.10).

### 3.5 Code blocks (copy-edges-Q11, Q16)

A code block: a backtick or tilde fence, a `{code-block}` or `{code}` directive, an indented code
block.

| Selection | Off | On |
| --- | --- | --- |
| both edges in one code block's content | verbatim (the code text; in a container, the later lines keep their indentation or `> `) | the code text alone: no fence or container lines, and on every line after the first the code block's own indentation and the prefix of every container enclosing both edges removed, so it pastes as usable code |
| start in the code, end after the code block | verbatim | the crossed containers' openings, the code fence's opening line, the code from the edge |
| start before the code block, end in the code | verbatim | the code to the edge, the code fence's closing line, the crossed containers' closings |

An indented code block has no fence: crossed, it adds nothing, and the first, partial line gets
its four columns of indentation back so it stays code. Example (on): a fenced block in a list item
(content at column 2) holding `  foo()` and `  bar()`, a selection from "oo" to the end of "bar()":
`oo()` and `bar()` on two lines, no indentation.

### 3.6 Tables (copy-edges-Q3, Q12)

| Selection | Off | On |
| --- | --- | --- |
| both edges in one cell | verbatim | the cell text between the edges (inside only; 3.3 applies inside it) |
| edges in two cells of one table, or one edge outside the table | verbatim | the touched rows whole: the start edge moves to the start of its row's line, the end edge to the end of its row's line; with the start in a body row, the header row and the delimiter row first, verbatim |

- A start edge in the header row or the delimiter row starts at the header row (nothing added).
- Start before the table, end inside it: the header and delimiter are in the cut; the end row is
  completed.
- A table inside an admonition, start in a row, end after the admonition: the admonition's opening
  lines, then header, delimiter and the rows; with the end in the admonition (after the table), no
  admonition line (inside only).
- A table inside a blockquote or a list item keeps on the added header and delimiter rows the
  prefix or indentation of its crossed containers, as in the source (then 3.7 shifts list lines);
  the prefix of inside-only containers is removed (3.2).

### 3.7 Lists (copy-edges-Q4, Q9, Q12)

- Inside only: both edges in one list item copy its content, the item's content-column indentation
  removed from the later lines; no marker.
- Crossed at the start (the start edge in a list item the end edge is not in): the innermost such
  item keeps its marker (`-`, `*`, `+`, or its own number `3.` / `3)`, with its task box `[ ]` /
  `[x]` when it has one), followed by one space and what the other rules give: the cut text, or
  the opening line of a crossed container inside the item (then that container's other opening
  lines on the next lines, at the item's content column). The outer items enclosing the start give
  no marker and no text.
- The shift (Q4): among the list items whose marker is copied (the start item and every later item
  of the same top-level list whose marker line is in the cut), take the smallest marker column `m`,
  counted after the prefix of the containers enclosing the list (removed for inside-only ones,
  kept for crossed ones). Every copied line of that top-level list loses `m` columns of leading
  whitespace, clamped at column 0 (a lazy continuation line with less indentation keeps its text).
  Lines after that list's last line are not shifted.
- The cap (Q9): after the shift, when the start item's marker line would sit at column 4 or more,
  that line alone is moved to column 3, so it stays a list item and not an indented code block. The
  other lines keep the shift.
- Crossed at the end: a list has no closing line; the containers inside the item close as 3.4 says,
  at their source column minus `m` when the start edge is in the same top-level list.
- Examples (on), source:

  ```markdown
  - parent
    - child **world**
    - sibling
  - next
  ```

  From "rld" to the end of the list (`m` = 0):

  ```markdown
    - **rld**
    - sibling
  - next
  ```

  From "rld" to the end of `sibling` (the parent encloses both edges: inside only, its 2 columns
  removed):

  ```markdown
  - **rld**
  - sibling
  ```

  A start item three levels deep (marker at column 6) with a later top-level item selected: the
  start item's marker line at column 3, the rest shifted by 0.
- An admonition inside a list item, start in the admonition's paragraph, end after the list: the
  item's marker (shifted), the admonition's opening line on the marker line, the cut text and the
  later lines at the item's content column minus `m`.

### 3.8 Headings (copy-edges-Q5, Q10, Q12)

| Selection | Off | On |
| --- | --- | --- |
| both edges in one heading's text | verbatim | the text between the edges |
| start in an ATX heading's text, end after it | `llo` … | `## llo` …: the marker verbatim (the `#` run, the space, the heading's indentation) |
| start before a setext heading, end in its text | verbatim | the cut, then the underline line (`===` or `---`) verbatim on a new line |
| end in an ATX heading, start before it | verbatim | nothing added (closing `#`s are optional) |
| start in a setext heading's text, end after it | verbatim | nothing added (the underline is in the cut) |

### 3.9 Definition lists, HTML blocks, footnote definitions (copy-edges-Q15)

| Construct | Inside only (on) | Crossed at the start (on) | Crossed at the end (on) |
| --- | --- | --- | --- |
| a definition (`Term` line, then `: definition`) | the definition text | the term line and the `: ` marker, verbatim, before the cut | nothing |
| a raw HTML block (`<div …>` … `</div>`) | the text between the edges | the block's opening tag line, verbatim | the matching closing tag, on a new line |
| a footnote definition (`[^n]: text`) | the text between the edges | the `[^n]: ` label, verbatim | nothing |

A start in a definition list's term line adds nothing (the term line is cut, its `: ` line follows
in the cut). Off: verbatim.

### 3.10 Tab items and constructs inside them (copy-edges-Q14, answer 17 F2)

- In a tab item, the innermost frame of an edge is the tab item itself: its panel is mapped
  (`sourceProperties(item)` on the `myst-tab-panel` div, `src/core/render/mystGridToctree.ts`
  lines 534-541) while its plain blocks are unmapped (`unmapPlainBlocks`, line 533). The tab set
  is the frame around it. Both are fenced: their fence lines come from the fence scan.
- Lists, tables, headings, blockquotes, definition lists, HTML blocks and footnote definitions
  inside a tab item have no frame of their own: the line scan of `rawCopyScan.ts` reads them from
  the tab item's source lines (its frame's `line` to `endLine`), and 3.6 to 3.9 apply to them as
  anywhere else.

### 3.11 An edge the alignment cannot place (copy-edges-Q6, answer 13)

Setting off or on. An `unplaced` edge snaps to its innermost frame that is not atomic (the element
whose source the alignment could not match): the start edge to that frame's `start`, the end edge
to its `end`. The element is then whole in the copy. Setting off, the copy is the verbatim slice
between the snapped edges; on, the constructs enclosing the snapped edges follow 3.2 to 3.10. An
unplaced edge with no frame snaps to offset 0 (start) or the source's length (end). The copy is no
longer left native for this reason: this closes the base CR's open question 1 in the stacked pair
(until this CR merges, the base CR alone keeps the native copy).

## 4. Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md`, the okfreq baseline it links to and
`requirements/guidelines/project.guidelines.md` ("During a change"); run okfreq as
`uv run --no-sync --group requirements okfreq`.

- New SwRS in scope `block-editing` (token BLOCK), created with `okfreq new … --lifecycle
  proposed`, each deriving from the StRS the base CR creates ("A reader copies a selection as the
  exact Markdown under it"). Each of 2 to 8 holds a scenario table with explicit rows: **setting
  off** (the verbatim cut), **inside only** (setting on: content, no delimiter, prefix removed) and
  **boundary crossed** at the start and at the end (setting on: the delimiters added). The Driver
  may merge two only when one test file proves both.
  1. The setting `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`: boolean, off by default,
     read once at startup from the boot context (missing or non-boolean reads as off; a change
     reloads the page content); off gives the verbatim cut, on the balancing of SwRS 2 to 8
     (3.1, 3.2); depends on the base CR's SwRS 3. Modelled on SwRS-MDOKFSTUDIO-TOOLBAR-138.
  2. Inline constructs (3.3).
  3. Fenced containers, alerts and blockquotes, tab items, nested and across containers,
     opening-line edges, unclosed fences (3.4, 3.10).
  4. Code blocks: inside only gives the code text alone with prefixes removed; crossed gives the
     fences (3.5).
  5. Tables: one cell, or whole rows with header and delimiter rows (3.6).
  6. Lists: marker, shift by the shallowest item, 3-column cap (3.7).
  7. Headings: ATX marker, setext underline (3.8).
  8. Definition lists, HTML blocks, footnote definitions (3.9).
  9. An unplaceable edge snaps to its whole element, setting off or on (3.11).
- Changed SwRS, the base CR's, `proposed` in the same batch (no owner approval needed):
  - its SwRS 2 (scope): "or when an edge cannot be placed" is removed from the native cases, with
    a pointer to new SwRS 9;
  - its SwRS 3 (character-precise verbatim cut): "nothing added at the edges" gets "while
    `preview.rawCopy.balanceEdges` is off (the default); on, see <new SwRS 1>".
  The base CR's `@implements_req` of its SwRS 3 on `balanceRawCut` stays.
- No `approved` requirement is touched (none of the approved StRS covers copying a native
  selection); if the Driver finds one, it stops and asks.
- Markers: `@implements_req` of new SwRS 1 on the registry entry and on the page handler's read of
  the setting; of SwRS 2 to 9 at each rule's code point in `rawCopyInline.ts`, `rawCopyBalance.ts`
  and `rawCopyScan.ts`; `@tests_req` at each test; at most 3 IDs per marker block
  (`just check-markers`).
- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` under the day of
  the change, in a `### Raw copy: edge balancing (opt-in)` sub-heading.

## 5. Out of scope

- Everything the base CR owns: scope and native cases (but the unplaced one), the
  `previewSourceText` protocol, the alignment of a placed edge, opening-line edges, generated
  content and included blocks, side by side, Ctrl+A, chrome, text/html. The base CR's
  whole-construct list naming inline math is the base CR's change (answer 17 F3).
- Adding a link reference definition, a footnote definition or a label target that a copied
  construct points to.
- Rewriting the copied Markdown beyond what 3.2 to 3.10 add or remove: no marker normalization, no
  reflow, no renumbering of an ordered list, no path conversion.
- Balancing a cut (Ctrl+X) or any edit from a native selection.
- A live update of the setting in an open page without a content reload.

## Evidence

### Host and default matrix

The behaviour depends on a shipped default (off) versus a configured value. One line per cell:

| Host | Setting | Expected | Proved by |
| --- | --- | --- | --- |
| core | absent (`options` omitted) | verbatim cut, unplaced edge snapped | E2, `rawCopy.test.ts` (base CR's cases, setting off) |
| core | `balanceEdges: true` | balanced (3.2 to 3.10) | E2, `rawCopyBalance.test.ts` |
| registry | unset | default `false`; boot read off | E5 |
| registry | `false` / `"yes"` / `1` in the boot context | off | E5 |
| registry | `true` | on | E5 |
| Chromium simulated page | default page (no option) | verbatim | E3, off page |
| Chromium simulated page | `rawCopyBalanceEdges: true` | balanced | E3, on page |
| real VS Code window | default (unset) | verbatim | E4, the base CR's step unchanged |
| real VS Code window | set `true` in the workspace | balanced, after the page reloads | E4, new step |

### E1. Static and unit gates

- `just check` passes (formatting, TypeScript, import boundaries: the new modules are in
  `src/core` and import nothing above it; file size; unused exports; markers; settings schema;
  unit and contract tests).
- `just generate-settings` was run; `just check-settings` passes.
- `just requirements-lint` and `just requirements-update` pass, each new SwRS with a source marker
  and a test marker.
- `just preflight` passes (on Windows the static stage; CI runs the others), constitution
  section 4.

### E2. Core unit tests

Each case is a source written in the test, the selection's start and end named as rendered
characters, and the exact expected string. The edges are not written by hand: the test builds them
with the base CR's helper (`test/core/mapping/rawCopyFrames.ts`, real core renderer, the
sanitizer's `data-sphinx-source-line`, the same edge building as the page) and calls
`rawMarkdownForSelection`, so the frames are those the page sees (copy-raw answer 18, F5).

**Base CR tests** (`test/core/mapping/rawCopy.test.ts`, answer 17 F4). They call without `options`
(setting off) and keep the base CR's values, except the one snapping changes:

| Base CR case | Setting off (in `rawCopy.test.ts`) | Setting on (new case in `rawCopyBalance.test.ts`) |
| --- | --- | --- |
| seam `Hello **world** again` from "r" | unchanged: `rld** again` | `**rld** again` |
| seam `## Hello` from "llo" | unchanged: `llo` | `## llo` |
| seam: from admonition A's paragraph to B's paragraph | unchanged: verbatim | A's opening lines, the cut, B's closing line |
| seam: an unplaced edge gives `undefined` | **edited in place**: the copy snapped to the element (verbatim slice between the snapped edges) | snapped, inside an admonition, the admonition balanced |
| seam: start after end gives `undefined` | unchanged | unchanged |
| an edge in an admonition's title (start, end) | unchanged: opening line's start or end | the end case gets the closing line (3.4) |
| an edge inside a tab item's block | unchanged; its frame is the tab item (F2: if the base CR's test names the tab set, it is corrected to the tab item, the base CR's behaviour) | start crossing the tab item: the tab set's and tab item's opening lines |
| nested containers copied whole, atomic frames, CR LF, the whole document | unchanged | the whole document with the setting on: the source exactly (copy-raw-Q14) |

**New `test/core/mapping/rawCopyBalance.test.ts`** (split into `rawCopyBalanceInline.test.ts`
and `rawCopyBalanceBlocks.test.ts` if it outgrows the size limit). Every case asserts the setting
on value and, in the same test, that the setting off value equals the verbatim slice
`source.slice(start, end)` of the resolved edges. Cases, at least:

- every row of the 3.3 table (off and on columns), bold inside a link both inside only and
  crossed, inline code inside only (F6);
- inline math with an edge inside: whole, nothing added;
- clean edges: a selection between top-level blocks and one in a top-level paragraph outside any
  construct give the verbatim slice on;
- each row of the 3.4 table; a blockquote and an alert, inside only (prefixes removed) and crossed
  at the start (`> [!NOTE]` line, `> ` prefix on the first line);
- an admonition in an admonition (colon fences of 4 and 3 colons): both edges in the inner one
  (inner content only); start in the inner one and end in the outer one after it (inner opening
  only); start in the inner one and end after both (both openings); start before both and end in
  the inner one (both closings);
- a list inside an admonition, start in the second item, end after the admonition: the
  admonition's opening, the item's marker at column 0;
- an admonition inside a list item, start in the admonition's paragraph (3.7);
- the nesting grid: an admonition > list item > admonition, a start at each level 0 to 3 (before
  the deeper construct opens) by an end at each level 0 to 3 (after the deeper construct closes),
  the 16 expected on strings written out, each also checked off;
- each row of the 3.5 table, with the code block top level, in an admonition, in a list item (the
  3.5 example) and in a blockquote (Q16); an indented code block crossed;
- each row of the 3.6 table; a table in an admonition both ways; a start in the header row; a
  selection inside one cell's bold word crossing the bold only;
- the two 3.7 examples, the 3-column cap (Q9), an ordered list keeping its own number, a task item
  keeping `[x]`, a list in a blockquote (shift counted after `> `), two paragraphs of one list item
  (inside only);
- each row of the 3.8 table;
- each row of the 3.9 table;
- a tab set with two tab items: start in the second item's paragraph, end after the tab set (tab
  set and tab item openings); both edges in that paragraph (inside only); a list, a table and a
  heading inside a tab item, crossed at the start (Q14, the line scan);
- an unclosed colon fence, end inside it: nothing added;
- an unplaced edge (rendered text absent from the element's source): snapped, off and on;
- a CR LF document: the cut keeps CR LF and every added line uses CR LF.

### E3. Real browser: the base CR's `test/visual/capture_raw_copy.py`

The base CR's capture check (its scenario `test/visual/rawCopyScenarios.ts`, its fixture
`test/visual/fixtures/97-raw-copy.md` or the number it took) gets a second page, rendered with
`render: { rawCopyBalanceEdges: true }` (2.5), and the fixture gains the constructs it lacks (an
admonition > list > admonition nest, a tab set with a list inside a tab item, a code block in a
list item, a heading, a definition list). The fixture is the repository file rendered by the real
pipeline, the page runs the shipped page bundle, and `previewSourceText` carries the fixture's text
read from the repository, as the base CR's check does. For each case the check sets a DOM `Range`
on the rendered characters, dispatches the base CR's `copy` `ClipboardEvent`, and asserts
`defaultPrevented` and the exact text/plain.

- On page: `**rld** again`; `orl` (inside only); bold inside a link crossed; the nesting grid of E2
  (16 cases, copy-raw answer 18, F5); a word of a code line in a list item (the word alone) and a
  selection from that code to after the list item (fences added); a table row in an admonition
  from a bold word in the row; the nested list example with `m` = 0; a selection across two
  admonitions; the tab set case with the list inside a tab item; `## llo`; a definition crossed at
  the start; a clean selection (two whole paragraphs) equal to the verbatim slice; `selectAll`
  giving the fixture's text exactly.
- Off page (the base CR's page): the base CR's cases unchanged, plus `rld** again`, `llo` and the
  code-in-list-item word with its verbatim value, so the default is proved verbatim in the browser.

Each on case that adds or removes characters fails on the base CR alone (it gives the verbatim
cut), which is the failing test constitution section 3 asks for.

### E4. Real VS Code window: the base CR's `test/integration/realInput/rawCopy.ts`

The base CR's steps run with the setting at its default and keep their expected values. One more
step, inside `withRawCopyBalanceEdges(true, …)` (2.5): wait for the page to reload with the new
boot context, then in the opened fixture a Range from "r" of a bold word in a paragraph inside an
admonition to the middle of a row of a table after that admonition, the platform copy chord as
real input, then `vscode.env.clipboard.readText()` waited until it holds the admonition's opening
line, `**rld**` and the rest of that paragraph, the lines to the table, the table's header and
delimiter rows (in the cut) and the touched row whole; the setting and the clipboard restored at
the end. It runs in `just ci-integration` (a push to `main`, or
`gh workflow run ci.yml --ref <branch> -f heavy=true` on the branch, which the Driver runs before
asking for a merge).

### E5. Setting tests

- `test/core/configuration/settingsRegistry.test.ts` and `previewConfiguration.test.ts`: the key
  is in the preview table and in the startup boot keys, default `false`; the boot read gives `true`
  only for `true` (`false`, absent, `"yes"`, `1` give `false`).
- `test/security/package-contract.test.ts`: the setting name in the contributed list;
  `just check-settings` proves `package.json` matches the registry.
- `test/page/runtimeRawCopy.test.ts` (the base CR's node:vm harness), where the fake DOM allows
  it: with the boot flag on the handler passes `balanceEdges: true` to the core call, off or absent
  `false`. What the fake DOM cannot hold is proved in E3.
- Each test carries its `@tests_req`.

### E6. Pull request

The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and
`.agents/guidelines/pull-request.guidelines.md`, stacked on the base CR's PR per
`.agents/guidelines/stacked-prs.guidelines.md`: the Tests section lists the new and changed
requirement IDs with their source and test files, the new setting with its default, a short
before/after (setting off, setting on) of a copy starting inside a bold word of an admonition and
ending in a table row, and of a word copied inside a code block, the CHANGELOG line. Commit scope
per `.agents/guidelines/git-commit-allowed-scopes.md` (`feat(vscode)` or `feat(render)`, as the
base CR).
