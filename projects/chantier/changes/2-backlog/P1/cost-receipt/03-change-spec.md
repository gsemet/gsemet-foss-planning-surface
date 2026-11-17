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
`prototypes/01-mockups/final-costs.html` (desktop) and `prototypes/01-mockups/final-costs-phone.html` (phone) in this CR's
folder.

This is a change to what the user sees on a whole page and to its layout on a phone. It also
records, at `close`, the cost figures the receipt prints (steering, Drivers, workers, outside the
budget) in the batch's JSON record, since today only the batch's Markdown report holds them (see
section 1, Q6).

## Decisions carried from 02-answers.md

| Answer | Decision | Where it lands |
| --- | --- | --- |
| Q1 | Direction 3, the modern ticket (`prototypes/01-mockups/receipt-modern.html`): a sans-serif receipt on warm paper, a scalloped cut line with a scissors mark before a large total. The tear-off stub of Q1 is replaced by Q2. | 2 |
| Q2 | One piece, not a card and a stub: the per-CR detail sits under the total, after a dashed rule, and the ticket ends with the barcode. Desktop: the ticket on the left, today's cards on the right. Phone: the ticket on top, the cards below. The cards stay: Recompute with the computed age, the four figures, Per CR, Last merged. | 2, 3 |
| Q2 | The ticket's split bar uses three shades of the board's one accent, in the board's font, both from `board-visual-refresh`. | 2, Dependency |
| Q2 | `prototypes/01-mockups/final-costs.html` and `prototypes/01-mockups/final-costs-phone.html` are the reference to compare at delivery. | Evidence |
| Q3 | The page shows the running batch by default; with none running, the last closed one. | 4 |
| Q4 | Choosing another batch is not this CR: it is its own CR, aligned with `board-batch-view`'s previous/next navigation. This CR keeps today's Earlier batches unfold. | 4, Out of scope |
| Q5 | The thank-you line reads "thank you · N PRs", N the CRs with `result == "merged"` and a `pr`; no "0 reverted". | 1, 4 |
| Q6 | `close` writes `cost_receipt` in `batch-NN.json`; no back-fill; a record without it shows "roles not recorded for this batch". | 1 |
| Q7 | This CR goes after `board-visual-refresh`, stacked on it in the same batch, with a `depends.json` on `board-visual-refresh`. | Dependency |
| Q8 | The per-CR detail ends with "the rest, $X: steering and agents outside a CR", the parts named, each with its amount, when there are several. | 1, 3 |
| Q9 | The foot's Outside-the-budget cell holds two lines: the grill and the specifications; the Chief of Staff's steering (Foreman batch). | 1 |
| Q10 | A paused batch, or a running one with no usable live figure: the pill shows the real state (running, paused); the Steering, Drivers and split lines read "not computed yet" or the live error, with Recompute. "roles not recorded" is only for a closed record without `cost_receipt`. | 1, 2 |

## 1. Data: the figures the receipt prints

