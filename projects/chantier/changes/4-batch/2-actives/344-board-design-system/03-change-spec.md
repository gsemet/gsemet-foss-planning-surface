# Change Specification: the board's design rules are written once, in DESIGN.md, and every page follows them

## Goal

The user, on the abandoned `board-design-realign` (2026-11-17): "I don't want to realign
EVERYTHING, discard it. I want to fix the horrors that were put in recently":

1. the task cards are not the same from one page to the next;
2. the left border that bends round a card's rounded corner: it must be FORBIDDEN ("no rounded
   lateral accent border, that is what is ugly", DS-Q6);
3. the Triage and Kanban columns are not the same.

And the cause: a designer could propose to remove the Costs page's paper ticket because the
board's design rules and the features that must not be lost are written nowhere. So the rules are
written in Markdown, beside the code, and the CSS is refactored so that pages only lay out shared
components built on tokens: changing a token or a component sheet changes every page.

The look to reach is `intake/target-columns.html` (screenshot `intake/target-columns.jpg`): one
column, one card, one chip, the same on Triage and Kanban (DS-Q5). The mock's pixel values are
illustrative; the board keeps its own tokens (see "Raw values" below).

After this change:

- `board/web/DESIGN.md` holds the rules, the token table, the component table and the protected
  features (the Costs receipt and its stamp first);
- `css/tokens.css` stays the single source of every value; every sheet uses tokens only; the
  values with no token today become named tokens at their current values;
