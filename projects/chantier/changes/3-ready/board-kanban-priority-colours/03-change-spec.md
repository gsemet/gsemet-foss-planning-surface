---
type: cr-change-spec
description: The web board's Kanban gets a visible horizontal scrollbar; P1-P4 get a teal gradient wherever an item is drawn; the board gets pastel backgrounds (variant A), a lightly tinted sidebar and project marks off the state hues, the CR state colours untouched.
---

# Change Specification: board-kanban-priority-colours

Origin: verbal (the user, 2026-11-17). Folds in the inbox item `board-pastel-colours` (its folder
is the Chief of Staff's to drop; the Driver does not touch it).

## Goal

The user, on the web board:

1. The Kanban shows no horizontal scrollbar: fix it.
2. A colour code per priority, P1 to P4, as a gradient of one colour.
3. The style is elegant; it wants a little more pastel colour.

All of it without touching the CR colour code: the states' colours (blocked red, working blue,
ready green, draft brown, local violet, waits orange, queued grey, merged dark green) keep their
values and their meaning, here and in `status`, and no colour of the board may look like one of
them unless it shows that state.

## Decisions carried from 02-answers.md

| Answer | What it decides |
| --- | --- |
| scope-Q1 | One CR holds the colours: the Kanban's scrollbar, the priority colours, the pastel style (`board-pastel-colours` folded in). The other three CRs of the 2026-11-17 feedback (board-picker-surface-item, board-batch-navigator, board-config-role-descriptions) are not this CR. |
| kanban-Q3 | Replaced by kanban-Q3b (the warm gradient read like blocked, waits and draft). Nothing of it is implemented. |
| kanban-Q3b | The priority gradient is the board's teal accent: P1 `#1d5c63` (dark) to P4 `#cfe2e3` (very pale), on the card's left border and on its `Pn` chip; the card's background stays white. |
| pastel-Q4 | Variant A: the state chips, the project's avatar, the figure cards (Costs) and the Kanban's column headers get a pastel background; the pages' background stays white. Not chosen: a tinted page background, a coloured sidebar (variant C's strong one), A and B together. |
| Round 3, colour code | The eight state colours (`--state-*` in `css/tokens.css`) stay as they are; no new colour may look like one of them. |
| Round 3, sidebar | On top of variant A, the left sidebar's background is tinted lightly. |
| colours-Q11 | The `Pn` chip and the card's left border show everywhere the item is drawn: the Kanban, Triage and the panel's head; not on the Kanban only. |
| colours-Q12 | This CR moves the project-mark colours that look like a state colour (blocked, working, local, draft/waits) to hues no state uses. |
| colours-Q13 | Every Kanban column header takes one neutral pastel, the accent's tint (a header in its column's hue would make Backlog, Grill and 3-ready look like draft, waits and local); the column dots stay as they are. |
| Settled (Chief of Staff) | The Costs figure cards take the accent's teal tint (no violet, warm or blue tint, which read as states). A P4 chip close to the 3-ready chip is acceptable: 3-ready's chip does not change. |

