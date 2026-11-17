# Change Specification: the board's design is realigned across every page

## Goal

The user finds the web board ugly in three named places (the cards' thick coloured left border,
the Kanban's priority chips, the CR drawer) and asked for a full UX and design QA
(`intake/ux-qa.md`). The QA found sound tokens that the pages do not follow: every level draws its
own box, about 15 font sizes, 12 radii and 7 chip looks, mixed languages. This CR makes the board
read as one calm product on every page, desktop and phone, by the report's rules as the user
accepted them (design-Q2), and makes every word of the board go through its translations, with a
project rule and a test that keep it so (design-Q3).

Base: this CR is based on `board-design-bugs` (design-Q1), which goes first and fixes the four quick
bugs: the drawer tree's `.nm`/`.ind` class collisions, the Kanban priority buttons' browser border
and grey square, the front matter in `panel/markdown.js` (a muted key/value list), and the "---"
titles from `status/views.py` `_title()`. This CR does not redo them; it restyles what they leave
with the rules below and builds on the class names they chose.

Paths below are under `skills/chantier/scripts/cli/src/chantier/board/web/` unless they start
with the repository's root (`AGENTS.md`, `CONTRIBUTING.md`, `docs/`, `scripts/`,
`skills/chantier/scripts/cli/tests/`).

## The rules (design-Q2), as they apply to the code

1. **One surface, one edge.** Two surfaces: the page (white) and the card (white, 1px `--line`
   hairline, radius `--radius` 10px, no shadow at rest). A shadow only on what floats: the drawer
   (`--shadow-panel`), menus and popovers (`--shadow-menu`), dialogs (`--shadow-dialog`), a dragged
   card and the selection bar (`--shadow-float`). Never a border and a shadow together at rest. A
   selection or focus ring (`box-shadow: 0 0 0 Npx var(--...)`, no blur) is not a shadow (S13).
