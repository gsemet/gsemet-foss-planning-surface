# Change Specification: the board's Costs page shows where the money went, by model

## Goal

On the web board's Costs page, the user sees at a glance where a batch's money went, as in the
reference picture (`intake/reference.jpg`): a card titled "Where the money went", a switch at its
top right ("by model" / "by role"), one line "$X of the budget left unspent", one stacked
horizontal bar from $0 to the batch's budget (one coloured segment per model, the unspent rest
hatched), then one row per model: a colour swatch, the provider's logo, the model's name and
version, the number of turns and the cost. The Chief of Staff's spend outside the budget is one
grey row under the models, with no segment in the bar. The card follows the batch the page's
navigator shows (the latest by default, a past one when chosen). From now on `close` records the
per-model and per-role figures in the batch's record; a batch closed before shows "not recorded for
this batch".

## Decisions carried from `02-answers.md`

- money-Q1: on the Costs page, no new page. The card follows the batch of the navigator added by
  CR-327 (`‹ batch-n ›`, "Latest"; `state.batchId`, `shownBatch` in `model/receipt.js`): the
  latest by default, a past one when chosen.
- money-Q2: by model by default; a switch at the card's top right shows the same card by role.
- money-Q3: the bar spans $0 to the batch's budget, the unspent rest hatched; the line reads
  "$X of the budget left unspent". A batch with no budget: the bar spans the spend.
- money-Q4: `close` records the per-model and per-role figures in the batch's record from now
  on; a batch closed before shows "not recorded for this batch", as the receipt does.
- money-Q5: everything is counted. The batch's spend (Foreman or steering, Drivers, workers) makes
  the bar's segments; the Chief of Staff (steering and grill outside the budget) is one grey row of
  its own under the models, with no segment in the bar.
- money-Q6: columns as in the picture: colour swatch, provider logo, model name and version, the
  number of calls labelled "turns" (not "runs"), and the cost.
- money-Q7: the providers' real logos, as SVG icons, as in the picture.
- money-Q8: the marks are vendored from Lobe Icons (`lobehub/lobe-icons`, MIT, coloured, as in the
  picture) as inline SVG, with its licence file beside them and a docs line that the marks are their
  owners' trademarks.
- money-Q9: Anthropic (Claude, on both hosts; Copilot's Claude models show as Claude), OpenAI
  (GPT), Google (Gemini) and xAI (Grok) get a logo and a parsed name; any other model shows its
  exact id with no logo, never a guessed one.
- money-Q10: one colour per model, from a fixed palette in cost order (Opus and Sonnet stay apart
  in the bar).

## What the code has today (read 2026-11-17)

- The per-call model is known on both hosts. Claude: `costs/transcripts.py`, `_Scan._call` keeps
  each call's `model`; `_add` folds the calls into one row per agent and keeps only `models` (a
  set of ids), `model` (the last one) and `unpriced` (calls by model with no price); the dollars by
  model are lost. Copilot: `costs/copilot.py`, `_rows` reads each call record of
  `copilot-session-usage calls`, which carries `model` (see `tests/test_cost_copilot.py`), and
  drops it.
- `commands/cost/receipt.py`, `cost_receipt(d, rows, by_driver, chief)` builds the receipt's
  figures: `steering`, `drivers`, `split` (parts `steering`, `drivers`, `workers`, `agents` with
  `usd` and `unpriced`, apportioned in cents to add up to the total, from `split_parts` in
  `commands/cost/breakdown.py`; no calls), and `outside`/`outside_unknown` (from `chief_outside`
  in `commands/cost/sessions.py`: `grill`, and `steering` in a Foreman batch, each with `usd`,
  `calls`, `unpriced`; `outside: null` with the cause when the Chief of Staff cannot be measured,
  Copilot included).
- `cost_receipt` has two callers, so one change reaches both: `commands/closing.py`, `_closing`,
  which records it as `cost_receipt` in `5-archives/batches/batch-<n>.json` through
  `commands/close_archive.py`; and `board/costs.py`, `compute`, the board's live figure
  (`live.receipt`), laid over the running batch by `web/js/model/live.js`, `withLive`.
- The board serves the closed records as they are (`board/state.py`, `_history`), so a new field of
  `cost_receipt` reaches the page with no server change.
- The page: `web/js/views/costs.js` (`render`: the ticket on the left, the side column `.cside`
  with `ageLine`, `figures` (the kpis), `perCr`, `historyBlock`, `lastMerged`), the ticket in
  `views/costs-receipt.js`, the pure model in `model/receipt.js` (`receiptOf`, with `figures` one
  of `figures`, `pending`, `unrecorded`, `money`, `steeringName`), the words in
  `i18n/en-costs.js` and `i18n/fr-costs.js`, the styles in `css/views/costs.css` and
  `costs-receipt.css`, the page state in `core/store.js` (`batchId`, `copying`, `recomputing`).

