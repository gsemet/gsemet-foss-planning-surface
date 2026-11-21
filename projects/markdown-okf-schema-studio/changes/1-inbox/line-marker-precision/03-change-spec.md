# Line marker on the table row, the hidden tab and the front matter row

When Studio opens at a requested line and marks it (the arrow in the left margin and the light band
of CR-445 open-at-line-marker), the marker becomes precise in three places that CR-445 leaves at the
top of the enclosing block: a table marks the row of the line, a line in a tab that is not shown
selects that tab first and is then marked, and a front matter line marks its property's row in the
properties table.

Origin: verbal (owner, 2026-11-21). No tracker issue. Split off from CR-445 (decision 31). Code base:
`origin/main` at `5a84db8b` (release 1.11.0, which ships CR-445).

## 1. Goal, in the user's terms

- I search a word that sits in a table row and click the result: Studio opens with the arrow on
  that row, not on the top of the table.
- I search a word that sits in the second tab of a tab set: Studio shows that tab, then the arrow
  marks the line, as it already does for a folded section or a closed dropdown.
- I search a property of the front matter (`owner: alice`): the arrow marks the `owner` row of the
  properties table. A front matter line that is no property (the fences, a comment) marks the top
  of the properties table, as today.

## 2. Facts at 1.11.0 (the code this CR changes)

