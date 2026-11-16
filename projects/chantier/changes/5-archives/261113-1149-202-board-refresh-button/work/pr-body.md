## Summary

The `/chantier-board` pane in Claude Code checks its files every 15 seconds, but nothing in the pane said so, the only way to force a check was to run `/chantier-board` twice (which drops the page being read), and the header's "read Ns ago" was the age of the last time a file *changed*, so a quiet board showed "read 45s ago" although a check had run seconds before.

This PR adds a **Refresh** button to every view of the pane and makes the header say when the last check ran and how often it runs.

## Deliverables

The header of the board changes from `5 live · 0 waiting for you · read 45s ago` to:

```text
5 live · 0 waiting for you · checked 3s ago, every 15 s
```

| | Before | After |
| --- | --- | --- |
| Header | `read 45s ago` (age of the last change) | `checked 3s ago, every 15 s` (age of the last check) |
| Force a check | `/chantier-board` twice, the page is lost | `Refresh` button, page and folds kept |

- `checked Ns ago` is the age of the last check, periodic or pressed (0 right after a press); before the first check the line ends `· every 15 s`.
- `every 15 s` is written from the timer's own constant, so the note and the timer cannot drift.
- **Refresh** is one button for the whole pane, on every view (the board, a CR's sheet, a file list, a folder, a document, a page that shows nothing, and each one-line message). On a page it shares the top line with `< Back`.
- A press looks for the planning folders again (a project added to a surface, a `.agents/changes/` created after the pane opened), reads every file again even if unchanged, and keeps the page shown and the folds. It writes nothing and runs no process but `git rev-parse`; it does not refresh the batch's cost.
- Placement: the button is written for the top right of the pane (a row `Box` with `justifyContent`); that placement was not checked in a real pane (the test harness draws no layout). If the pane ignores the prop, the button sits at the top left, still on the first line.

## Blast radius

Grade: **1**. Only the Claude Code board pane and one documentation sentence change; the periodic check, the CLI and the remote board are untouched. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- One shared top bar helper draws the button on every view, so the button's place and key are the same everywhere.
- `View.readAt` is still set but no longer drawn (the specification allowed either).

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: `checkIndex`, `checkPage` and `check` take a `force` flag (the periodic timer still calls `check` unforced); a `refresh` function finds the root and the planning folders again, merges the views by folder without touching `pages` or `turned`, then runs a forced check; the press handler is wrapped in `guarded()`; the header uses `checkedAt` and `EVERY_MS`.
- `hooks/register.test.tsx`: nine new tests (header note and age, a press re-reading an unchanged file, page and folds kept, a folder found after opening for a project and a surface, the button on every view, no second timer); one existing test updated for the button's label.
- `types/index.d.ts`: the comment of `checkedAt` only.
- `docs/boards.md`: the sentence on refreshing now says the period, the button and what it does not refresh.

## Human decisions

- One Refresh button for the whole pane, on every view, at the top right where the layout allows it.
- A press reads files again even when unchanged, so the age returns to 0 and the button visibly does something.
- The header says `checked Ns ago, every 15 s`: the age of the last check, not of the last change.
- The pane stays read-only: a press does not refresh the batch's cost, and the period is not configurable.

## Impacts

The board's header wording changes and a Refresh button appears on every view of the pane. No visual proof is attached: the pane is a terminal view of the host.

## Test plan

- [x] New or changed tests (they fail on the previous code) at `97d5125`
- [x] Local gates at `97d5125`: `just mod` and `just check` pass (gate log); `just scenario` carried from `756a362`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [x] Evidence: none beyond the tests (the pane is not drawn by the harness)
- [x] Review: approved at `97d5125` (after a move review of the restack)
- [x] Verified at `97d5125`: tests and diff checked; the top-right placement is not provable without a real pane
- [x] CI green at `97d5125`

## Internal references

CR-202 board-refresh-button; archive and work files under the CR's folder.

</details>