## What changes

### 1. Per-model figures on each priced row (CLI, cost code)

- `costs/transcripts.py`: `_new_row` gains `by_model: {}`; `_add` adds, for each priced call,
  `by_model[model] = {"calls": +1, "usd": +sum(parts)}`. A call with no price stays in `unpriced`
  only (it already is by model). The grill sub-row (`row["grill"]`) gets the same field from the
  same code; nothing reads it.
- `costs/copilot.py`, `_rows`: each row gains `by_model`, fed from each call record's `model`,
  `llm_calls` (or 1) and `estimated_usd`. A call record with no `model` goes under the key `?`.
  Do not add a `models` key to Copilot rows: `"models" in r` is how the cost code tells a Claude
  row (`explain_line`, `_explain_notes`).
- Nothing else in the cost code changes; the `cost` command's text output is unchanged.

### 2. The receipt records the models and the roles' calls (CLI, `commands/cost/receipt.py`)

`cost_receipt` returns two more things; `close` records them and the board's live figure carries
them, through the existing callers, with no change to `closing.py`, `close_archive.py` or
`board/costs.py`:

- `models`: a list, one entry per model of the batch's spend rows (the rows `cost_receipt`
  already gets: the Chief of Staff's grill and specification agents are not in them),
  `{"model": <exact id>, "calls": <priced calls>, "usd": <dollars>, "unpriced": <calls with no
  price>}`, sorted by `usd` descending, then by id. The `usd` are apportioned in cents with
  `apportion` (largest remainder) so that they add up to the rows' total in cents, as `split`
  does. A model with only calls not priced has `calls: 0`, `usd: 0.0` and its count in
  `unpriced`; it is listed last.
- `split`: each part gains `calls` (the priced calls of that kind, from the same `breakdown`
  entries `split_parts` sums). The parts, their order and their `usd` do not change.

The new fields are additive: a record that holds `cost_receipt` without `models` is a batch
closed before this change. `close` never rewrites an older record.

### 3. The card on the Costs page (board, web only)

New files, each small and pure where it can be:

- `web/js/model/models.js` (pure): from an exact model id, `{provider, name, version}`:
  - `claude-<family>-<major>[-<minor>|.<minor>]`, the minor optional, then an optional trailing
    `-YYYYMMDD` and an optional trailing variant in parentheses (`-(fast-mode)`): provider
    `anthropic`, name "Claude", version "<Family> <major>[.<minor>]" and, with a variant,
    " (<variant with spaces for hyphens>)". Copilot's ids are in
    `playbook/copilot-models.json`.
  - `gpt-<version>[-<variant>]`: provider `openai`, name "GPT", version "<version> <Variant>"
    (`gpt-6.1-sol` gives "GPT 6.1 Sol").
  - `gemini-<version>[-<variant>]`: provider `google`, name "Gemini", version likewise.
  - `grok-<version>[-<variant>]`: provider `xai`, name "Grok", version likewise (money-Q9).
  - Any other id, and `?`: no provider, the exact id as the name (`?` reads "model not
    recorded"), no version, no logo. Never a guessed provider.
  The row's `title` attribute holds the exact id. The parametrized cases the function must meet:

  | id | provider | name | version |
  | --- | --- | --- | --- |
  | `claude-opus-5-5` | anthropic | Claude | Opus 5.5 |
  | `claude-sonnet-5-5-20261001` | anthropic | Claude | Sonnet 5.5 |
  | `claude-sonnet-5.5` | anthropic | Claude | Sonnet 5.5 |
  | `claude-opus-5` | anthropic | Claude | Opus 5 |
  | `claude-sonnet-5` | anthropic | Claude | Sonnet 5 |
  | `claude-fable-5` | anthropic | Claude | Fable 5 |
  | `claude-opus-4.8-(fast-mode)` | anthropic | Claude | Opus 4.8 (fast mode) |
  | `gpt-6.1-sol` | openai | GPT | 6.1 Sol |
  | `gpt-6-astra` | openai | GPT | 6 Astra |
  | `gemini-4-argon` | google | Gemini | 4 Argon |
  | `gemini-3.8-flash` | google | Gemini | 3.8 Flash |
  | `grok-4.7` | xai | Grok | 4.7 |
  | `mistral-large-2` | none | mistral-large-2 | none |
  | `?` | none | model not recorded | none |
- `web/js/ui/logos.js`: one inline SVG mark per provider (`anthropic` as the Claude mark,
  `openai`, `google` as the Gemini mark, `xai` as the Grok mark), trusted markup like
  `ui/icons.js`, copied from Lobe Icons (money-Q8): the coloured mark where Lobe Icons has one,
  else its mono mark drawn in the text colour (`currentColor`); sized to the row's text (about
  16 px). The vendored markup carries no `style=` attribute (`test_code_targets` refuses it): each
  colour of a mark is a token of `css/tokens.css` (for example `--logo-anthropic`), set through
  `fill="var(--...)"` or a class. A mark with a gradient gets its gradient `id` made unique per
  drawn instance (a counter suffix), since several rows or cards can draw the same mark on one
  page. Lobe Icons' MIT licence file sits beside it as `web/js/ui/logos-LICENSE.txt`, as
  `web/fonts/OFL.txt` sits beside the fonts; the file's header names the source, its version or
  commit, and, for each mark, the variant taken (coloured or mono).
