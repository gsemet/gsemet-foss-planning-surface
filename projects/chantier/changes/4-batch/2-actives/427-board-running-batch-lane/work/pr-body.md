## Summary

On the board's backlog page (Triage), the last column is now split in two halves, as Jira does: "Running batch" on top and "Next batch" (`3-ready`) below. Both halves are always shown, in every mode. A drop on "Running batch" writes only a mark in the CR's own folder (`work/running-batch`), or, for a `3-ready` CR, only a journal line; the Chief of Staff (chantier's planning role) then adds the CR to the open batch once its specification is final. With no open batch the top half is greyed ("no running batch") and a drop on it moves the CR to `3-ready`. The board still never edits a batch.

## Deliverables

- The Triage page's last column in two named lanes, the top one listing marked CRs ("waiting for its spec", "spec written: joins soon") and pending CRs ("waiting for a slot").
- **UNVERIFIED:** screenshots of the split column (open batch, and greyed with none) are not yet attached.
- Choices: a marked CR is drawn once, in the top half only; pending CRs are plain cards, neither draggable nor selectable; a grilled CR whose spec has not started is refused with "the grill is not finished".

## Blast radius

Medium: the board's move route, the journal's waking actions and the Triage view change. Roll back by reverting the PR; marks are plain files in backlog folders.

## Autonomous decisions

None.

## Known gaps

- No screenshots of the split column yet.
- The existing Triage screenshots in `docs/web-board/` (`triage-pc.png` and the phone ones) were not retaken with `just docs-screenshots` (no browser in the session that built this PR).

<details><summary>Details</summary>

## Changes

- Web client: named lane variant in `js/ui/column.js`, two-half last column, `running-batch` drop target and selection-bar target, words in both languages, `DESIGN.md` section.
- Server: `running-batch` target in `board/write_api.py`, `running_batch` item key, mark cleared by every move in `lifecycle/backlog.py`, `running-batch` waking action and texts in `hub/`.
- Cards, `AGENTS.md`, docs and scenario updated.

## Human decisions

- A drop on "Running batch" writes only the mark; the Chief of Staff adds the CR when its spec is final.
- With no open batch the half stays visible, greyed, and a drop places the CR in `3-ready`.
- The latest destination word wins, whether from the grill or the board.

## Impacts

Users see the split column on the backlog page.

## Test plan

- `just check`: pass at `160e292`.
- `just eval-dry-run`: pass at `fdc1d28` (carried over the clean restack to `160e292`).
- `just scenario` (local long gate, includes the new running-lane step): pass at `fd52787` (carried over the clean restack to `160e292`).
- CI (`gh pr checks 401`): all 5 checks pass at `160e292`.

## Internal references

- CR-427 board-running-batch-lane

</details>
