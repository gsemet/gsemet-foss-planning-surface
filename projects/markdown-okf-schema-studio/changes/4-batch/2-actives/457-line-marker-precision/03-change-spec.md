# Line marker on the table row, the hidden tab and the front matter row

When Studio opens at a requested line and marks it (the arrow in the left margin and the light band
of CR-445 open-at-line-marker), the marker becomes precise in three places that CR-445 leaves at the
top of the enclosing block: a pipe table marks the row of the line, wherever the table sits (top
level, quote, admonition, list item, tab item); a line in a tab that is not shown selects that tab
(and every hidden tab around it) and is then marked on its exact line; a front matter line marks its
property's row in the properties table.

Origin: verbal (owner, 2026-11-21). No tracker issue. Split off from CR-445 (decision 31). Code base:
`origin/main` at `5a84db8b` (release 1.11.0, which ships CR-445).

**Size and risk, plainly.** This CR is no longer page-only. The renderer must give source lines to
content that has none today (everything inside a tab item, and every row of a pipe table), under a
new attribute that no click, scroll sync or change bar reads. The risk is in the renderer: content
of a directive (an admonition, a tab item) may carry no position or a position relative to the
directive body, and a wrong line there puts the arrow on the wrong row or line silently. Rendered
HTML snapshots may change. The render tests of 7.1 prove the lines in every container before the
page work relies on them. The CR lands last in batch-07 (section 9).

## 1. Goal, in the user's terms

- I search a word that sits in a table row and click the result: Studio opens with the arrow on
  that row, not on the top of the table, also when the table sits in a quote, an admonition, a list
  item or a tab.
- I search a word that sits in the second tab of a tab set: Studio shows that tab (and the outer
  tab, if the tab set is nested in another), then the arrow marks the exact line, as for a folded
  section or a closed dropdown. Tab sets of the same sync group follow, as on a click.
- I search a property of the front matter (`owner: alice`): the arrow marks the `owner` row of the
  properties table, which opens if I had collapsed it. A front matter line that is no property (the
  fences, a comment) marks the top of the properties table, as today.

## 2. Facts at 1.11.0 (the code this CR changes)

- The marker is `src/page/features/lineMarker.ts` (`installLineMarker`, 209 lines): `reveal(line)`
  runs `place(true)`: the innermost mapped block holding the line (`containingBlock`, hidden blocks
  included), `unfold` (`rt.parts.headingFold.reveal`, `details.open`), `rt.scroll.measure()`, the
  entry `rt.scroll.entryForLine(line)` from the visible layout, a hidden check, and the box
  `lineBox(entry, line)`: a code line (`.myst-code-line` spans counted back from the end line,
  `codeSpanIndex`), a soft-wrapped paragraph line (`entry.lineTops`, measured by `measureLineTops` in
  `src/page/features/scrollCore.ts`, 599 lines), else the block top with one line height. `mark()`
  puts `data-sphinx-line-marker` and `aria-current="location"` on the entry's element. Later
  placements (`layoutMeasured`) call `place(false)`, which never unfolds. SwRS LIFE-178 (placement),
  LIFE-179 (lifetime), LIFE-180 (edit mode), all `proposed`.
- Mapping: a hast node with `data-line` (from `sourcePositionProperties`, `src/core/render/mystNode.ts:68`)
  becomes a mapped block in `injectSourceMappings` (`src/core/security/html-sanitizer.ts`): it gets
  `data-sphinx-source-file`, `-line`, `-end-line`, a block id and `tabindex`. Mapped blocks are what a
  click edits, what scroll sync and `markSourceLine` follow (`MAPPINGS_SELECTOR`,
  `src/page/features/pageRuntime.ts:789`). The sanitizer keeps every `data-okf-*` attribute.
- Tables: a top-level pipe table is one mapped block (the `<table>`, from its header line to its last
  row); its `<tr>` carry no line. A table inside a quote, an alert or an admonition is edited with its
  container and found by rank (`src/page/modules/tableInContainer.ts`, `tableRankIn`). A
  `{list-table}` strips the lines of its content (`stripSourceLines`, `src/core/render/mystTables.ts`)
  and sits in a `<figure>`; a raw HTML table is a `div.myst-raw-html-table`.