- The marker is `src/page/features/lineMarker.ts` (`installLineMarker`, 209 lines): `reveal(line)`
  runs `place(true)`, which finds the innermost mapped block holding the line (`containingBlock`,
  hidden blocks included), unfolds it (`unfold`: `rt.parts.headingFold.reveal`, `details.open`),
  measures again (`rt.scroll.measure()`), takes `rt.scroll.entryForLine(line)` from the visible
  layout, and draws the box `lineBox(entry, line)`: a code line (`.myst-code-line` spans counted back
  from the block's end line, `codeSpanIndex`), a soft-wrapped paragraph line (`entry.lineTops`), else
  the block top with one line height. `mark()` puts `data-sphinx-line-marker` and
  `aria-current="location"` on the entry's element. Later placements (`layoutMeasured`) call
  `place(false)`, which never unfolds. SwRS LIFE-178 (placement), LIFE-179 (lifetime), LIFE-180 (edit
  mode), all `proposed`.
- Tables: a top-level pipe table is one mapped block (the `<table>` carries
  `data-sphinx-source-line` = its header line and `data-sphinx-source-end-line`; its `<tr>` carry no
  line). A table inside a quote or an admonition is no block of its own (the container is;
  `src/page/modules/tableInContainer.ts` ranks it); a `{list-table}` strips the lines of its content
  (`stripSourceLines`, `src/core/render/mystTables.ts`) and sits in a `<figure>`.
- Tab sets: `buildTabSet` (`src/core/render/mystGridToctree.ts`) maps the `.myst-tab-set` and each
  `.myst-tab-panel` (`sourceProperties(item)`, from the `{tab-item}` line); a panel not shown has
  `hidden`. `unmapPlainBlocks` drops the lines of everything inside a tab item (a paragraph, a code
  block, a table or a nested tab set in it is no block). Selection lives in the page:
  `src/page/modules/tabs.ts` (`installTabs`, `select`, `chosenIndex`, `chosenSync`, `apply()` puts
  the choices back after a content patch); it is `rt.parts.tabs` (`TabsControl`). Today a line in a
  hidden panel marks the `.myst-tab-set` top and selects no tab (test "a line inside a hidden tab of
  a tab-set marks the tab-set top and selects no tab").
- Front matter: `renderPropertiesTable` (`src/core/frontmatter/propertiesTable.ts`) maps the
  `section[data-okf-properties]` at line 1 only (no end line). Each field row
  `tr[data-okf-field]` carries `data-okf-line` and `data-okf-end-line` (1-based, whole file,
  inclusive: from the key's line to the value's last line; `frontmatterFieldLines`,
  `src/core/frontmatter/frontmatterChanges.ts`, SwRS REVIEW-215), only when source mapping is on and
  the YAML is a valid mapping. The table can be collapsed by its toggle (`state.frontmatterCollapsed`,
  `html[data-okf-frontmatter-collapsed]`, SwRS FMSCHEMA-090, `src/page/features/pageInput.ts`); the
  issue badge expands it before jumping to a row (`pageInput.ts`, the `[data-okf-badge]` handler).
- Found while reading, both reached by this CR:
  - Since the properties section has no end line, a front matter line is matched to the nearest
    block by distance (`entryForLine`): in a long front matter, a line near its closing fence is
    closer to the first body block and the marker goes there.
  - `lineBox` counts code spans back from the entry's end line whenever the entry holds
    `.myst-code-line` spans and no mapped block. A shown tab panel holding a code block followed by
    a paragraph is such an entry: a line of the paragraph or of the code is put on the wrong code
    line.

## 3. Decisions

| # | Decision | Source | Where |
| --- | --- | --- | --- |
| 1 | One CR for the three places: the table row, the hidden `{tab-item}` (selected first, like an unfold) and the front matter property row (else the top of the properties table) | 02-answers lm-Q1 ("Les 3 ensemble") | the whole spec |
| 2 | The marker is CR-445's (merged in 1.11.0): same look, same lifetime, same edit mode; only its placement changes | 02-answers lm-Q1 | 4 |
| 3 | Table: the header row on the table's first line, the delimiter line to the header row, body row n on the table's first line plus n+1 | intake/request.md | 4.2 |
| 4 | A line in a non-selected `{tab-item}` of a `{tab-set}`: select that tab first, like an unfold, then mark the line | intake/request.md | 4.3 |
| 5 | A front matter line: the property's row in the properties table, else the top of the table | intake/request.md | 4.4 |
| 6 | Once final and ready, the CR goes into the running batch-07 | 02-answers (owner, 2026-11-21) | 9 |

CR-445's decisions 6 (look), 7 (lifetime), 8 and 31 (precision: exact paragraph and code line,
unfold), 16 (edit mode) and 17 (nothing in the side preview from CR-445 itself) still hold; this CR
narrows decision 31's "otherwise the top of the enclosing block" for the three places above.

## 4. What changes

### 4.1 Placement order (`src/page/features/lineMarker.ts`)

`place(unfoldFirst)` becomes, in order:

1. The innermost mapped block holding the line (`containingBlock`, unchanged), except a front
   matter line (4.4), which takes the properties block by its own range.
2. With `unfoldFirst`: unfold the heading section and the closed dropdowns (unchanged), then select
   every hidden tab around the block (4.3); measure again once if anything opened.
3. The entry (`rt.scroll.entryForLine`) and the hidden check (unchanged, plus 4.3's rule for a later
   placement).
4. The box, `lineBox`, in this order: a table row (4.2); a front matter row (4.4); a code line (4.5);
   a paragraph line (unchanged); else the top of the block with one line height (unchanged).
5. Draw, mark, scroll (unchanged). `aria-current="location"` and `data-sphinx-line-marker` stay on
   the mapped block (the `<table>`, the properties `section`, the tab panel), never on a row.

A row box is the row's own rectangle: `top` = its `getBoundingClientRect().top + window.scrollY`,
`height` = its height (a row whose cells wrap is marked over its whole height); the arrow stays
centred on the band (`src/core/preview/styles/lineMarkerStyles.ts` unchanged). The file stays under
the 800-line limit; `src/page/features/pageRuntime.ts` (789 lines) gains nothing (`rt.parts.tabs`
is already typed from `installTabs`).

### 4.2 Table row

Applies when the entry's element is a `<table>` (or holds exactly one `<table>`, a `.table-wrapper`)
that is a pipe table laid out as its lines say: one header row (`tHead.rows.length === 1`, or the
first row when there is no `<thead>`) and `endLine - sourceLine === 1 + bodyRowCount`. With `L` the
table's first line (`entry.sourceLine`):

- line `L`: the header row;
- line `L + 1` (the delimiter line): the header row;
- line `L + n + 1`, n >= 1: body row n (`tBodies[0].rows[n - 1]`);
- any other case (a row that is missing, a count that does not match): the table top, as CR-445
  does.

The count check keeps a `{list-table}`, a `{table}` directive with a caption and a raw HTML table
at the top of their block (their lines do not match their rows). Whether those, and a table inside
a quote, an admonition, a list item or a tab item, should get the row too is Q1; this CR covers the
top-level pipe table. The Driver proves the attributes with a render test: a rendered pipe table
has `data-sphinx-source-line` on its header line and `data-sphinx-source-end-line` on its last row
line (with a trailing blank line and at the end of the file).

### 4.3 A line in a hidden tab

- `src/page/modules/tabs.ts`: `TabsControl` gains `reveal(panel: Element): boolean`. It finds the
  tab of `panel` in the panel's own set (the `.myst-tab` whose `aria-controls` is the panel's id),
  shows it the way a click does (`show`, and `chosenIndex` recorded, so `apply()` keeps it after a
  content patch or a re-render), never moves the focus, and returns `true` when the shown tab
  changed. Whether the selection also switches the other tab sets of the same sync group, as a
  click does (`chosenSync`), is Q3. `@implements_req` of the new SwRS (4.6) on it.
