# Board UX and design QA (2026-11-17)

Method: single-context review (one agent, no separate A/B sub-agents), the `impeccable` critique
method plus its detector (`impeccable detect`) on `board/web/`, and the live board walked in a
browser at 1440x900 and at a phone's 375x812: Home, Triage, Kanban, Batch, PRs, Costs,
Configuration, and the CR drawer (desktop and phone). Nothing was edited, dragged or saved.
No PRODUCT.md or DESIGN.md exists; the board is judged as an Operate surface (a tool: scanability,
consistency and calm come before expression).

Screenshots saved here: `ux-qa-drawer.png` (desktop drawer), `ux-qa-drawer-phone.jpg`,
`ux-qa-kanban-phone.jpg` (the priority chips, plainly visible), `ux-qa-batch.jpg`,
`ux-qa-config.jpg`.

## Verdict

The tokens are sound: one teal accent, state colours with tints, a 4/8/12/16/24 spacing scale,
and two weights. The pages do not follow them. Every level of the layout draws its own box: page
section, column, lane, card, card band, row and chip each get a hairline, a fill or both, so the
eye sees frames, not content. Three of the user's complaints are not matters of taste. They are
plain bugs: class-name collisions and an unreset `<button>`, each fixed in a few lines. Fix those
first (P0). Then apply one container rule and one chip rule everywhere (P1), and the board reads
as one product.

Health score (Nielsen, 0-4): status 3, real-world match 2, control 3, consistency 1, error
prevention 3, recognition 3, efficiency 2, minimalism 1, error recovery 2, help 2: **22/40,
Acceptable**: it works, but it does not yet feel finished.

## The three named complaints: root causes

### 1. Borders

- `css/cards.css:69-72` gives a P1-P4 card `border-left: 3px solid var(--pri-c)` on a card with a
  14px radius (`--radius-card`). The thick edge bends round the rounded corners into a teal
  "bracket". The detector flags it as the side-tab anti-pattern, its strongest tell.
- The priority is already shown twice on the same card: the filled `P2` tag in the top row, and in
  the Kanban, the column or lane itself. The bar adds nothing.
- The nesting, on Triage: `.tcol` (1px line, 16px radius, `--col-fill`) > `.card` (1px line, 14px
  radius, shadow, 3px left bar) > `.meta` band (top hairline and grey fill) > `.tag` / `.lbl`
  chips (grey fill). On the Kanban it is the same, plus the `.colh` header in a teal-tint box.
  That makes four or five nested containers, each with its own radius.
- Home does it again: `.home .block` (bordered) > `.home .x` rows (each in its own
  `1px solid --line2` box) > chips. Batch: the graph panel (bordered and dotted grid) > node cards
  (bordered and shadowed) > band. The PR column (bordered) > PR cards (bordered) > band.

### 2. Kanban "Priorités" chips

- `js/labels/priority.js:16` draws each toggle as `<button class="lab lbtn">`. `.lab`
  (`css/tags.css:91`) is a `span` style and never resets `border`, so the browser's own button
  border shows: computed `2px outset rgb(0,0,0)`. That is the "double border".
- `.lab::before` (`tags.css:103`) draws the label-colour square. A priority has no label colour,
  so every chip gets the fallback `--label-5` grey square. That is the meaningless "dot".
- All five start `on` (`.lbtn.on`, teal tint), so the row looks identical whether filtered or not.
  An off chip falls back to the label chip's grey. The state is barely readable.
- The same chips are not the same anywhere else: the card's priority tag is a filled teal
  `.tag.pri-P2`; the triage legend uses glyphs; the label filter uses the same broken `.lab` button
  (`labels/filter.js:16`), so it has the same outset border.

### 3. CR drawer

- **File names in boxed chips, icons overlapping names, misaligned sizes: one class collision.**
  The tree writes `<span class="nm">` (`js/panel/tree.js:42`). `.nm` is also the card band's
  class: `css/cards.css:476-489` `.band, .meta, .nm { margin: 10px -12px -10px; padding: 8px 12px;
  border-top; background: var(--band) }`. Measured on the live page, each name box is 32px tall,
  starts 6px *left* of its icon's right edge (negative margin), and pushes the size out of line:
  sizes end at x=904 on one row and x=908 on the next. The panel's own `.panel .tree .nm` rule
  (`panel.css:877`) sets only overflow, so it does not undo the band.