- Tab sets: `buildTabSet` (`src/core/render/mystGridToctree.ts`) maps the `.myst-tab-set` and each
  `.myst-tab-panel`; a panel not shown has `hidden`. `unmapPlainBlocks` (line 468) deletes the lines
  of everything inside a tab item and sets `noSourceLine` (so `sourcePositionProperties` and
  `tableAlignmentSpec` emit none): a tab item is one block, a click in it edits the whole item
  (SwRS MYST-098). Node positions are kept "for the stages that read them". Selection lives in
  `src/page/modules/tabs.ts` (`installTabs(document)`, 116 lines; `select`, `chosenIndex`,
  `chosenSync`; `apply()` puts the choices back after a content patch and prefers the group's
  `chosenSync` over the set's `chosenIndex`); it is `rt.parts.tabs`, installed in `src/page/runtime.ts`
  (line 270) with no callback. SwRS MYST-098, MYST-099, `proposed`.
- Front matter: `renderPropertiesTable` (`src/core/frontmatter/propertiesTable.ts`) maps the
  `section[data-okf-properties]` at line 1 only. Each `tr[data-okf-field]` carries `data-okf-line`
  and `data-okf-end-line` (1-based, whole file, key line to last value line;
  `frontmatterFieldLines`, `src/core/frontmatter/frontmatterChanges.ts`, SwRS REVIEW-215) when source
  mapping is on and the YAML is a mapping. The toggle collapses the table
  (`state.frontmatterCollapsed`; `rt.input.applyFrontmatterVisibility()`, `src/page/features/pageInput.ts:107`,
  already in the `PageInput` interface of `pageRuntime.ts`; SwRS FMSCHEMA-090); the issue badge
  expands it before jumping to a row.
- Two bugs of CR-445's code this CR reaches and fixes: (a) the properties section has no end line,
  so a line near the closing fence of a long front matter goes to the first body block (nearest by
  distance); (b) `lineBox` counts code spans on any entry that holds spans and no mapped block, so a
  shown tab panel holding a code block followed by a paragraph puts a line on the wrong code line.
- `docs/user/open-studio.md` line 31 says the arrow "disappears on your next click, keystroke or
  scroll", which contradicts LIFE-179 (it stays through scrolls).

## 3. Decisions

| # | Decision | Source | Where |
| --- | --- | --- | --- |
| 1 | One CR for the table row, the hidden `{tab-item}` (selected first, like an unfold) and the front matter property row (else the top of the properties table) | 02-answers lm-Q1 ("Les 3 ensemble") | the whole spec |
| 2 | The marker is CR-445's (1.11.0): same look, lifetime and edit mode; its placement changes | lm-Q1 | 4 |
| 3 | Table: the header row on the table's first line, the delimiter line to the header row, body row n on the first line plus n+1 | intake/request.md | 4.3 |
| 4 | A line in a non-selected `{tab-item}`: select that tab first, like an unfold, then mark the line | intake/request.md | 4.4 |
| 5 | Front matter line: the property's row, else the top of the table | intake/request.md | 4.5 |
| 6 | Into the running batch-07 once final and ready | 02-answers (owner, 2026-11-21) | 9 |
| 7 | Once a hidden tab is shown, the arrow sits on the exact paragraph or code line inside it; the renderer gives line data inside a tab item without changing how a click edits the whole item (MYST-098) | lm-Q2 (owner, "Sur la ligne exacte") | 4.1, 4.4 |
| 8 | A pipe table inside a quote, an admonition or a list item gets its row, in this CR: the renderer gives these tables their lines | lm-Q3 (owner, "Oui, dans ce CR") | 4.1, 4.3 |
| 9 | A pipe table inside a tab item gets its row too (through decision 7) | Chief of Staff | 4.3 |
| 10 | `{list-table}`, a captioned `{table}` and raw HTML tables keep the top of their block (the intake's pipe-table rule; CR-445 decision 31) | Chief of Staff | 4.3 |
| 11 | Nested tab sets: every hidden tab around the line is selected | Chief of Staff | 4.4 |
| 12 | Selecting the tab takes the click's path (`select(tab, false)`): it records `chosenIndex` and `chosenSync`, the sets of the same sync group follow, no focus move (MYST-099) | Chief of Staff | 4.4 |
| 13 | A collapsed properties table expands on the request only (`place(true)`, like an unfold); collapsed later by the reader: LIFE-179's folded rule (not drawn until shown; a later placement never expands); FMSCHEMA-090 gains the boundary | Chief of Staff | 4.5 |
| 14 | A tab the reader leaves (keyboard, or through its sync group) hides the marker until it shows again (LIFE-179's folded rule); a keyboard tab change leads to a new placement | Chief of Staff | 4.4 |
| 15 | Fix `docs/user/open-studio.md` line 31 to LIFE-179 in this CR | Chief of Staff (critic C5) | 4.8 |
| 16 | The CR lands last in batch-07 | Chief of Staff | 9 |

CR-445's decisions 6 (look), 7 (lifetime), 8 and 31 (precision), 16 (edit mode) still hold; this CR
narrows decision 31's "otherwise the top of the enclosing block" for the places above.

## 4. What changes

### 4.1 Renderer: marker lines (`data-okf-marker-line`)

A new pair of attributes, `data-okf-marker-line` and `data-okf-marker-end-line` (1-based, whole
file, inclusive; the end only when it differs), read by the line marker only. They are not
`data-line`, so `injectSourceMappings` does not map them: no block id, no `tabindex`, no click target,
no scroll sync, no `markSourceLine`, no change bar (`src/page/modules/incomingChanges.ts` reads
`data-line` and `data-okf-line` only). The sanitizer keeps them (`data-okf-` prefix);
`src/core/export/exportContent.ts` adds both to `REMOVED_ATTRIBUTES`.

- **Inside a tab item.** `sourcePositionProperties` (`mystNode.ts:68`): for a node with
  `noSourceLine`, return the marker pair from the node's position instead of nothing (the included
  flag kept). `unmapPlainBlocks` keeps deleting `data-line`, `data-end-line`, `data-single-line`, and
  writes the marker pair instead from the node's position. So every paragraph, code block, list,
  table, card and nested tab panel inside a tab item carries its lines, and a click still edits the
  whole item (MYST-098, unchanged).
- **Rows of a pipe table.** Every row of a GFM pipe table gets `data-okf-marker-line` = its source
  line on its `<tr>` (the header row on the table's first line; body row n on the first line plus
  n+1), wherever the table is: top level, in a blockquote, a GitHub alert (`mystGithubAlerts.ts:188`
  deletes `data-line` there: the marker pair stays), an admonition or another directive body, a list
  item, a tab item. Set from the mdast `tableRow` positions; if the HTML writer drops row
  properties, set on the written table in `mystTables.ts` where the alignment spec is matched. No row
  line under a `{list-table}` or a `{table}` directive, nor in a raw HTML table (decision 10). A table
  inside a container or a tab item also gets the marker pair on its `<table>`.
- **Positions in a directive body.** Where a directive's content is parsed apart (an admonition, a
  tab item: `parseBody(body, raw.firstLine, …)` in `mystGridToctree.ts`), the lines must be whole-file
  lines. Where they are missing or relative, the renderer offsets them by the body's first line, as
  `buildTabSet` does. This is the risk named above; the render tests of 7.1 cover each container.
- **Front matter.** `propertiesTable.ts`: when source mapping is on, the properties `section` gets
  `data-okf-frontmatter-end-line="<closing fence line>"`, computed with `matchFrontmatterBlock`
  (`src/core/frontmatter/frontmatterParse.ts`) and passed with the field lines
  (`src/core/frontmatter/okfFrontmatter.ts`). Also added to `REMOVED_ATTRIBUTES`.

### 4.2 Placement order (`src/page/features/lineMarker.ts`)

`place(unfoldFirst)` becomes, in order:

1. **Block.** A line from 1 to the section's `data-okf-frontmatter-end-line` belongs to the properties
   section, whatever the distance to the first body block (fixes bug a). Otherwise the innermost
   mapped block holding the line (`containingBlock`, unchanged).
2. **Target.** Inside the block, the innermost element whose `data-okf-marker-line` to
   `data-okf-marker-end-line` holds the line, rows (`tr`) excluded; else the block itself.
3. **Open what hides it, with `unfoldFirst` only:** unfold the heading section and the closed
   dropdowns around the target (unchanged); select every hidden `.myst-tab-panel` around the target,
   itself included, outermost first (4.4); expand a collapsed properties table when the line has a
   property row (4.5). Measure once if anything opened.
4. **Hidden check.** The line is hidden, and the marker not drawn, when the target sits in a hidden
   tab panel, in a collapsed properties table on a row line, or (unchanged) folded away. A later
   placement (`place(false)`) opens nothing.
5. **Box,** in this order: the table row (4.3); the front matter row (4.5); a code line on a code
   block itself (4.6); a paragraph line, on a mapped paragraph (`entry.lineTops`) or on a target
   paragraph (`measureLineTops` on the target, its marker lines); the target's top with one line
   height when the target is not the block; else the block top (unchanged).
6. Draw, mark and scroll (unchanged). `aria-current="location"` and `data-sphinx-line-marker` stay on
   the entry's mapped element (the table or its container, the properties section, the tab panel,
   the tab set's outer panel), never on a row or a marker-line element.

A row box is the row's rectangle: `top` its `getBoundingClientRect().top + window.scrollY`, `height`
its height (a row with wrapped cells is marked over its whole height); the arrow stays centred on the
band (`src/core/preview/styles/lineMarkerStyles.ts` unchanged).

`measureLineTops` moves from `scrollCore.ts` to a new `src/page/modules/lineTops.ts` (document and
window passed in), imported by `scrollCore.ts` (its `@implements_req SwRS-MDOKFSTUDIO-LIFE-119`
moves with it) and `lineMarker.ts`. `pageRuntime.ts` (789 lines, limit 800) gains nothing: the tabs
are `rt.parts.tabs` (typed from `installTabs`), the properties table is reached through `state` and
`rt.input` (4.5). `lineMarker.ts` stays under 800 lines; if it grows past about 400, the placement
helpers go to `src/page/features/lineMarkerPlacement.ts`.

### 4.3 Table row

The rows are the `tr[data-okf-marker-line]` of the table holding the line (the entry when it is the
table, else the target `<table>` or the tables inside the target). The line of a row: that row. The
line after the header row's line (the delimiter line): the header row. No such row (a `{list-table}`,
a captioned `{table}`, a raw HTML table, a line past the last row): the top of the target or block,
as CR-445 does. The render test proves the rows' lines match the intake's rule: header on L, body row
n on L + n + 1.