The mock-up of variant A (published at https://claude.ai/artifact/SUJkNC5DQrjDngmdhxRpY9) gives
the state-chip shades quoted below; its priority colours (kanban-Q3's warm ones), its per-card
figure tints and its per-column header tints do not apply.

## What changes

All the files are under `skills/chantier/scripts/cli/src/chantier/board/web/` (called `web/`),
plus one paragraph pair in `docs/web-board.md` (section 6). The board's rules hold
(CONTRIBUTING.md, "board's page"): every colour lives in `css/tokens.css` and nowhere else
(`tests/test_code_targets.py` refuses a colour elsewhere), a colour computed in JS is passed as a
custom property through `vars()` / `data-vars` (as `dot()` does), no `style=`, no `!important`,
CSS nesting at most 3 levels, every `.js` and `.css` file at most 300 lines, every function at
most 50 lines. No Python, no CLI command, no card and no `status` output changes.

### 1. The Kanban's horizontal scrollbar

Cause, as read: `.main` (`css/shell.css`) scrolls vertically and hides its horizontal overflow;
`.view` is `flex: 1 0 auto`, so its height is its content's; `.kanban { height: 100% }` and
`.kanban .col { max-height: 100% }` (`css/views/kanban.css`) then resolve against no definite
height. The board (`.kanban .board`, `overflow-x: auto`) grows as tall as its tallest column, and
its horizontal scrollbar sits under that column, below the window's fold: the user never sees it.

Behaviour to reach:

- On the Kanban, the columns' row fills the main area's visible height, under the title row and
  the filters; the page itself does not scroll vertically on the Kanban (on a window tall enough
  for the title and filters).
- The horizontal scrollbar of `.kanban .board` is always on screen, at the bottom of the window,
  whenever the seven columns are wider than the main area.
- Each column scrolls vertically on its own (`.kanban .col` keeps `overflow: auto`, now bounded).
- The other views keep scrolling as today (only the Kanban changes). The phone layout keeps its
  snap per column (`@media (max-width: 760px)`), with the same bounded height above the bottom bar.

A way to do it, for the Driver to confirm in a browser: on the Kanban only, the view becomes a
bounded flex item of `.main` (for instance `.view:has(> .kanban) { flex: 1 1 0; min-height: 0; }`
and `.main:has(.kanban) { overflow-y: hidden; }`, so `height: 100%` resolves), with no JS. Any
other CSS that gives the same behaviour on the current Chrome, Edge, Firefox and Safari is fine.
The scrollbar keeps the board's style (`base.css`: thin, `--scroll` thumb).

`css/views/kanban.css`'s header comment says "five columns": it becomes "seven columns".

### 2. The priority colours (kanban-Q3b, colours-Q11)

Tokens, in `css/tokens.css`, a new group "the priorities: a gradient of the accent, P1 dark to P4
pale":

| Token | Value | Chip ink |
| --- | --- | --- |
| `--pri-1` | `#1d5c63` (the accent's value) | `--white` |
| `--pri-2` | an intermediate teal on the P1 to P4 gradient (the existing `--accent-mid` `#5f8d93` is on it) | `--white` or `--accent-dark`, whichever meets the contrast below |
| `--pri-3` | an intermediate teal on the gradient (the existing `--accent-light` `#8fb6ba` is on it) | `--accent-dark` |
| `--pri-4` | `#cfe2e3` | `--accent-dark` |

P1 and P4 are the user's values and do not move. P2 and P3 sit between them on the same teal; the
Driver may darken or lighten them along that line only to meet a contrast of at least 4.5:1
between the chip's text and its background, and records the four pairs and their ratios in the PR.
Each token may be a new value or a `var()` of the accent tokens; none is a new hue.

Where they show, everywhere a backlog item whose bucket is `P1`...`P4` is drawn:

- **The `Pn` chip.** `tag(\`pri-${bucket}\`, ...)` already renders `class="tag pri-P1"`...
  `pri-P4` in the shared item card (`js/ui/item-card.js`, used by the Kanban and by Triage through
  `js/triage/postit.js`) and in the panel's head (`js/panel/head.js`). `css/tags.css` gets
  `.tag.pri-P1` to `.tag.pri-P4`: background `--pri-N`, text its chip ink. Being on the tag, the
  colour shows in all three places. `pri-inbox` stays the grey chip and `pri-3-ready` stays as it
  is (accent tint, accent ink).
- **The card's left border.** Every item card of a `P1`...`P4` bucket has a left border of 3px in
  `--pri-N`; its other borders, its radius, its shadow and its white background stay. `itemCard`
  (`js/ui/item-card.js`) adds a class or attribute that names the priority (for instance `pri-P2`
  on the card, or a `data-pri`), and one rule in `css/cards.css` (not scoped to a view) draws the
  border, so it holds on:
  - the Kanban: the Backlog column, and the Grill column's items from a priority bucket;
  - Triage: the cards of the P1 to P4 lanes (Triage passes the lane as the bucket); the rule must
    win over `.card.pi.sel { border-color: var(--card-line) }` (`css/views/postit.css`) and over the
    pick-up and drag looks (`.pi:hover`, `.pi.drag`), so a selected or dragged card keeps its
    priority's left border; and when a card is dropped into another lane, its border follows the
    new lane at the next paint;
  - the panel's head: it draws no card, only the item's tags (`head.js`, the `pri-` tag, the slug,
    the stage word); there the priority shows in the chip. If the head's row has a container the
    Driver can give the same 3px left mark in `--pri-N` without new markup beyond a class, it does;
    else the chip alone is the head's priority mark, said in the PR.
- **Not coloured:** the Inbox's items (no priority), the 3-ready items, the batch's CRs (In
  progress, Handed back) and the merged CRs (Done): the board's data carries no priority for a CR
  (`board/state.py` gives priorities to backlog items only), and this CR adds none.
- The selected Kanban card (`.card.sel`, accent border and tint ring) keeps its look; its left
  border stays the priority's colour.

### 3. The pastel style, variant A (pastel-Q4, colours-Q13)

New tint tokens in `css/tokens.css`, each the pale version of an existing colour, never a new hue.
The state tints are of the states' own hue and are used only on a chip or badge that shows that
state:

| Token | Value (from the mock-up where it has one) |
| --- | --- |
| `--state-working-tint` | `#e7eefb` |
| `--state-ready-tint` | `#e4f4ec` |
| `--state-blocked-tint` | `#fbe7ea` |
| `--state-waits-tint` | `#fbf0de` |
| `--state-merged-tint` | `#e3f1ea` |
| `--state-draft-tint` | a pale of `--state-draft`'s hue (the mock-up has none) |
| `--state-local-tint` | a pale of `--state-local`'s hue (the mock-up has none) |
| `--state-queued-tint` | `var(--chip)` (the queued grey stays a grey) |
| `--mark-0-tint`...`--mark-5-tint` | a pale of each `--mark-N`, after section 5 moves the marks |

The `--state-*` values themselves do not change. Two comments change with the rule:

- `css/tokens.css`, "a state: one colour, for its icon, dot or badge only": it says a state has one
  colour for its icon, dot or badge, and its tint for the background of a chip or badge that shows
  that state, nowhere else.
- `css/tags.css`'s header ("neutral grey, no border. The only colours are the accent (the CR id,
  3-ready) and a state's own, in its icon"): it says the chips are grey but a state chip, on its
  state's tint, and a priority chip, on its priority's teal; the CR id and 3-ready keep the accent.

Where the tints go:

- **State chips.** A state chip takes its state's tint as background; its icon keeps the state's
  colour, its word keeps its ink. The chips are:
  - `stateTag()` (`js/ui/parts.js`): today `class="tag st"`; it adds the state's name
    (`tag st working`...). Used by the panel's head, Costs' tables, Home's PRs.
  - The breadcrumb's batch chip (`crumbs()` in `js/ui/header.js`, `.crumbs .chip` in
    `css/crumbs.css`): it adds the shown state's name (`working` or `queued`), and the tint comes
    from a rule per state class. A crumbs chip with no state class, or with a class that has no
    state tint, keeps today's grey `--chip` background: the base `.crumbs .chip` rule stays as it
    is and the tints are added only by state-class rules. This covers the `closed` chip that
    board-batch-navigator adds to `crumbs()`; whichever of this CR and board-batch-navigator
    merges second keeps both changes (the state tints, and the navigator's chip and its grey).
  - The Batch graph's state badge (`.batch .node .sb`, `css/views/batch-graph.css`), which already
    carries the state's class: its white background becomes the state's tint.
  - `nextTag()` ("next", `tag queued`): the queued tint, a grey, as today's grey chip.
  Rules in `css/tags.css` (and the two view files), one per state, from the tokens above.
- **The project's avatar.** `.mark[data-mark="N"]` (`css/components.css`) takes `--mark-N-tint` as
  background and `--mark-N` as the letter's colour, everywhere `mark()` draws it (sidebar picker,
  picker menu, All projects' table and cards). `.mark.all` (the overview's ink square) stays.
  Triage's stage marks (`js/triage/postit.js`'s own `mark`) are another component and stay.