- A second collision is latent: an indented file's button has class `ind` (`tree.js:42`), and
  `.ind` is Triage's pill indicator (`css/views/triage.css:17`, radius 999px, padding, chip
  fill). The panel's selector wins on padding and radius today, by luck of specificity.
- **Front matter as raw text.** `js/panel/markdown.js` has no front-matter step: the
  `---`/`key: value`/`---` block falls into `readParagraph` and is joined into one line:
  "--- type: cr-answers description: ... ---".
- **The same bug leaks into titles across the board.** `status/views.py:215` `_title()` takes a
  file's first non-blank line, which for a file with front matter is `---`. On the live data, 6 of
  the 8 batch CRs are titled "---" on Batch, PRs, Home's open PRs and the Costs tables.
  (`board/backlog.py:31` already strips front matter for the backlog; `_title` does not.)
- Other drawer defects: the facts row reuses the grey `.lbl` box for the slug, the stage and the
  cost, so everything is a chip; the info line repeats the folder path already shown in the head;
  the phone tree is capped at 150px (`panel.css:982`) and shows two and a half files; on the
  phone the "Modifier" button breaks inside the word ("Modif/ier").

## System-level problems

### Borders and containers

- There is no elevation policy. Hairline, fill and shadow are stacked at every level: `.card` has
  a border **and** `--shadow-card`; `.kpi` has a border and a soft shadow; `.tcol`/`.col` have a
  border and a fill; `.home .block` has a border; `.home .x` rows have a border.
- About 40 `border:` declarations across 25 CSS files, with dashed variants in 4 places (`.empty`,
  `.dropzone`, `.grpf`, `.stackrail`).
- Radii: 2, 3, 4, 6, 7, 8, 9, 10, 14, 16, 99, 999px and 50%. That is 12 values where 3 would do.

### Chips and badges

At least seven chip looks are in use: `.tag` (grey `--chip-2`), `.lbl` (grey `--chip`, a different
grey), `.lab` (grey with a coloured square), `.tag.pri-P1..P4` (filled teal, white text),
`.tag.st.*` (state tint), `.ind` (999px pill), `.pi .chgm` (9px radius teal tint),
`.kanban .colh .c` (count chip), the config `.eff` chips ("en vigueur : ..."), and the batch
`.mode` / config tab pills (999px with a border). Three neutral greys (`--chip`, `--chip-2`,
`--pill`) are in use, and nobody can tell them apart.

### Type scale

The CSS uses 11, 12, 12.5, 13, 13.5, 14, 15, 15.5, 16, 17, 18, 22, 24, 34 and 40px, as raw
literals in 14 places (`home.css`, `panel.css`, `prs.css`, `overview.css`, `batch-prs.css`...),
beside the tokens `--text` 14 / `--text-small` 12 / `--text-badge` 11 / `--title` 24. The 0.5px
steps (12.5, 13.5, 15.5) are invisible differences that only add noise. Headings inside blocks are
13.5px, smaller than body text (14px), so section titles do not lead.

### Spacing

The tokens exist, but the views mix in 6, 7, 10, 14, 20, 22 and 28px. Home uses 14px gaps between
tiles, the Kanban 12px, Triage 12px, PR cards 8px. The Kanban column header, sub-line and "New"
button are three stacked strips with three different insets (`colsub` has a 23px left pad).

### Colour use

- The accent tint is used both for "selected/on" (filter chips, `.lbtn.on`) and as decoration
  (Kanban column headers `.colh`, Costs KPI tiles, the batch mode strip). "On" has no exclusive
  look.
- The priority ramp is teal (`--pri-1..4`), the same hue as the accent, the links and the CR id,
  so P1 and a link read alike.
- The Kanban column dots use the state colours (grey, brown, amber, violet, blue, green) for
  columns that are not states, which contradicts the tokens' own rule (a state's colour is for
  that state only).

### Iconography

- The file icon is `.svgi` 16px with `vertical-align:-3px`; in the tree it sits in a flex row but
  keeps the inline offset, so the icon rides above the name's baseline even before the `.nm`
  collision.
