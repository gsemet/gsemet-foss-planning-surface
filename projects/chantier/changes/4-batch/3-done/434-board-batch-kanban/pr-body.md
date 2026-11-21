## Summary

The board's batch page showed a batch only as a graph, a Gantt and time cards, so there was no plain view of which CRs have not started, which are being worked on and which are merged. This adds a **Kanban** view to the page's view switch: three read-only columns, `1-pending`, `2-actives` and `3-done`, each holding the batch's CRs whose folder is there. It is the first view and the default, and the view you pick is meant to be kept on the device (**UNVERIFIED:** read in the code and checked on fixtures, not run in a browser).

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
- **UNVERIFIED:** the CSS layout (column flex, phone snapping, page scroll), the tab kept on the device and the closed-batch note were checked by static tests, a fixture probe and reading the diff only, never in a browser.
- The rows' `stage` field comes from #406 (a draft on another open PR's branch), not in this branch; until it merges, the Kanban columns stay empty on a live board. This PR is based on the default branch and waits on #406 and the PR under it for the stack.

<details>
<summary>Details</summary>

## Changes

- `js/core/router.js`, `js/core/store.js`: `TABS` starts with `kanban`; the tab kept on the device (`batchTab`) is read and written by the router and the store; `t=` is written for every Batch tab.
- `js/views/batch-kanban.js` (new), `js/views/batch.js`: the panel and the closed-batch note.
- `js/i18n/en-batch.js`, `js/i18n/fr-batch.js`: eight new keys.
- `css/views/batch.css`, `css/shell.css`: column layout on the batch page; the project Kanban's no-scroll rule narrowed to the project Kanban meant to keep the batch page scrolling (**UNVERIFIED:** not rendered).
- `docs/web-board.md`, `clients/web/DESIGN.md`, `tests/test_board_design.py`: doc and static checks.

## Human decisions

- The Kanban and the graph share the batch page's view switch; Kanban comes first, is the default, and the choice is kept on the device.
- Cards keep a stable order: CR number in the first two columns, last merged on top in the done column; a card leaves its column only when its folder moves.
- The view is read-only: the batch's folders move by the CLI's lifecycle, never by dragging.
- On a closed batch the Kanban tab shows a one-line note instead of columns.

## Impacts

The batch page opens on the Kanban instead of the Graph, and is meant to remember the last tab on the device (**UNVERIFIED:** read in the code, not run in a browser).

## Test plan

- [x] New or changed tests (they fail on the previous code): static checks in `test_board_design.py`
- [x] Local gates at `0aec452` (carried from `140c12a`, a clean rebase of the same patch): `just check` pass, `just eval-dry-run` pass, `just scenario` pass
- [ ] Evidence: none yet, no board running this head carries the `stage` field (see Known gaps); a fixture probe of the panel and the router passed at `0aec452`
- [x] Review: approved at `0aec452` (carried from `140c12a`)
- [x] Verified at `0aec452`
- [x] CI green at `0aec452`: `gh pr checks 407`, all five checks pass

## Internal references

- CR-434 board-batch-kanban

</details>
