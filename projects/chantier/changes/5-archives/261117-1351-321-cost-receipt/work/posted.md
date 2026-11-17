## Summary

The web board's Costs page showed the batch's cost as a few cards and tables, with no view of where the money went (steering, Drivers, workers, work outside the budget). This PR adds a supermarket-style receipt: the lines, then a cut line and the total, ending with a per-CR detail. On a desktop it stands on the left, with today's cards on its right; on a phone it is on top, the cards below. The batch's closing now also records these figures in its JSON record so the board does not parse Markdown.

## Deliverables

Desktop, at `89d43b1` (left: the approved mock-up; right: the real page):

| Mock-up | Page |
| --- | --- |
| ![Mock-up, desktop](https://github.com/user-attachments/assets/2e6a5b3b-2d62-4f62-b246-9790968725f1) | ![Costs page, desktop, at 89d43b1](https://github.com/user-attachments/assets/393398d9-c8c7-4dd3-8417-2e0a728d7df1) |

Phone, at `89d43b1`:

| Mock-up | Page |
| --- | --- |
| ![Mock-up, phone](https://github.com/user-attachments/assets/61132270-47b2-4365-88bf-8e4c7938aa2a) | ![Costs page, phone, at 89d43b1](https://github.com/user-attachments/assets/91cc840a-bcc0-46e1-9e32-cd42dc076c88) |

An older closed record with no recorded receipt ("roles not recorded for this batch"), at `89d43b1`:

![Costs page, older record, at 89d43b1](https://github.com/user-attachments/assets/a495fb41-b714-4a4f-b0bb-b6db742d798f)

A running batch with no live figure ("not computed yet", with Recompute), at `89d43b1`:

![Costs page, not computed yet, at 89d43b1](https://github.com/user-attachments/assets/8eafd65c-8357-4388-a893-0255b6eb889f)

```text
close  -> batch-NN.json: "cost_receipt": {steering, drivers, split, outside}
board  -> GET costs: live.receipt (same function, same rows)
web    -> model/receipt.js -> views/costs-receipt.js (+ css/views/costs-receipt.css)
```

Choices: one ticket in the board's accent (three shades) and Inter font; the cards stay and give the same information; the page shows the running batch, else the last closed one.

## Blast radius

Grade: 2. A new key in the batch record and a rewritten Costs page; `cost`, `cost --summary` and `batch-NN.md` print the same text as before. Revert restores the old page; records already written keep an unused key.

## Autonomous decisions

- The receipt function lives in a new `commands/cost/receipt.py`, as `breakdown.py` is over the 300-line target.
- The Costs words moved to `en-costs.js` and `fr-costs.js` for the same reason; the words test reads both files of a language.
- The docs' Costs capture moved from the `shop-api` demo project to `mobile-app`, whose closed batch carries a made-up `cost_receipt` (the `shop-api` running batch has no transcripts, so no live figures).
- Differences from the approved mock-up: the Steering line reads "Foreman" in a Foreman batch (the mock-up shows a direct batch, "Chief of Staff"); the Outside-the-budget cell has two lines, "grill and specifications" and "Chief of Staff, steering", each with its calls, where the mock-up has one; the Steering label is cut at its first comma on the ticket; the mock-up's unused cards are not reproduced; the Sum card's "rest" sub-line is blank when the rest is zero.

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `commands/cost/receipt.py`, `breakdown.py`, `sessions.py`: structured receipt figures; the Markdown lines are rendered from them, unchanged.
- `closing.py`, `close_archive.py`, `core/batch_records.py`: `close` records `cost_receipt`; a new record carries `null`.
- `board/costs.py`, `js/model/live.js`: the live figure carries `receipt`.
- Web: `receipt.js`, `costs-receipt.js`, `costs-receipt.css`, two-column `costs.js`/`costs.css`, phone fold of the Per CR table.
- Docs, demo data, scenario checks and `tests/test_cost_receipt.py`.

## Human decisions

- One modern ticket, with today's cards kept beside it.
- The page shows the running batch, else the last closed one; no batch chooser here.
- Older closed records show "roles not recorded for this batch"; nothing is back-filled.
- The thank-you line counts merged CRs with a PR.

## Impacts

The Costs page looks different on desktop and phone; batch records gain `cost_receipt`.

## Test plan

- [x] New or changed tests: `tests/test_cost_receipt.py`, scenario checks
- [x] Gates at `89d43b1`: `just check` (394 passed) locally; `just scenario (ubuntu-latest)` and the three `just check` jobs green in CI
- [x] Evidence: after at `89d43b1`, beside the mock-ups
- [x] Review: approved at `89d43b1`
- [x] Verified at `89d43b1` (claims 1-5 and 7 carried from `0664a69`)
- [x] CI green at `89d43b1`

## Internal references

CR-321 cost-receipt; depends on the board visual refresh CR (CR-319).

</details>

