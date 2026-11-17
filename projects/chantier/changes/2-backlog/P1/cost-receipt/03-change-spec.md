# Change Specification: the web board's Costs page shows the batch's cost as a supermarket receipt

## Goal

The user's words (2026-11-17, translated): on the board's Costs page, show the cost "in the style
of a supermarket receipt: the lines, then at the end the overall cost, and a cut-out look that
makes you think of a supermarket receipt."

After the mock-ups and a critique, the user settled on one receipt, a modern ticket: on a desktop
it stands on the left of the Costs page, today's cards stay on its right (Recompute with the
computed age, the four figures, Per CR, Last merged); on a phone the ticket is on top and the same
cards follow below it. "The ticket catches the eye; take it away and the cards still give the
information." The approved reference, to compare at delivery, is
`mockups/final-costs.html` (desktop) and `mockups/final-costs-phone.html` (phone) in this CR's
folder.

This is a change to what the user sees on a whole page and to its layout on a phone. It also
records, at `close`, the cost figures the receipt prints (steering, Drivers, workers, outside the
budget) in the batch's JSON record, since today only the batch's Markdown report holds them (see
"Data", Q3).

## Decisions carried from 02-answers.md

| Answer | Decision | Where it lands |
| --- | --- | --- |
| Q1 | Direction 3, the modern ticket (`mockups/receipt-modern.html`): a sans-serif receipt on warm paper, a scalloped cut line with a scissors mark before a large total. The tear-off stub of Q1 is replaced by Q2. | 2 |
| Q2 | One piece, not a card and a stub: the per-CR detail sits under the total, after a dashed rule, and the ticket ends with the barcode. Desktop: the ticket on the left, today's cards on the right. Phone: the ticket on top, the cards below. The cards stay: Recompute with the computed age, the four figures, Per CR, Last merged. | 2, 3 |
| Q2 | The ticket's split bar uses three shades of the board's one accent, in the board's font, both from `board-visual-refresh`. | 2, 6 |
| Q2 | `mockups/final-costs.html` and `mockups/final-costs-phone.html` are the reference to compare at delivery. | 7 |
| Q2, open | Which batch the page shows by default, how another is chosen, and the "thank you" line's figures: not decided by the answers; proposed below and asked in Q1 and Q2 at the end. | 4, Questions |

## 1. Data: the figures the receipt prints

The receipt prints, from top to bottom (the mock-up's own content):

- A head: the eyebrow "Receipt · <project>", the batch id, a pill with its state and how many of
  its CRs are merged ("closed · 11/11 merged", "running · 3/8 merged"), and on the right the shape
  and the steering ("stack, direct"), the opening and the closing time (or "now" while it runs),
  and the duration.
- **Steering**: one line, the steering session (Chief of Staff in direct mode, Foreman otherwise),
  its cost, and under it "N wakes · context M tokens on average" when wakes were measured.
- **Drivers, with their workers**: one line per Driver type, its calls and its cost (each with its
  workers), the costliest first.
- The split bar and its legend: Steering, Drivers, Workers (and, on a host with no parent link,
  "Agents, Driver or worker not measured" in place of Drivers and Workers), each amount
  apportioned so the parts add up to the total in cents, as `batch-NN.md` already prints it.
- The scissors cut line, then **Total** in large type.
- A foot of four cells: Budget (the amount and the share used, or "none"), Average per CR,
  Outside the budget (the grill and the specifications), and that part's calls.
- A dashed rule, "Detail · per CR": one line per CR of the batch, the costliest first (CR id, its
  title as `format.title()` shortens it, its cost), then "Sum of the CRs" and "the rest, $X, is
  steering".
- The barcode (decorative, `aria-hidden`), then the "thank you" line (Q2).

Today, the board has the total, the budget and each CR's cost (the record and the live figure),
but the Steering, Drivers, split and Outside-the-budget figures exist only as text lines: the
`## Cost` section of `5-archives/batches/batch-NN.md` (built by `cost_summary` and `chief_line`)
and what `chantier cost --summary` prints. The board must not parse that Markdown. So (Q3,
proposed):

1. **One structured source.** In `skills/chantier/scripts/cli/src/chantier/commands/cost/`, a
   function (in `breakdown.py`, beside `cost_summary`) returns the receipt's figures as data from
   the priced rows, `cost_groups(..., "driver")` and the Chief of Staff's figures:

   ```json
   {
     "steering": {"label": "Chief of Staff, steering the batch", "usd": 15.99, "calls": 0,
                  "unpriced": {}, "wakes": 61, "context_avg": 180750},
     "drivers": [{"type": "chantier:cr-driver", "usd": 41.99, "calls": 1843, "unpriced": {}}],
     "split": [{"part": "steering", "usd": 15.99, "unpriced": {}},
               {"part": "drivers", "usd": 15.33, "unpriced": {}},
               {"part": "workers", "usd": 30.46, "unpriced": {}}],
     "outside": {"usd": 5.10, "calls": 93, "unpriced": {}}
   }
   ```

   `split` holds the same parts as `_split` (with `"agents"` when it has a figure), the `usd` of
   each already apportioned in cents (`apportion`), so they add up to the total exactly. `drivers`
   is empty where Drivers cannot be told from workers (`measured` false in `cost_summary`, Copilot).
   `outside` is `null` when the Chief of Staff's session cannot be measured (`_chief_unknown`'s
   causes), with a `"outside_unknown": "<cause>"` beside it; never a $0.00. The exact key names are
   the Driver's; the content is this.
