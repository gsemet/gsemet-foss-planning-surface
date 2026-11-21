## Summary

The board's batch page showed a batch only as a graph, a Gantt and time cards, so there was no plain view of which CRs have not started, which are being worked on and which are merged. This adds a **Kanban** view to the page's view switch: three read-only columns, `1-pending`, `2-actives` and `3-done`, each holding the batch's CRs whose folder is there. It is the first view and the default, and the view you pick is kept on the device.

## Deliverables

The Kanban tab reuses the project Kanban's column and CR card; nothing is dragged, a click opens the CR's folder.

```text
Kanban | Graph | Gantt | Time cards      (tab kept per device, `&t=` in every address)
[1-pending]  [2-actives]  [3-done]
 CR number    CR number     last merged first
 ascending    ascending
```

- Columns are the CR's folder on disk, as the server reports it, never derived from its state. A cancelled or dropped CR is in no column but stays on the Graph.
- Order is stable: a card never moves inside its column when its CR changes state.
- A closed batch's Kanban tab shows a one-line note (its CRs are in `5-archives`).
- Screenshots: **UNVERIFIED:** none yet from a real board (see Known gaps).

## Blast radius

Grade: 1. Web client only (view, router, i18n, CSS, doc and static tests); `git revert` restores the previous page.

## Autonomous decisions

None.

## Known gaps

- No screenshots from a board running this head yet (wide, phone width, kept tab, closed batch).
- The rows' `stage` field comes from #406 (a draft on another open PR's branch), not in this branch; until it merges, the Kanban columns stay empty on a live board. This PR is based on the default branch and waits on #406 and the PR under it for the stack.

<details>
<summary>Details</summary>

## Changes

- `js/core/router.js`, `js/core/store.js`: `TABS` starts with `kanban`; the tab kept on the device (`batchTab`) is read and written by the router and the store; `t=` is written for every Batch tab.
- `js/views/batch-kanban.js` (new), `js/views/batch.js`: the panel and the closed-batch note.
- `js/i18n/en-batch.js`, `js/i18n/fr-batch.js`: eight new keys.
- `css/views/batch.css`, `css/shell.css`: column layout on the batch page; the project Kanban's no-scroll rule narrowed to the project Kanban so the batch page still scrolls.
- `docs/web-board.md`, `clients/web/DESIGN.md`, `tests/test_board_design.py`: doc and static checks.

## Human decisions

- The Kanban and the graph share the batch page's view switch; Kanban comes first, is the default, and the choice is kept on the device.
- Cards keep a stable order: CR number in the first two columns, last merged on top in the done column; a card leaves its column only when its folder moves.
- The view is read-only: the batch's folders move by the CLI's lifecycle, never by dragging.
- On a closed batch the Kanban tab shows a one-line note instead of columns.

## Impacts

The batch page opens on the Kanban instead of the Graph, and remembers the last tab on the device.

## Test plan

- [ ] New or changed tests (they fail on the previous code): static checks in `test_board_design.py`
- [ ] Local gates at `<sha7>`: <!-- filled at the commit -->
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-434 board-batch-kanban

</details>