### 4.4 A line in a hidden tab

- `src/page/modules/tabs.ts`: `TabsControl` gains `reveal(panel: Element): boolean`: it finds the
  `.myst-tab` of the panel's own set whose `aria-controls` is the panel's id and calls
  `select(tab, false)`: `chosenIndex` and, for a tab with a sync key, `chosenSync` are recorded, the
  sets of the same group follow, the focus does not move. It returns `true` when the shown tab
  changed. `@implements_req SwRS-MDOKFSTUDIO-MYST-099` there.
- `apply()` (fixes critic C1): today the group's `chosenSync` wins over the set's `chosenIndex`, so a
  revealed tab with no sync key, in a set whose group has another key chosen, is undone by the next
  content patch. `apply()` puts back, for each set, the later of the two choices: its own last
  selection or its group's last sync choice (a counter stamped on each `chosenIndex` and `chosenSync`
  entry). A click on a key-less tab follows the same rule.
- `installTabs(document, onChange?)`: `onChange` runs after any change of the shown tab (click, key,
  sync follow, `reveal`). `src/page/runtime.ts` passes `() => rt.scroll.stabilizeLayout()`, as it
  passes `keepReadingLine` to the chip toggle. That re-measures and emits `layoutMeasured`, so a
  keyboard tab change (or a set switched by its sync group) places the marker again: hidden while its
  tab is not shown, drawn again when it shows (decision 14). A pointer press already removes the
  marker (LIFE-179).