- Text glyphs pass for icons: "✓" and "⚡" in `.gs` (`triage.css:1550, 1559`), and "↗"/"→" in
  links. They mix with stroke SVGs.
- The phone header has an unlabeled orange-dot button (the autosync state) with no text and no
  visible meaning.

### Consistency between pages

- KPI tiles: white with a soft shadow on Home and Batch; teal-tint fill with a teal border on Costs
  (`css/views/costs.css:84`).
- Lists: PRs uses rows with dividers (right). Home's PR list uses boxed rows; Batch's PR column
  uses cards with bands; Costs uses a table. These are four looks for "a list of PRs".
- Costs is a different visual world: a paper receipt with grain, scissors and a perforation
  (`costs-receipt.css`; the detector flags its grid and stripe gradients). The board is otherwise
  flat and white.
- The language is mixed: French chrome ("Priorités", "fichiers", "brut") with English strings
  inside it ("+ New: a new idea", "Gate longue : exemptée : AGENTS.md: the long gate...").
- The loading state shows the wrong page: navigating to Triage first renders "Home ·
  Chargement..." with a "..." project mark.

## Findings per page

### Kanban

| What | Where | Sev | Fix |
|---|---|---|---|
| Priority chips show the browser's 2px outset border | `labels/priority.js:16`, `tags.css:91` `.lab` | high | Use the one filter-chip style below (`border:0`); drop `.lab` from buttons |
| Priority chips get a grey square that means nothing | `tags.css:103` `.lab::before` | high | No square on priority chips; if any mark, the P-tag itself |
| 3px teal left bar on rounded card | `cards.css:69-72` | high | Delete; the `P2` tag already says it |
| Column is a bordered, filled box, header is a tinted box inside it | `kanban.css:38` `.col`, `kanban.css:44` `.colh` | high | Column: no border, no fill (or a fill alone, no line); header: plain text row |
| "+ New: a new idea" button sits inside the Inbox column with its own border, in English | `views/kanban.js:62` | medium | Ghost "+" icon button in the column header; translate |
| Inbox cards repeat "Inbox" as a chip inside the Inbox column | `ui/item-card.js:26` | medium | Hide the bucket tag when the column already says it |
| Card band (grey strip with hairline) on every card | `cards.css:476` | medium | Meta line in `--ink3` text, no fill, no hairline |
| Column state dots in state colours | `views/kanban.js:45-53` | low | Neutral or none |
| Phone: 7-item bottom bar, "Configuration" cramps | `shell.css:132` | medium | 5 items + "More", or icon labels shortened |

### Triage

| What | Where | Sev | Fix |
|---|---|---|---|
| Lane (bordered, filled) > card (bordered, shadow, left bar) > band > chips | `triage.css:116` `.tcol`, `cards.css` | high | Lanes as unboxed sections with a heading and a top hairline; one card surface |
| Group frame is a dashed box inside a lane box | `postit.css:69` `.grpf` | medium | A light fill (no dash) or an indented rule |
| Hover tilts card `rotate(-0.6deg)` | `postit.css:16` | low | Lift on drag only, not on hover |
| `.gs` grill marks mix text glyphs (✓ ⚡) with SVG icons | `triage.css:1544-1560` | low | SVG icons from `ui/icons.js` |
| Indicator pills (`.ind`) a 999px radius unlike every other chip | `triage.css:17` | low | The one chip style |

### Home

| What | Where | Sev | Fix |
|---|---|---|---|
| Every list row in a box inside a bordered block | `home.css:113` `.home .x` | high | Rows with a bottom divider only (as on PRs) |
| PR titles show "---" | `status/views.py:215` | high | Strip front matter in `_title` (reuse `backlog.FRONTMATTER`) |
| Five KPI tiles: the fifth alone on a second row | `home.css:3` `auto-fit minmax(220px)` | medium | Four tiles, or `repeat(5,1fr)` on wide screens |
| Block headings 13.5px, smaller than body | `home.css:38` | medium | Section heading = 15px/500 |
| Stat label "Dernier signe du Foreman" wraps, breaking the row's baseline | `home-batch.js` | low | Shorter label ("Foreman vu") |

### Batch

