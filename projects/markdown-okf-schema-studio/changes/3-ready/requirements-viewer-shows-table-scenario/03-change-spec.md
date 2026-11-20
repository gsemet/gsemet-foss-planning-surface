# Requirements viewer shows table scenarios, not empty columns

Short name: `table-scen`. Origin: verbal, the owner on 2026-11-20 (no GitHub issue).

## Goal

On the published requirements site, a behaviour page shows each scenario of the SwRS in a card
(click to open). Today, when the source writes the scenario as a table (`| Input | Outcome |`),
the card opens on three empty columns, GIVEN, WHEN and THEN. The owner saw it on
SwRS-MDOKFSTUDIO-BLOCK-130 ("les scenario sont vide").

After this change, a reader who opens a scenario card sees what the source says:

- a table scenario shows its table, with the headers the source uses;
- a list scenario (GIVEN / WHEN / THEN / AND lines) shows the three columns, exactly as today;
- a scenario with both shows both, in source order, and a note line under the heading is shown as
  a paragraph;
- no card is ever empty when its source section has content.

Scale, measured on `main` at `a18bcac1`: 421 SwRS files under `requirements/tiers/swrs/` hold at
least one table scenario (the intent says 343; the count grew since). Of 3 799 scenario sections,
about 7 000 table lines, 8 500 step lines, 185 prose lines and 19 non-step bullet lines. No
StRS holds a table scenario.

## Cause

`parseScenarios` in `test/site/requirementsViewer/model.ts` keeps only the lines
`- GIVEN|WHEN|THEN|AND ...` (and indented continuation lines of a step). Every other line under a
`### Scenario` heading is dropped. `scenarioColumns` in `test/site/requirementsViewer/pages.ts`
then always draws the three columns, empty when there are no steps.

## What changes

### 1. The model: `test/site/requirementsViewer/model.ts`

- `Scenario` keeps `kind`, `name` and `steps` (all GIVEN / WHEN / THEN / AND lines, as today: the
  home page example `exampleFrom` and `layout.ts` read it unchanged). It gains
  `blocks: readonly ScenarioBlock[]`, the content of the section in source order:
  - `{ type: "steps"; lines: string[] }`: a run of step lines (with their joined continuation
    lines), the same strings as in `steps`;
  - `{ type: "table"; header: string[]; rows: string[][] }`: one Markdown table;
  - `{ type: "note"; text: string }`: a prose paragraph or a non-step bullet.
- `parseScenarios` fills `blocks` with these rules:
  - Section bounds are unchanged: from `### Scenario (kind): name` to the next heading of level 1
    to 3, and never past `<!-- okf:links:start -->`.
  - A step line `- GIVEN|WHEN|THEN|AND ...` goes to the current `steps` block, or opens one.
  - A line whose first non-blank character is `|` is a table line. A run of consecutive table
    lines is one table. Its first line is the header. A separator line right after it (cells made
    of `-` with optional `:`, for example `| --- | :---: |`) is skipped. Every other line is a row.
  - Cells are split on `|` that are not escaped; the leading and trailing pipe are optional; each
    cell is trimmed; `\|` in a cell becomes `|` (89 table lines of the bundle carry `\|`).
    Rows keep their cell count as written: no padding, no cut.
  - An indented line (two spaces or more) continues the last step or the last note, joined with a
    space, as continuation lines of steps are today (a blank line between them keeps the current
    step behaviour: it still joins).
  - A non-step bullet line (`- text` or `* text`) is a note whose text is the line without its
    marker.
  - Any other non-blank line is prose: consecutive prose lines form one note, ended by a blank
    line, a step, a table line or a bullet.
- HTML entities (answers, Q7): the parser decodes `&lt;`, `&gt;`, `&amp;` and `&quot;` in every
  step line, note text, header and cell, so the stored text is what GitHub shows. One pass with one
  regular expression (`/&(lt|gt|amp|quot);/gu`), so `&amp;lt;` becomes `&lt;`, not `<`. Other
  entities stay as written. The page escapes the decoded text as it does today, so nothing the
  source writes becomes markup. The answers count 7 step lines of the bundle whose display changes
  (for example `&lt;b&gt;` now shows `<b>`, as on GitHub); `steps` carries the decoded lines too,
  so the home page example shows the same text as the card.