- `web/js/model/spend-by.js` (pure): `spendBy(r, by)` from the object of `receiptOf` and the switch
  (`model` or `role`), returning `{state, line, span, budget, segments, rows, chief}`:
  - `state`: `figures` when the shown batch's `cost_receipt` holds `models`; `unrecorded` for a
    closed record without it (both views: the record has no per-model figures, and its `split`
    has no calls); `pending` and the live error as `receiptOf`'s `figures` and `note` say for a
    running or paused batch.
  - By model, the rows are the `models` entries; by role, the `split` parts, filtered as the
    ticket's `parts()` does (the `agents` part, on a host with no parent link, stands in place of
    `drivers` and `workers`), named as the ticket names them (`steeringName` of the steering label,
    "Drivers", "Workers", "Agents, Driver or worker not measured").
  - `segments`: one per row with dollars, in the rows' order, width `usd / span`; a segment of a
    few cents keeps a minimum visible width (2 px), as the picture's thin blue segment.
  - `span`: the budget; with no budget, or when the spend is over the budget, the spend.
  - `line`, in the board's money words (`money`, two decimals, "at least" with calls not priced):
    - within the budget: "$X of the budget left unspent", X = budget - total; with calls not
      priced, "at most $X of the budget left unspent" (the spend is a floor);
    - over the budget: "$X over the budget" ("at least $X over the budget" with calls not priced);
    - no budget: "No budget: $X spent".
  - `chief`: the grey row, from the receipt's `outside`: the label "Chief of Staff, outside the
    budget" with a small "grill and specifications" (and ", steering" when `outside.steering` is
    there, a Foreman batch), its turns (the parts' `calls` summed) and its cost (the parts' `usd`
    summed, "at least" with calls not priced). `outside: null` (Copilot, or no Chief of Staff
    transcript) reads "unknown" with no turns; a part with `usd: null` (calls without a time)
    reads "unknown" too. Never $0.00 for what is not measured. The same row in both views.
