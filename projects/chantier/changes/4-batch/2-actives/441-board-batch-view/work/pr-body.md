## Summary

On the board's Batch page, the graph of connected cards draws one arrowhead for every arrow, so a card that waits for several others gets a pile of heads at one point, and with a light on they add up to a heavy grey head under faint lines. The lit arrows also pass behind the cards they cross, so an arrow that skips a level cannot be followed. And nothing says how to change a batch's mode. This PR gives each waiting card one arrowhead, draws the lit arrows above the cards, and adds a tooltip on each word of the Stack / Series / Parallel switch.

## Deliverables

- One arrowhead per waiting card, drawn once whatever its number of sources (2 or 7), at the middle of its left edge, whole and touching the card. The demo's `localised-receipts` card now waits for three others, in three rows and two levels, so the picture shows it.
- On hover or focus, the lit arrows and their heads are drawn again in the accent colour in a layer above the cards. Unlit arrows stay behind the cards.
- Each mode word of the switch on a running batch has a tooltip (hover and keyboard focus): `To switch, ask the Chief of Staff to "change the batch to series"`, or "This batch's mode." on the batch's own mode, in English and French. A closed batch has none. Clicking a mode does nothing: the board edits no batch.

Before and after, `localised-receipts` hovered (before at `9b22d87` plus the demo change, after at `<HEAD7>`):

<!-- IMAGES: before-graph-cr148-hovered.png | after-graph-cr148-hovered.png | after-graph-cr146-keyboard-focus.png | after-switch-tip-series-en.png | after-switch-tip-series-fr.png, attached through the forge's CLI -->

Design choices: no new layout, colour, size or token; no routing of arrows around cards; the Gantt keeps its own markers.

## Blast radius

Grade: 1. The web client's graph and switch only, plus the demo data and pictures; no server, protocol, CLI or record change. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The new test sits in its own file, `tests/test_board_graph_arrows.py`, because adding it to `tests/test_board_design.py` would pass that file's line limit.
- `panel()` in `scripts/docs_screenshots.py` now opens the Batch graph tab before clicking a card: since the Kanban became the default tab, its selector never matched.
- Pictures that changed only by rendering noise were left as they were; only the pictures the demo change or the new graph picture alter are committed.

## Known gaps

- None of the pictures of a closed batch's arrows: the demo's closed batches hold no dependency, so a closed batch's arrows rest on the live graph's checks and on the code both share.

<details>
<summary>Details</summary>

## Changes

- `js/views/batch-graph.js`, `css/views/batch-graph.css`: arrows lose their `marker-end`; `drawEdges` draws one `path.head[data-to]` per waiting card; `light` lights and dims heads and fills a second layer `svg.edges.top` (above the levels, no pointer events) with copies of the lit arrows and heads; `.head`, `.head.hl`, `.head.dim` rules.
- `js/views/batch-head.js`, `css/views/batch.css`, `js/i18n/en.js`, `js/i18n/fr.js`: mode-word tooltips (`mode.switch_to`, `mode.current`), child selectors for the switch's rules.
- `clients/web/DESIGN.md`: a bullet in the title-row section and a section on the graph's arrows.
- Demo (`docs/demo/projects/shop-api`): `localised-receipts` waits for three CRs. `docs/web-board.md`, `scripts/docs_screenshots.py` and the pictures under `docs/web-board/` follow, with a new `batch-graph-pc.png`.
- `tests/test_board_graph_arrows.py`: reads the shipped files and checks each of the above.

## Human decisions

- A repair, not a redesign: levels stay columns, cards stay white, arrows grey, the hover light stays.
- All arrows of a card that waits for several others arrive at the middle of its left edge, level, under one whole arrowhead.
- Hover or focus lights a card, what it waits for and what waits for it; the lit arrows are drawn above the cards. Nothing else is added: no list on the card, no click to pin.
- The Gantt's arrows do not change.
- The tooltip uses the page's own tooltip pattern on each of the three mode words, not a browser `title`; clicking a mode does nothing; a closed batch has none; on a phone the switch stays hidden.
- English text: `To switch, ask the Chief of Staff to "change the batch to <mode>"`; the batch's own mode says "This batch's mode."

## Impacts

The Batch graph's arrowheads and the lit arrows look different, and the switch shows tooltips; the pictures above show them. The demo's next CR to start changes, so a few shipped pictures changed: `batch-pc`, `batch-phone`, `batch-gantt-pc`, `batch-cards-pc`, `kanban-pc`, `kanban-phone`, `panel-pc`, plus the new `batch-graph-pc`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_board_graph_arrows.py`
- [ ] Local gates at `<HEAD7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: before at `9b22d87`, after at `<HEAD7>`: one head into the waiting card, its tip 0 px from the left edge's middle, its three arrows ending there; top layer with 3 arrows and 1 head in the accent; every tooltip inside the viewport; no tooltip on a closed batch; no horizontal scroll at 375 px
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-441 batch-graph-arrows (batch-30, after CR-435)

</details>