- `lineMarker.ts`, step 2 with `unfoldFirst`: for the block and each of its ancestors that is a
  `.myst-tab-panel` with `hidden`, from the outermost to the innermost, `rt.parts.tabs.reveal(panel)`.
  A tab set inside a closed dropdown or a folded section is unfolded first, then its tab selected.
  The selection posts nothing to the host (no edit, the file never changes) and opens no editor.
- Then the line is marked inside the shown panel. The panel is the entry: its content carries no
  source line (`unmapPlainBlocks`), so CR-445's rules put the marker at the panel's top. Whether the
  marker should instead sit on the exact paragraph or code line inside the tab is Q2.
- The line on the `:::{tab-item}` line itself belongs to the panel's range: it selects the tab too.
  The line on the `::::{tab-set}` line is the set's own block: its top, no tab selected.
- A later placement (`place(false)`) never selects a tab, as it never unfolds. If the reader then
  shows another tab without a pointer press (the keyboard; a press removes the marker already),
  what the marker does is Q6.
- A tab set nested in a tab item has no source lines; selecting its hidden tab is Q4. This CR selects
  only mapped panels.

### 4.4 Front matter row

- `src/core/frontmatter/propertiesTable.ts`: when source mapping is on, the properties `section`
  also carries `data-okf-frontmatter-end-line="<line of the closing fence>"` (1-based, whole file),
  computed with the front matter block (`matchFrontmatterBlock`, `src/core/frontmatter/frontmatterParse.ts`)
  and passed in the result the table renders from (`src/core/frontmatter/okfFrontmatter.ts`, next to
  the field lines). A separate attribute, so scroll sync, clicks and `markSourceLine` keep reading
  the section as today. `src/core/export/exportContent.ts` strips it with the other `data-okf-line`
  attributes (`REMOVED_ATTRIBUTES`).
- `lineMarker.ts`: a line from 1 to that end line belongs to the properties section, whatever the
  distance to the first body block (fixes the nearest-block slip of section 2). The box is the
  `tr[data-okf-field]` whose `data-okf-line <= line <= data-okf-end-line` (a line inside a multi-line
  value marks its row); a line with no such row (a fence, a comment, a blank line, invalid YAML, no
  line attributes) marks the top of the properties section, as CR-445 does today. No properties
  table rendered: CR-445's nearest-block rule, unchanged.
- A collapsed properties table (the reader pressed its toggle on a Studio tab that then receives a
  jump): expand it like an unfold, as the issue badge does, then mark the row; or mark the section
  top and leave it collapsed: Q5. A freshly opened tab is always expanded (FMSCHEMA-090).

### 4.5 Code lines only in a code block

`lineBox` counts `.myst-code-line` spans only when the entry is the code block itself (its element is
the code block's own element, not a tab panel or another container that happens to hold one code
block and no mapped block). A container entry falls through to the paragraph and block-top rules.
This keeps 4.3 from putting a tab's line on a wrong code line (section 2).

### 4.6 Requirements (okfreq, `lifecycle-sync`)

Per `requirements/guidelines/project.guidelines.md` ("During a change"). No `approved` requirement
is changed (LIFE-178, LIFE-179, LIFE-180, MYST-098, MYST-099, FMSCHEMA-090, REVIEW-215 are
`proposed`).

- New SwRS, deriving from `StRS-MDOKFSTUDIO-LIFE-023`, IDs taken with okfreq's next free number at
  the time of the change:
  - "The line marker marks the table row of the line": the rule of 4.2, its fallbacks.
  - "The line marker selects the hidden tab that holds the line": 4.3 (and Q3, Q4 as answered).
  - "The line marker marks the front matter property row of the line": 4.4 (and Q5 as answered).
