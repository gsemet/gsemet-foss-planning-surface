# Change Specification: the web board, lighter and more elegant

## Goal

The user finds the web board beautiful but wants it "a little lighter and even more elegant", in
the spirit of the reference mock-up (`intake/reference.png`): one modern sans-serif at two
weights, a white sidebar with a hairline, almost no colour but one deep accent, states as tiny
icons, two-tone cards, a breadcrumb header that stays on top when the page scrolls. Every view of
the board takes this style; what the board shows and does stays the same, except the Batch view
changes the critique named (Q7) and the three the user's inbox item `board-batch-view` asked for
(Q9): no Merged PR section, no grouping by state (each CR keeps one place, its state a coloured
badge in the top right corner), and level heads without ": after level N".

The reference to compare at delivery, approved by the user (02-answers, Q7):
`prototypes/01-mockups/final-batch.html`, `prototypes/01-mockups/final-costs.html`, `prototypes/01-mockups/final-costs-phone.html`,
`prototypes/01-mockups/final-config.html`, with `prototypes/01-mockups/critique.md`. The HTML files are the reference, not the
scripts that generated them. The single-option files (`layout-a-sidebar-light.html`,
`spacing-comfortable.html`, `colour-one-accent-dots.html`, `cards-two-tone.html`,
`type-inter-two-weights.html`) show each choice alone; where they differ from a `final-*` file,
the `final-*` file wins. Where `final-batch.html` differs from Q9, Q9 wins: see section 5, "Where
the delivery differs from `final-batch.html`".

The CR is verbal (no `issue:` line). It is one CR (Q10).

## Decisions carried from 02-answers.md

| Q | Decision |
| --- | --- |
| Q1 layout | Layout A: a white sidebar with a hairline, the active item a grey pill with no border, section captions in small grey capitals, a breadcrumb header. |
| Q2 spacing | Comfortable: an 8px rhythm on a 4px base, nav rows 36px, card padding 10px (vertical) / 12px (horizontal), text 14px. |
| Q3 colours and states | One deep accent; states as small dots or icons, not tinted borders and fills; the legend in a tooltip. |
| Q4 typography | One sans-serif, Inter, shipped with the board (no network); two weights, regular (400) and medium (500); page titles 24px medium. |
| Q5 cards | Two-tone: a white body, a grey band at the bottom for the metadata (rounds, PR, cost, folder, long gate); radius 14px; a diffuse shadow. |
| Q6 scope | Every view: Home (surface and project), Triage, Kanban, Batch, PRs, Costs (with its receipt), Configuration; the docs screenshots redone; cost-receipt's ticket follows this style. |
| Q7 combined and critique | On the Batch page: no "For information." label, no earlier batches' CRs; one PR column; no "Batch" figure card and no counters line under the title; one "nothing to review" sentence; the picker's subtitle names the batch, not a cut path. |
| Q8 order | cost-receipt waits for this CR (`depends.json`); timing-settings runs in parallel (they share files only), and whichever of the two lands second takes the other's changes. |
| Q9 board-batch-view | This CR takes three points of that inbox item: no Merged PR section; no grouping by state (each CR keeps one position, its state shown by its colour plus a badge in the top right corner); no ": after level 0". The rest of that item (history navigation, arrowheads, the mode tooltip) stays there. |
| Q10 split | No split: one CR; the approved mock-up covers the restyle and the Batch view's content. |
| Q11 sticky header | The breadcrumb bar stays sticky, with its hairline and a light shadow when the page scrolls; the point leaves board-triage-polish. |

