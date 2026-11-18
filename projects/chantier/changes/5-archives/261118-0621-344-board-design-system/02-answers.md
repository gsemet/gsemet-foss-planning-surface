# Answers: board-design-system

## DS-Q1: the source of the design values
**Answer (A):** `tokens.css` stays the single source of every value (colours, radii, spacing,
type scale). `DESIGN.md` holds the rules; a test fails when the two disagree (its token table
against `tokens.css`). No build step.

## DS-Q2: scope
**Answer (A):** the three recent horrors plus the foundation:
- one task card everywhere (today six separate builders: `triage/columns.js`, `ui/item-card.js`,
  `kanban-cards.js` twice, `kanban.js`, `overview.js`, `config-timing.js`);
- no side border on any element (`cards.css:71`'s 3px left border curving along the card's
  radius; `batch-prs.css:52`);
- the Triage and Kanban columns are one shared component (today `.tcol`/`.lanes` against
  `.kanban .col`/`.cards`);
- `DESIGN.md`, the shared component sheets (card, column, chip), and the test.
The rest of the UX QA (`intake/ux-qa.md`) stays out; each point may come back as its own item.

## DS-Q3: enforcement
**Answer (A):** a blocking test in `just check`. It refuses a side border, a raw value outside
the tokens, a component class styled in two sheets, and a task card built outside the one card
builder.

## DS-Q4: how a card shows its priority without the left border
**Answer (user's own words):** "there is already a P1 chip in the Triage page, which is very
good." That chip is the model: the same priority chip on every card, on every page.

## Settled by the Chief of Staff
- `DESIGN.md` lives beside the code, in `board/web/`; the project's `AGENTS.md` gains one
  line: any change under `board/web/` reads `DESIGN.md` first and keeps it true.
- `DESIGN.md` names the protected features, starting with the Costs page's paper receipt and its
  stamp, so no design pass removes them.
- The translation rule of design-Q3 (every string through the i18n keys, in every language) is a
  rule of `DESIGN.md`.
- Changing a token or a component sheet changes every page: pages only lay components out
  (grid, gaps), never restyle them.
## DS-Q6: separators and the side-border rule
**Answer (user's words):** "no rounded lateral accent border, that is what is ugly." The rule
forbids a coloured accent border on one side of an element (left or right), above all one that
follows a rounded corner. A plain straight hairline separating two regions of a page (the
sidebar's edge, the drawer tree's edge, the stack rail) stays allowed.

## DS-Q5: the shared column's look
**Answer:** the user asked to see both looks first ("show me"). The screenshots of today's board
(`intake/column-triage.jpg`, `intake/column-kanban.jpg`) confused them, since they still show the
accent borders and the old Kanban filter chips the CR removes; the user asked what there was to
choose.

**Settled by the Chief of Staff** (the user does not want to choose a look; the target is
`intake/target-columns.html`, screenshot `intake/target-columns.jpg`):
- one column on every page: Triage's light area, a hairline border, a plain header (dot, name,
  count) with Kanban's one-line grey subtitle saying what the column holds;
- one card with no side accent: a hairline border all around, the priority chip at its top left;
- one chip: Triage's P1 chip, filled with the priority colour; the Kanban priority filters are
  these same chips, filled when on and outlined grey when off.

## Settled by the Chief of Staff (after the spec)
- Raw values: keep today's look; off-scale values become named tokens at their current values,
  no shift of a few pixels across pages.
- The Batch page's CR nodes and PR cards are cards too: they come from the one card builder.

## Settled by the Chief of Staff (after the spec critic)
- Triage's grey sub-line uses two new keys in both word files: `triage.inbox_sub` ("1-inbox:
  filed") and `triage.backlog_sub` ("2-backlog: P1 to P4"). 3-ready keeps `kanban.ready_sub`. The
  Kanban words would be false on Triage, which holds grilled items too.
- A column that appears on both pages gets Kanban's dot colour on both: Backlog brown, 3-ready
  violet.