2. **`cost_summary` and `chief_line` print from it**, so the Markdown lines and the JSON never
   disagree: the split, wakes and Driver lines of `cost_summary` are built from this data, and
   `chief_line`'s grill figures come from a structured reading of `_Chief` (in
   `commands/cost/sessions.py`) that both the text lines and the receipt use. The text they print
   does not change by one byte (the scenario's `batch-NN.md` checks and `cost --summary` stay as
   they are).
3. **`close` records it.** `close_archive._close_files` adds the receipt data to the record as
   `cost_receipt` (through `history.close_record`), from the same rows it already prices once
   (`Closing.rows`). `core/batch_records.blank_record` gains `"cost_receipt": null`, so a running
   batch's record (`open_record`) and a back-filled one carry the key empty. `SCHEMA` stays 1: the
   key is added, and every reader uses `.get`.
4. **The board's live figure carries it.** `board/costs.py`'s `compute()` adds `"receipt"` (the
   same function, on the same rows; it also reads the Chief of Staff's transcripts, as `cost`
   does); `_failed()` and `Live.snapshot()`'s empty default carry `"receipt": None`. The board
   still records nothing.
5. **A record from before this change** (`cost_receipt` missing or `null`) shows a receipt with
   what it has: the head, the total, the budget, the per-CR detail and its sum; in place of the
   Steering and Drivers groups and the split, one muted line, "roles not recorded for this batch".
   Nothing is back-filled, no figure is guessed from the Markdown.

Money words follow the board's existing rules: a figure with calls of an unpriced model reads "at
least $X"; an unknown one reads "unknown", never $0.00; a missing one reads "—" (`format.usd`).

## 2. The receipt (web)

In `skills/chantier/scripts/cli/src/chantier/board/web/`:

- **`js/views/costs-receipt.js`** (new): the receipt's markup, `receipt(view)` built with `html`
  from `core/dom.js`, from one plain object (below). No `fetch`, no `localStorage`, no inline
  style: the split bar's widths go through `vars()` / `data-vars` as `costs-tables.js` does for its
  bars. The barcode and the cut line are CSS only and `aria-hidden`. The `<section>` has
  `aria-label` "Cost receipt for <batch>".
- **`js/model/receipt.js`** (new, pure, no DOM): builds that object from the store's data for the
  chosen batch: from the running batch (`data.batch`, with `withLive`'s figures and the live
  `receipt`), or from a closed batch's record in `data.history` (`cost_usd`, `budget_usd`, `crs`,
  `cost_receipt`, `opened`, `closed`, `mode`, `steering`). The Driver type is shown without a
  `<plugin>:` prefix ("cr-driver"); no role name is written in the board's code.
- **`js/model/live.js`**: `withLive` also lays the live `receipt` on the running batch
  (`batch.cost_receipt`) when the live figure is usable, as it does for `spent_usd`.