| What | Where | Sev | Fix |
|---|---|---|---|
| 6 of 8 CR titles are "---" | `status/views.py:215` | high | As above |
| Gate line clipped 315px past the PR card's edge (`overflow:hidden`) | `batch-prs.css`, `.prc` | high | Let it wrap, or ellipsis with a `title` |
| Graph panel (bordered, dotted grid) > node cards (bordered, shadowed) | `batch-graph.css:5, 64` | medium | Drop the panel border; the grid is enough to mark the canvas |
| PR column bordered > PR cards bordered > band | `batch-prs.css:7, 105` | medium | Column unboxed; cards plain |
| Mode strip (Stack/Série/Parallèle) teal-tinted band of text | `batch.css:10` | low | A segmented control in the one chip style, explanation as a caption |

### PRs

| What | Where | Sev | Fix |
|---|---|---|---|
| Titles "---"; Markdown backticks shown raw ("`writes:`") | `views.py:215`; `prs-row.js` | high | Strip front matter; render inline code |
| "Lu sur la forge il y a 0 s" repeated on every row | `prs-row.js` | medium | Once, in the page's header line (it is there already) |
| Each row a dense 3-line block; state chip grey for "ouverte" with a grey dot | `prs.css` | low | Row: `#289 CR-331 Title` then one muted meta line; state chip from the state palette |
| The list itself is right: dividers, no boxes | | | Keep it as the model for every list |

### Costs

| What | Where | Sev | Fix |
|---|---|---|---|
| KPI tiles teal-tinted, unlike Home/Batch | `costs.css:84` | medium | The one KPI style |
| Receipt skeuomorph (grain, scissors, perforation) out of the board's world | `costs-receipt.css` | medium | Keep only as the "Copier en image" export; on screen, a flat panel |
| CR column wraps id and slug over 3 lines; state chip and round wrap apart | `costs-tables.js` | medium | ID only in the column, slug in a `title`; state chip and round on one line |
| "---" titles in the per-CR table and receipt | `views.py:215` | high | As above |

### Configuration

| What | Where | Sev | Fix |
|---|---|---|---|
| Each row repeats the effective value three times (input placeholder, grey `.eff` chip, "hérité : ..." line) | `views/config.js`, `config.css:63` | high | One muted line under the control: "inherited: claude-sonnet-5-5"; no chip |
| `.eff` chips wrap to two lines in the Model column | `config.css:63` | medium | Plain text, ellipsis |
| Legend "défaut livré / défini dans chantier.yaml" looks like two buttons | `config.css:67` | medium | Caption text with a small swatch, not bordered pills |
| Tabs "Modèles / Délais" are bordered pills | `config-timing.css:12` | low | The segmented control (one style for Batch mode and here) |
| Table in a bordered box; "Démarre comme" header wraps | `config.css:30` | low | Unboxed table; shorter header |

### CR drawer (panel)

| What | Where | Sev | Fix |
|---|---|---|---|
| File name boxed, overlapping icon, sizes misaligned (`.nm` collision) | `panel/tree.js:42`, `cards.css:476` | high | Rename to `.fname`; better, scope the band rule to `.card > .meta` and drop the `.nm` alias |
| Latent `.ind` collision with Triage's pill | `tree.js:42`, `triage.css:17` | medium | Rename to `.nested` |
| Front matter rendered as a paragraph | `panel/markdown.js:92` | high | Parse it and render as a key/value list (below) |
| Facts row: every fact a grey chip | `panel/head.js:23-33` | medium | CR id + state chip only; the rest as muted text separated by "·" |
| Info line repeats folder path and size | `panel/file-view.js:57` | low | Show only the file name; the folder is in the head |
| Phone: tree capped at 150px; "Modifier" breaks mid-word | `panel.css:982`, `.info` | medium | Phone: a file picker (select) above the doc; button `white-space:nowrap` |

## Proposed realignment: the target rules

1. **One surface, one edge.** A page has two surfaces: the page (white) and the card (white, 1px
   `--line` hairline, radius 10px, **no shadow at rest**). Shadow is for things that float: the
   drawer, menus, dialogs, a dragged card. Never a border and a shadow together at rest.