- `web/js/views/costs-models.js`: the card's markup from `spendBy`:
  - the head: the title "Where the money went" and, at its top right, the switch: the `.seg`
    segmented control, two buttons "by model" and "by role", the current one pressed
    (`aria-pressed`), keyboard reachable (board-design-realign, which lands after this CR, builds
    on that control);
  - the line, then the bar (`role="img"` with an `aria-label` that says the line), the hatched
    rest (CSS only, a repeating linear gradient as the picture's grey stripes) when the spend is
    under the budget; when it is over, no hatch and a thin vertical mark at the budget's position;
    under the bar, "$0" on the left and "Budget $B" on the right (with no budget, "Spent $S");
  - one row per model or role: the swatch (the segment's colour), the logo (by model only; the
    slot stays empty for a model with no provider), the name in the text colour and the version
    muted beside it (by role: the role's name, no version), "N turns" ("1 turn"), and the cost
    right-aligned, bold; a model not priced reads "not priced" in the cost cell;
  - the grey row under a thin rule, its swatch grey, no logo;
  - `unrecorded`: the head and the switch, then one muted line "not recorded for this batch";
    `pending`: one muted line "not computed yet" (or the live error), no Recompute button of its
    own (the page's Recompute is in `ageLine`).
- Colours: a palette of eight tokens `--m1`...`--m8` in `css/tokens.css`, given to the model rows
  in their order (by cost), cycling after eight, one colour per model (money-Q10); by role, the ticket's shades `d1`, `d2`, `d3`
  (as `SHADE` in `costs-receipt.js`); the Chief of Staff's row a neutral grey token. The swatch and
  the segment of a row always share one colour.
- `web/css/views/costs-models.css`, linked in `web/index.html` beside `costs.css`: the card as the
  picture (title, the `.seg` switch at the top right, the muted line, the rounded bar about 24 px
  high with 2 px gaps between segments, the axis labels, the rows separated by thin rules, tabular
  figures for turns and cost). To fit board-design-realign, it uses only the five type sizes
  (11, 12, 14, 16, 24 px, through their tokens), the radii 6 px, 10 px and full, and the spacing
  scale's tokens, a 2 px gap being the one value allowed outside it. It works at phone width (the
  row's version may wrap under the name; turns and cost stay on the row).
- `views/costs.js`, `render`: the card is the first card of the side column, right after the
  figures (`figures(r)`) and before the Per CR table, for every batch the navigator shows; with no
  batch (`r` null) there is no card. `mount` binds the switch with `delegate` on
  `[data-spend-by]`.
- `core/store.js`: one more field, `spendBy: 'model'`, the switch's choice, kept while the page is
  open (it stays when the navigator changes batch); not in the address, not saved across reloads.
- Words: every string above in `i18n/en-costs.js` and `i18n/fr-costs.js` (keys `costs.money_*`;
  French: "Où est passé l'argent", "par modèle", "par rôle", "tours", "$X du budget non
  dépensés", "non enregistré pour ce batch"...), with the `.one` forms for one turn. Each French
  value equal to its English one (for example "Claude", "GPT", "Gemini", "Grok", "$0") is listed
  in the PR's description for board-design-realign's glossary.
- The receipt (the ticket), its image copy and the other cards do not change.

### 4. Documentation and demo

- `docs/web-board.md`, "Costs": one paragraph on the card: by model by default, the switch to by
  role, the bar against the budget, the grey Chief of Staff row outside the budget, the line for no
  budget and over budget, and "not recorded for this batch" for a batch closed before this change;
  and one line that the providers' marks come from Lobe Icons (MIT) and are their owners'
  trademarks, shown only to name the provider (money-Q8).
- `docs/costs.md`: the paragraph on `cost_receipt` names the two new fields (`models`, and
  `calls` on each `split` part).
- `docs/demo/projects/mobile-app/changes/5-archives/batches/batch-02.json`: its `cost_receipt`
  gains `models` (two or three models, Claude and one other provider, adding up to the record's
  `cost_usd` within a cent) and `calls` on its `split` parts, so the demo shows the card; then
  `just docs-screenshots` refreshes `docs/web-board/costs-pc.png` and `costs-phone.png`. Leave
  the demo's other closed records as they are, so one shows "not recorded for this batch".
  `docs/web-board/costs-*.png` are regenerated by whichever of this CR and board-design-realign
  lands second, so the published pictures show both changes.

## Out of scope

- No new page and no history page (money-Q1).
- No `--by model` for the `cost` command's text, and no model figures in `batch-NN.md`, in
  `status`, in the CR board pane or in the receipt's image copy.
- No backfill: a batch closed before this change keeps its record; the card says "not recorded
  for this batch".
- No per-model split of the Chief of Staff's own spend: it is one grey row (money-Q5).
- No new server endpoint: the board serves the records and the live figure as today.

## Evidence

- `just test` (budget: AGENTS.md, at most 30 s above 18.5 s on the user's Windows machine; add no
  more than these, parametrized):
  - `tests/test_cost_receipt.py`: one parametrized test on prepared rows carrying `by_model`: the
    `models` entries are sorted by cost, their cents add up to the rows' total in cents, a model
    with only calls not priced is listed last with `calls: 0` and its `unpriced`; each `split` part
    carries its `calls`, and the parts' calls add up to the rows' priced calls.
  - `tests/test_cost_reading.py` (or `test_cost_copilot.py`): one case each that a Claude
    transcript with two models and a Copilot call list with two models give rows whose `by_model`
    holds both, with the right calls and dollars, and that a Copilot row has no `models` key.
- `just lint` (ruff, mypy, Biome on `board/web`) and `just check`, on Linux, macOS and Windows.
- `just scenario` (a CLI change; AGENTS.md's long gate): in `scenario/run_scenario.py`, the
  close step's check on `cost_receipt` (around "`batch-NN.json` keeps the receipt's figures")
  also requires `models` to be a non-empty list whose `usd` add up to `cost_usd` within a cent,
  each entry with `model`, `calls`, `usd`, `unpriced`, and each `split` part to carry `calls`; the
  `open` step's check that `cost_receipt` is `None` stays.
- By hand, on the board served on the demo (`just docs-screenshots` serves it; or `chantier
  board` on a copy of `docs/demo`): `models.js`'s cases of the table above, each checked from the
  browser's console against the served module (the board has no JavaScript test runner, and this
  CR adds none); on Costs, the latest closed batch-02 shows the card by model,
  the swatches matching the segments, the logos, "turns", the grey Chief of Staff row; the switch
  shows it by role and back; `‹` to an older record shows "not recorded for this batch"; the
  phone width keeps each row on one line for turns and cost. The refreshed `costs-pc.png` and
  `costs-phone.png` are the PR's Deliverables.
