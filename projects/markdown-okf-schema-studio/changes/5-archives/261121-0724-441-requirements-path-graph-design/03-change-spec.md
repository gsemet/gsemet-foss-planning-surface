# Change specification: the use case path graph as a joined map, smaller and readable

Short name: `path-graph`. Origin: verbal (owner, 2026-11-20); no tracker issue.

## Goal

On the published requirements site, the page of a use case (StRS) draws its Main paths as a map
(the "path graph"). The owner likes its look but finds it far too big (he read it at 50 % zoom)
and hard to read: side-branch labels, test counts and captions overlap each other and the dashed
lines. This change redraws the map so that:

- a state shared by two paths is **one** node: the paths join into it and split out of it, each in
  its own colour, like the lines of a metro map (never a grey copy per row);
- the map is drawn at its own size, not stretched to the page, and is shorter: the prototype
  measured, on six use cases (`work/before/metrics.txt` and `work/after/metrics.txt`), 17 to 59 %
  shorter at 1280 px, and at 800 px from 13 % taller (FMSCHEMA-014) to 41 % shorter;
- no text or pill overlaps another, and no text runs past the map, on every real use case page;
- every link to a requirement shows its full ID (`StRS-MDOKFSTUDIO-BLOCK-014`, not `BLOCK-014`),
  the pills of the map included;
- a reader who is not a specialist understands, from one short line and the legend, that a use
  case is reached by one or more paths, that each step is a behaviour (SwRS) with its own tests,
  and that paths can share steps.

The look stays: cream background, rust path 1, pills with an ID and a test count, coloured
scenario dots, the Play path buttons.

The design is already proven: prototyped and checked on six use cases at two widths through four
critic rounds (`work/design.md` in this CR folder). The reference implementation is
`work/graph-design.patch` (this CR folder); it applies with `git apply` to `origin/main` (it was
made on 7c88b89c; main moved to a18bcac1 without touching `test/site/requirementsViewer/`). The
coder may apply it as the starting point; the points below that the patch does not cover yet are
marked **(beyond the patch)**. The patch's pills hold the short ID on one line; this
specification changes them to the full ID on its own line, so the measured sizes above are the
prototype's and are measured again on the real maps (see "Evidence").

## What changes

All files are in the project repository `markdown-okf-schema-studio`.

### 1. The map layout: `test/site/requirementsViewer/layout.ts`

From the patch:

- New exported `buildMetroMap(paths: readonly MainPath[]): MetroMap` builds the joined map:
  - one `MapNode` per distinct state text, whatever the number of paths through it (`paths`: the
    set of path indexes through it; `goal`: the last state of a path; `options`: the "Option"
    outcomes of every path at that state, without duplicates; `drop`: a line leaves it to a lower
    row);
  - one `MapEdge` per (state, behaviour, next state) triple, listing every path that takes it
    (`paths`) and the step index of that edge on each of them (`steps`); a second behaviour between
    the same two states is drawn as an arc (`arc`);
  - path 1 on row 0; each later path puts the states it does not share on a new row, and joins or
    leaves the other rows at the shared states;
  - columns: each state is one column right of the state before it on every path (longest way
    from a start);
  - packing: a path that shares no state with the others goes on the right of an earlier row
    (never path 1's row 0) when it fits within one more column than the widest row, one free
    column right of the last state or climb of that row, so it never reads as the continuation of
    another path; empty rows are removed.
- `metroSvg(model, paths, fromDir)` (keeps its `@implements_req SwRS-MDOKFSTUDIO-CORE-081`) draws
  that map:
  - **Size:** the SVG has a `width` attribute equal to its natural width (`viewBox` the same size),
    `min-width` 85 % of it, and CSS `max-width:100%`; it is never upscaled to the page.
  - **States:** one circle per node, drawn last (over the lines), its name above it, wrapped at 24
    characters. A state of several paths has the class `join` and a thicker circle. A goal ring
    takes the colour of its first path, and of the other paths that end there as dashed arcs
    (`circle.tone`). Its `<title>` names the paths through it ("(paths 1, 2)").
  - **Steps:** one group per edge (`<a class="tr">` when the behaviour has a page, else `<g>`),
    with `data-paths="<i> <j>"` (the 0-based path indexes, space-separated) and one
    `data-step-<i>="<n>"` per path (the step index on that path). One stroke per path, in its
    colour, side by side (offset by stroke width + 1); one pill bordered in the first path's
    colour; the scenario dots centred under the pill; the caption under the dots, wrapped at 34
    characters (24 when the next state's path goes down, to stay clear of its lane). The `<title>`
    gives the full ID and title, and adds "(paths 1 and 2)" for a shared step.
  - **Joins and splits:** a line between two rows runs down (or up) in a lane 26 px left of the
    state of the upper row, then along its own row, with rounded bends.
  - **Start disc:** a path whose first state belongs to an earlier path shows its number in a disc
    of its colour on the lane under that state (`g.badge`).
  - **Other outcomes:** listed under their state on a dotted stem, each a dashed pill (same two
    lines as a step's pill) with its dots under it, then its caption wrapped to the room before the
    next state of the row. An outcome whose behaviour is already a step of the map shows no second
    pill: its full ID and its test count in grey text (`text.oid`, the ID on one line, the count on
    the next), then its dots.
  - **Text:** a caption's backtick spans are drawn in monospace (`tspan.code`), without the
    backticks.

**(beyond the patch) Full IDs in the pills, the layout widened:**

- A pill (`rect.pill` and its `text.pt`) holds two lines: the requirement's full ID
  (`SwRS-MDOKFSTUDIO-BLOCK-117`) on the first line, its test count ("3 tests") on the second. Its
  width follows the longer line, its height the two lines; the dots and the caption move down by
  the added line.
- The column width (`COLUMN`, 230 px in the patch) grows so that two neighbouring pills keep a gap
  of at least 24 px with the widest pill of the map, its estimated width raised by the width margin
  below; the outcome room (`INLINE_ROOM`) and the row heights follow. The map gets wider, never
  wider than needed by its own widest pill.
- **Width margin for unpinned fonts:** the layout estimates a text's width from its length
  (`CHAR` px per character and the pill's per-character width). The estimates leave at least 10 %
  more room than the text takes in the pinned test fonts (section 6), so a reader's own fonts, up
  to 10 % wider, do not overlap. The browser test checks this margin (section 6); when it fails,
  the estimates or gaps grow, never the check's tolerance.

Also from the patch:

- Path colours: `pathColour(index)` returns `var(--p1)`, `var(--p2)`, `var(--p3)`; a fourth path
  and later reuse `var(--p3)`. `metroList` (the phone list) uses the same three colours.
- `buildGraph` and `walkCount` stay as they are (the walk count sentence is unchanged). `tspans`
  stays only if still used; otherwise it is removed.

### 2. Full IDs on every link to a requirement (beyond the patch)

The owner, on the caption "Step 1 of path 2 in BLOCK-014": every link to a requirement page shows
the requirement's full ID. `shortId` (`urls.ts`) is no longer used for the text of a link:

- `layout.ts`: the map's pills and grey outcome IDs (section 1), and the phone list `metroList`
  (the `<b>` of `.vvia` and `.vopt`).
- `pages.ts`: the "where" captions of a behaviour page ("Step 1 of path 2 in
  StRS-MDOKFSTUDIO-BLOCK-014: from … to …" and "Another outcome at step …"), the use case links of
  an area page (`.stop .id`), the behaviour rows of a use case page (`a.brow .id`), the
  "superseded by" links of `retiredNote`.
- Tooltips (`<title>`) already give the full ID; they stay.
- `viewer.css`: the ID columns fit a full ID: `.brow` (its first column, 110 px today) and
  `.stop .id`, on wide and narrow screens; long IDs never overlap the next column (they may wrap
  at a hyphen on narrow screens).
- Not changed here, left to the viewer-ids CR, which asks for them by name: the page title, the
  eyebrow ("Use case BLOCK-003"), the breadcrumb and the search. Non-link labels keep `shortId`.

### 3. The map section: `test/site/requirementsViewer/pages.ts`, `mapSection`

From the patch:

- The old hint paragraph above the map ("Circles are the states a user goes through; …") is
  removed and replaced, inside `.map`, by one line `<p class="mapread">`, in these exact words
  (three sentences, kept as the owner saw them):

  > This use case (StRS) is reached by 3 paths, one per coloured line. A path goes from one
  > **situation** (circle) to the next; each **step** (pill) is a behaviour (SwRS) with its own
  > tests. Where paths meet, they share the circle or the step.

  - with one path: "is reached by one **path** (the coloured line)"; with N paths: "**N paths**,
    one per coloured line";
  - "(StRS)" and "(SwRS)" in `<span class="soft">` (grey);
  - the last sentence only when two paths share a state.
- The legend lists, in this order: each path key with its title ("path 2: Move a block with the
  keyboard"), followed by ", starts at (2)" (a disc `b.pnum` in the path's colour) when the path
  starts at a state of an earlier path; a "shared step" key (`i.lshared`, two colours) only when two
  paths share a step; "other outcome" (dotted); then "one dot = one scenario checked:" with the
  nominal, boundary and refusal dot swatches.
- **(beyond the patch)** The legend key class clamps like the stroke colour: path 4 and later use
  `lp3`, so every key has a swatch.

### 4. Styles: `test/site/requirementsViewer/viewer.css` and `test/site/siteTheme.ts`

From the patch: the `.map` and `.ucd` boxes scroll sideways (`overflow-x:auto`) with a shadow on
the right edge while there is more to see; `svg.metro{max-width:100%;height:auto}` (no more
`width:100%`); the rules for `.join`, `.tone`, `.badge`, `.oid`, `.mapread`, `.lshared`, `.pnum`,
`.lp3`, `.end`, `.code`; captions 13.5 px, state names 14 px; the hover thickening only on steps
(`.tr:not(.opt)`); the rules of the removed option states (`.st.alt`) go away.

**(beyond the patch)** The third path colour is a site token, not a raw value in `viewer.css`:

- `siteTheme.ts`: add `"--p3": "--studio-charts-yellow"` to `SITE_TOKEN_SOURCES` and
  `"--p3": "#7d5500"` to `SITE_TOKENS` (the value of `--studio-charts-yellow` in the extension's
  cream block, `src/core/preview/styles/pageChromeStyles.ts`). The existing test "every site token
  equals its variable in the cream block of the extension" then covers it.
- `viewer.css`: do not declare `--p3` in `:root` (the patch's `--p3:#8a5f0f` is dropped); update
  the header comment ("path 1, path 2 and the scenario kinds are the only other colours") to name
  the three path colours.

### 5. Play: `test/site/requirementsViewer/viewer.js`

From the patch: `play(pi)` collects the steps with `.tr[data-paths~="<pi>"]` and orders them by
their `data-step-<pi>` attribute, so Play path 2 runs through the joined states and the shared
steps. The states lit are found as today (the circles at both ends of each step's `.hit` path).

**(beyond the patch)** The walking token takes the colour of the path played: `var(--p1)`,
`var(--p2)`, then `var(--p3)` for path 3 and later (today `pi ? "var(--p2)" : "var(--p1)"`).

The reduced-motion rule is unchanged: with `prefers-reduced-motion: reduce`, Play does nothing.

### 6. Requirements (`requirements/`, okfreq)

Read `requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md` ("During a change") first.

- **Update `SwRS-MDOKFSTUDIO-CORE-081`** (`requirements/tiers/swrs/rendering-core/`), "The site
  requirements viewer draws the map of a use case from its Main paths". Its description and
  normative text say, in substance: the map is an SVG drawn at its natural size (never upscaled,
  scrolling sideways when wider than the page); a state shared by several paths is drawn once and
  the paths join into it and leave it in their colours; a step taken by several paths shows one
  stroke per path; a pill shows the behaviour's full ID and its test count; a path starting at a
  state of an earlier path shows its number there; one line above the map says what a path, a
  situation and a step are; the legend names each path; other outcomes are listed under their
  state; no text or pill overlaps another; plus what it says today (the phone list, the walk-count
  sentence, and "the paths are not written yet" without Main paths). Scenarios: keep the nominal
  one (fixture StRS-X-001) and the boundary one (no Main paths); add a nominal scenario "Two paths
  share states" (one node per shared state, one stroke per path on a shared step, the start disc,
  the "Where paths meet" sentence) and a boundary scenario "A map wider than the page" (natural
  size, at least 85 %, the box scrolls, nothing overlaps). Update its verification notes to name
  the new tests.
- **Full IDs on links:** update the SwRS that describe the other links of section 2, in
  substance "a link to a requirement shows its full ID": `SwRS-MDOKFSTUDIO-CORE-080` (area page,
  use case list), `SwRS-MDOKFSTUDIO-CORE-082` (behaviour page: "where" captions), the SwRS whose
  text names the behaviour rows of a use case page (CORE-081 or CORE-082), and
  `SwRS-MDOKFSTUDIO-CORE-083` (retired requirements) for the "superseded by" links if its text
  names that link. Each gets a `@tests_req` at the test that checks the full ID.
- **New SwRS for Play**, created with `uv run --no-sync --group requirements okfreq new` in scope
  `rendering-core` (its ID is the one okfreq gives; never hand-allocated), deriving from
  `StRS-MDOKFSTUDIO-CORE-008`. Title, in substance: "The site requirements viewer plays a path of a
  use case map". Normative: when the reader presses "Play path N", the viewer SHALL light, in path
  order, every step of path N and every state at their ends, the steps and states path N shares
  with other paths included, with a token in the colour of path N; with reduced motion asked, it
  SHALL do nothing. Scenarios: nominal "Play a path through joined states", boundary "Reduced
  motion". `@implements_req` on `play()` in `viewer.js`; `@tests_req` in the browser test (section
  7). If `just requirements-update` does not link the marker in `viewer.js`, put the
  `@implements_req` on the code of `metroSvg` that writes `data-paths` and `data-step-<i>`
  instead, and say so in the PR body.
- **The guideline allows three paths:** `requirements/guidelines/project.guidelines.md`, section
  "Main paths of a StRS": "names one or two paths through the use case" becomes "names one to
  three paths through the use case", and the rule "One or two paths per StRS." becomes "One to
  three paths per StRS." (BLOCK-014 has three; the map draws three colours).
- The text of `StRS-MDOKFSTUDIO-CORE-008` is not edited (its `derived_by` is generated).
- Then `just requirements-update` (generated files committed) and a dated entry in
  `requirements/tiers/log.md` (CORE-081, the full-ID SwRS, the new Play SwRS, the guideline's
  three paths).

### 7. Tests

All new tests carry `@tests_req` markers at the test (at most 3 IDs per marker block). Each new
assertion fails on the code before the change.

**Unit tests** (Node, `node:test`, run by `just check` through `test:unit`):

- New `test/site/requirementsViewer/metroMap.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-CORE-081`:
  - `buildMetroMap` on two paths sharing their last two states: one node per shared state (its
    `paths` holds both), one edge per shared step listing both paths with their step indexes, the
    unshared states of path 2 on row 1, columns as computed by hand;
  - `buildMetroMap` on three paths where path 3 shares nothing (the BLOCK-014 shape): path 3's
    states move to row 1, starting one free column right of that row's last state or climb, and
    the map has 2 rows;
  - `metroSvg`: every `.tr` step group has `data-paths` and a `data-step-<i>` per listed path; a
    shared step has one `path.ln` per path with that path's colour; the SVG has a `width`
    attribute equal to its `viewBox` width and no `width:100%`; a path starting at a state of an
    earlier path has a `g.badge` with its number; a state of two paths has the class `join`; a
    caption with backticks has a `tspan.code` and no backtick; with a behaviour
    `SwRS-MDOKFSTUDIO-…` the pill's first line is the full ID and its second the test count.
- `test/site/requirementsViewer/pages.test.ts`:
  - `@tests_req SwRS-MDOKFSTUDIO-CORE-081`: the use case page of the fixture holds
    `<p class="mapread">` with "reached by one <b>path</b>" and no "Where paths meet"; a two-path
    use case holds "<b>2 paths</b>", "Where paths meet" and the legend key "path 2: <title>"; the
    old hint "Circles are the states" is gone. The existing assertions of "a use case with paths
    draws the map, the phone list and the walk count" keep their intent (none is weakened).
  - Full IDs (`@tests_req` CORE-080, CORE-081, CORE-082 at the tests that check them): the
    fixture's IDs (`SwRS-X-010`) carry no `MDOKFSTUDIO` and so cannot show the difference; add to
    the fixture a use case and behaviours with `MDOKFSTUDIO` IDs, and assert the full ID in the
    map pill, the phone list, the area page's use case link, the behaviour row, the "where"
    caption ("Step 1 of path 1 in StRS-MDOKFSTUDIO-…") and a "superseded by" link.
- `test/site/siteTheme.test.ts`: unchanged; it now also checks `--p3` against the cream block.

**Pinned fonts** (`test/page/pinnedFont.ts`): add a site variant (for example
`pinSiteFonts(page)`) that loads the KaTeX faces from `node_modules/katex/dist/fonts` as
`pinTestFonts` does (sans regular and bold, typewriter, plus `KaTeX_Main-Regular` and
`KaTeX_Main-Italic` as a pinned serif) and points the site's `--sans`, `--serif` and `--mono` to
them on the root element. A face that does not load throws, as today.

**Browser test** (Chromium through `playwright-core`, the pattern of
`test/page/tableBreakout.test.ts`), new `test/site/requirementsViewer/metroMap.browser.test.ts`.
Every page is built with `writeViewerPages(site, report, <repository root>)` into a temporary
folder, so the pages use `viewer.css` and `viewer.js` as they ship from
`test/site/requirementsViewer/` at the head under test (no copied or prepared stylesheet or
script); fonts are pinned before any measure; the checks assert on every platform.

- **The check**, shared by both groups below, `@tests_req SwRS-MDOKFSTUDIO-CORE-081`: at
  1280 x 900 and 800 x 900, no two boxes among the SVG's `text` elements (pill texts `text.pt`
  excepted, they sit inside their pill) and `rect.pill` elements overlap, each text box first
  widened by 5 % of its width on each side (the 10 % width margin); and no widened text box ends
  right of the SVG's box. At 1280 px the rendered SVG is never wider than its `width` attribute,
  and at least 85 % of it.
- **Frozen shapes:** new fixture `test/site/requirementsViewer/metroShapes.ts`: a requirements
  report (the shape of `fixture.ts`) holding six use cases whose Main paths text is a frozen copy
  of the Main paths sections, at the head of the change, of StRS-MDOKFSTUDIO-BLOCK-003 (one path,
  three other outcomes), FMSCHEMA-014 (path 2 splits early), BLOCK-014 (three paths, two join, one
  alone), MYST-006 (short), REVIEW-012 (long captions), MYST-009 (path 2 splits mid-way), and every
  SwRS they cite with the scenario kinds and the number of test files it has in the bundle at that
  head. On these: the check; at 800 px the BLOCK-014 map box scrolls sideways
  (`scrollWidth > clientWidth`); a PNG of the `.map` box of each page at both widths, 12 files,
  written to `out/reports/requirements-viewer-graph/` (`<StRS short id>-<desktop|narrow>.png`), as
  review evidence, no pixel comparison.
- **Every real use case:** from `out/reports/requirements/requirements-report.json` (made by
  `just requirements-report`), every active StRS with a Main paths section gets the check. A
  failure names the StRS, the width and the two boxes. When the report is missing, the test skips
  with "no requirements report (run `just requirements-report` first)", unless
  `STUDIO_REQUIRE_REQUIREMENTS_REPORT=1`, where it fails.
- **Play**, `@tests_req <the new Play SwRS>`: on the frozen BLOCK-014 page at 1280 px, with
  `reducedMotion: "no-preference"`, a click on "Play path 2" ends with exactly the three steps of
  path 2 (`.tr.on`: BLOCK-130, BLOCK-117, BLOCK-058, the last two shared with path 1) and its four
  states (`.st.on`, the three it shares with path 1 included) lit; with `reducedMotion: "reduce"`
  the click lights nothing.
- When no Chromium can start, the test skips with the message "no Chromium can start here (run
  `just dev` to install it)", unless `STUDIO_REQUIRE_CHROMIUM=1`, where it fails with the launch
  error (the helper of `tableBreakout.test.ts`; share it rather than copy it if that stays small).

### 8. CI, scripts and CONTRIBUTING

- `package.json`: new script `"test:viewer-graph": "node scripts/node-test.mjs viewer-graph
  out/test/site/requirementsViewer/metroMap.browser.test.js"`.
- `justfile`, target `ci-visual`: after the breakout line, add `just requirements-report ||
  failed=1`, then `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 {{ npm }} run
  test:viewer-graph || failed=1`, and name both in the target's comment (report under
  `out/reports/viewer-graph/`, captures under `out/reports/requirements-viewer-graph/`). The
  workflow `.github/workflows/ci.yml` does not change: `just dev-ci visual` already installs the
  `requirements` group (okfreq), and the `visual` job already uploads `out/reports/`.
- `CONTRIBUTING.md`, the paragraph on what CI runs on a pull request (around lines 278-285, the
  parenthesis after `ci-visual`): add that `ci-visual` then generates the requirements report and
  runs the path graph tests of the requirements viewer (`test:viewer-graph`, with
  `STUDIO_REQUIRE_CHROMIUM=1` and `STUDIO_REQUIRE_REQUIREMENTS_REPORT=1`, in pinned fonts, asserted
  on every platform), with their report under `out/reports/viewer-graph/` and the map captures
  under `out/reports/requirements-viewer-graph/`.
- The browser test also runs inside `test:unit` (its pattern covers `out/test/site/**`), where it
  skips without Chromium, and its real-report part skips without a report.

## Each decision of 02-answers.md

- "A state shared by two paths is ONE node: the paths join at it and split from it, never a copy
  per row": `buildMetroMap` (section 1), checked by the unit and browser tests (section 7).
- "The graph explains itself to a non-specialist in a few words, no paragraph": the one
  `mapread` line and the legend (section 3), replacing the old hint paragraph.
- "The CR ships the proven design of `work/design.md` and `graph-design.patch`": sections 1 to 5
  carry it; additions are marked "beyond the patch".
- "Links in the graph and its caption use full IDs, as the viewer-ids CR asks": with path-graph-Q-c4,
  section 2.
- "Spec critic: yes, on Fable": for the Chief of Staff; nothing in the code.
- path-graph-Q-c1 (overlap check on every real use case page in CI, report generated in
  `ci-visual` first, plus frozen shapes): section 7 "Every real use case" and "Frozen shapes",
  section 8.
- path-graph-Q-c2 (pin the fonts as the breakout tests do, assert on every platform, a width
  margin): section 1 "Width margin", section 7 "Pinned fonts" and "The check".
- path-graph-Q-c3 (one to three paths per StRS, the three-path design stays): section 6, the
  guideline change.
- path-graph-Q-c4 (full ID on every link: caption, tooltips, pills; full ID on its own line in the
  pill; layout widened; checks run again on the real maps): sections 1 and 2, section 7, "Evidence".
- path-graph-Q-c5 (keep the three sentences, the legend stays): section 3.

## Decided in the spec

The answers leave these points open; each is decided for the product and the answers, without the
owner.

1. **Narrow screens scroll** (open point of `design.md`): kept as designed. At 800 px a wide map
   scrolls sideways with the edge shadow; below 760 px the phone list replaces the map, as today.
   No stronger scroll hint in this CR.
2. **A map wider than the page** (BLOCK-014, five columns, wider still with full IDs): kept as
   designed, drawn down to 85 % of its natural size before it scrolls.
3. **Path numbers on the graph and a two-colour border on shared pills** (critic round 4): not in
   this CR. Only a path that starts on another path's state shows its number; a shared pill keeps
   the first path's colour as border, the two strokes show the sharing.
4. **Outcome stem 26 px beside a climb**: accepted as is.
5. **Third path colour:** a site token `--p3` from the extension's cream `--studio-charts-yellow`
   (`#7d5500`), not the patch's raw `#8a5f0f`, because the published site takes every colour from
   the cream block (SwRS-MDOKFSTUDIO-CORE-086 and its token test). A fourth path reuses it.
6. **Play** gets its own new SwRS (no SwRS covers Play today) rather than an item of CORE-081, so
   its test and marker stay apart; its token takes the colour of the path played.
7. **Where full IDs stop:** every link text naming a requirement shows its full ID (section 2);
   the page title, the eyebrow, the breadcrumb and the search stay with the viewer-ids CR, whose
   intake names them, so the two CRs do not change the same lines. Whichever lands second rebases.
8. **Width margin of 10 %**, checked as boxes widened by 5 % on each side: large enough for a
   reader's sans or serif that is wider than the pinned KaTeX faces, small enough not to spread the
   map.
9. **A missing report in CI fails**, through `STUDIO_REQUIRE_REQUIREMENTS_REPORT=1`, like a missing
   Chromium; locally and in `test:unit` it skips with the command to run.
10. **Captures without baseline:** the 12 captures are review evidence only; the overlap and size
    checks are the pass criteria.
11. **Size bound:** with full-ID pills the maps are measured again; the bound kept is "below its
    before height" at 1280 px only (at 800 px FMSCHEMA-014 was already 13 % taller in the
    prototype). The prototype's "after + 10 %" bound is dropped, since the two-line pills change
    the layout it was measured on.

## Out of scope

- Numbered badges at every path's start, a two-colour border on shared pills, a stronger scroll
  hint, making a shared behaviour on two separate edges (BLOCK-058 on path 3 and on paths 1-2) read
  as the same.
- The phone list's layout (only its colours and its full IDs change), the walk-count sentence and
  `walkCount`.
- The page title, eyebrow, breadcrumb and search of the viewer (the viewer-ids CR), the table
  scenarios (the requirements-viewer-shows-table-scenario CR).
- The text of any StRS, the writing skill (no rendered Markdown syntax changes), the extension
  under `src/` (only the site viewer changes; `pageChromeStyles.ts` is read, not changed).

## CI environment of the changed job

- **Job:** `visual` (`.github/workflows/ci.yml`), `ubuntu-latest`, 15 min timeout, set up by
  `just dev-ci visual` (Node from `.nvmrc`, `npm ci`, `uv sync` with the `requirements` group,
  Chromium with its system libraries and fonts from the apt archive cache), then `just ci-visual`.
  It runs on every pull request.
- **Different from a local Windows machine:** the system fonts (irrelevant to the checks, which run
  in the pinned KaTeX fonts from `node_modules/katex`, installed by `npm ci`); a fresh `out/` with
  no requirements report until `ci-visual` makes one; no git history beyond the checkout (the
  report and the pages read the files, `currentCommit` reads the checked-out head); the `visual`
  artifact now also carries `out/reports/requirements/`, which the `gallery` job regenerates on its
  own anyway.
- **Proof before the push:** `just check` (runs the browser test inside `test:unit`, Chromium from
  `just dev`), then `just requirements-report` and `STUDIO_REQUIRE_CHROMIUM=1
  STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph` locally, passing on every real
  map, with the 12 captures looked at. `just preflight` on Windows runs the static stage only.
- **Only the first CI run can prove:** that okfreq makes the report in the `visual` job, that
  Chromium starts and loads the pinned faces there for this suite, and the suite's time in the
  job (one page load per real use case and width). If a check fails only there, the fix is in the
  layout's estimates or gaps, never a looser check.

## Evidence

- `just check` passes: unit tests (new `metroMap.test.ts`, updated `pages.test.ts` and fixture,
  `siteTheme.test.ts` with `--p3`), the browser test, markers (`just check-markers`), file sizes
  (`layout.ts` stays far under 1 500 lines).
- `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph` passes
  locally and in the `visual` CI job on every real use case map and the six frozen shapes; the
  captures are in the job's artifact.
- `just requirements-update` run and committed; `okfreq validate --check-links --project-root .`
  and coverage pass as CI runs them; CORE-081, CORE-080, CORE-082 (and CORE-083 if changed) and
  the new Play SwRS each have their `@implements_req` and a `@tests_req` at each test; a dated
  entry in `requirements/tiers/log.md`.
- `just preflight` passes (static stage on Windows).
- **PR evidence on the real site, in the reader's fonts:** `just requirements-report`, then the
  six real pages (BLOCK-003, FMSCHEMA-014, BLOCK-014, MYST-006, REVIEW-012, MYST-009) shot at 1280
  and 800 px before (base) and after (head), with `work/shoot.cjs` of this CR folder (run from the
  repository root's `out/` layout it expects) or the same steps: after, every map shows
  `overlaps=0`, and at 1280 px each map is shorter than its before height. The measured heights,
  before and after, at both widths, go in the PR body; the before/after captures go in the PR's
  Impacts per the pull-request guideline.
- **Scenario steps** (a reviewer, on the built site): open the BLOCK-014 use case page at 1280 px;
  read the line above the map ("reached by 3 paths … Where paths meet, they share the circle or
  the step."); see the states "The host is asked to swap the block with its neighbour", "The two
  blocks are swapped in the document" and the goal drawn once, with paths 1 and 2 both entering
  them and two strokes on the pills of SwRS-MDOKFSTUDIO-BLOCK-117 and SwRS-MDOKFSTUDIO-BLOCK-058,
  each pill showing its full ID over its test count; see path 3 apart on the right, not continuing
  path 2; press "Play path 2": the token, purple, walks BLOCK-130, BLOCK-117, BLOCK-058 and lights
  the four states; at 800 px the map scrolls sideways with a shadow on the right edge; no label
  overlaps anywhere. Open the behaviour page of SwRS-MDOKFSTUDIO-BLOCK-130: its caption reads
  "Step 1 of path 2 in StRS-MDOKFSTUDIO-BLOCK-014".

## Delivery notes

- One pull request; commit type `feat` (for example "feat: draw the use case path graph as a
  joined map"); the site is not one of the allowed scopes, so no scope, as the commit and scope
  guidelines say.
- The viewer-ids CR touches `layout.ts`, `pages.ts` and `urls.ts` too: whichever lands second
  rebases on the other.