- **`css/views/costs-receipt.css`** (new, linked in `index.html` after `costs.css`): the ticket as
  in `mockups/final-costs.html` (`.ticket` and what follows it there): warm paper with its faint
  texture, 16px radius, the scalloped bottom edge, the scissors cut line, the dashed rule, the
  large total, the tabular figures. Every colour comes from `css/tokens.css` (new tokens for the
  paper and its lines; the three split shades are `board-visual-refresh`'s `--accent`,
  `--accent-dark` and `--accent-light`, the mock-up's `--tk`, `--tk1` and `--tk3`). No
  `!important`, no id selector, nesting at most 3.
- On a desktop the ticket is about 420px wide and `position: sticky` at the top of the page while
  the cards scroll; under the phone breakpoint (`max-width: 760px`, today's) it takes the full
  width, is not sticky, and its padding narrows (the phone mock-up's `.ticket` override).

## 3. The page around it

- **`js/views/costs.js`**: the page becomes two columns, the receipt on the left and today's cards
  in a column on the right (`.cwrap` / `.cside` in the mock-up), one column on a phone with the
  receipt first. The cards stay (the age line with Recompute and its note, the four figures, Per
  CR, Last merged, Earlier batches (Q1)), and the four figures' labels and sub-lines follow the
  approved mock-up `mockups/final-costs.html`, the delivery reference:
  - Spent: the label "Spent, <batch>"; the sub-line "closed, <duration>" for a closed batch
    ("closed, 10 h 56 min"), "running, <duration so far>" while it runs; the budget gauge stays
    under it when a budget is set, as today.
  - Budget: the budget or "none"; the sub-line "$X outside it (grill, specs)", X the receipt's
    Outside-the-budget figure, in the money words of section 1 ("unknown" when the Chief of
    Staff's session cannot be measured, "—" on a record with no `cost_receipt`). The share used
    moves to the receipt's foot (section 1).
  - Sum of the CRs: as today, sub-line "the rest: steering".
  - Average per CR: the label without "active" (today "Average cost per active CR"); sub-line as
    today, "N CRs with a cost".
- **On a phone** (under `max-width: 760px`), as `mockups/final-costs-phone.html` does, and only
  here (`board-visual-refresh` leaves both to this CR):
  - `js/views/costs-tables.js`: the Per CR table shows CR, Title and Cost; its State column and its
    bar fold away (`hide-phone`). Today it folds the Title and the bar; the Title comes back, the
    State goes, so a row fits 390px. Last merged keeps today's fold.
  - `js/views/costs.js` / `css/views/costs.css`: the age line wraps, and its note ("the server
    reads the transcripts again: no agent turn") is hidden; the time and the Recompute button
    stay.
- **`css/views/costs.css`**: the two-column layout and its phone form; the four figures in four
  columns beside the ticket on a desktop, two on a phone (as today).
- **Words**: every new word (the eyebrow, Steering, "Drivers, with their workers", the split's
  parts, Total, Budget, none, Average per CR, Outside the budget, "grill and specs, N calls",
  "Detail · per CR", "Sum of the CRs", "the rest, $X, is steering", "N wakes · context M tokens
  on average", "roles not recorded for this batch", the thank-you line, the state pill) is a
  `costs.receipt_*` key in each language file under `js/i18n/` (`en.js` and `fr.js`), the same
  keys in each; the cards' changed words (`costs.spent`, `costs.avg`, and the new Spent and Budget
  sub-lines) change in both files alike.
- Each file stays within CONTRIBUTING.md's targets (300 lines a file, 50 lines and complexity 10 a
  function): the receipt is its own module, not more lines in `costs.js`.

## 4. Which batch the page shows (Q1, proposed) and the thank-you line (Q2, proposed)

Proposed, pending the user's answer to Q1:

- By default the page shows the running batch; with no batch running, the last closed one (the
  newest record of `data.history` whose `state` is `closed`). Today, with no batch running, the
  page shows "no batch" and the history; the mock-up shows batch-22, closed.
- Another batch is chosen in the **Earlier batches** table: a click (or Enter, Space) on a row puts
  that batch on the page; the row is marked chosen; a link "back to <running batch>" above the
  table (only when a batch runs and another is chosen) puts the running one back. The row no
  longer unfolds its CRs, since the receipt and Per CR list them. The choice lives in the store
  (`core/store.js`, a `costsBatch` key next to today's `historyOpen`, which goes), not in the URL.
- The whole page follows the chosen batch: the receipt, the four figures and Per CR. For a closed
  batch they read its record (Per CR shows its `result` and `rounds` in the State column), and
  the age line says "final, recorded at close" with no Recompute button (a closed record is final;
  the live figure prices only the running batch). Last merged and Earlier batches stay as they
  are.

Proposed, pending the user's answer to Q2: the thank-you line keeps "thank you · N PRs", N being
the CRs of the batch with `result == "merged"` and a `pr` recorded (not null): a dropped CR also
records its `pr` (`history.cr_entry`), so a PR alone does not count. For the running batch, the CRs
whose state is merged and that have a `pr`. It drops "· 0 reverted": no record says whether a PR
was reverted, and no figure is made up.

## 5. Docs

- `docs/web-board.md`, "### Costs": rewritten for the receipt, its place on a desktop and a phone,
  what it prints, "roles not recorded" on an older record, and how a batch is chosen.
- `docs/web-board/costs-pc.png` and `costs-phone.png` redone with `just docs-screenshots`. The
  demo surface (`docs/demo/`) gains a `cost_receipt` in
  `projects/mobile-app/changes/5-archives/batches/batch-02.json` (made-up figures that add up) so
  a screenshot shows a full receipt; the Driver chooses whether the Costs capture
  (`scripts/docs_screenshots.py`, `views()`) moves to `mobile-app` or keeps `shop-api` (whose
  running batch has no transcripts, so no live receipt figures), and says which in the PR.
- `docs/costs.md`: one line that the batch's record keeps the receipt's figures
  (`cost_receipt`) from `close` on.

## Out of scope

- Any other page's look: `board-visual-refresh` restyles every view, the Costs cards included.
  This CR builds the receipt and the page's two-column layout, in that CR's accent and font.
- Back-filling `cost_receipt` into the records of batches closed before this change.
- What `chantier cost`, `cost --summary`, `status` and `batch-NN.md` print: unchanged, byte for
  byte.
- A print or export of the receipt; a History page (`board-history`, P3).
- The CR board pane (`hooks/`) and `STATUS.json`: not touched, so no pane screenshot is owed.

## Dependency

The receipt uses the Inter font and the accent's three shades that `board-visual-refresh` brings
(`2-backlog/P1/board-visual-refresh/03-change-spec.md`, its section 2; its Q6 says
"cost-receipt's ticket follows this style"): `--accent` (`#1d5c63`), `--accent-dark` and
`--accent-light` in `css/tokens.css`, the tints `--accent-tint` and `--accent-tint-2` for a pill.
That CR leaves the Costs page's layout to this one, and also the phone fold of the Per CR table and
the Recompute note on a phone, stated once here, in section 3. This CR goes after it (in the same
batch, stacked on it, or in a later batch): the Chief of Staff records the dependency (Q4). A
Driver who finds those tokens absent stops and says so; it does not invent a colour.

## Evidence

- **pytest** (`just test`, kept fast, in the existing cost tests, parametrized): the receipt
  function on prepared rows gives a split whose parts add up to the total in cents, a Steering
  line with wakes and average context, one Driver line per type sorted by cost; with no parent
  link (Copilot rows) no Driver line and an `agents` part; with the Chief of Staff not measured,
  `outside` null and its cause, never 0. And `cost_summary`'s lines are the same text as before for
  the same rows (one case whose expected lines are written out).
- **`just check`**: lint (Biome on the new JS and CSS, ruff, mypy), the code targets test (file
  and function sizes, no inline style, colours in `tokens.css`), the words test (same keys in
  `en.js` and `fr.js`).
- **`just scenario`** (the CLI's `close` and the board's live figure change, so the long gate is
  due before the PR; and, as the top of its stack, the local run on Windows):
  - after `close --yes`: `batch-NN.json` has `cost_receipt`, its `split` adds up to `cost_usd`
    within a cent, its Driver lines match the "Driver ... with its workers" lines of
    `batch-NN.md`'s `## Cost`, and the existing checks of that section pass unchanged;
  - a record from `open` carries `"cost_receipt": null`;
  - the board's `GET costs` after `POST costs/recompute`: `live.receipt` is present and its split
    adds up to `live.spent_usd` within a cent.
- **Delivery against the reference**: the PR's Deliverables carry two screenshots of the real
  Costs page from the PR's head, desktop and phone width, on a batch with a full receipt (the demo
  surface's or a made-up one: no real path or user name in any image), each beside the matching
  mock-up (`final-costs.html`, `final-costs-phone.html`), captioned with the head's seven-character
  SHA, and one of a record with no `cost_receipt` ("roles not recorded"). Differences from the
  mock-up are listed in the PR body, each with its reason.

No CI job is added or changed.

## Questions for the user

1. **Which batch, and how another is chosen.** Proposed (section 4): the running batch, or with
   none the last closed one; a click on an Earlier batches row shows that batch on the whole page
   (receipt, figures, Per CR) instead of unfolding its CRs, with a link back to the running batch;
   a closed batch shows "final, recorded at close" and no Recompute. Yes, or another way?
2. **The thank-you line.** Proposed: "thank you · N PRs" from the record, N the CRs merged with
   a PR (`result == "merged"` and a `pr`; a dropped CR's PR does not count), without "0 reverted",
   which nothing records. Keep it so, drop the whole line, or keep it as a plain
   "thank you"?
3. **Recording the receipt's figures.** The Steering, Drivers, split and Outside-the-budget lines
   exist today only as text in `batch-NN.md`. Proposed: `close` also writes them as data in
   `batch-NN.json` (`cost_receipt`), the board's live figure computes them for the running batch,
   and batches closed before this change show their receipt without those lines ("roles not
   recorded for this batch"), with no back-fill. Yes, or should older records be back-filled, or
   the receipt hold only the per-CR lines and the total?
4. **Order with `board-visual-refresh`.** Proposed: this CR goes after `board-visual-refresh`
   (it takes that CR's font and its `--accent`, `--accent-dark` and `--accent-light`), stacked on
   it in the same batch or in a later one; `board-visual-refresh` leaves the Costs layout, the
   phone fold of Per CR and the Recompute note on a phone to this CR. Yes?