- one card builder draws every card (the Batch page's CR nodes and PR cards included), one column
  builder draws the Triage and Kanban columns, one chip sheet holds the chips; the priority chip is
  Triage's P1 chip, at the top left of every card that has a priority, and the Kanban priority
  filters are the same chips;
- no element has a coloured accent border on one side; a straight hairline separating two regions
  of a page stays allowed;
- a blocking test in `just check` refuses a side accent border, a raw value outside the tokens, a
  component class styled in two sheets, a card built outside the card builder, and a token table
  that disagrees with `tokens.css`.

Every other finding of the UX QA (`intake/ux-qa.md`) stays out (DS-Q2).

Paths: `<cli>` is `skills/chantier/scripts/cli/src/chantier/`, `<web>` is `<cli>/board/web/`,
read at main `f36277c6`. Line numbers are main's; CR-338, CR-339, CR-340 and CR-341 (batch-24)
move some of them before this CR starts (see "Overlaps").

## Decisions carried from `02-answers.md`

- DS-Q1: `tokens.css` is the single source of every value (colours, radii, spacing, type scale).
  `DESIGN.md` holds the rules. A test fails when DESIGN.md's token table and `tokens.css`
  disagree. No build step.
- DS-Q2: scope = the three horrors plus the foundation: one task card everywhere (today's builders
  in `triage/columns.js`, `ui/item-card.js`, `views/kanban-cards.js` twice, `views/kanban.js`,
  `views/overview.js`, `views/config-timing.js`); no side border on any element (`cards.css:71`,
  `batch-prs.css:52`); the Triage and Kanban columns one shared component (today `.tcol`/`.lanes`
  against `.kanban .col`/`.cards`); `DESIGN.md`, the shared component sheets (card, column,
  chip) and the test. The rest of the UX QA stays out; each point may come back as its own item.
- DS-Q3: a blocking test in `just check` refuses a side border, a raw value outside the tokens, a
  component class styled in two sheets, and a task card built outside the one card builder.
- DS-Q4 (the user's words): "there is already a P1 chip in the Triage page, which is very good."
  That chip is the model: the same priority chip on every card, on every page.
- DS-Q5 (settled by the Chief of Staff; target `intake/target-columns.html`,
  `intake/target-columns.jpg`): one column on every page (Triage's light area, a hairline border,
  a plain header: dot, name, count, with Kanban's one-line grey subtitle saying what the column
  holds); one card with no side accent (a hairline all around, the priority chip at its top left);
  one chip, Triage's P1 chip filled with the priority colour; the Kanban priority filters are
  these same chips, filled when on and outlined grey when off.
- DS-Q6 (the user's words): "no rounded lateral accent border, that is what is ugly." The rule
  forbids a coloured accent border on one side of an element (left or right), above all one that
  follows a rounded corner. A plain straight hairline separating two regions of a page (the
  sidebar's edge, the drawer tree's edge, the stack rail) stays allowed.
- Settled by the Chief of Staff: `DESIGN.md` lives in `board/web/`; the project's `AGENTS.md`
  gains one line (any change under `board/web/` reads `DESIGN.md` first and keeps it true);
  `DESIGN.md` names the protected features, starting with the Costs page's paper receipt and its
  stamp; the translation rule (every string through the i18n keys, in every language) is a rule of
  `DESIGN.md`; pages only lay components out (grid, gaps), never restyle them.
- Settled by the Chief of Staff (after the first spec): raw values keep today's look, the
  off-scale values become named tokens at their current values, no shift of a few pixels across
  pages; the Batch page's CR nodes and PR cards are cards and come from the one card builder.
- Settled by the Chief of Staff (after the spec critic): Triage's grey sub-line uses two new keys
  in both word files, `triage.inbox_sub` ("1-inbox: filed") and `triage.backlog_sub` ("2-backlog:
  P1 to P4"); 3-ready keeps `kanban.ready_sub` (the Kanban inbox and backlog words would be false
  on Triage, which holds grilled items too). A column that appears on both pages gets Kanban's dot
  colour on both: Backlog brown (`--brown`), 3-ready violet (`--violet`).

Working choices this specification makes where the answers leave a detail open, each marked
"(working choice)" below; none goes against an answer:

- The card's meta band keeps today's look (grey band under a hairline); the mock draws a white
  foot under a hairline, but the band's removal is a UX QA point DS-Q2 leaves out.
- The stack rail stays a separator, as DS-Q6 allows, but as a plain straight hairline (1 px solid
  `--line`) instead of today's 2 px dashed line, so the one-side borders left are all hairlines.
- Triage's grill-state counts stay in the column's and the lane's head, after the count, in the
  count's grey.
- The mock's chip, column and card sizes are not copied: the board's tokens and today's values
  rule, the mock gives the structure and the looks.

## What the code has today

- **Cards.** `css/cards.css` styles `.card` (hairline `--card-line`, `--radius-card` 14 px,
  `--shadow-card`), the band `.band, .meta, .nm` (grey strip `--band` under a `--band-line`
  hairline, negative margins), `[data-open] { cursor: pointer }`, `.card[data-open]:hover`,
  `.row-tags`, `.ttl`, `.desc`, the priority left border
  `.card.pri-P1..P4 { border-left: 3px solid var(--pri-c) }` and its keep-colour rule (lines
  65-94), `.card.sel`, `.card.lifted`, and the KPI tile `.kpi`. Builders: `ui/item-card.js:26`
  `itemCard` (backlog items, used by Kanban's `backlogCard` and Triage's `postit`),
  `views/kanban-cards.js:36,47` `doneCard` and `crCard`, `views/batch-graph.js` `node` and
  `recordedNode` (`.node card`, title `.nt`, band `.nm`, state badge `.sb`), `views/batch-pr-card.js`
  `shell` (`prc card`, an `<a>` when the PR has a web address), `views/overview.js:66` `card`
  (`.apc card` with a `.band`), `views/config-timing.js:47` `card` (`<section class="hcard">`,
  styled apart in `config-timing.css:43`). Pages restyle cards and chips: `postit.css`
  (`.pi:hover` tilt, `.card.pi.sel`, `.pi.drag`, `.pi.pend`), `kanban.css` (`.kanban .card`,
  `.kanban .meta .step`), `batch-graph.css` (`.batch .node .row-tags`, `.tag`, `.lbl`, `.sb` at
  `:48`, `:58`, `:72`, `.node.dim`, `.node.hl`, `.nt`, `.np`, `.nm .gate`), `batch-prs.css`
  (`.prc .nt`, `.prc.draft`), `overview.css` (`.apc .band`), `home.css:124` (`.home .x .tag`),
  `prs.css:41` (`.prview .pvrow .si`). `.row-tags` is also the drawer head's row
  (`panel/head.js`); `.meta` is also the receipt's (`costs-receipt.css`, `.ticket .meta`).
- **Columns.** Triage: `triage/columns.js:59` `column()` builds `<section class="tcol">` (head
  `.colh`: dot, `h2`, count `.c`, grill counts `.scs`; body `.tbody` with groups `.grpf` and a
  `.dropzone`; 3-ready's foot `.rfoot`); `lanes()` (`:70`) wraps the four lanes P1-P4 in `.lanes`
  under a `.lanesh` heading ("Backlog", `triage.urgent`), each lane a `.tcol.lane` headed by a dot
  and its name; styled in `triage.css` (`--col-fill`, 1 px `--line`, `--radius`). No sub-line.
  Kanban: `views/kanban.js:64` `column` builds `<section class="col">` (head `.colh` in a
  teal-tint box, count chip, the Inbox's "New" button `.colact`, sub-line `.colsub` with a 23 px
  left pad, body `.cards`), styled in `kanban.css`; its dots are Inbox `--grey`, Backlog
  `--brown`, Grill `--amber`, 3-ready `--violet` (`kanban.js:45-48`). `.colh` is styled in both
  `triage.css` and `kanban.css`. Triage's drag (`triage/drag.js`) targets `.pi`, `.grpf`,
  `[data-col]` and adds `.over`/`.drag`.
- **Chips.** `css/tags.css`: `.tag` (with `.badge`, `.cr`, `.pri-3-ready`, `.pri-P1..P4` filled in
  the priority ramp `--pri-1..4`, `.st.*` on the state tints, `.queued`), `.lbl`, `.lab` with its
  `::before` square, `.si`, `.sb`. `ui/parts.js` `tag()`, `stateTag()`, `nextTag()`. The priority
  chip on a card is `tag(\`pri-${bucket}\`, name)` in `itemCard`, the same on Triage and Kanban.
- **Kanban filters.** `labels/priority.js` `priorityRow` draws the priority toggles as
  `<button class="lab lbtn[ on]" data-pf=...>` (a grey label chip, the on state on the accent
  tint, `postit.css:157-165`); `labels/filter.js` draws the label toggles the same way, with the
  label's colour square.
- **Side borders** (`border-left`/`border-right`): `cards.css:71` and `:77` (the priority bar,
  following the card's 14 px radius), `batch-prs.css:52` (`.stackrail`, 2 px dashed `--line`),
  `sidebar.css:8` (`.side`, 1 px `--side-line`), `panel.css:46` (`.panel .tree`, 1 px `--line`;
  `:190` resets it on a phone).
- **Raw values.** About 237 declarations of `font-size`, `border-radius`, `margin*`, `padding*`
  and `gap` in 29 sheets carry a literal length (for example `padding: 10px var(--space-3)`,
  `font-size: 13.5px`, `border-radius: 999px`, `gap: 6px`). Colours are already tokens only
  (`tests/test_code_targets.py`, `COLOUR`).
- **Docs.** `docs/web-board.md` lines 61 (Kanban) and 67 (Triage) say a card shows its priority on
  its chip "and its card's left border" / "and their left border".
- **Tests.** `tests/test_code_targets.py` (238 lines): `MAX_STYLE_LINES = 300` per sheet,
  `MAX_SCRIPT_LINES = 300` per script, `MAX_FILE_LINES = 400` per Python file (tests included), no
  colour outside `tokens.css`, no id selector, nesting at most 3, no `style=`/`on...=` in JS
  markup, no `innerHTML` outside `dom.js`, both word files with the same keys.

## What changes

### 1. `<web>/DESIGN.md` (new)

Written in English, plain Markdown, no link to another origin. It holds, in this order:

1. **Purpose and reading rule.** The board's design rules; any change under `board/web/` reads
   this file first and keeps it true (the same rule as `AGENTS.md`'s line, section 8).
2. **Rules**, each one short and checkable:
   - Tokens: every colour, radius, spacing and type size is a token of `css/tokens.css`; a sheet
     names it through `var()`; no literal (test). Margins, paddings and gaps take a space token,
     or a size token for a frame's offset (`--bar-height`).
   - No side accent border: no element has a border on its left or right side only, by any means
     (a `border-left`/`border-right`/`border-inline*` declaration, a one-side inset shadow, a
     pseudo-element bar), above all one that follows a rounded corner. One exception: a plain
     straight separator between two regions of a page (today the sidebar's edge, the drawer
     tree's edge, the Batch stack rail): `1px solid` in a separator colour (`--line`,
     `--side-line`), on an element with no radius, never on a component. A card shows its
     priority with the priority chip (test, for the declarations).
   - Components: a component (card, column, chip) is styled in its own sheet only, with its
     variants; a page's sheet only lays components out (its grid or flex container, gaps, and on a
     component only placement and size: `grid-*`, `flex*`, `order`, `*-self`, `width`,
     `min-width`, `max-width`, `height`, `min-height`, `max-height`, `overflow*`,
     `scroll-snap-*`, `margin*`), never restyles one (test, for the component classes).
   - One card: every card is built by `js/ui/card.js` (test): a hairline all around, no side
     accent, the priority chip (when the item has one) first in its top row, at the top left.
     One column: every board column (Triage, Kanban) is built by `js/ui/column.js`: a light area,
     a hairline, a plain head (dot, name, count) and a one-line grey sub-line saying what it
     holds; a column that appears on both pages has the same dot colour on both. One chip:
     `css/components/chip.css`; the priority chip is Triage's, filled with the priority colour, on
     every card that has a priority (inbox, P1-P4, 3-ready); a chip used as a filter toggle is the
     same chip, filled when on, outlined grey when off, the same size in both states.
   - Words: every string the board shows goes through the i18n keys (`t()`/`tn()`), in every
     language file (design-Q3); data (titles, slugs, file contents) is shown as it is.
   - The reference look: DESIGN.md describes the column, card and chip in words only (no picture
     ships in the package); the PR's screenshots are the visual record.
3. **Token table**: one row per custom property of `tokens.css`, in its order:
   `| Token | Value | Kind | Use |`, the name and the value in backticks, the value on one line
   (whitespace collapsed), Kind one of `colour`, `space`, `radius`, `type`, `shadow`, `font`,
   `size`, `other`. The tokens added in section 2 are grouped under a heading of their own
   ("Off-scale values, kept as they were").
4. **Component table**: `| Component | Sheet | Builder | Classes |`, the classes in backticks, a
   trailing `-*` meaning a prefix. Its three rows:
   - card: `css/components/card.css`, `js/ui/card.js`, `card`, `card-*`;
   - column: `css/components/column.css`, `js/ui/column.js`, `column`, `column-*`;
   - chip: `css/components/chip.css`, `js/ui/parts.js`, `tag`, `lbl`, `lab`, `si`, `sb`.
5. **Protected features**: features no design pass removes, flattens or restyles; a change to one
   is a CR of its own on the user's word. The list starts with: the Costs page's paper receipt
   (warm paper, grain, perforation, scissors: `css/views/costs-receipt.css`, `--paper-*` tokens),
   its red "NOT FINISHED" / "PAS FINI" stamp on a batch that is not closed
   (`css/views/costs-stamp.css`, CR-339), and the receipt's "Copy as image", which carries both
   (`js/views/costs-image.js`).

### 2. Tokens only (DS-Q1, DS-Q3, raw values settled)

- Every literal length in `font-size`, `font`, `border-radius` (and its corner longhands),
  `margin*`, `padding*`, `gap`, `row-gap`, `column-gap`, in every sheet but `tokens.css`, becomes a
  `var()` of a token of `tokens.css`, of the matching kind: a space token for margins, paddings
  and gaps (or a `size` token for a frame's offset, such as `--bar-height`); a radius token; a type
  token. Allowed as they are: `0`, `auto`, `inherit`, `initial`, `unset`, and `calc()` combining
  tokens with unitless numbers (a negative margin is `calc(-1 * var(--space-2))`).
- No page changes because of this step (settled: keep today's look, no shift of a few pixels): a
  value equal to an existing token of the right kind takes it (4/8/12/16/24 px:
  `--space-1`..`--space-5`; 32 px: `--gap-main`; 6/8/9/14/16 px radii: `--radius-s`,
  `--radius-nav`, `--radius-m`, `--radius-card`, `--radius`; 11/12/13/14/24 px type:
  `--text-badge`, `--text-small`, `--text-stat`, `--text`, `--title`); a value with no token gets a
  new named token at that exact value (for example `--space-0-5: 2px`, `--radius-pill: 999px`,
  `--radius-round: 50%`, `--text-13-5: 13.5px`; names at the Driver's choice, each listed under
  "Off-scale values, kept as they were" in DESIGN.md). Two values that render the same where they
  are used (99 px and 999 px on a chip) may share one token. Folding them into the scale is not
  this CR's.
- A custom property declared in a view sheet may hold an angle, an opacity or a width (CR-339's
  `--stamp-tilt`, Triage's `--card-w`), never a value of the four kinds above.
- No new colour.

### 3. The component sheets (DS-Q2)

New folder `<web>/css/components/`, linked in `index.html` after `components.css` (replacing the
`tags.css` and `cards.css` links), each under 300 lines:

- `card.css`: the card and its parts and variants (section 4), and `.card[data-open]:hover`.
  Takes `cards.css`'s card rules; `cards.css` is deleted; its `.kpi` rules and
  `[data-open] { cursor: pointer }` move to `components.css` unchanged.
- `column.css`: the column, its lanes, parts and variants (section 5), from `triage.css` and
  `kanban.css`.
- `chip.css`: `tags.css` moved whole (it is deleted), plus:
  - the chip-as-toggle rules: the priority filter toggle (section 6) and the label filter
    toggle's rules that name `.lab`/`.lbtn` (from `postit.css:157-165`, as CR-338 leaves them: no
    border, the page's font, the label toggle's square kept, its on/off looks unchanged);
  - the Batch node's state badge: `batch-graph.css`'s `.batch .node .sb` rules (`:48`, `:58`,
    `:72`) become a chip variant in `chip.css` (same look), picked by its class;
  - `home.css:124` (`.home .x .r, .home .x .tag`) and `prs.css:41` (`.prview .pvrow .si`): each
    keeps only layout declarations (`flex`, `margin*`...) in its page sheet; a declaration that is
    not layout (`white-space`, `vertical-align`) moves into `chip.css` as a variant, so the look is
    unchanged.
- The drawer head's `.row-tags` rule moves from `cards.css` to `panel.css` (the head keeps its
  markup; `panel/head.js` does not change).
- `js/views/costs-image.js` `SHEETS` lists the sheets the receipt's image needs: if the receipt
  uses a class that moved (a chip, the KPI tile), the new sheet is listed there, so the copied
  image is unchanged.
- `CONTRIBUTING.md`, "The board's page": the `css/` layout line names `components/` (card,
  column, chip) and points to `DESIGN.md`; the CSS line adds "tokens only, as DESIGN.md says".
- `docs/web-board.md`: line 61 drops "and its card's left border" (the priority shows "on its
  `Pn` chip"), line 67 drops "and their left border" (the post-its carry the shade "on their
  chip").

### 4. One card (DS-Q2, DS-Q3, DS-Q5)

- New `<web>/js/ui/card.js`, pure, `card(parts)` returning the card's markup. Its parts cover
  every card of the board (names at the Driver's choice): the element (`div`, `section`, or `a`
  with an `href`, `target="_blank" rel="noopener"` as `batch-pr-card.js` does today), extra
  classes and attributes (opener, drag, `data-*`, `aria-*`), the priority (a bucket or none), the
  top row, the title (and an optional heading tag for a card that is a section), the labels, the
  description, a free block (the Kanban round bars, the Batch phase line, the Configuration host's
  table), the meta band (left items and a right-aligned end), and a variant. It is the only module
  that writes the class `card` or a `card-*` class.
- The top row: when the card has a priority, `priorityChip(bucket)` (section 6) is its first
  element, at the top left, then the slug or CR id and the other tags, as the target draws them.
  A picked Triage card's check mark comes right after the priority chip.
- Part classes are prefixed: `card-top`, `card-title`, `card-desc`, `card-meta`, `card-end`,
  `card-body` (or the Driver's names, all `card-*`), replacing `.row-tags` (on cards), `.ttl`,
  `.nt`, `.desc`, `.meta`, `.band`, `.nm`, `.r`. The card band rule's `.band` and `.nm` aliases
  are deleted (CR-338 left `.nm` for the Batch cards; they now use `card-meta`).
- (working choice) The meta band keeps today's look: the grey `--band` strip under its
  `--band-line` hairline, flush with the card's edges. The card body keeps today's hairline
  (`--card-line`) all around, radius `--radius-card` and `--shadow-card`.
- Callers, each building its content and calling `card()`:
  - `ui/item-card.js` `itemCard` (backlog items; Kanban's `backlogCard` and Triage's `postit` keep
    calling it); its header comment loses the left-border sentence;
  - `views/kanban-cards.js` `doneCard`, `crCard`;
  - `views/overview.js:66` `card` (a project, on a phone);
  - `views/config-timing.js` `card` (a host's timing settings): a card whose body is the table;
    `.hcard`'s border, radius and fill rules in `config-timing.css` go (the card draws them);
  - `views/batch-graph.js` `node` and `recordedNode`, and `views/batch-pr-card.js`
    `shell`/`prCard` (settled: the Batch page's CR nodes and PR cards are cards).
  `triage/columns.js` and `views/kanban.js` build columns, not cards: they change in section 5.
- One anatomy, one look: the same top row, title, description and meta band on every page. The
  differences a page needs are variants defined in `card.css` and picked by a builder option,
  never a page rule: the Batch graph's compact node (title clamped to 2 lines, as today), the open
  card (`sel`: accent hairline all around and the tint ring, today's `.card.sel`), Triage's
  pick-up (hover tilt and lift, today's `.pi:hover`), picked (check mark and lift, today's
  `.card.pi.sel`), dragged and pending (today's `.pi.drag`, `.pi.pend`), Batch's dimmed and
  highlighted (today's `.node.dim`, `.node.hl`), the PR card's draft (today's `.prc.draft`).
  Triage keeps `.pi`, `data-slug` and `[data-col]` as its drag and selection hooks
  (`triage/drag.js`, `triage/selection.js` unchanged in behaviour).
- No priority bar: `cards.css:65-94`'s `border-left`, `--pri-c` and the `:is(...)` keep-colour rule
  are deleted; `itemCard`'s `priClass` goes. The priority shows in the priority chip only.

### 5. One column (DS-Q2, DS-Q5)

- New `<web>/js/ui/column.js`, pure, `column(parts)`: a `<section class="column">` with an
  optional `data-col` (Triage's drop target), its `data-key` (the paint), its `aria-label`, the
  head, an optional action (Kanban's "New"), the sub-line, the body (cards, lanes, groups, drop
  zone, the "none" line), an optional foot (3-ready's foot, Done's "more"), and a variant: a stack
  (one card per row) or a grid (cards side by side), and an empty lane (the thin strip).
- The look, on both pages, is the target's: the light area `--col-fill`, a 1 px `--line` hairline
  all around, radius `--radius`, padding `--space-3`, gap `--space-2` (Triage's values today); the
  head a plain text row: the dot, the name (`h2`, `--text`, weight 500), the count in `--ink3` at
  `--text-small`, then the optional extras; under it the sub-line, one line, `--ink3` at
  `--text-small`, aligned with the dot (no 23 px pad), ellipsed when too long. Kanban loses its
  teal-tint head box and its grey count chip; its "New" button stays where it is, under the head.
- Dots (settled): a column on both pages has Kanban's dot colour on both: Inbox `--grey`, Backlog
  `--brown`, 3-ready `--violet`; Triage's `DOTS` (`model/triage.js`) changes to match for Backlog
  and 3-ready.
- Triage's sub-lines (settled): Inbox `triage.inbox_sub` ("1-inbox: filed"), Backlog
  `triage.backlog_sub` ("2-backlog: P1 to P4"), 3-ready `kanban.ready_sub`. The two new keys go in
  both word files (`i18n/en-*.js`, `i18n/fr-*.js`, French "1-inbox : déposé", "2-backlog : P1 à
  P4").
- Triage's Backlog becomes one column built by `column()`, as the target draws it: dot, "Backlog"
  (`triage.backlog`), the `triage.urgent` hint in the count's place (ellipsed in the head like the
  sub-line), the sub-line; its body holds the four lanes P1-P4. It carries no `data-col`: only its
  lanes do. A lane is a part of `column.css` (`column-lane`), not a column: its head is the
  priority chip of its bucket, its count and its grill-state counts after the count (no dot, no
  name); its body the lane's cards and drop zone; it keeps `data-col="P1"`...`"P4"` for the drops
  and the empty lane's thin strip. `lanes()` returns that column; `.lanes` and `.lanesh` go.
- (working choice) Triage's grill-state counts (`.scs`) stay in the head after the count, in the
  count's grey, in a column's head and a lane's head alike.
- `triage/columns.js` `column()` and `lanes()`, and `views/kanban.js` `column`, call it. Classes
  `.tcol`, `.col`, `.colh`, `.colsub`, `.cards` (Kanban), `.tbody`, `.colact` become `column`,
  `column-head`, `column-sub`, `column-body`, `column-act`, `column-lane`... (all `column-*`). The
  drop state (`.over` that `triage/drag.js` adds to a column or a lane) is a variant in
  `column.css`; `.grpf` and `.dropzone` stay Triage's (`postit.css`, `triage.css`). The columns'
  widths stay the pages' (Kanban 290 px and 86 % on a phone; Triage's grid), set by the page
  sheets as layout.

### 6. The one chip and the priority chip (DS-Q4, DS-Q5)

- `ui/parts.js` gains `priorityChip(bucket)`: the chip Triage shows today (`.tag.pri-P1..P4`
  filled in the ramp, `.tag.pri-3-ready` on the accent tint, the inbox in the neutral chip, the
  words of `priority.inbox` and the bucket's name). `card()` places it (section 4), so every card
  that has a priority shows it at the top left; Triage's lane heads use it too (section 5). A CR of
  a batch has no bucket in the record: its cards get no chip. Its look does not change.
- The Kanban priority filters are these chips (`labels/priority.js` `priorityRow`): each toggle is
  `priorityChip(bucket)` drawn as a `<button>` (keeping `data-pf`, `data-key`, `aria-pressed`),
  filled when on (as on a card, with a 1 px border in its fill colour), and when off a variant
  `off` in `chip.css`: the panel's white, `--ink2` text, a 1 px `--line` hairline all around; on
  and off are the same size. The `.lab lbtn` classes and their square leave the priority toggles;
  `bindPriority` and the filter's behaviour do not change. The label filter (`labels/filter.js`)
  keeps its `.lab lbtn` look.

### 7. No side accent border (DS-Q2, DS-Q6)

- `cards.css:71`, `:77`: deleted (section 4).
- `batch-prs.css:52` `.stackrail`: (working choice) the 2 px dashed line becomes a plain straight
  separator, `1px solid var(--line)`; the stacked PRs keep their indent (`margin-left`,
  `padding-left`).
- Allowed and kept as they are: `sidebar.css:8` `.side` (1 px `--side-line`), `panel.css:46`
  `.panel .tree` (1 px `--line`, and `:190`'s reset on a phone).

### 8. The test (DS-Q1, DS-Q3) and the rule line

- New `skills/chantier/scripts/cli/tests/test_board_design.py` (a new file: `test_code_targets.py`
  is at 238 lines of the 400 a Python file may hold), reading `<web>` in-process, fast, few
  functions:
  - **Token table**: the rows of DESIGN.md's token table and the custom properties declared in
    `tokens.css`'s `:root` are the same names with the same values (whitespace collapsed); a
    missing, extra or different one is named in the failure.
  - **Sheets**: for every `.css` under `<web>/css/` but `tokens.css`: (a) a
    `border-left*`/`border-right*`/`border-inline*` declaration has the value `0` or `none`, or is
    a separator: the exact value `1px solid var(--line)` or `1px solid var(--side-line)` (the
    separator colours DESIGN.md names), in a rule that sets no `border-radius` and whose selector
    names no class of the component table; no `border-width`, `border-style` or `border-color` with
    more than one value; (b) in `font-size`, `font`, `border-radius` and its longhands, `margin*`,
    `padding*`, `gap`, `row-gap`, `column-gap`: no literal length or percentage, and every
    `var(--x)` names a token of `tokens.css` whose DESIGN.md kind matches the property (`space`,
    or `size` for margins, paddings and gaps; `radius`; `type`); (c) every class of DESIGN.md's
    component table (prefixes included) appears in the selectors of its own sheet only, except in
    a rule whose declarations are all layout (`grid-*`, `flex`, `flex-*`, `order`, `align-self`,
    `justify-self`, `place-self`, `width`, `min-width`, `max-width`, `height`, `min-height`,
    `max-height`, `overflow*`, `scroll-snap-*`, `margin*`).
  - **One card**: no `.js` under `<web>/js/` other than the card row's builder (`ui/card.js`), and
    outside `js/i18n/`, writes the class word `card` or a `card-*` class, in a `class="..."`
    attribute or in a string or template literal used as a class list (so `batch-pr-card.js`'s
    `` `prc card ${cls}` `` is caught). The values of other attributes (`data-key`, `aria-*`) do
    not count. No exemption: the Batch page's cards go through the builder.
  - **The checker refuses**: one parametrized test feeding the checks small prepared texts: a
    `border-left: 3px solid var(--accent)`, a `border-left: 1px solid var(--line)` in a rule with
    a `border-radius`, a `.card { border-right: 1px solid var(--line) }`, a `padding: 10px`, a
    `font-size: var(--local)`, a `border-radius: var(--space-2)` (wrong kind), a
    `.card { color: ... }` in a page sheet, a `<div class="card">` in a view module, a token
    missing from the table; and one allowed text of each (`border-top: 1px solid var(--line)`,
    `.side { border-right: 1px solid var(--side-line) }`, `margin: calc(-1 * var(--space-2)) 0`, a
    page rule `.kanban .column { flex: 0 0 290px; max-height: 100% }`, a
    `<div data-key="card-3">` in a view module).
  The test runs in `just test`, so `just check` blocks on it; it stays within AGENTS.md's budget
  (`just test` at most 30 s above 18.5 s).
- `AGENTS.md` (project root) gains one line, near the other board rules:
  "- A change under `skills/chantier/scripts/cli/src/chantier/board/web/` reads its `DESIGN.md`
  first and keeps it true."

## Overlaps

Running in batch-24 (their specs in `4-batch/2-actives/`); none has landed on main at `f36277c6`;
this CR lands after them and keeps their decisions:

- **CR-338 board-design-bugs** (`panel/tree.js`, `panel.css`, `postit.css`, `labels/priority.js`,
  `panel/markdown.js`, titles). Kept: the tree's `.fname` and `.nested`, the `.lbtn` reset, the
  label toggles' look (their rules move to `chip.css` unchanged when they name `.lab` or `.lbtn`),
  the front matter list `.panel .doc .fm` (its values are tokens already). CR-338's priority
  toggles with no square become the priority chips (section 6), which have no square either. This
  CR does what CR-338 left to `board-design-realign`: the card band's `.nm` alias is deleted.
  CR-338's "not here" items (the `type:` chip, the file list grid) stay out here too; its "filter
  chip style" item is done here for the priority filters only, as DS-Q5 says.
- **CR-339 Costs receipt stamp** (`css/views/costs-stamp.css`, `costs-receipt.js`,
  `costs-image.js` `SHEETS`, `index.html`). The stamp is a protected feature of DESIGN.md. Its
  sheet passes the test as written (tokens only; `--stamp-tilt` and the ink's opacity are an
  angle and an opacity); if this CR renames a token it uses, it renames it there. The stamp's
  sheet stays its own file, linked in `index.html` and listed in `SHEETS`.
- **CR-340 cost by model** (`css/views/costs-models.css`, `views/costs-models.js`, tokens `--m1` to
  `--m8` and `--logo-*`, the `.seg` switch). Its tokens join DESIGN.md's table. Its sheet's 2 px
  gap (CR-340 allowed it "outside the scale") takes the off-scale token for 2 px. If its card
  carries the class `card`, it goes through `ui/card.js`; otherwise it is a Costs block and stays
  as it is. The `.seg` control is not touched (the segmented control is out of scope). CR-340
  left the refresh of `docs/web-board/costs-*.png` to `board-design-realign`: this CR does it
  (Evidence).
- **CR-341 board-forge-links**: Home's open-PR rows (`views/home-prs.js`) and the drawer's links.
  This CR does not change those modules (rows are not cards; the drawer head keeps `.row-tags`,
  its rule moved to `panel.css`); a link style it adds uses tokens only, and a chip rule it adds
  in a page sheet moves into `chip.css` as this CR's rebase does for `home.css` and `prs.css`.

Beside this CR in the inbox:

- **board-batch-view-tabs**: the user asked that its Gantt and new views use this CR's rules and
  pieces (tokens, the one card and chip, the Triage priority chip, no side accent border). Its
  time cards go through `ui/card.js` (with a variant in `card.css` if they need one) and its stamps
  follow CR-339's model. Both touch the Batch page (`views/batch-graph.js`, `batch-*.css`):
  whichever lands second rebases; if it lands before this CR, this CR's Driver moves its cards and
  sheets under the rules.

## Out of scope

- The rest of the UX QA: the "one surface" and "no box in a box" rules, unboxing lanes, blocks and
  rows, the label filter chips and the segmented control, the KPI tile, the card band's removal,
  the type scale and radii folded into a scale, the drawer's head and file list, the Batch PR
  card's clipped gate line, Configuration's repeated values, the language mix, the glyph icons,
  the phone bar, the loading state. Each may come back as its own item.
- The mock's exact sizes (its 250 px column, 12 px and 9 px radii, 5 px chip radius): the board's
  tokens and today's values stay.
- Any change to the Costs receipt, its stamp or its image copy.
- New words: only `triage.inbox_sub` and `triage.backlog_sub`, in both word files; the builders
  take the existing keys otherwise.
- No Python change outside `tests/`, no server, record, card (role) or hook change.

## Evidence

- **Tests**: `tests/test_board_design.py` (section 8) green, and `tests/test_code_targets.py`
  green (sheet and script sizes, colours, markup, both word files with the same keys).
- **Gates** (AGENTS.md): before the first push, `just check` and `just eval-dry-run` in the
  worktree at the rebased head (a change under the CLI's `src/`); the pipeline's `just scenario
  (ubuntu-latest)` green at the PR's head (no scenario step added; it must stay green); the local
  `just scenario` (`chantier gate`) when this CR's PR is the top of its batch's stack. `just mod`
  is not owed (no `hooks/` or `types/` change); no pane screenshot is owed (the pane and
  `STATUS.json` do not change).
- **Screenshots**, before (main at the CR's base) and after (the PR's head), same data, side by
  side in the PR's Deliverables, at 1440x900, captioned with the head's SHA (seven characters), no
  username or home folder in view, set against `intake/target-columns.jpg`:
  1. Triage and Kanban: the same column (light area, hairline, plain head, grey sub-line, the same
     dot colours), the same card with no side accent and its priority chip at the top left,
     Triage's Backlog column with its P1-P4 lanes headed by their chips, a picked post-it with its
     check mark after the chip, and the Kanban priority filters as chips, some on (filled) and
     some off (outlined grey), the same size.
  2. Batch (graph and PR column) and the Overview's phone card (375x812): the one card, the node's
     state badge unchanged; the stack rail as a straight hairline.
  3. Configuration's Timing tab: the host cards.
  4. Costs: the receipt unchanged, with its stamp on a running batch, and its copied image
     ("Copy as image") unchanged, stamp included.
  5. Home, PRs and the drawer: unchanged (the sidebar's and the tree's separators kept).
- **Docs**: `docs/web-board.md` lines 61 and 67 corrected (section 3); `just docs-screenshots`
  refreshes `docs/web-board/*.png` (the pages changed; CR-340's `costs-*.png` included); the
  refreshed pictures are in the PR.

## Open questions

None. The working choices above (the meta band kept grey, the stack rail as a solid hairline,
Triage's grill counts kept in the heads, the mock's sizes not copied) stand unless the user says
otherwise.