- `SwRS-MDOKFSTUDIO-LIFE-178`: description and boundary table: "the top of the enclosing block" no
  longer covers a pipe table, a hidden tab or the front matter; they point to the new SwRS. The
  "a line of a table, list or quote" row becomes "a line of a list or quote, or of a table other
  than a pipe table". The code-line rule says "of a code block itself" (4.5).
- `SwRS-MDOKFSTUDIO-LIFE-179`: the tab row of Q6 as answered.
- Markers: `@implements_req` at the new code points (`lineMarker.ts`, `tabs.ts`,
  `propertiesTable.ts`), `@tests_req` at each test (section 7), at most 3 IDs per marker block.
- `just requirements-update`, a dated entry in `requirements/tiers/log.md`.

### 4.7 Docs and vocabulary

- `docs/user/open-studio.md`, "Open at a line": one sentence: in a table the arrow marks the row; a
  line in a tab that is not shown opens that tab first; a front matter line marks its property's row.
- `CHANGELOG.md`, "Unreleased": one entry in the same voice.
- `.agents/glossary/common.md`, "Line marker": add that it marks a table row or a front matter
  property row when the line is one.
- The writing skill (`skills/writing-for-markdown-okf-schema-studio/`) is not touched: no rendered
  syntax changes.

## 5. Out of scope

- The look, the lifetime (except Q6) and the edit mode rules of the marker (CR-445).
- Tables other than a top-level pipe table, unless Q1 says otherwise.
- The exact line inside a tab item (Q2) and nested tab sets (Q4), unless answered otherwise.
- The side preview's own trigger (CR side-preview-jump-marker, section 6).
- Any host-side, setting or opening-policy change: this CR is page and renderer only.
- `docs/user/open-studio.md` says the arrow goes on a scroll, which contradicts LIFE-179 (it stays):
  not fixed here (a separate finding for the Chief of Staff).

## 6. Overlap with CR side-preview-jump-marker

That CR (inbox, being specified, also bound for batch-07) shows the same marker in the side preview
on a jump and states "no page code changes": it reuses `lineMarker.ts` and LIFE-178 to LIFE-180 as
they are. Hence:

- Behaviour: whichever merges first, the side preview inherits this CR's placement (table row, tab
  selection, front matter row), since both pages run the same feature. Nothing to add for it here;
  its own evidence should say the placement is LIFE-178 plus this CR's SwRS when both are in.
- Files both touch: `test/visual/lineMarkerScenarios.ts` (both add scenarios: scenario ids
  `lifecycle-sync/vNN-line-marker-…` must not collide; the second to merge renumbers),
  `requirements/tiers/swrs/lifecycle-sync/` (both add SwRS: same next free LIFE ids; the second to
  merge renumbers and runs `just requirements-update`), `SwRS-MDOKFSTUDIO-LIFE-178` and LIFE-179
  (this CR edits their text, the other cites them), `requirements/tiers/log.md`,
  `docs/user/open-studio.md` ("Open at a line"), `CHANGELOG.md` and possibly
  `.agents/glossary/common.md`.
- `lineMarker.ts` itself: changed only by this CR, unless the other CR's trials make it change the
  page; then the two PRs stack per `.agents/guidelines/stacked-prs.guidelines.md`.

## 7. Evidence

No host or default dependency (no setting, no host API): no host and default matrix. No CI job
changes. The visual scenarios read the shipped fixture from the repository at the head under test.

### 7.1 Unit and contract tests

