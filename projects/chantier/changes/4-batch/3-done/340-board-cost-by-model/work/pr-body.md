## Summary

The board's Costs page showed what a batch cost in total and by kind of agent, but not where the money went by model. This adds a "Where the money went" card to the page: one stacked bar from $0 to the batch's budget, one coloured segment per model with the unspent rest hatched, and one row per model (colour swatch, the provider's logo, name and version, turns, cost). A switch at the card's top right shows the same card by role. The Chief of Staff's spend outside the budget is one grey row under the models, with no segment in the bar. From now on `close` records the per-model figures in the batch's record; a batch closed earlier shows "not recorded for this batch".

## Deliverables

The card, by model (default) and by role, for the batch the page's navigator shows:

```text
Where the money went                          [ by model | by role ]
$X of the budget left unspent
[ Opus ][ Sonnet ][ Haiku ]////// hatched rest //////
$0                                                    Budget $B
[swatch] [logo] Claude  Opus 5.5        12 turns      $4.20
...
------------------------------------------------------------
[grey]  Chief of Staff, outside the budget  ...        $1.10
```

Before at the base `a45b214` (the Costs page without the card), after at `e323364`:

![Before: the Costs page without the card](./verifier/evidence/before-costs-pc.png)
![After: the card by model, in the Costs page](./verifier/evidence/after2-card-pc.png)
![The card by role](./verifier/evidence/after2-card-role-pc.png)
![The card at phone width](./verifier/evidence/after2-card-phone.png)

Choices:

- One colour per model from a fixed eight-colour palette in cost order, so two models of one family stay apart; the swatch and its segment share a colour.
- Logos for Anthropic (Claude), OpenAI (GPT), Google (Gemini) and xAI (Grok); any other model shows its exact id with no logo, never a guessed one.
- Over budget: no hatch and a thin mark at the budget; no budget: the bar spans the spend. Calls with no price make the line say "at least" or "at most", never a made-up figure.
- The Chief of Staff row reads "unknown" when it cannot be measured, never $0.00.

Data shape (additive, in the batch's record):

```text
cost_receipt.models: [{model, calls, usd, unpriced}]   sorted by usd, adding up to the total
cost_receipt.split.<part>.calls                         priced calls of that kind
```

## Blast radius

Grade: **1**. The new fields are additive, no older record is rewritten, and the new card is a separate view; a `git revert` restores the previous page and receipt.

## Autonomous decisions

- The switch (`.seg`) did not exist yet, so its styles are defined in the card's stylesheet.
- The card's radius uses the existing 9 px radius token, as there is no 10 px token.
- French strings equal to their English ones, for the design glossary: `costs.money_zero` ("$0") and `costs.money_axis_budget` ("Budget {x}").

## Known gaps

- The refreshed `docs/web-board/costs-phone.png` shows only the receipt ticket: the card sits below the first screen at phone width, so that published picture does not show it (the phone capture above does).

<details>
<summary>Details</summary>

## Changes

- Cost code: `costs/transcripts.py` and `costs/copilot.py` keep `by_model` per row; `commands/cost/receipt.py` and `breakdown.py` add `models` and per-part `calls` to `cost_receipt`.
- Board: `model/models.js` (id to provider, name, version), `model/spend-by.js`, `views/costs-models.js`, `ui/logos.js` (marks vendored from Lobe Icons, MIT, licence beside them), `css/views/costs-models.css`, palette tokens, the `spendBy` store field and the French and English words.
- Docs: `docs/web-board.md`, `docs/costs.md`, the demo's `batch-02.json`, and the refreshed `docs/web-board/costs-pc.png` and `costs-phone.png`.
- Scenario: the close step also checks `models` and the parts' `calls`.

## Human decisions

- The card lives on the Costs page and follows the batch of the page's navigator; by model by default, a switch for by role.
- The bar spans $0 to the budget with the unspent rest hatched.
- Everything is counted in the bar; the Chief of Staff's spend is one grey row outside it.
- Real provider logos from Lobe Icons, vendored as inline SVG with their licence; unknown models show their exact id.
- No backfill: older batches show "not recorded for this batch".

## Impacts

The Costs page gains the card; the receipt ticket and the other cards are unchanged.

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_cost_receipt.py`, `tests/test_cost_copilot.py`, `tests/test_costs.py`
- [x] Local gates carried from `e323364`: `just check` (476 passed), `just eval-dry-run` (17 of 17 as expected)
- [x] Evidence: before at `a45b214`, after at `e323364`
- [x] Review: approved carried from `d4d4d67`
- [x] Verified carried from `e323364`
- [x] CI green at `abcc959`

## Internal references

- CR-340 board-cost-by-model; stacked on the Costs receipt stamp change.

</details>
