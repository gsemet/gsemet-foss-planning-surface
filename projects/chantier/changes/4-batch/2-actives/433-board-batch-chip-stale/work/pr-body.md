## Summary

On the web board, a card of a CR that is in a batch showed the priority chip of the folder it came from, and `3-ready` for its whole life in the batch, which says nothing about where it is now. The card now shows the batch folder the CR is really in (`1-pending`, `2-actives` or `3-done`) in that place, in a neutral grey chip. The backlog views keep their priority chips.

## Deliverables

The board server's batch rows swap one key for another, and four batch views read the new one:

```text
before: row.priority  (origin of the CR's "add" event: inbox | P1..P4 | 3-ready)
after:  row.stage     (folder on disk: 1-pending | 2-actives | 3-done | null)
```

- `stage` is read from the CR's own folder under `4-batch/`, so it says what the planning folder shows; a CR out of the batch's folders (a cancelled CR moved back to the inbox or the backlog, or no folder found) has `stage: null` and draws no chip.
- The Batch graph node, the Gantt label, the Batch time card and the PRs page's card pass `priority: c.stage` to the same card builder; the chip uses the existing neutral `.tag` style, with no new colour or token. The Kanban's card of a batch CR is unchanged.
- The Triage page's running-batch lane draws its pending CRs through the same card, with `priority: c.stage` (`js/triage/columns.js`), so they show `1-pending`.
- `priority_of` and its helper are removed: nothing reads them any more.
- No screenshot: the change is a chip's text on existing cards.

## Blast radius

Grade: 1. A batch row's `priority` key is gone from the board's published state; the only readers were the four views changed here. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- A small `stage_of` helper in `board/crs.py` computes the folder, so the test can name it and `_row` stays short.

## Known gaps

- The screenshots of `docs/web-board.md` are not retaken, as the specification says.
- Not yet checked by hand on a running board (the batch graph, the Gantt, the time cards and the PRs page).

<details>
<summary>Details</summary>

## Changes

- `board/crs.py`: `_row` drops `priority`, gains `stage` (via `stage_of`, using `lifecycle/stages.py:STATE_FOLDERS`).
- `board/times.py`: `priority_of` and `PRIORITY_AFTER` removed.
- `clients/web/js/views/batch-graph.js`, `batch-gantt.js`, `batch-timecards.js`, `batch-pr-card.js`: `priority: c.stage`, and the same in `js/triage/columns.js` (the running-batch lane); comments in `js/ui/card.js`, `js/ui/parts.js` follow.
- `clients/web/DESIGN.md` ("One card, one column, one chip") and `docs/web-board.md` ("Batch") say the batch folder chip.
- Tests: a parametrized server test (`test_board_waits.py`), a shipped-files check (`test_board_design.py`), `test_priority_of` removed.

## Human decisions

- A batch CR's card shows the batch folder it is really in, in the place of the old priority chip, and never `3-ready` (this replaced an earlier answer of "no chip").
- This holds in every board view that draws the CR as a batch CR with that chip; the backlog views keep their priority chips.
- The Kanban page's card of a batch CR stays unchanged for now.

## Impacts

Visible: a batch CR's card shows `1-pending`, `2-actives` or `3-done` in a grey chip where the priority chip was. Developers: the batch row has `stage`, no `priority`.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: none (no visual capture)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-433 board-batch-chip-stale

</details>
