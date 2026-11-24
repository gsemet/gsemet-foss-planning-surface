<!-- draft; SHAs filled at ship -->

## Summary

The web board's menu carried a Kanban page nobody uses, an "Inbox" entry easily confused with the `1-inbox` folder, and a Help entry in the middle. The All-projects home showed no activity and no PRs, and History was per project only. This change trims the menu, dims the page behind an open panel, hides the unfinished Grill button, and makes the All-projects pages a place to follow every project at once.

## Deliverables

- Menu: the Kanban page is gone; "Inbox" reads "Notifications" (same view and address); Help is last (after Configuration, after History on All projects).
- Detail panel: the page behind is dimmed (new `--backdrop` token); a click on it closes the panel through the same leave check as Escape, so an unsaved edit asks first.
- Grill button hidden behind one constant in `js/panel/griller.js`, off as shipped; the server's Griller is untouched.
- All-projects home: an Open PRs block (ready to merge, red CI, working) and a Recent activity block (20 newest CR and release events), read from the record, the hub's journal and the History index; no new forge read.
- History on All projects: the project page widened to every project, with project and type filter chips and the project's mark on each row; the `history` topic and `history.get` accept `*`.
- Screenshots: to be added at the head.

## Blast radius

Grade: 2. Mostly web client files, plus the `board` and `history` reads of the server. A revert restores the old menu and pages.

## Autonomous decisions

- Shared `.kanban` rules moved to `batch.css`, since the Batch tab uses them.
- Red CI is read as a `checks-red@1` line after the CR's last hand-back.
- The public key still reads no cost or rounds: feed events are rebuilt from an allow-list.

## Known gaps

- No screenshots retaken yet: the docs pictures still show the old menu, and the PR's own screenshots at the head are owed.
- Red CI stays shown until the CR's next hand-back; the hub journals no green line.

<details>
<summary>Details</summary>

## Changes

- Client: registry, sidebar/bottom bar, `overview.js`, `history.js`, `history-filter.js`, `main.js` backdrop, `griller.js` constant, CSS, i18n (en, fr), DESIGN.md.
- Server: `board/overview.py`, `reads.py`, `history_page.py`, `api/topics.py`; docs `web-board.md`, `server-api.md`.

## Impacts

The menu and the All-projects pages change; a project's pages are unchanged.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`
- [ ] Evidence: after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-482 web-board-menu-home-history

</details>