- `parseScenarios`'s doc comment says it reads steps, tables and notes and decodes the basic
  entities. It carries `// @implements_req SwRS-MDOKFSTUDIO-CORE-082`, since it produces the new
  reading (it has no marker today).

### 2. The page: `test/site/requirementsViewer/pages.ts`

- The body of a scenario card (`<details class="scn">` in `behaviourPage`) renders `blocks` in
  order, instead of always one `<div class="gwt">`:
  - a `steps` block renders the existing `<div class="gwt">` with its three columns, through
    `scenarioColumns`, with the same markup as today (a list-only scenario's HTML does not change);
  - a `table` block renders
    `<div class="scn-table"><table><thead><tr><th>..</th></tr></thead><tbody><tr><td>..</td></tr></tbody></table></div>`,
    headers and cells escaped with `escapeHtml`, every cell plain text (answers, Q6: no `<br>` rule;
    the only `<br>` of the bundle is an element name in code, in CORE-071);
  - a `note` block renders `<p class="scn-note">..</p>`, escaped.
- A scenario with no block at all (a heading with nothing under it; the bundle has none today)
  renders `<p class="hint">No text under this scenario in the source.</p>` in the card, so no card
  is ever blank.
- Export the function that renders one scenario card body (name it `scenarioBody(scenario)`), so
  the bundle guard of section 5 renders cards the same way the page does. It carries
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-082`.

### 3. The style: `test/site/requirementsViewer/viewer.css`

- `.scn-table`: border-top `1px solid var(--line)`, `overflow-x: auto` so a wide table scrolls
  inside the card on a narrow screen.
- `.scn-table table`: full width, collapsed borders, 14px text like `.gwt div`; `th` styled like
  the column labels of `.gwt b` (600 11px `var(--sans)`, uppercase, `var(--soft)`), left aligned;
  `th` and `td` with `10px 14px` padding and a bottom border `1px solid var(--line)`, the last row
  without it; cells aligned top.
- `.scn-note`: `padding: 10px 14px; margin: 0; font-size: 14px; border-top: 1px solid var(--line)`.
- The existing colours and variables only; no new colour.

### 4. The fixture and the unit tests

- `test/site/requirementsViewer/fixture.ts`: give `SwRS-X-014` (active, gfm, derived from
  `StRS-X-003`, not on any map, so no walk or scenario count of the existing tests moves) a `text`
  with two scenarios:
  - `### Scenario (nominal): Table only`, a table with the headers `Input | Outcome`, its
    separator line, two rows, one cell holding `` `a \| b` `` (escaped pipe in inline code) and
    one cell holding `&lt;b&gt; &amp;lt;` (entities);
  - `### Scenario (boundary): Steps, note and table`: a GIVEN / WHEN / THEN list, then a prose
    note line, then a non-step bullet, then a table with three headers (`Given | When | Then`,
    shown as a table, not converted).
- `test/site/requirementsViewer/model.test.ts`, a new test "the model reads table scenarios, notes
  and mixed scenarios in source order": blocks and their order for both scenarios of `SwRS-X-014`;
  header and rows; the escaped pipe read as `|`; the separator line skipped; the note and the
  bullet text; `steps` of the mixed scenario equal to its three step lines; the entity cell read as
  `<b> &lt;` (decoded once); a step line and a note with `&quot;x&quot;` read as `"x"`; the existing
  `SwRS-X-011` scenario has exactly one `steps` block with the same lines as `steps`.
- `test/site/requirementsViewer/pages.test.ts`, a new test "a table scenario shows its table and a
  mixed scenario shows steps, note and table in order": the page of `SwRS-X-014` holds a `<table>`
  with `<th>Input</th><th>Outcome</th>` and one `<tr>` per row; the `|` of the escaped pipe; the
  entity cell rendered as `&lt;b&gt; &amp;lt;` in the HTML (decoded, then escaped: the reader sees
  `<b> &lt;` and no `<b>` element is written); in the mixed card the `gwt` block comes before the note, which comes before the table;
  the `Given | When | Then` table is a `<table>` (its headers are `<th>`), not a `gwt` grid; the
  table-only card holds no `class="gwt"`. A third check in the same test: the page of `SwRS-X-011`
  (list scenarios) still holds `<div class="gwt">` with `Given`, `When`, `Then` and no `<table>`.
- Each new test carries `// @tests_req SwRS-MDOKFSTUDIO-CORE-082`. The existing assertions keep
  their intent; none changes.
- Both new tests fail on the current code (no `blocks`, no table in the page, no decoding).

### 4b. The home page hint: `test/site/requirementsViewer/home.ts`

- The hint "What the requirements are" (line 155) says a SwRS is "written with its scenarios
  (given, when, then, or a table)" instead of "(given, when, then)". The rest of the line stays.
- This is CORE-069's home (its `@implements_req SwRS-MDOKFSTUDIO-CORE-069` sits above it, line
  147). `test/site/requirementsViewer/home.test.ts`, test "home: layers, areas, sections and
  figures", gains one assertion that the body holds "given, when, then, or a table"; no existing
  assertion changes. CORE-069's text ("explains what the requirements are") still holds, so its
  file does not change.

