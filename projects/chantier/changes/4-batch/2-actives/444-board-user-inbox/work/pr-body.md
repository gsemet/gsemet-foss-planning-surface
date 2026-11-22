## Summary

The web board has no single place that says what is waiting for the user: a question from an agent, an approval asked on a pull request, a PR ready to merge, a blocked CR. This adds an **Inbox** page, second in the navigation right after Home, that lists them as one card each with Open, Snooze (1 hour), Later (next 08:00) and Discard. It is not the planning inbox (`1-inbox`). The page notifies by a count beside its navigation entry, the count in the browser tab's title, a "new" mark and, on the user's yes, a browser notification while a board page is open. It works on a project and on "All projects".

## Deliverables

- The server builds the entries once: a pure `needs_you(state)` in `board/needs.py`, read-only, published as one new key on each project line of the `board` topic (no new op, topic or protocol number).

```mermaid
flowchart LR
  rec[batch rows + backlog waits + seat] --> needs[board/needs.py needs_you]
  needs --> line[board topic: project line needs_you]
  line --> model[js/model/inbox.js]
  marks[js/inbox/marks.js: device hides via store.js] --> model
  model --> page[views/inbox.js]
  model --> count[inbox/count.js: sidebar, bottom bar, tab title]
  line --> watch[inbox/watch.js: guarded browser notification]
```

- Four kinds: question, approval asked, ready to merge, blocked. An entry exists only while its fact lasts; a new occurrence is a new entry.
- Hides (snooze, later, discard) live in the browser only, through the store; the board edits no batch and messages no agent.
- Screenshots: **UNVERIFIED:** not attached yet (see Known gaps).

## Blast radius

Grade: 1. One added read-only key on the `board` topic and a new page; the other pages are unchanged. A `git revert` restores the previous board.

## Autonomous decisions

- The retaken documentation pictures of the other pages are committed: the navigation now shows the Inbox entry, so they changed.

## Known gaps

- **UNVERIFIED:** no Node run was made: the navigation count, the tab title, the "new" mark and the browser notification are not exercised by a test.
- **UNVERIFIED:** the written check of the hides and the screenshots are not yet captured.
- The plain-HTTP case (no notification API in a non-secure context) is not exercised.
- The guarded notification call is not exercised on Android Chrome.
- `just docs-screenshots` fails at its `panel` step on a selector that predates this change; the panel, editor, new, writer, picker and selection pictures are not retaken.

<details>
<summary>Details</summary>

## Changes

- `board/needs.py` (new), `board/state.py` (`needs_you` on each project line), `docs/server-api.md`.
- Web client: `views/inbox.js`, `inbox/{marks,count,watch,entry}.js`, `model/inbox.js`, `css/views/inbox.css`, `.tag.st.off` in `chip.css`, registry, bottom bar badge, header title, tab title, icon, words in English and French, `DESIGN.md` section.
- Tests: `tests/test_board_needs.py`, `test_the_inbox_is_the_second_view_and_reads_only`.
- Docs: `docs/web-board.md`, demo waits, `scripts/docs_screenshots.py`.

## Human decisions

- Four kinds only, built from the published record: question, approval asked, ready to merge, blocked. Nothing from the forge, pipelines, events or journal lines.
- Open is a link or the side panel and never a write; snooze, later and discard are kept in the browser, not on the server, so a hide on one device does not hide on another.
- A CR both ready to merge and with an open approval wait shows two cards, each hidden on its own.
- A paused batch still feeds the Inbox: its waits and blocked CRs are still what the user must act on.
- The browser notification is off by default and asked by a button on the page; the browser's own permission prompt follows the click.
- The hides are proved by a written check, not by a test that runs Node; a static test only checks that the pure model stays pure.

## Impacts

A new Inbox page and a count in the navigation and the tab title; no change elsewhere.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `ae76a80`: `just lint`, `just test`, `just check`, `just eval-dry-run` pass
- [ ] Evidence: after at `ae76a80`
- [ ] Review: approved at `ae76a80`
- [ ] Verified at `ae76a80`
- [ ] CI green at `ae76a80`

## Internal references

CR-444 board-user-inbox.

</details>
