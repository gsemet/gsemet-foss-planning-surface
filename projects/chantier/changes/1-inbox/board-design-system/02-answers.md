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