### 5. The bundle guard (answers, Q4)

- New test file `test/site/requirementsViewer/bundle.test.ts`, run by `just unit` (it falls in
  `out/test/site/**/*.test.js`), test "no scenario card of the requirements bundle is empty":
  - It reads every `*.md` under `requirements/tiers/strs/` and `requirements/tiers/swrs/` from the
    repository as it ships, at the head under test (`process.cwd()` is the repository root, as in
    `test/core/frontmatter/requirementSchemas.test.ts`), not a copy or a prepared text.
  - For each file it runs `parseScenarios` and checks that the number of scenarios equals the
    number of `### Scenario` headings above the links block.
  - For each scenario whose source section holds a non-blank line, it renders the card body with
    `scenarioBody` and checks that its text, tags removed, is not blank, and that it holds no
    `gwt` grid whose three columns are all empty.
  - It checks it is not vacuous: at least one table scenario and one list scenario were seen.
  - It carries `// @tests_req SwRS-MDOKFSTUDIO-CORE-082`.
- On the current code this test fails (on SwRS-MDOKFSTUDIO-BLOCK-130 among 421 files).

### 6. Requirements

- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-082.md` (`proposed`, so no
  owner approval is needed), edited by hand in its authored parts only (never the generated
  links block):
  - new scenario `### Scenario (nominal): A table scenario shows its table`: GIVEN an active SwRS
    whose scenario is written as a table with its own headers, WHEN its page is written, THEN the
    scenario card shows that table with the same headers and one row per source row, and no empty
    Given / When / Then columns;
  - new scenario `### Scenario (boundary): A scenario with steps, a note and a table`: GIVEN a
    scenario with GIVEN / WHEN / THEN lines, a note line and a table, WHEN its page is written,
    THEN the card shows the steps in their three columns, the note as a paragraph and the table,
    in source order;
  - "Verification notes": name the two new tests of section 4 and the bundle guard of section 5.
- `just requirements-update`, its generated files committed, and a dated entry in
  `requirements/tiers/log.md`.
- No other requirement file changes (answers, Q3).

### 7. Sibling change requests

Three CRs of the inbox also edit these files: `requirements-path-graph-design`,
`requirements-viewer-ids` and `requirements-share-cards` (they touch
`test/site/requirementsViewer/pages.ts`, `viewer.css`, `pages.test.ts` and
`requirements/tiers/log.md`). Whichever lands second rebases on the first and resolves the
conflicts; on the same day, the `log.md` entries go under the same date heading.

### 8. Commit

One commit, `fix: show table scenarios on the requirements site instead of empty columns`
(no scope: the allowed scopes cover the extension, and the viewer is site tooling under `test/`).

## Decisions of the answers, carried

1. table-scen-Q1, show the table, do not convert it: sections 1 and 2; the card shows the source
   table with its own headers, a `Given | When | Then` table included (section 4 tests it).
2. table-scen-Q2, mixed scenarios and notes: steps, tables and notes render in source order;
   prose under a scenario heading is a paragraph, not dropped (sections 1, 2, 4).
3. table-scen-Q3, requirements files are not rewritten: no table scenario of the bundle is
   converted or moved; only the viewer's own SwRS, CORE-082, gains scenarios (see below).
4. table-scen-Q4, guard over the real bundle: section 5.
5. Spec critic on Fable: for the Chief of Staff to run on this spec; nothing in the change itself.
6. table-scen-Q6, no `<br>` rule: every cell is escaped text; the `x<br>y` fixture cell is gone
   (sections 2 and 4).
