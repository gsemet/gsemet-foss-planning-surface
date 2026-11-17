## Summary

The web board's Costs and Batch pages only showed the running batch, or the last closed one. This change adds a batch navigator (previous, next, "Latest") to both pages, lets the Costs receipt be copied to the clipboard as an image, makes a closed batch's dependency graph readable from its record, and spells out "Change Request" in the receipt's per-CR heading.

## Deliverables

- Navigator in the page header, next to the title: `‹ batch-04 ›` plus a "Latest" pill shown only when the page is not on the latest batch. The chosen batch is in the address (`&b=batch-04`), so a link opens the same batch; it is kept between Costs and Batch and cleared on any other view.
- Closed batches record each CR's `order` and `after` list at close (checked by the scenario's close step, green in CI at `carried from 643b29c`; the browser run used copied records); the Batch page draws a closed batch's graph from it. For older batches, dependencies are recovered from the archived CR folders where possible, and the page says when they are partial or absent.
- "Copy as image" button on the Costs page: the ticket is rendered to a PNG (SVG `foreignObject` on a canvas, no third-party code) and put in the clipboard. It needs a secure origin; elsewhere the button is greyed with a tooltip linking to the board's 127.0.0.1 address, which the board now prints on a second line (`on this machine: ...`) and returns as `local_url` in `api/board`.

```text
board command line:  board on <LAN link> over <folder>
                     on this machine: http://127.0.0.1:<port>/?k=<key>
```

The image copy uses a `data:` image source (`img-src 'self' data:`), proven in Chrome. **UNVERIFIED:** the copy in Edge and Firefox.

Screenshots from Chrome on `127.0.0.1`, at `carried from 643b29c`, over a scratch copy of past batch records:

![The Costs page on a past batch: navigator, Latest pill, receipt and the Copy as image button (carried from 643b29c)](./04-costs-past-batch-pill.png)

![The receipt of a record with no dates, batch-01: no duration shown (carried from 643b29c)](./05-costs-batch-01-receipt.png)

![The Batch page of a closed batch, drawn from its record (carried from 643b29c)](./06-batch-page-closed-graph.png)

## Blast radius

Grade: 2. The closed record gains two keys per CR (additive), the board's CSP gains one image source, and the board's start prints one more line. Revert is a plain `git revert`; records already written stay valid.

## Autonomous decisions

- The new tests of `recovered_after` and `local_url` live in a new test file, to keep `test_board.py` under the project's line limit.
- A closed batch row's folder name drops the archive's date stamp.
- `crumbs()` was split into a helper to satisfy the complexity lint.
- With no live batch and no `b`, the Batch page shows the newest closed record; `after` lists are de-duplicated in `recovered_after`; closed-record graph nodes are focusable.

## Known gaps

- The image copy is proven in Chrome only (it works with a `data:` image source; a `blob:` source fails there with a tainted canvas, so `img-src` allows `data:`). Edge and Firefox are not installed on the machine that ran the proof, so they are untried.
- A live batch and the tooltip's hover were not exercised in the browser run; the run used closed batches.
- A record with no mode and no steering (batch-01) shows a lone "," in the receipt's head box.
- The copied image has a transparent strip of about 50 px under the receipt's scalloped edge.

<details>
<summary>Details</summary>

## Changes

- `board/web/js/model/history.js`: `batchSequence`, `recordRows`. `router.js`, `store.js`: the `b` part of the address. `ui/batch-nav.js`, `css/batch-nav.css`, `main.js`, `index.html`: the navigator.
- `model/receipt.js`, `views/costs.js`, new `views/costs-image.js`: the chosen batch and the image copy. `views/batch.js`, `batch-graph.js`, `ui/header.js`: a closed batch on the Batch page.
- `history.py`: `order` and `after` per CR at close. New `board/archived.py`: `recovered_after`. `board/address.py`, `command.py`, `routes.py`, `reply.py`: the 127.0.0.1 link and the CSP source.
- Docs: `docs/web-board.md`, `docs/costs.md`, `docs/planning-folder.md`, `session-start.md`; the scenario's close check.

## Human decisions

- The navigator is two arrows around the batch id and a "Latest" pill, in the page header; the chosen batch is in the address.
- The image copy needs a secure origin (127.0.0.1 or localhost); elsewhere the button is greyed out, with no download and no other replacement.
- A past batch keeps its CRs' order and dependencies, recorded at close; for batches closed earlier, only what the archives still give is used, and the page says where nothing is known.
- The board prints a second, 127.0.0.1 link next to the LAN one, since the LAN link is plain http.

## Impacts

Users see the navigator on Costs and Batch and the copy button; the receipt's heading reads "Detail · per Change Request".

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just check` at `carried from 643b29c`: pass on the three systems in CI
- [x] Evidence: screenshots from a browser on 127.0.0.1 at `carried from 643b29c`, in Deliverables
- [x] Review: approved at `carried from 643b29c`
- [x] Verified at `carried from 643b29c`
- [x] CI green at `carried from 643b29c`: `just check` (3 systems), `just eval-dry-run` and `just scenario` (ubuntu-latest, the long gate) pass

## Internal references

CR-327 board-batch-navigator.

</details>