Q8 is the batch's frame, not code: when the batch opens, the Chief of Staff writes cost-receipt's
`depends.json` on this CR; timing-settings gets none on it.

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/board/` unless named
otherwise.

### 1. The font: Inter, shipped

- Add `web/fonts/` with Inter's official `woff2` files for the two weights only, 400 and 500
  (upright; no italic, no other weight), covering at least Latin and Latin-1 (the French page
  needs its accents). Take them from Inter's official release (rsms/inter), pin the version, and
  ship its licence (SIL Open Font License 1.1) beside them as `web/fonts/OFL.txt`, with one line
  naming the version and its source. No other font file.
- `.gitattributes` (repository root): add the line
  `skills/chantier/scripts/cli/src/chantier/board/web/fonts/*.woff2 binary`, after the existing
  `skills/chantier/scripts/cli/src/chantier/board/web/** text eol=lf` rule, so that the later line
  wins for the fonts and git never rewrites a font's line endings. `OFL.txt` stays under the
  `text eol=lf` rule.
- Declare them with two `@font-face` rules (`font-family: "Inter"`, `font-display: swap`,
  `src: url("../fonts/<file>.woff2") format("woff2")`) in a CSS file of `web/css/` (in
  `tokens.css`, or a new `fonts.css` linked first from `web/index.html`). The URL is relative and
  inside `web/`, as `skills/chantier/scripts/cli/tests/test_code_targets.py` requires.
- `static.py` already serves `.woff2` as `font/woff2`: no change there.
- `reply.py`: `HTML_POLICY` has `default-src 'none'` and no `font-src`, so the browser would
  refuse the font. Add `font-src 'self'` to it. Nothing else in the policy changes.
- `tokens.css`: `--font: "Inter", "Segoe UI Variable Text", "Segoe UI", system-ui, -apple-system,
  "Helvetica Neue", sans-serif`. `--mono` stays. No weight other than 400 and 500 anywhere in
  `web/css/` (every `font-weight: 600`, `700` or `bold` becomes 500), so the browser never
  synthesises a bold.

### 2. Tokens (`web/css/tokens.css`)

Every colour stays in `tokens.css` (the test refuses a colour anywhere else). The values below are
those of the `final-*` mock-ups; a Driver may round a value but not change the look.

- Surfaces and ink: the page, the sidebar and the main area white; hairline `#ececef`; ink
  `#1a1c21`, `#545862`, `#868a94`; chip and pill grey `#f2f3f5`; hover `#f6f7f8`; a column's
  background `#fbfbfc`; the card band `#f6f7f8` with a top hairline `#eff0f2`; a card's own
  border `#ebecef`.
- One accent, deep teal, for the primary buttons, links, the CR id, the active marks and the
  meters; its light tints for a pill or a badge on the accent; two more shades of the same teal for
  a split bar (Home's batch meter, Costs' split, the receipt), never violet, green or blue
  (critique 5). These names are fixed, so that the cost-receipt CR can cite them:
  - `--accent: #1d5c63` (the accent);
  - `--accent-dark: #123d42` (the darker shade);
  - `--accent-light: #8fb6ba` (the lighter shade);
  - `--accent-tint: #e9f1f1` and `--accent-tint-2: #e7f0f0` (the pill and badge tints).

  The three shades are those of the mock-ups' ticket (`--tk`, `--tk1`, `--tk3` in
  `final-costs.html`).
- States: one colour each, used only in a state icon, dot or badge (the Batch node's badge, section
  5), never in a card's border or fill: blocked `#d14b5e`, working `#4a76d9`, ready `#2f9e6b`,
  draft `#a77b4f`, local `#8b6bd8`, waits `#d08a1f`, queued `#a3a7af`, merged `#2a7a55`.
- Removed: the `--tint-*-edge` / `--tint-*-fill` pairs, the `--tag-*-fill` / `--tag-*-ink` pairs
  of the states, `--tag-cr-*`, and the three `--mode-*` colours, once nothing uses them. The
  six label colours stay, for a label's small square only (below). The autosync pill's state
  colours and the dark selection bar and toast stay.
- Type: `--text` 14px, `--text-small` 12px, `--text-badge` 11px, `--title` 24px (weight 500,
  letter-spacing about -0.02em), `--title-phone` stays 24px or less; captions 11px, weight 500,
  upper case, letter-spacing 0.08em, grey `#8d919a`.
- Space and shape: the 4px base and 8px rhythm (`--space-*` as today); nav row height 36px; nav
  radius 8px; card padding 10px / 12px; gaps 12px, 20px and 32px between sections; `--radius`
  16px (a column, a section), a card's radius 14px; sidebar 248px wide, padding 16px / 14px; the
  main area's side padding 32px; the breadcrumb bar about 58px high.
- Shadows: a card `0 1px 2px rgb(16 24 40 / 4%), 0 8px 24px -10px rgb(16 24 40 / 14%)`; a figure
  card the same, a little softer; menus and the tooltip `0 10px 30px rgb(16 24 40 / 12%)`; the
  sticky breadcrumb bar, once the page has scrolled, a light one such as
  `0 1px 8px rgb(16 24 40 / 6%)` (a token, e.g. `--shadow-head`).

### 3. The shell (`web/index.html`, `web/css/shell.css`, `web/js/ui/`)

- Sidebar (`shell.css` `.side`, `.nav`, `.sec`, `.foot`; `ui/sidebar.js`): white, a 1px hairline
  on its right. The active item is a grey pill (`#f1f2f4`), no border, no ring
  (`--ring-nav` goes), its text ink and medium; the others `#545862`. Icons thin, monochrome
  (`icons.js`'s outlines with a 1.5 stroke), grey, the active one ink. The counters stay on the
  rows that have one (`registry.js` unchanged) but in a light grey `#a3a7af` at 12px. Section
  captions in small capitals: "Views" above the views, and "Sync" above the autosync pill when it
  shows (new key `nav.sync` in `js/i18n/en.js` and `fr.js`, "Sync" / "Synchro"). The foot keeps
  the data's age and the language button, without its top border.
- Picker (`ui/picker.js`, `trigger`): no border at rest, a light hover; the project's sub-line is
  the batch and its state only (`batch-12 running`, or the no-batch words), never the inbox count
  that made it too long to fit (critique 4). The open menu is lighter (the user's word,
  2026-11-17): each row shows the project's mark, its name and, only while a batch runs, the
  batch and its completion in percent (`batch-23 · 40 %`, the CRs done over the batch's CRs, as
  Home's batch meter counts them); no inbox count, no folder, no repo line (`pathsOf` leaves the
  menu; those go to the project's Home). The surface's own row shows its name only. The
  project's mark stays a small coloured square (radius 8px). A long project name
  (`agentic-planning-surface` at the sidebar's width) never runs into the chevron: the name
  shrinks and ends in an ellipsis, with a fixed gap before the chevron, which stays centred on
  the button's height (the user's screenshot, 2026-11-17: the name touched the chevron, and the
  chevron sat below the name's line).
- Header (`index.html` `.head`, `ui/header.js`, `main.js` `drawFrame`): a breadcrumb bar on top
  of the main area, under a hairline: grey parents, the current page in ink, "/" separators in a
  lighter grey, and **+ New** at its right as today. Its crumbs: the project, then the view; on
  the Batch view, the batch's id and a grey chip with its state icon and state ("running",
  "paused", ...); on All projects, the surface's name, then the view. Under the bar, the page title
  (24px medium) with the counters line beside it on the same baseline, quieter (13px, grey,
  figures in `#545862` medium), not under it. The Batch view shows no counters line: the crumbs
  and the mode strip say it (critique 2). The refused-key notice stays, restyled as a quiet
  bordered line without a red fill (red text is enough).
- Sticky breadcrumb bar (Q11): today `.head` (`shell.css`) is not sticky. It becomes
  `position: sticky` at the top of the scrolling area, on a white background, above the content
  (a `z-index` under the menus, the panel and the dialogs), with its bottom hairline always drawn;
  once the page has scrolled away from the top, it also carries the light shadow above (a class
  that `ui/header.js` sets from the scroll position, or an equivalent the Driver picks), and loses
  it back at the top. The page title under the bar scrolls away with the content. The same holds
  at a phone width for the top row the bar folds to. The picker's menu and the **+ New** dialog
  still open above everything.
- Phone (`@media (max-width: 760px)`, `ui/bottombar.js`): the same tokens; the bottom bar white
  with a hairline, the active item in ink medium; the breadcrumb bar folds to the picker button
  and **+ New** at the top as today; the page title stays. A row of every view fits 390px wide.

### 4. Shared pieces (`web/css/components.css`, `web/css/widgets.css`, `web/js/ui/parts.js`, `web/js/ui/icons.js`)

- State icons: add to `icons.js` one small outline glyph per state, drawn in the state's colour,
  as in the mock-ups (working: an open ring; draft: a dotted ring; ready: a ring with a check;
  waits: a ring with a clock hand; merged: the merge glyph; blocked, queued, local: their own
  glyph or a plain dot). `parts.js` gets `stateIcon(state)`; `stateTag` and every view that drew a
  tinted tag or card for a state draw the icon (or a dot where there is no room) and the state's
  word in grey ink, except the Batch node's badge (section 5), whose word takes the state's
  colour. `tint()` and the `st-*` fill and border rules go; a card is white with its hairline in
  every state.
- Chips and tags: neutral grey (`#eceef1` / `#f2f3f5`), no border, 12px, radius 6px, ink
  `#545862`. The CR id keeps a colour: the accent, medium, with no fill. A label is a grey chip
  with a 6px square in its label colour before the word. A priority (P1...P4) is a grey chip;
  `3-ready` the accent tint. The "release" and "fix" kinds are grey chips.
- Two-tone cards: a white body (the ids, the title, the step), then a grey band at the bottom
  (`margin: 10px -12px 0; padding: 8px 12px`, the band colour, the top hairline) holding the
  metadata: the round, the dependencies, the PR, the cost, the folder icon, and the long gate's
  line. Radius 14px, the card shadow, overflow hidden so the band follows the radius. This
  applies to the Batch graph's nodes, the Batch PR cards, the Kanban cards, the Triage post-its
  (their files, state mark and source go in the band) and Home's cards.
- Figure cards (`kpi`): white, radius 14px, the soft shadow, no border colour of a tone; the label
  12px grey, the figure 24px regular, the sub-line 12px grey. The `tone` classes (calm, go, hot)
  keep their meaning through a state icon or the accent, not a tinted fill.
- Meters: 6px high, grey track, the accent (or its shades for a split).
- Buttons: the primary one the accent with white text, radius 8px, medium; the others white with a
  hairline.
- The Triage "modified" mark sits inside the post-it's top row, at its right, as in the
  `final-batch.html` strip (accent tint, 11px), so it is never cut at the card's top edge.

### 5. The views (`web/js/views/`, `web/css/views/`)

The rule for every view: the tokens and the shared pieces above; the content and the actions stay
as today unless this list says otherwise.

- **Batch** (`views/batch.js`, `batch-graph.js`, `batch-prs.js`, `batch-pr-card.js`,
  `model/semantics.js`, `css/views/batch.css`, `css/views/batch-prs.css`):
  - Four figure cards: Slots, Working, Handed back ready, Spent. The "Batch" figure card goes
    (`figures` drops the `t('batch.batch')` kpi; the key goes from both languages if unused).
    Handed back ready keeps its sub-line (`batch.review_merged`, "N to review · N merged").
  - The mode strip names the mode and the steering, "Stack · Foreman" (`modeWords(...).name` and
    `steeringWord(batch)`), on the accent tint; its text and the three mode pills as today, the
    current one a grey pill.
  - The graph sits on a light dotted grid (a 1px dot every 16px on `#fcfcfd`, a hairline border,
    radius 16px). The arrows a light grey as today.
  - Each arrow ends on its card (the user's screenshot, 2026-11-17: on CR-321's card the head
    floated left of the card, pointing right, apart from its line, which came up from below):
    the head sits at the end of its line, on the card's edge, and points along the line's last
    segment, whatever the line's route (straight, bent, coming from above or below). This CR
    takes this one point of `board-batch-view`'s arrowheads; the heads when a CR waits for
    several others stay there.
  - Levels, no state groups (Q9): each level is one column with its head in grey and its CRs
    under it, with no state group head. `batch-graph.js`'s `group` and the `groupByState` call
    go; `groupByState` goes from `model/semantics.js` when nothing else uses it (today only
    `batch-graph.js` does), and the `.batch .grp` and `.batch .gh` rules from `batch.css`. A CR's
    place is its level and its order in the batch's record (`batch.crs`, as `levels` keeps it):
    a change of state never moves it, so a CR stays where it is from queued to merged. A merged
    CR stays in its level as a node like the others.
  - Level heads (Q9): level 0 keeps `batch.no_dep` ("No dependency" / its French); the others say
    only "Level N": `batch.level` becomes `'Level {i}'` in `en.js` and `'Niveau {i}'` in `fr.js`,
    and `batch-graph.js` passes only `i`.
  - The state on a node (Q9): a badge in the node's top right corner, on the row of the CR id and
    the folder's slug, the CR id and slug at its left: a small chip (radius 6px, 11px text) with
    the state's icon and the state's word (`t('state.<state>')`), both in the state's colour, on
    white with a hairline, or on a light grey; the node itself stays white with its hairline
    (Q3, Q5): no tinted border or fill. The badge does not push the title to a second row: the
    slug truncates first. `nextTag` keeps its place. For a merged CR, the band (Q5) says
    "merged N ago" (`prs.merged_ago`) and, when the record holds it, the long gate's line, so
    nothing the Merged section showed is lost.
  - The legend row goes from the page: a "States and arrows" grey pill, focusable
    (`tabindex="0"`), opens a tooltip on hover and on focus with the eight states (icon and word,
    in `STATE_ORDER`) and the arrow's sentence; beside it, a grey hint ("hover for the legend";
    new key in both languages). The note under the graph (`batch.hover`) stays.
  - One PR column (`batch-prs.js`), about 380px wide, so the graph gets the width back
    (critique 1): "PRs to review" with its count; when there is none, one sentence that says
    there is nothing to review and why (today's `reviewHint` and `prs.none` become one sentence,
    critique 3); the drafts under it ("In draft · N") on the stack rail as today. Nothing under
    the drafts: no Merged section (Q9). `mergedColumn`, `mergedCard`, `earlierCard`, `EARLIER`
    go from the code, and `prs.merged`, `prs.none_merged`, `prs.info`, `prs.earlier` from both
    language files (`prs.merged_ago` stays, for the merged node's band). The board's `merged`
    data stays served (Home and Costs read it).
  - Where the delivery differs from `prototypes/01-mockups/final-batch.html` (Q9 wins over the mock-up): the
    mock-up groups each level's nodes under state heads ("working · 1", "PR in draft · 1", ...);
    the delivery has no state heads and keeps each CR in its record order. The mock-up says
    "Level 1: after level 0"; the delivery says "Level 1". The mock-up's nodes carry no state
    badge (the state is in the group head); the delivery's carry the badge in the top right
    corner. The mock-up's PR column ends with "Merged · 1" under a hairline rule; the delivery
    ends with the drafts. Everything else on the page (the crumbs, the figures, the mode strip,
    the legend pill, the dotted grid, the two-tone nodes, the PR cards, the Triage strip) follows
    the mock-up.
- **Triage** (`views/triage.js`, `triage/*.js`, `css/views/triage.css`, `css/views/postit.css`):
  the columns on `#fbfbfc` with a hairline, radius 16px; the post-its as two-tone cards; the
  grill-state legend stays inline in the bar, grey; the next-batch indicator a grey pill; the
  "modified" mark inside the card (above). Column widths and the post-its' fixed width stay as
  today.
- **Kanban** (`views/kanban.js`, `kanban-cards.js`, `css/views/kanban.css`): the columns and
  cards as Triage's; the state as an icon in the card's band.
- **Home**, project and surface (`views/home*.js`, `views/overview.js`, `css/views/home.css`,
  `css/views/overview.css`): the tiles as figure cards; the blocks as white sections with a
  hairline and radius 16px, their headings 13.5px medium; the batch meter in the accent's shades;
  the pipeline legend's dots in grey and the accent shades; the surface table with hairline rows,
  the project marks as today. The project's Home gets a "Project" section (the user's word,
  2026-11-17): its folder in the planning surface, its repository's path, and its upstream URL
  (the repository's `origin` remote, as a link to the forge's page when it is an HTTPS or a
  `git@host:owner/repo` remote; the raw text otherwise; "none" with no remote). These lines leave
  the picker's menu (Picker, above). The surface's Home shows the surface's own path and upstream
  URL the same way.
- **PRs** (`views/prs*.js`, `css/views/prs.css`): hairline rows, the forge state and the checks
  as state icons with their word; the warning lines in red text, no red fill.
- **Costs** (`views/costs*.js`, `css/views/costs.css`): a restyle only, the page's content
  unchanged: the Recompute line, the four figure cards, the per-CR table, the earlier batches and
  the last merged CRs keep what they show, in this style: tables with hairline rows and no zebra,
  the CR id in the accent, the cost right-aligned. This CR changes no column and no line of the
  page, and does not touch `costs-tables.js`'s columns. The phone fold of the per-CR table (no bar
  and state columns, no Recompute note, so a row fits 390px; critique 7) belongs to the
  cost-receipt CR, which owns the Costs page and edits `costs-tables.js` on the same lines. The
  receipt (the ticket) and the page's two-column arrangement (ticket on the left, sticky, the
  cards on the right; ticket on top on a phone) are the cost-receipt CR's work too, done after
  this CR lands (Q8); its ticket uses this CR's font and the accent's three shades, `--accent`,
  `--accent-dark` and `--accent-light` (Q6).
- **Configuration** (`views/config.js`, `css/views/config.css`): a white card per host, radius
  16px, a header row in grey small text, hairline rows, a value in a grey chip, a value set in the
  project's `chantier.yaml` in the accent tint; the select boxes and the Save button in the button
  style above. The Timing tab of `final-config.html` belongs to the timing-settings CR, which runs
  in parallel with this one (Q8): whichever of the two lands second rebases on the other and
  takes its changes in `tokens.css` and `css/views/config.css` (the Timing tab in these pieces).
- **Panel, dialogs, editor, journal, autosync, toast** (`css/panel.css`, `css/dialog.css`,
  `css/editor.css`, `css/journal.css`, `css/autosync.css`): the tokens, the font and the radii;
  structure unchanged. The autosync pill keeps its state colours (as dots).

### 6. Docs

- `just docs-screenshots` retakes every picture of `docs/web-board/` (all views, both sizes) on the
  new style.
- `docs/web-board.md`, "Batch": the figures are four (slots, working, handed back ready, spent);
  the CRs sit in levels, "Level N" with no "after level" words, each CR in one place for its whole
  life, merged ones included; "The colour is the state" becomes: the state is a badge in the CR's
  top right corner, its icon and word in the state's colour, its legend in the "States and
  arrows" tooltip; the right column is one column, the PRs to review then the drafts (the
  "**Merged PRs**: for information, this batch's and the earlier batches'" bullet goes, and the
  batch picture's alt text no longer names merged PRs). "The views": the breadcrumb at the top,
  which stays in place when the page scrolls. Nothing else in the docs names the old look.
- `CONTRIBUTING.md`: the "Page" bullet adds that the page loads its own font from `web/fonts/`
  (`font-src 'self'`), and no font from outside.
- The release notes of the version that ships it name the new look, as the release process asks.

## Out of scope

- The cost receipt itself, the Costs page's two-column layout and the phone fold of its per-CR
  table and Recompute note (CR cost-receipt, which waits for this one), including the
  two points `prototypes/01-mockups/critique.md` leaves open (which batch Costs shows by default and how to pick
  another one; whether the receipt's "thank you · N PRs · 0 reverted" line has record figures or
  goes): cost-receipt's answers keep them open for its own specification.
- The Configuration page's Timing tab and its settings (CR timing-settings).
- The rest of the inbox item `board-batch-view`: the batch history navigation (previous / next
  batch), the arrowheads when a CR waits for several others, the tooltip on the mode pills, and
  the wider rework of the connected cards (Q9). Removing from that item the three points this CR
  takes, and from `board-triage-polish` its sticky-header point (Q11), is the Chief of Staff's
  edit of those folders, not this CR's.
- The Triage column alignment of the inbox item `board-triage-polish`; only the clipped "modified"
  mark is fixed here, because the reference draws it inside the card.
- Layouts B and C, the compact and airy spacings, serif titles, soft tints, flat cards: rejected
  in the grill.
- A dark theme; any change to what the board reads, writes or serves, other than the font files
  and the `font-src` line; the CR board pane in Claude Code (`hooks/`).

## Evidence

- `just check` passes (Linux, macOS, Windows): Biome on `board/web`, and
  `skills/chantier/scripts/cli/tests/test_code_targets.py` (no colour outside `tokens.css`, at
  most 300 lines per CSS or JS file, no id selector, nesting at most 3, every `url()` relative and
  inside `web/`, no other origin).
- `skills/chantier/scripts/cli/tests/test_board.py`, `test_the_frame_is_shipped_with_the_package`:
  add the two `woff2` files and `fonts/OFL.txt` to its list; and one assertion that
  `reply.HTML_POLICY` holds `font-src 'self'`. No other new test.
- The words' test (`skills/chantier/scripts/cli/tests/`): the keys stay the same in both languages
  (the existing check), with `nav.sync` and the legend hint added, and `prs.info`, `prs.earlier`,
  `prs.merged`, `prs.none_merged` (and `batch.batch` if unused) removed from both.
- In a browser on `chantier board` over `docs/demo/` (as `just docs-screenshots` starts it), the
  developer tools show the two Inter files loaded from the board itself, no CSP error, no request
  to another origin, and the computed font of a title "Inter" at 500.
- The Batch view over the demo: no state group heads; level heads "No dependency", "Level 1",
  "Level 2" (French "Niveau 1"...); each node carries its state badge at its top right in the
  state's colour, the node white; a merged CR sits in its level with its "merged ... ago" band;
  the PR column ends with the drafts, with no Merged section. Every arrow's head touches its
  card at the end of its line and points along it, for a wait between two levels and for one
  whose line bends (a screenshot showing CR-321's wait on CR-319, as in batch-23). Then, on a copy of the demo with
  one CR's state changed in the record (e.g. working to ready, and draft to merged), the board
  redraws those CRs at the same place in their level, only their badge changed.
- The sticky bar: on a view longer than the window (Triage, Batch, Costs over the demo) at desktop
  and at 390px, scrolling keeps the breadcrumb bar (or its phone row) at the top with its
  hairline, the shadow shows once scrolled and goes back at the top; the picker's menu and the
  **+ New** dialog open above it.
- The picker with a long project name: over a project named `agentic-planning-surface`, at
  desktop and at 390px, the name ends in an ellipsis before the chevron with a visible gap, and
  the chevron is centred on the button's height; one screenshot of each.
- The picker's open menu over the demo: each row is the mark, the name and, for a project with
  a running batch only, `batch-<n> · <p> %`; no inbox count, folder or repo line. The project's
  Home shows its folder, repository path and upstream URL (a link for a GitHub remote); one
  screenshot of each.
- `just docs-screenshots` run; the new `docs/web-board/*.png` committed. The PR's Deliverables
  carry, side by side, the Batch, Costs (desktop and phone) and Configuration screenshots with
  `prototypes/01-mockups/final-batch.html`, `final-costs.html`, `final-costs-phone.html` and
  `final-config.html` at the same size, and the Home, Triage, Kanban and PRs screenshots, each
  captioned with the head's SHA (seven characters). The Batch pair names the Q9 differences
  listed in section 5; a difference from a mock-up that the cost-receipt or timing-settings CR
  owns is named, not hidden.
- The French page checked once (`?lang=fr`): the accents in Inter, no text cut in the sidebar,
  the crumbs, the node badges or the PR column.
- A phone width of 390px and 375px: no horizontal scroll on any view but the Batch graph's own
  scroller.
- The long gate: the board is part of the CLI package, so the PR passes `just scenario
  (ubuntu-latest)` on CI at its head. No CI job changes.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17), keeping the approved Q3 and Q5: the
state's colour is in the badge (icon and word, in the state's colour), the node stays white. The
user sees it in the PR's screenshots and can ask for a coloured edge then.
