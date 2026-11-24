## Summary

The web board's menu carried a Kanban page nobody uses, an "Inbox" entry easily confused with the `1-inbox` folder, and a Help entry in the middle. The All-projects home showed no activity and no PRs, and History was per project only. This change trims the menu, dims the page behind an open panel, hides the unfinished Grill button, and makes the All-projects pages a place to follow every project at once.

## Deliverables

- Menu: the Kanban page is gone; "Inbox" reads "Notifications" (same view and address); Help is last (after Configuration, after History on All projects).
- Detail panel: the page behind is dimmed (new `--backdrop` token); a click on it closes the panel through the same leave check as Escape, so an unsaved edit asks first.
- Grill button hidden behind one constant in `js/panel/griller.js`, off as shipped; the server's Griller is untouched.
- All-projects home: an Open PRs block (ready to merge, red CI, working) and a Recent activity block (20 newest CR and release events), read from the record, the hub's journal and the History index; no new forge read.
- History on All projects: the project page widened to every project, with project and type filter chips and the project's mark on each row; the `history` topic and `history.get` accept `*`.
- Screenshots: none at this head, see Known gaps.

## Blast radius

Grade: 2. Mostly web client files, plus the `board` and `history` reads of the server. A revert restores the old menu and pages.

## Autonomous decisions

- Shared `.kanban` rules moved to `batch.css`, since the Batch tab uses them.
- Red CI is read as a `checks-red@1` line after the CR's last hand-back.
- The public key still reads no cost or rounds: feed events are rebuilt from an allow-list.

## Known gaps

- No screenshots retaken yet: the docs pictures still show the old menu, and the PR's own screenshots at the head are owed.
- UNVERIFIED: the five screenshots the change owes (All-projects home, All-projects History, menu, dimmed panel, leave dialog), real red CI from a live forge and the Grill constant switched on were not exercised.
- Red CI stays shown until the CR's next hand-back; the hub journals no green line.

<details>
<summary>Details</summary>

## Changes

- Client: registry, sidebar/bottom bar, `overview.js`, `history.js`, `history-filter.js`, `main.js` backdrop, `griller.js` constant, CSS, i18n (en, fr), DESIGN.md.
- Server: `board/overview.py`, `reads.py`, `history_page.py`, `api/topics.py`; docs `web-board.md`, `server-api.md`.

## Human decisions

- The All-projects home lists the open PRs of every project's batch, in three states (ready to merge, red CI, working).
- The recent-activity feed holds the 20 newest events and only the CRs' life and releases.
- History on All projects is complete per period (day, week, month), not one unpaged list.
- A click on the dimmed page asks first only when an edit holds unsaved changes.
- The Grill button is hidden by one constant in the client, with no configuration key.

## Impacts

The menu and the All-projects pages change; a project's pages are unchanged.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `f1c0f5a`: `just check` pass, `just eval-dry-run` pass (19 of 19), `just scenario` pass
- [x] Evidence: tests at `f1c0f5a` (no screenshots: Playwright not available)
- [x] Review: approved at `f1c0f5a`
- [x] Verified at `f1c0f5a`
- [x] CI green at `f1c0f5a`

## Internal references

CR-482 web-board-menu-home-history

</details>