- `lineMarker.ts` step 3: `rt.parts.tabs.reveal(panel)` for each hidden panel around the target,
  outermost first (nested tab sets, decision 11). A tab set inside a closed dropdown or a folded
  section is unfolded first. Nothing is posted to the host, no editor opens.
- Then the exact line inside the shown panel (decision 7): a paragraph line by its measured wrapped
  line tops, a code line by its span, a table row by 4.3, any other element by its top.
- The `:::{tab-item}` line belongs to the panel (selects the tab); the `::::{tab-set}` line is the
  set's own block (its top, no tab selected).

### 4.5 Front matter row

- The box is the `tr[data-okf-field]` with `data-okf-line <= line <= data-okf-end-line` (a line in a
  multi-line value marks its row). No such row (a fence, a comment, a blank line, invalid YAML): the
  top of the properties section, as today. No properties table rendered: CR-445's nearest-block rule.
- Collapsed (decision 13): with `unfoldFirst` and a row for the line, `lineMarker.ts` sets
  `state.frontmatterCollapsed = false` and calls `rt.input.applyFrontmatterVisibility()`, the badge's
  path, then measures. A line with no row leaves the table collapsed and marks the section top (the
  title row stays visible). If the reader collapses the table later (by keyboard; a press removes the
  marker), the row line is hidden: not drawn until the table shows again, never re-expanded by a
  later placement.