2. **Never a box in a box.** A grouping (column, lane, block, section) is a heading and white
   space, at most one hairline between groups, never a frame. Lists are rows with a bottom divider
   (the PRs page's rows), never boxed rows (S8).
3. **No side bars.** No coloured left or right border anywhere. A side border is only a 1px
   `--line`/`--side-line` divider between two layout regions (the sidebar, the drawer's tree
   column). Priority shows once, in the priority chip.
4. **One chip** (`.chip`), **one filter chip** (`button.chip`), **one segmented control**
   (`.seg`), **one KPI tile** (`.kpi`), **one card** (`.card`), defined once (below) and used on
   every page.
5. **Type scale, five steps; radii, three steps; spacing on its scale** (tokens below), referenced
   by token only.
6. **Class hygiene:** no short class name shared by unrelated components; each view's rules are
   scoped under its root (`.kanban ...`, `.panel .tree ...`); the generic names `.x`, `.r`, `.c`,
   `.lbl`, `.lab`, `.band`, `.eff` are renamed or deleted where they are touched.
7. **The accent tint means "on" and nothing else:** it leaves the Kanban column headers, the Costs
   KPI tiles and the Batch mode strip.

## Tokens (`css/tokens.css`)

- **Type scale:** `--text-badge: 11px`, `--text-small: 12px`, `--text: 14px`, `--text-heading:
  16px` (new; weight 500), `--title: 24px`. Delete `--text-stat` (13px) and `--title-phone`
  (24px, same as `--title`). Every `font-size` in `css/` is one of these five tokens; delete each
  raw literal (today 12.5, 13, 13.5, 14, 15, 15.5, 16, 17, 18, 22px in `home.css`, `overview.css`,
  `home-project.css`, `kanban.css`, `prs.css`, `batch-prs.css`, `panel.css`, `dialog.css`,
  `components.css`, `widgets.css`, `config-timing.css`). The only exception: the Costs paper ticket,
  on screen and in its image (realign-Q1), takes `--ticket-*` size tokens (from today's 13, 22, 34 and 40px in `costs-receipt.css`),
  used only in `css/views/costs-receipt.css`. Two weights stay: 400 and 500.
  Mapping: badges and counts 11; meta lines, captions, chips, table cells and small buttons 12;
  body, card titles (500), column and lane headings (500), PR row titles 14; section headings
  (Home blocks, Costs sections, Configuration hosts, Batch sections, a dialog's title, the
  drawer's title, a rendered document's `h1`) 16/500 (S7); page title and KPI figures 24/400.
  A rendered document's `h2`/`h3` 14/500, deeper headings 12/500 `--ink2`.
- **Radii:** `--radius-s: 6px` (chip, input, select, button, segmented control, hover and selected
  fills of rows), `--radius: 10px` (card, KPI tile, drawer, dialog, menu, popover, toast, selection
  bar, a Kanban column's field), `--radius-full: 999px` (dots, swatches and avatars only; replaces
  `50%`). Delete `--radius-m` (9px), `--radius-card` (14px), `--radius-nav` (8px) and every literal
  (`2px`, `3px`, `4px`, `7px`, `9px`, `10px`, `99px`, `999px`, `var(--space-2)`): the sidebar's
  nav items take `--radius-s`.
- **Greys:** one chip grey, `--chip`. Delete `--chip-2`, `--pill`, `--band` and
  `--band-line`; `--state-queued-tint` keeps pointing at `--chip`. `--hover`, `--hover-soft` and `--row-hover` (all
  `#f6f7f8`) become one `--hover`.
- **Shadows:** keep `--shadow-menu`, `--shadow-panel`, `--shadow-dialog`, `--shadow-float`, and the
  ticket's two (the paper ticket only). Delete `--shadow-card`, `--shadow-card-soft`, `--shadow-note`,
  `--shadow-note-hover`, `--shadow-head`.
- **Spacing:** `--space-1..5` (4/8/12/16/24) plus `--space-6: 32px` (new); `--gap-main` becomes
  `var(--space-6)`. Every `margin`, `padding` and `gap` value is `0`, `auto`, a `--space-*` token,
  its negative (`calc(-1 * var(--space-N))`), a component token below, or a 1px/2px optical offset.
  Groups are 24px apart, cards 8px apart.
- **Component tokens (S6):** `--chip-h: 20px`, `--chip-pad: 6px`, `--dot: 6px`, `--row-h: 32px`
  (a file row), `--icon: 16px`, `--size-col: 56px`.

## The components (defined once)

- **Card** (`css/cards.css`): `.card` white, 1px `--line`, `--radius`, padding `--space-3`, no
  shadow; hover darkens the edge (`--card-hover`); `.card.sel` an `--accent` edge and a 2px
  `--accent-tint` ring; `.card.lifted` (dragged) no edge and `--shadow-float`. Anatomy: a top row
  (`.row-tags`: the CR id as bare accent text, chips), the title 14/500 (`.ttl`), the description
  12 `--ink2` (`.desc`), the meta line 12 `--ink3` with an 8px top gap, on white: no band, no fill,
  no hairline, no negative margins (the `.band`/`.meta` rule becomes `.card .meta`). Delete the
  priority left border (`.card.pri-P1..P4` and its `:is(.sel, .pi, .lifted, ...)` rule) and
  `--pri-c`. Triage's post-it (`.card.pi`) is this card: no tilt and no shadow on hover; the lift
  shows on drag only; a selected post-it shows its check mark and the `.card.sel` look.
- **Chip** (`css/tags.css`, which keeps the chips and the state icons): `.chip` inline-flex,
  height `--chip-h`, padding `0 var(--chip-pad)`, `--radius-s`, 12px/500, `border: 0`, fill
  `--chip`, ink `--ink2`, gap `--space-1`. Variants change only fill and ink: `.chip.st-<state>`
  (the state's tint, its icon in the state's colour); `.chip.pri` (neutral, a `--dot` swatch in
  `--pri-1..4`, word `--ink2`: S4); `.chip.label` (neutral, a `--dot` swatch in the label's
  colour); `.chip.badge` (11px). The CR id is not a chip: bare text in `--accent`, 500
  (`.crid`). Slugs, rounds, costs, batches and other facts are text, not chips. This replaces
  `.tag`, `.tag.badge`, `.tag.cr`, `.tag.pri-*`, `.tag.pri-3-ready`, `.tag.st.*`, `.lbl`, `.lab`,
  Triage's `.ind` pill, `.pi .chgm`, the Kanban `.colh .c` count (plain `--ink3` text now), the
  Configuration `.eff` chip (deleted, below) and the Batch `.mode` pills (the segmented control).
  `ui/parts.js` (`tag`, `stateTag`, `dot`) and `labels/tags.js` draw the new classes.
- **Filter chip:** `button.chip` resets the user agent (`border: 0; background: var(--chip); font:
  inherit; color: var(--ink2)`). Off: the neutral chip. On (`aria-pressed="true"`): `--ink` text on
  `--accent-tint` with an inset 1px `--accent-line` ring. Focus: the focus ring. The label filter
  (`labels/filter.js`) and the priority filter (`labels/priority.js`) use it; a label adds its
  swatch, a priority none (the bugs CR removed its square). The `.lfil`/`.lbtn`/`.lclr` rules move
  to it (`.lclr` stays a text link button).
- **Segmented control** (`css/components.css`): `.seg` a `--chip` track, `--radius-s`, padding 2px;
  segments 12px, `--ink2`; the selected one white with a 1px `--line` edge and `--ink`. Used by the
  Batch mode strip (read-only: the board never edits a batch, so the segments are `span`s, the
  current one selected, no button) with the mode's sentence below as a 12px `--ink3` caption, and
  by the Configuration tabs (Models / Timing: buttons, `role="tab"`).
- **KPI tile** (`css/cards.css` `.kpi`): white, 1px `--line`, `--radius`, no shadow; label 12
  `--ink3`, figure 24/400, sub-line 12 `--ink3`. The same on Home, Batch and Costs: delete the Costs
  override (teal tint and teal border in `css/views/costs.css`).
- **List row:** the PRs page's row (`.pvrow`, `css/views/prs.css`) is the model: no box, a 1px
  `--line` bottom divider, hover `--hover`, padding `--space-2` `--space-3`; a first line (the PR
  number, the CR id, the title 14/500) and one meta line 12 `--ink3`. Factor it so Home's open PRs
  and the Batch PR column draw the same row (S8).
- **Icons:** stroke SVGs from `ui/icons.js` only, `vertical-align: 0` inside a flex row. Replace
  the text glyphs: `✓`/`⚡` (`triage/postit.js` `MARKS`, and the `⚡` inside the French and English
  `postit`/`grill` strings), `✓`/`✗` (`model/events.js`), `✕` (`triage/selection.js`), `→`
  (`triage/selection.js`), `↗` (`views/overview.js`); add the icons that `ui/icons.js` lacks.
  The `→` between two dates in `views/costs-receipt.js` is punctuation and stays.

## Page by page

Each page lists what changes and its files (CSS under `css/`, JS under `js/`).

### Shell (every page)

- The header's shadow becomes a bottom `--line` hairline (S13). The loading state names the view
  being opened, not Home: navigating to Triage shows "Triage · Loading…" (`js/main.js`,
  `ui/header.js`). The phone's autosync dot gets an accessible name and a `title`
  (`t('autosync.title', ...)`) (`ui/autosync.js`, `css/autosync.css`).
- Phone bottom bar: four views and More (Home, Triage, Kanban, Batch, More); More opens a menu
  (the picker's menu style) with PRs, Costs and Configuration; the current view under More marks
  More as current; new key `nav.more` (S12) (`ui/bottombar.js`, `css/shell.css`).
- Sidebar, crumbs, picker, batch navigator: radii and sizes on the scales; the batch navigator's
  `99px` pill and `--text-stat` move to the chip and the 12px step.
- Files: `css/tokens.css`, `base.css`, `shell.css`, `sidebar.css`, `crumbs.css`, `picker.css`,
  `batch-nav.css`, `components.css`, `widgets.css`, `tags.css`, `cards.css`, `autosync.css`,
  `journal.css`, `dialog.css`, `editor.css`; `js/main.js`, `ui/header.js`, `ui/bottombar.js`,
  `ui/sidebar.js`, `ui/picker.js`, `ui/parts.js`, `ui/icons.js`, `ui/item-card.js`,
  `ui/autosync.js`, `ui/dialog.js`, `ui/toast.js`, `journal/journal.js`.

### Home (All projects and a project's Home)

- Blocks are sections (a 16/500 heading, no frame); their list rows (`.home .x`) are rows with a
  bottom divider, the class renamed; Home's open PRs use the list row.
- The KPI tiles: the one tile; on a desktop width all tiles share one row (no fifth tile alone on
  a second row); two per row on a phone.
- The stat label "Dernier signe du Foreman"/"du CoS" becomes short: fr "Foreman vu"/"CoS vu", en
  "Foreman seen"/"CoS seen" (`home.sign_foreman`, `home.sign_cos`).
- The overview's project lines and the project page: rows with dividers, chips and type on the
  scales; `↗` becomes the icon.
- Files: `css/views/home.css`, `home-project.css`, `overview.css`; `js/views/home.js`,
  `home-batch.js`, `home-backlog.js`, `home-feed.js`, `home-history.js`, `home-prs.js`,
  `home-project.js`, `overview.js`.

### Triage

- Lanes (`.tcol`): unboxed sections, a 14/500 heading with its count in `--ink3`, a top `--line`
  hairline, no fill, no radius (S9). Cards: the one card, no left bar, no band.
- A group frame (`.grpf`): a `--col-fill` fill with `--radius`, no dashed edge; its close button
  is a ghost icon button (rename `.grpf .x`).
- Grill marks (`.gs`) and indicators (`.ind`, whatever the bugs CR left of it): SVG icons and the
  one chip. The post-it hover tilt is deleted.
- The selection bar keeps its dark floating look (it floats), radius `--radius`, its buttons
  `--radius-s`; `✕` and `→` become icons.
- Files: `css/views/triage.css`, `postit.css`; `js/views/triage.js`, `triage/columns.js`,
  `triage/postit.js`, `triage/groups.js`, `triage/selection.js`, `triage/bar.js`,
  `model/grill.js`.

### Kanban

- Columns (`.col`): a `--col-fill` field, `--radius`, no border (S9). The header (`.colh`) is a
  plain text row: the column name 14/500, the count 12 `--ink3`, no tinted box, no state dot (the
  column dots in state colours are deleted from `views/kanban.js`). The sub-line (`.colsub`) is a
  12px `--ink3` caption on the same inset as the header (no 23px pad).
- The Inbox's "+ New" button leaves the column body: a ghost "+" icon button in the Inbox header,
  with `aria-label` and `title` `t('new.kanban')`.
- An Inbox card does not repeat its "Inbox" bucket chip inside the Inbox column
  (`ui/item-card.js`, `views/kanban-cards.js`).
- The filter row: the label filter and the priority filter are filter chips; "Priorities"/"Labels"
  are 12px `--ink2` captions; the count stays at the row's end.
- Files: `css/views/kanban.css`, `postit.css` (the filter rules move to the chip's file),
  `tags.css`; `js/views/kanban.js`, `kanban-cards.js`, `labels/filter.js`, `labels/priority.js`,
  `labels/tags.js`, `ui/item-card.js`, `model/columns.js` (only if a colour field goes).

### Batch

- The four KPI tiles: the one tile.
- The mode strip: the segmented control, read-only, the sentence as a caption (no teal band).
- The graph panel: no border; the dotted grid alone marks the canvas. Nodes are the one card (no
  shadow; the highlight keeps its `--halo` ring).
- The PR column: unboxed, a 16/500 heading per group (to review, drafts), the list row for each PR
  (S8); the stack rail (`border-left: 2px dashed` in `batch-prs.css`) becomes the stack position
  as text in the row's meta line ("1 of 3"), no side border.
- The long gate line is never clipped: it wraps inside the row (no `overflow: hidden` cutting
  it); its waiver text is data (S2).
- Files: `css/views/batch.css`, `batch-graph.css`, `batch-prs.css`; `js/views/batch.js`,
  `batch-graph.js`, `batch-prs.js`, `batch-pr-card.js` (becomes the list row's PR variant).

### PRs

- The row stays the model; its title renders inline code (backticks as `<code>`, through one
  helper in `core/format.js` used for every title the board shows: cards, nodes, rows, the drawer,
  Costs).
- "Read on the forge N s ago" is shown once, in the page's header line, not on every row
  (`readAt` leaves `prRow`).
- The state chip: draft, merged and closed in their state's tint and icon; open on the neutral
  chip with no icon (S11). The kind (`release`, `fix`) is a neutral chip.
- Files: `css/views/prs.css`; `js/views/prs.js`, `prs-row.js`, `prs-feed.js`, `core/format.js`.

### Costs

- The KPI tiles: the one tile (no teal).
- The receipt stays the paper ticket, on screen and in "Copy as image" (realign-Q1, which overrules
  S10): its grain, scissors, perforation, large figures and the red "PAS FINI" stamp that
  `costs-receipt-not-finished-stamp` puts on it are kept as they are. Only what surrounds it is
  realigned: the page's KPI tiles, tables, headings and the copy action's button. Its sizes and
  shadows move into `--ticket-*` tokens, used only in `costs-receipt.css`; if that CR has not
  merged when this one rebases, the stamp is out of this CR's scope and nothing here removes it.
- The per-CR table: the CR id alone in its column (the slug in the cell's `title`); the state chip
  and the round on one line; the table unboxed, rows with dividers; the history and last-merged
  tables likewise.
- Files: `css/views/costs.css`, `costs-receipt.css`; `js/views/costs.js`, `costs-receipt.js`,
  `costs-image.js`, `costs-tables.js`, `costs-history.js`, `costs-action.js`.

### Configuration

- Each cell shows the value once: the control (an input or select whose placeholder or empty
  option reads "inherited"), then at most one 12px `--ink3` line under it, "inherited: <value>
  (<layer>)" when the row's own value is empty. The `.eff` "effective" chip and its line are
  deleted; the "overridden by <path>" line, a reset line and a refusal stay (one line each).
- The legend ("shipped default / set in chantier.yaml"): caption text, each with a `--dot` swatch,
  not bordered pills (`config-timing.css`).
- The tabs (Models / Timing): the segmented control.
- The tables unboxed (no frame around `.scroll`), rows with dividers; the "Starts as" header is a
  short word that does not wrap (fr "Démarrage").
- A layer's name and a file's label from the server (`defaults`, a layer's label in `view.files`
  and `layers`) go through `t('layer.<code>')` (S2).
- Files: `css/views/config.css`, `config-timing.css`; `js/views/config.js`, `config-timing.js`.

### CR drawer (panel)

- Head (`panel/head.js`): the CR id and its state chip (an item: its priority chip; a merged CR:
  its id and the merged chip), then the title 16/500, then one muted 12px line of facts as text
  joined by " · ": a CR `slug · round 2/3 · $1.45 · gate words · after N · 5 files` (the gate stays
  a link when it has one), an item `slug · stage · N files`, a merged CR `batch · cost · N files`;
  then the folder's path, 12px `--ink3`. No `.lbl` chip. The close button: a ghost icon button.
- File list (`panel/tree.js`): no chips. Each row a grid `var(--icon) | name (ellipsis) |
  size` with the size right-aligned in a fixed `--size-col` column, `tabular-nums`, `--ink3`;
  height `--row-h`, gap `--space-2`; the hover and selected fills only, `--radius-s`. Folder
  headings are 11px uppercase `--ink3` captions ("INTAKE · 1"); nested rows indented
  `--space-4`.
- Front matter (from the bugs CR's key/value list): a 12px two-column grid, keys `--ink3`, values
  `--ink`, no box, one hairline after it; `type:` as a neutral chip, `description:` as the lead
  line in `--ink2`.
- The file's info line (`panel/file-view.js`): the file's path inside the CR's folder and the Edit
  button; the folder (already in the head) and the size (in the tree) leave it.
- Phone: the tree becomes a `<select>` file picker above the document (no 150px cap); the Edit
  button never breaks inside its word (`white-space: nowrap`).
- Files: `css/panel.css`, `editor.css`; `js/panel/panel.js`, `head.js`, `tree.js`,
  `file-view.js`, `markdown.js`, `files.js`, `edit/markdown-editor.js`.

### Dialogs, menus, toasts, the editor, the autosync popover

- They float: they keep their shadow, radius `--radius`; their inputs and buttons `--radius-s`;
  sizes on the scale (the dialog title 17px becomes 16/500).
- Files: `css/dialog.css`, `editor.css`, `autosync.css`, `picker.css`; `js/ui/dialog.js`,
  `edit/new-idea.js`, `ui/toast.js`, `ui/autosync-events.js`.

## Every word through the translations (design-Q3)

- **Scope (S2):** every word the board composes goes through `t()`/`tn()` (`js/model/words.js`):
  text in `html` templates, `title`, `aria-label`, `placeholder`, `alt`, `textContent` and
  `setAttribute(...)` literals, toasts, dialogs, empty and loading states. A fixed code from the
  server (a layer name, a PR or check state) is mapped through `t()` by its code. Data (file
  contents, titles, slugs, role descriptions from the shipped defaults, a CLI refusal or
  diagnostic, a waiver's rule quoted from `AGENTS.md`) is shown as it is, inside a translated frame
  ("exempt: {rule}").
- **Now:** the literal "PR" in `views/batch-graph.js` (two places) and the fallback refusal
  `the board answered ${res.status}` in `views/config.js` go through keys; every glyph
  moved into icons leaves its string; every French value equal to its English one is translated
  unless it is in the glossary (S3, confirmed by realign-Q2): today 62 keys are equal, among them `costs.receipt_steering`,
  `costs.receipt_part_steering` (Pilotage), `grill.auto`, `pipe.auto`, `postit.legend_auto`
  (automatisable), `sel.label`, `label.name`, `labels.title` (Étiquette(s)); the rest are glossary
  words or formats. Every new key of this CR (for instance `nav.more`, the PR word, the layer
  names) is added in English and French at once.
- **The rule (S1):** one line in the root `AGENTS.md`, in the rules list, worded close to:
  "A change to the board's web files (`skills/chantier/scripts/cli/src/chantier/board/web/`)
  shows every user-facing word through the board's translations (`js/i18n/`, English and
  French, the same keys), French included: no literal word in a view, a title, a label or a
  placeholder; data (file contents, titles, the CLI's own messages) is shown as it is. `just
  check` refuses a literal word and a French value left equal to its English one outside the
  glossary; see [CONTRIBUTING.md](CONTRIBUTING.md), "Words"."
  And `CONTRIBUTING.md`'s "Words:" bullet (the board's targets) grows to say the same with the
  detail: what counts as a word and as data, the glossary and how a key joins it, and the test
  that enforces it. Its "CSS:" bullet gains the design targets the second test enforces (below):
  the five type tokens, the three radii, the spacing scale, the shadows only on what floats, no
  side bar.
  Why there: `AGENTS.md` is what every session in this repository loads (Claude Code and
  Copilot) and the root of `chantier rules`, which every chantier role reads before its card; the
  line names the folder, so it applies whenever a change touches the web files. The repository has
  no folder-scoped rule mechanism, and a new one (a nested file, `.github/instructions/`) would
  serve one host and would not be listed by `chantier rules`.
- **The tests** (`skills/chantier/scripts/cli/tests/test_code_targets.py`, beside
  `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`; fast, file reads
  and regular expressions only):
  1. `test_the_board_shows_no_untranslated_word`: in every `js/**/*.js` outside `js/i18n/`, inside
     each `html` tagged template (holes `${...}` removed, nested templates handled), no text
     between tags and no `title`/`aria-label`/`placeholder`/`alt` literal holds a letter; no
     string literal with a letter is passed to `textContent =`, `setAttribute('title'|'aria-label'
     |'placeholder', ...)` or `toast(...)`; every literal key given to `t(`/`tn(` exists in the
     English file; every French value equal to its English one has its key in the test's
     `GLOSSARY` set (S3). Code in comments is ignored. A parametrized case per kind feeds the
     checker a planted literal and asserts it is caught, so the checker cannot silently pass.
  2. `test_the_board_css_keeps_the_design_tokens`: in every `css/**/*.css` but `tokens.css`, a
     `font-size` is one of the five type tokens (`--ticket-*` allowed in `costs-receipt.css`
     only); a `border-radius` is `0` or one of the three radii; a `margin`/`padding`/`gap` value
     is as the spacing rule says; a `box-shadow` is one of the floating shadows (the ticket's in
     `costs-receipt.css` only) or a ring with no blur; a `border-left`/`border-right` is absent or
     `1px solid var(--line|--side-line)`; every `var(--name)` used is declared in some CSS file or
     set by `setProperty` in `js/`.
  Both report every finding with its file and line, and the current tree passes them only once
  this CR's realignment is done.

## Out of scope

- The four bugs of `board-design-bugs` (its CR, first).
- A dark theme, a new colour, a new view, a change of what a view shows or does, a change of
  the server's API or of the record, a new language. The priority filter's behaviour (all on at
  the start, Inbox and P1..P4) stays.
- Translating data: file contents, titles, role descriptions, the CLI's messages (S2).
- The CR board pane of Claude Code (`hooks/`) and `status.py`'s `STATUS.json`: untouched, so the
  pane screenshot rule and `just mod` do not apply.

## Evidence and gates

AGENTS.md's gates for a change under the CLI's `src/`:

- `just check` in the worktree at the rebased head the Driver pushes (it runs `just lint` with
  Biome on `board/web/`, `just test` with the two new tests, `release-notes`); `just test` stays
  within 30 s above its 18.5 s of 2026-11-14.
- `just eval-dry-run` there before the first push (a change under the CLI's `src/`).
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head before
  its PR goes ready (a change to the CLI). If this CR is on top of the batch's stack, it also
  passes `just scenario` locally (`chantier gate`) at its head before the user merges.
- Not owed: `just mod` (no change to `hooks/` or `types/`); the pane screenshot (no change to the
  pane or `STATUS.json`).

Screenshots (S14):

- `scripts/docs_screenshots.py` gains `--lang en|fr` (default `en`: the `lang=` of `goto` and the
  context's locale), `--out <folder>` (default `docs/web-board/`) and `--root <checkout>` (default
  the script's own; the checkout whose CLI serves the board and whose `docs/demo/` is copied), and
  a PRs step that fulfils `**/api/projects/*/prs` with a fixed answer built from the demo batch's
  CRs that have a PR (one open, one draft, one merged), so the PRs page has `prs-pc.png` and
  `prs-phone.png`. Its `new_dialog` step's selector follows the "+ New" button if its name changes.
- **Before/after:** the head's script run twice in French: `--root <the base: board-design-bugs's
  head> --lang fr --out <work>/before` and `--root <this CR's head> --lang fr --out
  <work>/after`, each view at 1400x860 and 375x812: Home (All projects), a project's Home,
  Triage, Kanban, Batch, PRs, Costs, Configuration, the CR drawer, the editor, the New dialog, the
  picker, the autosync popover, and Triage's phone selection. The PR's Deliverables shows the
  pairs side by side, each captioned with its SHA (before at the base's, after at the head's), at
  least Kanban, Triage, the drawer, Batch, Costs and Configuration at both widths; the full set is
  under the CR's `work/` and named in Internal references, as the PR template says.
- **The docs:** `just docs-screenshots` at the head (English, as today) refreshes every
  `docs/web-board/*.png`, plus the new `prs-pc.png`/`prs-phone.png`; `docs/web-board.md` gets
  the PRs image in its PRs section and its words follow the new looks (the Kanban filter row, the phone's bar with More and the
  autosync dot, line 122). README's `docs/web-board/batch-pc.png` is refreshed with the rest.

The Verifier's checks, on the head, in French and in English, at both widths:

1. No coloured side border on any card; no card, tile or row with both a border and a shadow at
   rest (computed styles of `.card`, `.kpi`, a list row).
2. Kanban: columns with a fill and no border, the header a plain text row with no dot; the
   priority and label filters show the filter chip, with on and off told apart at a glance; the
   "+" in the Inbox header opens the New dialog; no "Inbox" chip on an Inbox card.
3. Triage: lanes unboxed; no tilt on hover; group frames with no dash; icons, no glyphs.
4. The drawer: the head as specified, the file rows aligned (every size ends at the same x), the
   front matter as a key/value list; on a phone, the file picker and an unbroken Edit button.
5. Batch: the mode as a read-only segmented control, the gate line whole, the PR column as rows.
6. PRs: inline code rendered in a title, the forge read time once.
7. Costs: KPI tiles as Home's; the receipt still the paper ticket on screen, with its stamp when
   the CR is not finished; "Copy as image" still copies it (on a secure origin).
8. Configuration: each value once, the segmented tabs, the legend as captions.
9. In French, no English chrome word on any page (the before/after French set shows it); the two
   new tests fail on a planted literal and pass on the head.
10. The phone bar: four views and More, More reaches PRs, Costs and Configuration.

## Open questions

None: the answers, the choices settled in `02-answers.md` (S1 to S14, S10 overruled by realign-Q1) and realign-Q1/Q2 cover the specification.