- `test/page/runtimeLineMarker.test.ts` (305 lines; the test limit is 1500), with the harness of
  `test/page/runtimeHarness.ts` extended for table rows and properties rows as needed:
  - table: line L marks the header row's top and height; line L+1 the header row; line L+3 body
    row 2; a line past the last row and a table whose line count does not match its rows (a
    list-table shape) mark the table top; `aria-current` on the `<table>`;
  - replaces "a line inside a hidden tab of a tab-set marks the tab-set top and selects no tab":
    a line in a hidden panel selects its tab (the panel is no longer `hidden`, its tab
    `aria-selected="true"`), marks the panel's top (or per Q2), `aria-current` on the panel, posts
    no `previewEdit` and no other host message; a re-render keeps the tab (through `tabs.apply()`)
    and the marker; a later placement selects nothing; a tab set inside a closed dropdown: the
    dropdown opens and the tab is selected; the `{tab-set}` line itself selects nothing;
  - front matter: a key line marks its row; a line inside a multi-line value (a list) marks its
    row; the opening fence and a comment line mark the section top (the existing test "a front
    matter line marks the top of the front matter block" stays); a front matter of 20 lines with
    the first body block on line 22: line 19, on no row, marks the section, not the body block; a
    collapsed table per Q5;
  - code: a tab panel with a code block then a paragraph: a line of the paragraph is not put on a
    code span (4.5); the existing code-line tests stay green.
- `test/page/modules/tabs.test.ts`: `reveal(panel)` shows the panel's tab, returns `true`, then
  `false` when called again; the choice survives `apply()`; the focus does not move; the sync group
  per Q3.
- `test/core/frontmatter/propertiesTable.test.ts`: the section carries
  `data-okf-frontmatter-end-line` on the closing fence (front matter of 1 line and of several,
  CRLF text), none without source mapping; the export strips it
  (`test/core/export/htmlExport.test.ts`).
- A render test, `test/core/render/lineMarkerTableLines.test.ts` (new): the mapped lines of a
  rendered pipe table (4.2).

### 7.2 Visual captures (`test/visual/lineMarkerScenarios.ts`, group `lifecycle-sync`, 900 px)

- `v08-line-marker-table-line-dark-900` (line 43 of `91-line-marker.md`, the `beta` row): the
  marker's top and height match the `beta` row (within 3 px), `table[aria-current='location']`
  count 1; its description says "marks the row".
- `v06-line-marker-edit-mode-light-900` (same line, edit mode): unchanged assertion that the arrow
  meets no row handle, now on the row whose handle is centred on the same height.
- A new fixture `test/visual/fixtures/93-line-marker-precision.md` (or the next free number when
  the change is made): a front matter with a one-line key, a list value over three lines and a
  comment; a `{tab-set}` whose second `{tab-item}` is not selected, holding a paragraph and a code
  block; a pipe table. New scenarios, next free `vNN`: the delimiter line of the table marks the
  header row (light); a line of the second tab: the tab is shown and the marker sits in its panel
  (light, and dark once); a line of the list value marks its property row (dark); the comment line
  marks the top of the properties table (light).
- The PR's Impacts section shows before (1.11.0) and after captures, light and dark, per
  `.agents/guidelines/pull-request.guidelines.md`.

### 7.3 Gate

`just check`, `just requirements-update`, `just requirements-lint`, then `just preflight` (on Windows
the static stage; CI runs the visual job on the PR). The change touches no real VS Code path: the
heavy CI run is not required by this CR.

## 8. Commits and PR

`feat(render)` for the placement, the tab reveal and the front matter attribute, per
`.agents/guidelines/git-commit-message.guidelines.md` and its allowed scopes; the PR per
`.agents/guidelines/pull-request.guidelines.md`, listing the SwRS added or changed with their source
and test files, and the answers to the questions below.

## 9. Delivery

Into the running batch-07 once final and ready (owner, 2026-11-21).

## 10. Open questions for the owner

- **Q1 (other tables).** Should the row also be marked for a table inside a quote, an admonition, a
  list item or a tab item, a `{list-table}`, a `{table}` directive with a caption and a raw HTML
  table, or do those keep the top of their enclosing block? A row for them needs the renderer to
  give each row its source line, which it does not today.
- **Q2 (line inside the shown tab).** Once the tab is selected, should the marker sit on the exact
  paragraph or code line inside the tab, or on the top of the tab's panel? The exact line needs line
  data on the tab's content, which today carries none so that a click edits the whole tab item.
- **Q3 (sync group).** Selecting the tab for the marker: also switch the tab sets of the same sync
  group, as a click on the tab does, or only the tab set that holds the line?
- **Q4 (nested tab set).** A line in a hidden tab of a tab set nested inside a tab item: select the
  inner tab too, or only the outer one?
- **Q5 (collapsed properties table).** When the reader collapsed the properties table and a jump to
  a property line arrives: expand the table like an unfold (as the issue badge does) and mark the
  row, or mark the top of the collapsed table and leave it collapsed?
- **Q6 (the reader shows another tab).** After the marker selected a tab, the reader shows another
  tab with the keyboard: hide the marker until its tab shows again (what LIFE-179 says for a section
  the reader folds), or move it to the top of the tab set?
