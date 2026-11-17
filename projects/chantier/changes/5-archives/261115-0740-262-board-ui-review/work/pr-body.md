## Summary

After a first page-by-page tour of the web board, several views misled: the Kanban showed a crowded "intake" and "grill" with nothing done, the header counted differently from the columns, Triage cards looked unlike the other pages and showed a blue outline when selected, and Costs and Home ignored the batches that were already closed. This PR fixes them, reading data the board's state already carries.

## Deliverables

- **Kanban**: seven columns, Inbox, Backlog, Grill, 3-ready, In progress, Handed back, Done. Grill holds the items being grilled or specified; Done shows the 20 newest merged changes with a "{n} more" foot. A row of toggles (Inbox, P1 to P4) hides priorities from the Inbox, Backlog and Grill columns for the session.
- **Header figures** (inbox, in grill, in progress, handed back) count what the column of the same name holds, through one shared model module; **UNVERIFIED:** a blocked change now counts as in progress (no blocked change in the check data).
- **Triage** cards are the Kanban item card (one shared function); the pick-up tilt, lift, drag fade and drop targets are kept; a selected card is marked by a check and a held shadow, with no blue outline.
- **Costs** lists the earlier batches (a row unfolds that batch's changes), also when no batch runs.
- **Home** gains an In grill tile, an Earlier batches block, a recent-activity block that names the last closed batch when none runs, merged changes with their batch, and a "Waiting for you" tile that counts blocked changes only.
- A card's title is its `summary.json` title when it has one.

| | Before | After |
| --- | --- | --- |
| Kanban columns | Intake, Backlog, Grill (every non-specified item), 3-ready, In progress, Handed back | Inbox, Backlog, Grill (being grilled or specified), 3-ready, In progress, Handed back, Done |
| Header "in progress" | `working` changes only | `queued` and `working` changes (**UNVERIFIED:** `blocked` too) |
| Triage card | its own post-it, blue outline when selected | the Kanban item card, check mark and held shadow when selected |
| Costs, no batch running | "No batch running" only | plus the earlier batches, each unfolding its changes |
| Home | no In grill tile; "Waiting for you" added unread asks to blocked changes | In grill tile, Earlier batches block, last closed batch in the activity block |

Before (base `33fc800`) and after (head `93a67aa`; the selected card at `63a6138`), English then French:

| View | Before | After |
| --- | --- | --- |
| Kanban, P3 and P4 off (EN) | ![Kanban before EN](../evidence/kanban-p3p4-off-en-real-before-33fc800.png) | ![Kanban after EN](../evidence/kanban-p3p4-off-en-real-after-93a67aa.png) |
| Kanban, P3 and P4 off (FR) | ![Kanban before FR](../evidence/kanban-p3p4-off-fr-real-before-33fc800.png) | ![Kanban after FR](../evidence/kanban-p3p4-off-fr-real-after-93a67aa.png) |
| Triage (EN) | ![Triage before EN](../evidence/triage-en-real-before-33fc800.png) | ![Triage after EN](../evidence/triage-en-real-after-93a67aa.png) |
| Triage (FR) | ![Triage before FR](../evidence/triage-fr-real-before-33fc800.png) | ![Triage after FR](../evidence/triage-fr-real-after-93a67aa.png) |
| Selected Triage card (EN) | ![Selected before EN](../evidence/triage-selected-en-demo-mobile-before-33fc800.png) | ![Selected after EN](../evidence/triage-selected-en-after-63a6138.png) |
| Selected Triage card (FR) | ![Selected before FR](../evidence/triage-selected-fr-demo-mobile-before-33fc800.png) | ![Selected after FR](../evidence/triage-selected-fr-after-63a6138.png) |
| Costs, no batch running (EN) | ![Costs before EN](../evidence/costs-en-demo-mobile-before-33fc800.png) | ![Costs after EN](../evidence/costs-en-demo-mobile-after-93a67aa.png) |
| Costs, no batch running (FR) | ![Costs before FR](../evidence/costs-fr-demo-mobile-before-33fc800.png) | ![Costs after FR](../evidence/costs-fr-demo-mobile-after-93a67aa.png) |
| Home (EN) | ![Home before EN](../evidence/home-en-real-before-33fc800.png) | ![Home after EN](../evidence/home-en-real-after-93a67aa.png) |
| Home (FR) | ![Home before FR](../evidence/home-fr-real-before-33fc800.png) | ![Home after FR](../evidence/home-fr-real-after-93a67aa.png) |

```js
// model/columns.js: one rule per column, read by kanban.js, header.js and Home's In grill tile
export const inboxItems = (backlog) => entries(backlog, ['inbox']).filter(at(['raw']));
export const grillItems = (backlog) => entries(backlog, FILTERED).filter(at(['grill', 'spec']));
export const progressCrs = (batch) => /* queued, working; UNVERIFIED: blocked */;
```

## Blast radius

Grade: **1**. Reading changes in the board's own web page and one title field in its API; no write path, no change to `STATUS.json` or the CR board pane. A plain `git revert` restores the previous board.

## Autonomous decisions

- The open questions of the specification took their recommended defaults: one change, the priority filter kept for the session, "Waiting for you" counts blocked changes only, a check mark and a held shadow for a selected Triage card, the words "Triage" and "Home" kept, seven Kanban columns.
- Earlier-batch lists keep only records that are closed; back-filled records with no date, mode or cost show a dash.
- New words went to sibling `en-board.js` and `fr-board.js` files to keep the language files under 300 lines.
- The demo project `mobile-app` gains two made-up closed batch records (batch-01 and batch-02) so that its changes have a batch.

## Known gaps

- Home's first load stuck on "Loading..." could not be reproduced on the live board (four headless loads: fresh profile, cookie only, French, Kanban); no change was made to the refresh code.
- The "44 questions" figure of "Waiting for you" could not be reproduced on the live board (0 unread asks at the base); the tile now counts blocked changes only.
- **UNVERIFIED:** that a blocked change counts as "in progress" in the header: the code does it, but no blocked change existed in the data used for the checks.
- The repository's own planning folder no longer holds the grill items the specification expected and runs a batch, so the Inbox, Grill and "no batch running" Costs screenshots come from the demo project.
- The sidebar's "inbox" label was renamed in the last commit, so the other "after" screenshots (taken at 93a67aa) still show the old "intake" word in the sidebar line; only the selected Triage card was shot again at the head.
- The Costs "after" and the selected Triage card come from the demo project; the Kanban, Triage and Home shots come from a copy of this repository's planning folder taken during the verification, with a batch running.
- Home's state at the base, point by point on the live board: no In grill tile (the header said "15 in grill"); "Waiting for you" 1 (one blocked change, 0 unread asks); recent activity filled while a batch runs, empty only with no batch (read from the code, not staged); last merged changes without their batch and with the "Change Specification:" lead; first load drew Home every time.

<details>
<summary>Details</summary>

## Changes

- `board/backlog.py`: an item's title prefers `summary.json`.
- `web/js/model/columns.js`, `history.js`: one rule per column, used by the Kanban, the header and Home; history helpers.
- `web/js/labels/priority.js`, `core/store.js`, `core/router.js`: the priority filter and the open Costs rows, reset on a project change.
- `web/js/ui/item-card.js`, `views/kanban-cards.js`, `triage/postit.js`, `css/views/postit.css`: the shared item card and the selection mark.
- `web/js/views/costs-history.js`, `home-history.js`, `home-feed.js`, `home-backlog.js`, `home.js`, `costs.js`: earlier batches on Costs and Home.
- `web/js/model/semantics.js`: "Waiting for you".
- `web/js/i18n/`: words in both languages, `kanban.intake*` renamed `kanban.inbox*`.
- `docs/web-board.md`, `docs/demo/`, `docs/web-board/*.png`: documentation and retaken pictures.

## Impacts

The web board reads differently on Kanban, Triage, Costs and Home; the screenshots show it.

## Test plan

- [ ] New or changed tests: structure tests only (sizes, same keys in each language)
- [x] Local gates at `63a6138`: `just check`, `just scenario`
- [x] Evidence: before at `33fc800`, after at `93a67aa` (selected Triage card at `63a6138`)
- [x] Review: approved at `63a6138`
- [x] Verified at `63a6138` (the selected-card claim, the sidebar label and `just check` judged again there; the other claims carried from `93a67aa`, since the later commit touches only those)
- [x] CI green at `63a6138`

## Internal references

- CR-262 board-ui-review
- Investigation and notes: `work/investigation.md`, `work/coder/r1.md`

</details>