7. table-scen-Q7, decode the basic entities before escaping, in cells, notes and steps, with a
   test (sections 1 and 4).

## Decided in the spec

- **CORE-082 is updated.** The constitution (section 1) asks every fix to update its SwRS. The
  viewer's scenarios are SwRS-MDOKFSTUDIO-CORE-082, so it gains the two scenarios of section 6.
  Q3 is read as "the 421 content requirements are not rewritten", which this keeps.
- **Source order everywhere.** Q2 says "steps first, then the table, in source order"; the blocks
  follow the source, so a table written before the steps shows first.
- **Non-step bullets and wrapped prose are notes.** The 19 `- text` lines and the indented
  continuation lines under scenarios are shown, not dropped: each bullet is its own paragraph
  without its marker, a wrapped line joins the line it continues.
- **Cells are text.** Table cells, like step lines today, are escaped text; inline code keeps its
  backticks as written. Rendering inline Markdown in scenarios (code, links, emphasis) is out of
  scope.
- **Entities decode once.** One pass decodes the four entities of Q7, so `&amp;lt;` shows `&lt;`;
  other entities (`&nbsp;`, numeric ones) stay as written.
- **`\|` is a pipe, rows are kept as written.** An escaped pipe splits no cell; a row with more or
  fewer cells than the header is shown as it is.
- **The steps markup does not change.** A list-only scenario renders the same HTML as today, so
  the existing tests and the look of list scenarios hold.
- **An empty section says so.** A scenario heading with nothing under it shows a hint line rather
  than a blank card (none in the bundle today).
- **The fixture's table scenarios sit on SwRS-X-014.** It is on no map, so the walk and scenario
  counts of the existing tests do not move.
- **The home page example's code is not touched.** It reads `steps` of the first scenario of
  SwRS-MDOKFSTUDIO-GFM-021, a list scenario; it shows decoded text like the cards.
- **The writing skill is not touched.** The viewer is site tooling, not a rendered syntax of the
  extension.

## Out of scope

- Rewriting any table scenario of the bundle as GIVEN / WHEN / THEN, or any other edit of the 421
  files.
- Inline Markdown rendering in scenario text (code spans, links, emphasis).
- Column alignment from the separator line (`:---:`).
- Entities other than `&lt;`, `&gt;`, `&amp;` and `&quot;`; entities in titles and statements.
- The home page example's layout (it only gets the decoded step text), the use case maps, the scenario dots and counts, the search index.
- The okfreq tool and its validation of scenario forms.

## Evidence

- `just check` passes: the two new unit tests and the bundle guard pass; every existing viewer
  test passes with its assertions unchanged.
- The three new tests and the new home assertion fail on `main` at the commit the branch starts from (run once before the
  fix, result noted in the PR body).
- `just requirements-update` run, `requirements/tiers/log.md` entry, `okfreq validate
  --check-links --project-root .` clean (as the project guidelines ask before the PR).
- `just preflight` passes (on Windows, its static stage; CI runs the rest).
- Scenario steps, on a locally built site (`just requirements-report`, then
  `fnm exec -- npm run site`):
  1. Open `out/site/requirements/block-editing/SwRS-MDOKFSTUDIO-BLOCK-130/index.html`.
  2. Open the first scenario card: a table with the headers Input and Outcome and four rows; no
     Given / When / Then columns.
  3. Open the card "The move chord in the text box moves the block and reopens its editor": the
     note line "The move chord is Cmd+Alt ..." shows as a paragraph above the table.
  4. Open the card "A refused keyboard move can be retried": the Given / When / Then columns, as
     before.
  5. Open `out/site/requirements/gfm/SwRS-MDOKFSTUDIO-GFM-021/index.html` (a list-only SwRS):
     its cards look as before.
  6. Narrow the window to a phone width: a wide table scrolls inside its card and the page does
     not scroll sideways.
- The PR body carries a screenshot of steps 2 and 3, and its Tests section lists
  SwRS-MDOKFSTUDIO-CORE-082 with `test/site/requirementsViewer/pages.ts`, `model.ts` and the
  three test files, and SwRS-MDOKFSTUDIO-CORE-069 with `home.ts` and `home.test.ts`.

No host or default matrix: the change does not depend on the host or on a setting. No CI job is
added or changed.