### 4.6 Code lines only on a code block

`lineBox` counts `.myst-code-line` spans only on an element that is the code block itself: it holds
the spans and no descendant with `data-sphinx-source-line` or `data-okf-marker-line`. A tab panel
(whose content now carries marker lines) is never counted as a code block (fixes bug b). The span
index is counted back from that element's own end line (`codeSpanIndex`, unchanged).

### 4.7 Requirements (okfreq)

Per `requirements/guidelines/project.guidelines.md` ("During a change"). No `approved` requirement is
changed (all below are `proposed`).

- New SwRS in `lifecycle-sync`, deriving from `StRS-MDOKFSTUDIO-LIFE-023`, IDs from okfreq's next
  free number at the time of the change:
  - "The line marker marks the table row of the line": 4.3, the containers, the fallbacks.
  - "The line marker shows the hidden tabs that hold the line and marks its exact line": 4.4.
  - "The line marker marks the front matter property row of the line": 4.5, the collapsed table.
- `SwRS-MDOKFSTUDIO-LIFE-178`: "the top of the enclosing block" no longer covers a pipe table, a tab
  item or the front matter (pointing to the new SwRS); the boundary row "a line of a table, list or
  quote" becomes "a line of a list or a quote, or of a list-table, captioned table or raw HTML
  table"; the code rule says "of a code block itself".
- `SwRS-MDOKFSTUDIO-LIFE-179`: boundary rows "the reader shows another tab (keyboard or sync group):
  the marker is not drawn until its tab shows again" and "the reader collapses the properties table:
  not drawn until it shows again; a later placement never expands it".
- `SwRS-MDOKFSTUDIO-LIFE-180` (critic C2): boundary rows "a table row in edit mode (fixture line 43,
  body row 2; line 41 is the delimiter and marks the header row): the marker is on the row, its arrow
  meets no row handle" and "a property row and a line in a tab panel in edit mode: the arrow meets no
  control, no editor opens".
- `SwRS-MDOKFSTUDIO-MYST-098`: boundary row "the content of a tab item carries marker lines; a click
  in it still edits the whole item".
- `SwRS-MDOKFSTUDIO-MYST-099`: boundary rows "the line marker selects a tab the way a click does
  (sync group followed, no focus move)" and "after a content patch each set shows its later choice:
  its own selection or its group's sync choice".
- `SwRS-MDOKFSTUDIO-FMSCHEMA-090`: boundary row "a requested line on a property row expands a
  collapsed table; any other line leaves it collapsed".
- Markers at the code points (`lineMarker.ts`, `tabs.ts`, `mystNode.ts`, `mystGridToctree.ts`,
  `mystTables.ts`, `propertiesTable.ts`, `lineTops.ts`) and `@tests_req` at each test, at most 3 IDs
  per marker block. `just requirements-update`, a dated entry in `requirements/tiers/log.md`.

### 4.8 Docs and vocabulary

- `docs/user/open-studio.md`, "Open at a line": line 31 corrected to LIFE-179 (decision 15): the
  arrow stays while you scroll and goes on your next click in the page, when you start an edit, or
  when another line is asked. Then one sentence: in a table the arrow marks the row; a line in a tab
  that is not shown opens that tab first; a front matter line marks its property's row and opens the
  properties table if it was collapsed.