- **The figure cards (Costs).** The four `.kpi` of the Costs view (`.costs .kpi`,
  `css/views/costs.css`) take the accent's tint (`--accent-tint`) as background and a slightly
  darker tint of the accent as border, all four the same. Home's figure cards (`.kpi` elsewhere)
  stay white.
- **The Kanban's column headers (colours-Q13).** Every column's header (`.kanban .colh`) takes the
  same neutral pastel, the accent's tint (`--accent-tint`), with a small radius and room so the
  count chip still reads; a CSS rule in `css/views/kanban.css` is enough, no JS change. The column
  dots (`dot(c.color)` in `js/views/kanban.js`) stay as they are, colours included.
- **The sidebar's active row** (variant A in the mock-up): `.nav.on` (`css/sidebar.css`) takes the
  accent's tint as background and `--accent-dark` as ink and icon colour, in place of the grey
  pill.
- The pages' background (`--bg`, `--panel`) stays white; the cards stay white.

### 4. The lightly tinted sidebar (Round 3)

`--side` in `css/tokens.css` changes from white to a very light tint of the accent, lighter than
`--accent-tint` so the active row (above) still stands out on it; the sidebar's right hairline
takes a matching tint. The hover of a row (`.nav:hover`, `button.ws:hover`) stays visible on the
tint. What sits on the sidebar and is white today (the language button, the picker's menu) stays
white. The phone has no sidebar: nothing changes there.

### 5. The project marks off the state hues (colours-Q12)

The six marks (`--mark-0`...`--mark-5` in `css/tokens.css`; `markOf()` in `js/core/format.js`
picks one from a project's id, unchanged) today are:

| Token | Today | Looks like |
| --- | --- | --- |
| `--mark-0` | `#c8401f` red-orange | blocked |
| `--mark-1` | `#2f6f9f` blue | working |
| `--mark-2` | `#5b7a2a` olive green | to judge against ready and merged |
| `--mark-3` | `#7a4aa8` violet | local |
| `--mark-4` | `#a8691f` ochre | draft and waits |
| `--mark-5` | `#1f7a74` teal | no state (the accent's family) |

The Driver moves `--mark-0`, `--mark-1`, `--mark-3` and `--mark-4`, and `--mark-2` if it judges it
reads as ready or merged, to hues no state uses: each new hue at least 25 degrees (HSL hue) away
from every state colour's hue (`--state-blocked`, `-working`, `-ready`, `-draft`, `-local`,
`-waits`, `-merged`; the queued grey has none), the six marks still distinct from one another, and
none equal to a `--pri-N` value. The free regions today are roughly the magentas and pinks, the
yellow-olives, the cyans and the slate blue-greys. Their strength stays close to today's (they
now show as the letter's ink on the tint, section 3, at least 4.5:1 against their tint). The PR
carries a table: each mark's old and new value, its hue, and its nearest state hue with the gap.

### 6. The guide (`docs/web-board.md`)

One sentence each, in the existing paragraphs:

- **Kanban** (the paragraph under the Kanban picture): a backlog item's priority shows as a teal
  shade, darkest for P1 and palest for P4, on its `Pn` chip and its card's left border.
- **Triage** (the paragraph under the Triage picture): the post-its of P1 to P4 carry the same teal
  shade of their priority on their chip and left border as on the Kanban (and the panel's head
  shows the same chip).

The pictures in `docs/web-board/` are not retaken (see out of scope).

## Out of scope

- The `--state-*` colours, their meaning, and `status`'s output.
- The Kanban's column dots.
- A priority for the batch's CRs or the merged ones (not in the board's data).
- The 3-ready chip (kept, though close to P4).
- A tinted page background (variant B), a strongly coloured sidebar (variant C), A and B together.
- The priority filter's toggles (`js/labels/priority.js`): they keep the label chips' look.
- Home's figure cards, the Triage view's grill-state marks and lane colours, the Costs receipt.
- The labels' six colours (`--label-0`...`--label-5`).
- The documentation's screenshots of the board (retaken by hand before a release).
- The `board-pastel-colours` folder (the Chief of Staff drops it).
- The other three CRs of the 2026-11-17 feedback.

## Evidence

- `just check` green (Biome, `tests/test_code_targets.py`: no colour outside `tokens.css`, file and
  function sizes, nesting; `just test` within its time budget).
- `just scenario` green on the pipeline (`ubuntu-latest`) at the PR's head (the board's web files
  ship with the CLI package).
- In the PR's Deliverables, screenshots of the board served by `chantier board` from the PR's head,
  on a project with items in P1 to P4, captioned with the head's SHA (seven characters):
  - the Kanban in a window about 1280x800 with its seven columns: the horizontal scrollbar visible
    at the bottom without scrolling the page; the four priority chips and left borders; the
    column headers in the one accent tint, the dots unchanged;
  - the same on a phone width (about 390px): one column at a time, the snap kept;
  - Triage with cards in the four lanes, one of them selected: the chips and left borders kept;
  - the panel of a P1...P4 item (its head's priority mark) and the panel of a CR (its state chip);
  - the Costs view (the four figure cards), the Batch view (state badges and the breadcrumb's
    chip), the sidebar with its tint, its active row and a project's mark, and All projects with
    several projects' marks.
- A table in the PR: each new text-on-background pair (the four `Pn` chips, the active nav row,
  each mark's letter on its tint) with its contrast ratio, each at least 4.5:1.
- The marks' table of section 5.
- A short check in the PR that `tokens.css`'s `--state-*` value lines are unchanged (`git diff` of
  those lines empty; only the group's comment changes).

## Open questions

None: colours-Q11, colours-Q12, colours-Q13 and the Chief of Staff's settled points closed them.
