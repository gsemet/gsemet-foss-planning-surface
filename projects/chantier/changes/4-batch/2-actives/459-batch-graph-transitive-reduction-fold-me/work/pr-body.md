## Summary

On a real batch, the board's Graph tab is hard to read. Every declared wait is drawn as a long arrow, although most are already implied by a chain of other waits. The merged CRs take most of the columns while the few CRs in flight are what matter. The cards within a level are not ordered to avoid crossings. And the levels are a fixed 300px wide, so with the PR side panel only two and a half levels fit and the graph scrolls sideways.

This PR draws only the transitive reduction of the waits, folds the merged and cancelled CRs behind one "N merged" chip, orders the cards within each level to reduce crossings, and lets the levels share the central column's width. It touches the web client only, in English and French; the Gantt, the server, the protocol and the CLI are unchanged.

This is the first of two planned rounds: the design notes, demo data, docs page and screenshots are not part of this head yet (see Known gaps).

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

Screenshots: none yet (see Known gaps).

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

- No browser check yet: the fold toggle, the container-query badge and the fit were not exercised in a browser. **UNVERIFIED:** the levels fit the column at a 1600 x 900 window with the PR panel, with no sideways scroll.
- No screenshot yet: the before/after pictures of the Graph tab (desktop and phone) are not attached.
- The design notes (`DESIGN.md`), the demo data, the `docs/web-board.md` paragraph and the committed docs picture are not updated yet; they come in the second round. The board's own docs still describe the old behaviour ("each CR stays in one place for its whole life").
- A local run of `test_board_ui.py::test_the_web_client_is_outside_the_servers_package...` failed, apparently only because the test environment (`uv run --project` on the main checkout) imports the main checkout's install rather than this worktree. **UNVERIFIED:** it passes in a clean environment.

<details>
<summary>Details</summary>

## Changes

- `js/model/semantics.js`: new `reducedEdges` and `orderLevels`; `edges`, `levels` and `related` unchanged.
- `js/views/batch-graph.js`: `unfolded` flag and exported `toggleFold()`; `foldBar` builds the chip (`data-fold`, `aria-expanded`); `graphBlock` draws `orderLevels(levels(shown), reducedEdges(shown))`; `drawEdges` draws the reduction of the CRs present in the DOM and zeroes both SVG layers before measuring; `deps` gets the "Waits for ..." title; `badge` wraps the state word in `.sbw` and adds a `title`.
- `js/views/batch.js`: a `[data-fold]` click handler calls `toggleFold()` then re-renders.
- `css/views/batch-graph.css`: `.graph` gap and `min-width: min-content`; `.lvl` flex sizing and a `graph-level` container; `.gbar`; phone keeps 250px levels.
- `css/components/chip.css`: `@container graph-level (max-width: 239px)` hides `.sbw`.
- `js/i18n/en.js`, `js/i18n/fr.js`: keys `batch.fold_merged`, `batch.fold_cancelled`, `batch.fold_show`, `batch.fold_hide`, `batch.waits_for`; `batch.arrow` now says an implied wait is not drawn.
- `tests/test_board_graph_arrows.py`: one new test reading the shipped files.

## Human decisions

- Draw only the transitive reduction of the waits; the hidden waits must stay discoverable (hover, the card).
- Fold the merged CRs behind a chip "N merged" that expands.
- Order the cards within a level to reduce crossings, with a simple barycentre pass.
- Fit the graph to the width (no sideways scroll for a normal batch at desktop width, the side panel considered), with the canvas height following its content.

## Impacts

On a live batch the Graph tab opens folded, with fewer arrows, ordered levels, no horizontal scroll at a wide window, and no empty canvas below. The hint line about arrows now says implied waits are not drawn. No screenshot yet (see Known gaps).

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_the_graph_draws_the_reduction_folds_the_done_and_fits_the_column`
- [ ] Local gates at `<sha7>`: partial run before the commit: board, sheet, component, token and design tests, 395 passed, 1 failed (environment, see Known gaps), 1 skipped; `just check` and `just eval-dry-run` not yet run
- [ ] Evidence: none yet (no browser run, no screenshot)
- [ ] Review: approved at `<sha7>` (none recorded yet)
- [ ] Verified at `<sha7>` (none yet)
- [ ] CI green at `<sha7>` (not pushed yet)

## Internal references

- CR-459 batch-graph-transitive-reduction-fold-merged-fewer-crossings (batch-30), round 1 of 2 planned.
- Specification: `03-change-spec.md`; round notes: `work/coder/r1.md`.
- Follow-up for round 2: DESIGN.md, `docs/demo/` data, `docs/web-board.md`, `docs/web-board/batch-graph-pc.png`, the Playwright measures and screenshots.

</details>