- `CHANGELOG.md`, "Unreleased": one entry in the same voice.
- `.agents/glossary/common.md`, "Line marker": it marks a table row or a front matter property row
  when the line is one; add "marker line" (`data-okf-marker-line`: a source line for the line marker
  only, never a block).
- The writing skill is not touched: no rendered syntax changes.

## 5. Out of scope

- The marker's look, its other lifetime rules and its edit-mode placement rules (CR-445).
- Rows of a `{list-table}`, a captioned `{table}` and a raw HTML table (decision 10).
- Making the content of a tab item, or a table row, a block of its own (a click target): marker
  lines are never mapped.
- Any host-side, setting or opening-policy change.

## 6. Overlap with CR-456 side-preview-jump-marker

CR-456 (batch-07, pending; spec final) shows the same marker in the side preview on a jump: every
`Command` selection change with one selection marks (its decisions 4 and 6; VSCodeVim moves are a
written known limit). It reuses `lineMarker.ts` and LIFE-178 to LIFE-180 with no page code change.

- Behaviour (critic C6): once both are in, every jump marked in the side preview takes this CR's
  placement: it selects hidden tabs (and switches their sync group, recording the choice for the
  page's later patches), expands a collapsed properties table, and marks table rows. Since CR-456
  marks every `Command` move (F3, F8, Go to Symbol, Go Back), such moves in the text editor will
  switch tabs and open the properties table in the side preview too. The file never changes. CR-456's
  evidence should name LIFE-178 plus this CR's SwRS as the placement.
- Files both touch: `test/visual/lineMarkerScenarios.ts` (scenario ids `lifecycle-sync/vNN-…`),
  `requirements/tiers/swrs/lifecycle-sync/` (next free LIFE ids), `SwRS-MDOKFSTUDIO-LIFE-178` to
  LIFE-180, `requirements/tiers/log.md`, `docs/user/open-studio.md` ("Open at a line"; this CR
  rewrites line 31), `CHANGELOG.md`, `.agents/glossary/common.md`. This CR lands last: it rebases on
  CR-456 and renumbers its scenario and SwRS ids.
- `lineMarker.ts`: changed by this CR only, unless CR-456's trials change the page; then the PRs
  stack per `.agents/guidelines/stacked-prs.guidelines.md`.

## 7. Evidence

No host or default dependency (no setting, no host API): no host and default matrix. No CI job
changes. The visual scenarios read the shipped fixtures from the repository at the head under test.

### 7.1 Render and contract tests (first: the page work relies on them)

- New `test/core/render/markerLines.test.ts`, rendering real Markdown through the renderer:
  - a top-level pipe table, one in a blockquote, one in a GitHub alert, one in a `:::{note}` and a
    `:::{admonition}`, one in a list item, one in a tab item, one at the end of the file and one after
    a front matter: each `<tr>` carries `data-okf-marker-line` = header line L, body row n = L + n + 1;
  - a `{list-table}`, a captioned `{table}` and a raw HTML table: no row line;
  - a tab set whose second item holds a soft-wrapped paragraph, a fenced code block, a table and a
    nested tab set: each carries whole-file marker lines; none carries `data-line` or
    `data-sphinx-source-line`; the item's panel stays the only mapped block (MYST-098);
  - CRLF text gives the same lines.
- `test/core/frontmatter/propertiesTable.test.ts`: `data-okf-frontmatter-end-line` on the closing
  fence (1 line and several, CRLF), none without source mapping.
- `test/core/export/htmlExport.test.ts`: the export strips the three new attributes.
- The existing click tests of a tab item (MYST-098) pass unchanged; one assertion added: a click on a
  paragraph inside a tab item opens the whole item's editor.

### 7.2 Page tests

- `test/page/runtimeLineMarker.test.ts` (305 lines; test limit 1500), harness
  `test/page/runtimeHarness.ts` extended for rows and marker-line elements:
  - table: line L marks the header row (top and height), L+1 the header row, L+3 body row 2; a table
    in a quote (the quote is the mapped block): its row; a list-table shape (no row lines) and a line
    past the last row: the block top; `aria-current` on the mapped block;
  - replaces "a line inside a hidden tab of a tab-set marks the tab-set top and selects no tab": a
    line of a paragraph in a hidden panel selects its tab (panel not `hidden`, tab
    `aria-selected="true"`), marks the exact wrapped line, posts no host message; a code line in it
    marks its span; a nested hidden tab: both tabs selected, outermost first; a tab set in a closed
    dropdown: opened then selected; a re-render keeps the tab and the marker; the reader shows
    another tab by keyboard: the marker is not drawn, and is drawn again when the tab shows; a later
    placement selects nothing; the `{tab-set}` line selects nothing;
  - front matter: a key line marks its row; a line inside a list value its row; the fence and a
    comment line the section top (the existing test stays); a 20-line front matter, first body block
    on line 22, line 19 on no row: the section, not the body block; a collapsed table and a row line:
    expanded (`state.frontmatterCollapsed` false, `aria-expanded="true"` on the toggle), row marked;
    a collapsed table and the fence line: stays collapsed, section top; collapsed again by the reader:
    not drawn, a later placement does not expand it;
  - code (bug b): a tab panel with a code block then a paragraph: a paragraph line is not put on a
    code span; the existing code-line tests stay green.
- `test/page/modules/tabs.test.ts`: `reveal(panel)` shows the tab, returns `true`, then `false`; the
  focus does not move; "the other set of the group follows; a set of another group does not";
  `onChange` runs on click, key, sync follow and reveal; C1: a group with key A chosen, reveal a
  key-less tab of a set that has an A tab, then `apply()`: the revealed tab stays; reveal a tab with
  key B, then `apply()`: every set of the group shows B.
- A unit test of `src/page/modules/lineTops.ts` replaces nothing: the LIFE-119 tests of
  `scrollCore.ts` stay green through the moved function.

### 7.3 Visual captures (`test/visual/lineMarkerScenarios.ts`, group `lifecycle-sync`, 900 px)

- `v08-line-marker-table-line-dark-900` (line 43 of `91-line-marker.md`, the `beta` row): the
  marker's top and height match the `beta` row within 3 px; `table[aria-current='location']` count
  1; the description says "marks the row".
- `v06-line-marker-edit-mode-light-900` (same line, edit mode; C2): the marker is on the `beta` row
  and its arrow meets no row handle (the row's own handle is centred on the same height).
- New fixture `test/visual/fixtures/93-line-marker-precision.md` (or the next free number): a front
  matter with a one-line key, a list value over three lines and a comment; a pipe table in a quote and
  one in a `:::{note}`; a `{tab-set}` whose second item (not selected) holds a soft-wrapped
  paragraph, a long numbered code block and a nested `{tab-set}` whose second tab holds a line. New
  scenarios, next free `vNN`, each with "one marker", "inside the viewport" and its position within
  3 px: the delimiter line marks the header row (light); a body row of the quoted table (dark) and of
  the note's table (light); the third wrapped line of the paragraph in the hidden tab (light) and a
  code line there (dark); the line in the nested hidden tab (light); a line of the list value marks
  its row (dark); the comment line marks the section top (light); C4, edit mode (dark): on a property
  row and on a line in a tab panel, the arrow meets no control (row handle, list handle, block
  action, properties controls) and no `textarea` opens.
- The PR's Impacts section shows before (1.11.0) and after captures, light and dark, per
  `.agents/guidelines/pull-request.guidelines.md`.

### 7.4 Gate

`just check`, `just requirements-update`, `just requirements-lint`, then `just preflight` (on Windows
the static stage; CI runs the visual job on the PR). No real VS Code path changes: the heavy CI run is
not required by this CR.

## 8. Commits and PR

`feat(render)` for the marker lines and the placement (two commits: the renderer, then the page),
per `.agents/guidelines/git-commit-message.guidelines.md` and its allowed scopes; the PR per
`.agents/guidelines/pull-request.guidelines.md`, listing the SwRS added or changed with their source
and test files, and saying the renderer risk and its render tests in the body.

## 9. Delivery

Into the running batch-07 once final and ready (owner, 2026-11-21), landing last in the batch, after
CR-456 (decision 16).

## 10. Open questions for the owner

None.
