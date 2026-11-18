## Summary

On the web board's Costs page, the receipt of a running batch looked like the receipt of a closed one: only a small teal pill said "running". A batch that is not closed now carries a red stamp, set at an angle on the ticket, reading "NOT FINISHED" (English) or "PAS FINI" (French), so a live receipt is not taken for a final one. The stamp is part of the ticket, so "Copy as image" carries it too. A closed batch's receipt is unchanged.

## Deliverables

- The stamp shows whenever the shown batch's state is not `closed` (running, paused, closing): a double red border, bold capitals, tilted about 12 degrees, slightly translucent, in the ticket's upper half, inside the ticket's box, so it is neither clipped on the page nor in the copied image.
- Its words are in the dictionaries (`costs.receipt_stamp`), as real text rather than CSS content, so a screen reader and the image read the same words.
- Its look is a new sheet, `costs-stamp.css`, built on the design tokens; only the tilt, the ink opacity and the border width are declared as custom properties of the stamp.

Stamped receipt of a running batch, Costs page, at a45b214:

![The running batch's receipt with the red NOT FINISHED stamp](./shop-api-pc-en.png)

The receipt of a closed batch, no stamp, at a45b214:

![The closed batch's receipt, unchanged](./mobile-app-pc-en.png)

The copied image of the stamped receipt ("Copy as image" on a 127.0.0.1 address), the stamp whole and red, at a45b214:

![The copied PNG of the stamped receipt](./copied.png)

French at phone width, "PAS FINI", at a45b214:

![The French receipt at phone width](./shop-api-phone-fr.png)

## Blast radius

Grade: 1. Local to the Costs ticket's markup and one new sheet; `git revert` restores the previous board.

## Autonomous decisions

- The phone width keeps the desktop's 4 px border (no spacing token gives 3 px): the stamp stays tokens-only rather than shrinking its border.

## Known gaps

- The closed receipt is shown for the latest record only, not for an older record reached with the navigator's previous button.

<details>
<summary>Details</summary>

## Changes

- `js/views/costs-receipt.js`: `stamp(r)` returns nothing for a closed batch, else a `.stamp` element, placed first inside the `.ticket` section.
- `js/i18n/en-costs.js`, `fr-costs.js`: `costs.receipt_stamp` ("NOT FINISHED", "PAS FINI").
- `css/views/costs-stamp.css` (new), linked in `index.html` and listed in `costs-image.js`'s `SHEETS`, so the copied image draws it.
- `docs/web-board.md`: one sentence in the Costs section.

## Impacts

The receipt of a running or paused batch shows the red stamp; a closed batch's receipt looks as before.

## Test plan

- [x] No behaviour change in the server or the record; no new test (the sheet length cap in `tests/test_code_targets.py` still passes).
- [x] Local gates carried from `a45b214`: `just check` pass, `just eval-dry-run` 17 of 17 cases as expected
- [x] Evidence: the stamped receipt, the closed receipt and the copied image at `a45b214`, in a real Chromium on the demo, English and French, desktop and phone width
- [x] Review: approved carried from `a45b214`
- [x] Verified carried from `a45b214`
- [x] CI green at `a45b214`: all five jobs pass

## Internal references

CR-339 "costs-receipt-not-finished-stamp", batch-24.

</details>