The receipt prints, from top to bottom (the mock-up's own content):

- A head: the eyebrow "Receipt · <project>", the batch id, a pill with its real state (closed,
  running, paused: the record's `state`) and how many of its CRs are merged ("closed · 11/11
  merged", "running · 3/8 merged", "paused · 3/8 merged"), and on the right the shape and the
  steering ("stack, direct"), the opening and the closing time (or "now" while it runs or is
  paused), and the duration.
- **Steering**: one line, the steering session (Chief of Staff in direct mode, Foreman otherwise),
  its cost, and under it "N wakes · context M tokens on average" when wakes were measured.
- **Drivers, with their workers**: one line per Driver type, its calls and its cost (each with its
  workers), the costliest first.
- The split bar and its legend: Steering, Drivers, Workers (and, on a host with no parent link,
  "Agents, Driver or worker not measured" in place of Drivers and Workers), each amount
  apportioned so the parts add up to the total in cents, as `batch-NN.md` already prints it.
- The scissors cut line, then **Total** in large type.
- A foot of four cells: Budget (the amount and the share used, or "none"), Average per CR, Outside
  the budget, and that part's calls. The Outside-the-budget cell holds two lines (Q9): "grill and
  specifications", its amount; and "Chief of Staff, steering", its amount, in a Foreman batch only
  (in a direct batch the Chief of Staff's steering is the batch's Steering line, inside the
  budget). Its calls cell gives each part's calls on the same two lines.
- A dashed rule, "Detail · per CR": one line per CR of the batch, the costliest first (CR id, its
  title as `format.title()` shortens it, its cost), then "Sum of the CRs" and the rest (Q8):
  "the rest, $X: steering and agents outside a CR", X the total less the sum of the CRs. When the
  receipt's data tells its parts and more than one has a figure, each is named with its amount
  ("steering $a · agents outside a CR $b"), the steering part being the Steering line's figure and
  the other the remainder; when only one part has a figure, that part alone is named ("the rest,
  $X: steering"). On a record without `cost_receipt` the line keeps the answer's words, with no
  parts.
- The barcode (decorative, `aria-hidden`), then the thank-you line (Q5, section 4).

Today, the board has the total, the budget and each CR's cost (the record and the live figure),
but the Steering, Drivers, split and Outside-the-budget figures exist only as text lines: the
`## Cost` section of `5-archives/batches/batch-NN.md` (built by `cost_summary` and `chief_line`)
and what `chantier cost --summary` prints. The board must not parse that Markdown. So (Q6):

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
     "outside": {"grill": {"usd": 5.10, "calls": 93, "unpriced": {}},
                 "steering": null}
   }
   ```

   `split` holds the same parts as `_split` (with `"agents"` when it has a figure), the `usd` of
   each already apportioned in cents (`apportion`), so they add up to the total exactly. `drivers`
   is empty where Drivers cannot be told from workers (`measured` false in `cost_summary`, Copilot).
   `outside.grill` is the `GRILL_OUT` part of `_Chief` (`commands/cost/sessions.py`) and
   `outside.steering` its `STEER_OUT` part, set in a Foreman batch and `null` in a direct one.
   `outside` is `null` when the Chief of Staff's session cannot be measured (`_chief_unknown`'s
   causes), with a `"outside_unknown": "<cause>"` beside it; never a $0.00. The exact key names are
   the Driver's; the content is this.
2. **`cost_summary` and `chief_line` print from it**, so the Markdown lines and the JSON never
   disagree: the split, wakes and Driver lines of `cost_summary` are built from this data, and
   `chief_line`'s grill and steering figures come from a structured reading of `_Chief` that both
   the text lines and the receipt use. The text they print does not change by one byte (the
   scenario's `batch-NN.md` checks and `cost --summary` stay as they are).
3. **`close` records it.** `close_archive._close_files` adds the receipt data to the record as
   `cost_receipt` (through `history.close_record`), from the same rows it already prices once
   (`Closing.rows`). `core/batch_records.blank_record` gains `"cost_receipt": null`, so a running
   batch's record (`open_record`) and a back-filled one carry the key empty. `SCHEMA` stays 1: the
   key is added, and every reader uses `.get`.
4. **The board's live figure carries it.** `board/costs.py`'s `compute()` adds `"receipt"` (the
   same function, on the same rows; it also reads the Chief of Staff's transcripts, as `cost`
   does); `_failed()` and `Live.snapshot()`'s empty default carry `"receipt": None`. The board
   still records nothing.
5. **A closed record from before this change** (`cost_receipt` missing or `null`, `state`
   closed) shows a receipt with what it has: the head, the total, the budget, the per-CR detail
   and its sum; in place of the Steering and Drivers groups and the split, one muted line, "roles
   not recorded for this batch". Nothing is back-filled, no figure is guessed from the Markdown.
6. **A running or paused batch with no usable live figure** (Q10: never computed, still
   computing, or failed) shows the same head (its real state in the pill), total, budget and per-CR
   detail; the Steering, Drivers and split lines each read "not computed yet", or the live error
   (`live.error`, as `_failed()` gives it) when the last computation failed, and the receipt holds
   a Recompute button there (`data-recompute`, the same action as the age line's, disabled while
   computing). "roles not recorded for this batch" never shows for a running or paused batch.

Money words follow the board's existing rules: a figure with calls of an unpriced model reads "at
least $X"; an unknown one reads "unknown", never $0.00; a missing one reads "—" (`format.usd`).

## 2. The receipt (web)

In `skills/chantier/scripts/cli/src/chantier/board/web/`:

- **`js/views/costs-receipt.js`** (new): the receipt's markup, `receipt(view)` built with `html`
  from `core/dom.js`, from one plain object (below). No `fetch`, no `localStorage`, no inline
  style: the split bar's widths go through `vars()` / `data-vars` as `costs-tables.js` does for its
  bars. The barcode and the cut line are CSS only and `aria-hidden`. The `<section>` has
  `aria-label` "Cost receipt for <batch>". Its Recompute button (section 1, point 6) is bound by
  `costs.js`'s existing `delegate(root, 'click', '[data-recompute]', ...)`.
- **`js/model/receipt.js`** (new, pure, no DOM): builds that object from the store's data for the
  batch the page shows (section 4): the running or paused batch (`data.batch`, with `withLive`'s
  figures and the live `receipt`), or the last closed batch's record in `data.history`
  (`cost_usd`, `budget_usd`, `crs`, `cost_receipt`, `opened`, `closed`, `mode`, `steering`,
  `state`). It tells the three cases apart: figures present; running or paused without a usable
  live figure ("not computed yet" or the error); closed without `cost_receipt` ("roles not
  recorded"). The Driver type is shown without a `<plugin>:` prefix ("cr-driver"); no role name
  is written in the board's code.
- **`js/model/live.js`**: `withLive` also lays the live `receipt` on the running batch
  (`batch.cost_receipt`) when the live figure is usable, as it does for `spent_usd`.
- **`css/views/costs-receipt.css`** (new, linked in `index.html` after `costs.css`): the ticket as
  in `prototypes/01-mockups/final-costs.html` (`.ticket` and what follows it there): warm paper with its faint
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
  CR, Earlier batches with today's unfold, Last merged), and the four figures' labels and
  sub-lines follow the approved mock-up `prototypes/01-mockups/final-costs.html`, the delivery reference:
  - Spent: the label "Spent, <batch>"; the sub-line "closed, <duration>" for a closed batch
    ("closed, 10 h 56 min"), "running, <duration so far>" while it runs, "paused, <duration so
    far>" while it is paused; the budget gauge stays under it when a budget is set, as today.
  - Budget: the budget or "none"; the sub-line "$X outside it (grill, specs)", X the receipt's
    Outside-the-budget figure (its two parts summed in a Foreman batch), in the money words of
    section 1 ("unknown" when the Chief of Staff's session cannot be measured, "—" on a record
    with no `cost_receipt` or a running batch with no usable live figure). The share used moves
    to the receipt's foot (section 1).
  - Sum of the CRs: as today; its sub-line follows Q8: "the rest: steering and agents outside a
    CR", or only the part that has a figure when the receipt's data tells it ("the rest:
    steering").
  - Average per CR: the label without "active" (today "Average cost per active CR"); sub-line as
    today, "N CRs with a cost".
- **On a phone** (under `max-width: 760px`), as `prototypes/01-mockups/final-costs-phone.html` does, and only
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
  parts, Total, Budget, none, Average per CR, Outside the budget, "grill and specifications",
  "Chief of Staff, steering", "N calls", "Detail · per CR", "Sum of the CRs", the rest's line and
  its two part names, "N wakes · context M tokens on average", "roles not recorded for this
  batch", "not computed yet", the thank-you line, the state pill with closed, running and paused,
  "final, recorded at close") is a `costs.receipt_*` key (or `costs.*` for the cards) in each
  language file under `js/i18n/` (`en.js` and `fr.js`), the same keys in each; the cards' changed
  words (`costs.spent`, `costs.avg`, `costs.rest`, and the new Spent and Budget sub-lines) change
  in both files alike.
- Each file stays within CONTRIBUTING.md's targets (300 lines a file, 50 lines and complexity 10 a
  function): the receipt is its own module, not more lines in `costs.js`.

## 4. Which batch the page shows (Q3, Q4) and the thank-you line (Q5)

- **The batch shown** (Q3): the running batch (`data.batch`, running or paused); with none, the
  last closed one, the newest record of `data.history` whose `state` is `closed`. Today, with no
  batch running, the page shows "no batch" and the history; now it shows that last closed batch.
  With no batch running and no closed record, the page keeps today's "no batch" and the history.
- **The whole page follows the batch shown**, so the cards give the same information as the
  receipt (Q2): the receipt, the four figures and Per CR. For the last closed batch they read its
  record (Per CR shows its `result` and `rounds` in the State column), and the age line says
  "final, recorded at close" with no Recompute button (a closed record is final; the live figure
  prices only the running batch).
- **No batch chooser** (Q4): Earlier batches stays as it is today (`costs-history.js`, a row
  unfolds its CRs, `historyOpen` in the store); a click on a row does not change the batch shown.
  Choosing another batch is its own CR (Out of scope).
- **The thank-you line** (Q5): "thank you · N PRs", N the CRs of the batch with `result ==
  "merged"` and a `pr` recorded (not null): a dropped CR also records its `pr`
  (`history.cr_entry`), so a PR alone does not count. For the running or paused batch, the CRs
  whose state is merged and that have a `pr`. There is no "· 0 reverted": no record says whether a
  PR was reverted, and no figure is made up.

## 5. Docs

- `docs/web-board.md`, "### Costs": rewritten for the receipt, its place on a desktop and a phone,
  what it prints, which batch the page shows, "not computed yet" on a running or paused batch,
  and "roles not recorded" on an older closed record.
- `docs/web-board/costs-pc.png` and `costs-phone.png` redone with `just docs-screenshots`. The
  demo surface (`docs/demo/`) gains a `cost_receipt` in
  `projects/mobile-app/changes/5-archives/batches/batch-02.json` (made-up figures that add up) so
  a screenshot shows a full receipt; the Driver chooses whether the Costs capture
  (`scripts/docs_screenshots.py`, `views()`) moves to `mobile-app` or keeps `shop-api` (whose
  running batch has no transcripts, so no live receipt figures), and says which in the PR.
- `docs/costs.md`: one line that the batch's record keeps the receipt's figures
  (`cost_receipt`) from `close` on.

## Out of scope

- Choosing another batch on the Costs page (Q4): its own CR, aligned with `board-batch-view`'s
  previous/next navigation. The Chief of Staff files it; this CR neither adds a chooser nor
  changes Earlier batches.
- Any other page's look: `board-visual-refresh` restyles every view, the Costs cards included.
  This CR builds the receipt and the page's two-column layout, in that CR's accent and font.
- Back-filling `cost_receipt` into the records of batches closed before this change (Q6).
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
the Recompute note on a phone, stated once here, in section 3.

Order (Q7): this CR goes after `board-visual-refresh`, stacked on it in the same batch; the CR's
`depends.json` names `board-visual-refresh` (the Chief of Staff writes it). A Driver who finds
those tokens absent stops and says so; it does not invent a colour.

## Evidence

- **pytest** (`just test`, kept fast, in the existing cost tests, parametrized): the receipt
  function on prepared rows gives a split whose parts add up to the total in cents, a Steering
  line with wakes and average context, one Driver line per type sorted by cost; with no parent
  link (Copilot rows) no Driver line and an `agents` part; with the Chief of Staff not measured,
  `outside` null and its cause, never 0; in a direct batch `outside.steering` null, in a Foreman
  batch both parts set. And `cost_summary`'s and `chief_line`'s lines are the same text as before
  for the same rows (one case whose expected lines are written out).
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
  SHA; one of a closed record with no `cost_receipt` ("roles not recorded"); and one of a running
  or paused batch with no live figure ("not computed yet" and the receipt's Recompute). Differences
  from the mock-up are listed in the PR body, each with its reason.

No CI job is added or changed.

## Questions for the user

None. The Chief of Staff settled the last one (2026-11-17), following Q9's "(Foreman batch)": in a
direct batch the outside-the-budget cell shows the grill and specifications line only
(`outside.steering` null); the Chief of Staff's calls outside its steering window stay in
`batch-NN.md` alone, as `chief_line` prints them today.
