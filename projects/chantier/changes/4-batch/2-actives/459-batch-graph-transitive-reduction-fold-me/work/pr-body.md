## Summary

On a real batch, the board's Graph tab is hard to read. Every declared wait is drawn as a long arrow, although most are already implied by a chain of other waits. The merged CRs take most of the columns while the few CRs in flight are what matter. The cards within a level are not ordered to avoid crossings. And the levels are a fixed 300px wide, so with the PR side panel only two and a half levels fit and the graph scrolls sideways.

This PR draws only the transitive reduction of the waits, folds the merged and cancelled CRs behind one "N merged" chip, orders the cards within each level to reduce crossings, and lets the levels share the central column's width. It touches the web client only, in English and French; the Gantt, the server, the protocol and the CLI are unchanged.

The design notes (`DESIGN.md`), the demo data, the `docs/web-board.md` paragraph and the committed docs picture are updated with it.

## Deliverables

- **Fewer arrows.** `reducedEdges(rows)` in `js/model/semantics.js` keeps a wait only when no other chain of waits among the drawn CRs implies it. A hover still lights every declared wait's card, and a card's wait count names all of them in its `title` ("Waits for CR-435, CR-438, ..."), so a hidden wait stays discoverable.
- **Fold chip.** On a live batch with both done and open CRs, the merged and cancelled CRs are folded by default behind a toggle chip above the graph ("12 merged", plus "· 1 cancelled" when relevant). Clicking it (or Enter/Space) unfolds them back into their levels. A closed record is never folded.
- **Crossings.** `orderLevels(cols, pairs)` sorts each level by a deterministic three-pass barycentre (down, up, down) of the drawn arrows; ties keep the record's order.
- **Fit.** Levels use `flex: 1 1 0` between 180px and 300px with a 30px gap and share the column; the box scrolls sideways only when they cannot fit. Both SVG layers are measured from zero at each draw, so the canvas is as tall as the tallest level and no taller. Below 240px a level shows the state badge as an icon only (the word stays in its `title`).

```js
// js/model/semantics.js
export const reducedEdges = (rows) => /* edges(rows) minus the pairs implied by a chain; a cycle returns edges(rows) whole */;
export const orderLevels = (cols, pairs) => /* same CRs per level, reordered by barycentre */;
```

Choices made: the fold resets at each page load; cancelled CRs fold with the merged ones; the Gantt keeps every declared wait.

Measured in a browser (Playwright, 1600 x 900 window with the PR panel, the demo batch, `work/evidence/measures.json`): the folded graph is 518 px high against 661 px unfolded, 886 px wide in both with no sideways scroll, the chip reads "1 merged", and the levels run in the order CR-142, CR-146, CR-144, CR-149 / CR-143, CR-147 / CR-145 / CR-148, the same after a reload. Folding and unfolding again returns to 518 px; Enter on the chip unfolds it.

![The batch graph, folded, with the reduced arrows](https://github.com/gsemet/chantier/blob/a2a083af9e92e5949c683fae754752999b542618/docs/web-board/batch-graph-pc.png?raw=true)

## Blast radius

Grade: 1

Web client only (one model file, two views, two stylesheets, the two language files, one test); a plain revert restores the previous graph. The Gantt still reads every declared wait.

## Autonomous decisions

- The fold is not remembered across reloads: a per-device preference would add stored state for a view that is quick to toggle.
- Cancelled CRs fold with the merged ones, so the chip counts both.
- Below 240px the state badge keeps only its icon so four levels fit at a 1600px window.
- The Gantt is left unchanged rather than drawing the same reduction.
- On a cycle among the waits, the reduction returns every wait rather than risk dropping both sides of a pair.

## Known gaps

- No "before" picture of the base was taken: the screenshot shows the new graph only.
- At 1400 to 1600 px wide, some cards' state badges are clipped at the card's right edge. The specification does not cover it, and a sideways scroll at 1400 px was accepted.
- The long gate (`just scenario`) runs in CI; it was not run locally.

<details>
<summary>Details</summary>

## Changes

- `js/model/semantics.js`: new `reducedEdges` and `orderLevels`; `edges`, `levels` and `related` unchanged.
- `js/views/batch-graph.js`: `unfolded` flag and exported `toggleFold()`; `foldBar` builds the chip (`data-fold`, `aria-expanded`); `graphBlock` draws `orderLevels(levels(shown), reducedEdges(shown))`; `drawEdges` draws the reduction of the CRs present in the DOM and zeroes both SVG layers before measuring; `deps` gets the "Waits for ..." title; `badge` wraps the state word in `.sbw` and adds a `title`.
- `js/views/batch.js`: a `[data-fold]` click handler calls `toggleFold()` then re-renders.
- `css/views/batch-graph.css`: `.graph` gap and `min-width: min-content`; `.lvl` flex sizing and a `graph-level` container; `.gbar`; phone keeps 250px levels.
- `css/components/chip.css`: `@container graph-level (max-width: 239px)` hides `.sbw`.
- `js/i18n/en.js`, `js/i18n/fr.js`: keys `batch.fold_merged`, `batch.fold_cancelled`, `batch.fold_show`, `batch.fold_hide`, `batch.waits_for`; `batch.arrow` now says an implied wait is not drawn.
- `DESIGN.md` (web client), `docs/web-board.md`, `docs/web-board/batch-graph-pc.png`, and the demo batch data (a later wait added to its last CR): the new graph described and pictured.
- `tests/test_board_graph_arrows.py`: one new test reading the shipped files.

## Human decisions

- Draw only the transitive reduction of the waits; the hidden waits must stay discoverable (hover, the card).
- Fold the merged CRs behind a chip "N merged" that expands.
- Order the cards within a level to reduce crossings, with a simple barycentre pass.
- Fit the graph to the width (no sideways scroll for a normal batch at desktop width, the side panel considered), with the canvas height following its content.

## Impacts

On a live batch the Graph tab opens folded, with fewer arrows, ordered levels, no horizontal scroll at a wide window, and no empty canvas below. The hint line about arrows now says implied waits are not drawn. The docs picture shows it.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_the_graph_draws_the_reduction_folds_the_done_and_fits_the_column`
- [x] Local gates at `a2a083a`: `just check` passed (1883 passed; one known Windows flake, `test_w2_a_shell...`, passed on rerun); `just eval-dry-run` passed
- [x] Evidence: Playwright measures at 1600 x 900 in `work/evidence/measures.json`, and the docs picture
- [x] Review: approved at `dce2c644` (diff), `d5ef37f3` and its lint diff (`a2a083a`)
- [ ] Verified at `a2a083a`
- [ ] CI green at `a2a083a`

## Internal references

- CR-459 batch-graph-transitive-reduction-fold-merged-fewer-crossings (batch-30), two rounds done.
- Specification: `03-change-spec.md`; round notes: `work/coder/r1.md`, `work/coder/r2.md`; measures: `work/evidence/measures.json`.
- Commits: `1c3a4ef7` (feature), `d5ef37f3` (docs), `a2a083af` (lint fixes).
</details>