2. **Never a box in a box.** A grouping (column, lane, block, section) is a heading and white
   space, with at most one hairline *between* groups, never a frame. Kanban columns and Triage
   lanes get no border; if they need a field, a fill of `--col-fill` without a line. Lists are
   rows with a bottom divider (the PRs page's rows), never boxed rows.
3. **No side bars.** No coloured left or right borders anywhere. Priority shows once, in the
   P-tag.
4. **One chip.** `.chip`: height 20px, padding 0 6px, radius 6px, 12px/500, `border:0`, neutral
   fill `--chip` (a single grey; drop `--chip-2` and `--pill`). Variants change only the fill and
   ink: state (its tint and ink), priority (P1..P4: a neutral chip with the ramp in the text and
   a 6px swatch, so it no longer competes with links), accent (CR id stays bare text). Slugs and
   facts are **text**, not chips.
5. **One toggle/filter chip.** `button.chip` resets the UA (`border:0; background; font:inherit`).
   Off is the neutral chip with `--ink2`; on is `--ink` text on `--accent-tint` with a 1px inset
   `--accent-line` ring. The label filter and the priority filter use it; a label adds its
   swatch, a priority none. The accent tint means "on" and nothing else (remove it from column
   headers and KPI tiles).
6. **One segmented control** for Batch mode, Configuration tabs and similar: a `--chip` track,
   the selected segment white with a hairline.
7. **One KPI tile** (Home's, minus the shadow) on Home, Batch and Costs.
8. **Card anatomy.** Top row (id/tag), title 14px/500, description 12px `--ink2`, meta line 12px
   `--ink3` on white with an 8px top gap. No grey band, no hairline inside the card.
9. **Type scale, five steps:** 11 (badge), 12 (small/meta), 14 (body), 16 (section heading, 500),
   24 (page title). Delete every 12.5/13/13.5/15.5 literal; reference tokens only.
10. **Radii, three steps:** 6 (chip, input, button), 10 (card, tile, drawer), full (dots and
    avatars only). Delete 2/3/4/7/8/9/14/16/99/999.
11. **Spacing:** tokens only (4/8/12/16/24/32); groups 24px apart, cards 8px apart.
12. **Class hygiene:** no shared short class names across components (`.nm`, `.ind`, `.x`,
    `.r`, `.c` are each used by two or more unrelated parts). Scope each view's rules under its
    root (`.panel .tree ...`, `.kanban ...`) and rename the generic ones.

### How the drawer renders front matter and the file list

- **Front matter:** strip a leading `---` ... `---` block (the regex in `board/backlog.py:31`,
  ported to `markdown.js`) and render it above the body as a compact definition list: a 12px
  two-column grid, keys in `--ink3`, values in `--ink`, no box, followed by one hairline and the
  document. `type:` shows as a neutral chip; `description:` as the lead paragraph in `--ink2`.
  Fix `status/views.py:_title` the same way, so no title is ever "---".
- **File list:** a plain list, no chips. Each row is a 32px grid
  `16px icon | name (ellipsis) | size (right-aligned, tabular-nums, --ink3, fixed 56px column)`,
  gap 8px, radius 6px for the hover and selected fill only. Folders are 11px uppercase `--ink3`
  captions ("INTAKE · 1") with nested rows indented 16px. Icons are `vertical-align: 0` in the
  flex row. On a phone, the tree turns into a single `<select>` file picker above the document.
- **Head:** CR id + state chip, then the title (18px/500), then one muted line:
  `slug · round 2/3 · $1.45 · 5 files`. Close button: a ghost icon button with no fill.

## Priority order

1. **P0 (bugs, a few lines each):** the `.nm` and `.ind` collisions in the tree; the `<button>`
   border reset on `.lab`/`.lbtn`; front matter in `markdown.js` and in `_title`; the clipped gate
   line on Batch PR cards.
2. **P1 (the user's three complaints, done properly):** remove the side bar; unbox columns,
   lanes, blocks and rows; the one chip and toggle style; drawer head and file list as specified.
3. **P2:** type scale and radius consolidation; one KPI tile; Configuration de-duplication; the
   PR-row model for every list; the language mix.
4. **P3:** Costs receipt as export only; the glyph icons; the phone bottom bar; the loading state's
   wrong title.
