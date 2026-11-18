## Summary

On the web board, the Kanban's horizontal scrollbar sat below the window's fold, so it was never seen. Backlog items had no visual priority cue, and the board was plain grey and white. This PR bounds the Kanban to the window so its scrollbar stays at the bottom, colours P1 to P4 as a teal gradient, and adds a light pastel style, without touching the colours of the CR states.

## Deliverables

- **Kanban scrollbar.** On the Kanban the columns' row fills the visible height; the page no longer scrolls vertically, the board's horizontal scrollbar sits at the window's bottom, and each column scrolls on its own. The phone layout keeps its snap per column. Other views scroll as before.
- **Priority colours.** `--pri-1` to `--pri-4` run from the accent's dark teal (`#1d5c63`) to a pale one (`#cfe2e3`). They colour the `Pn` chip and a 3px left border on every backlog item card (Kanban, Triage) and the chip in the panel's head. Inbox, 3-ready, CR and merged items are not coloured.
- **Pastel style.** State chips and badges take a tint of their own state's colour; project marks, the Costs figure cards, the Kanban's column headers and the sidebar's active row take teal or mark tints; the sidebar gets a very light teal. Pages and cards stay white. The eight `--state-*` colours are unchanged.
- **Project marks** moved off the hues of the states (table in Changes).
- **State colours unchanged.** `git diff origin/main -- css/tokens.css`, filtered on the `--state-<name>:` value lines, is empty at carried from de0993f; only the group comment changes.

Kanban, before at 33a2305 (left) and after at carried from de0993f (right):

| Before | After |
| --- | --- |
| ![Kanban before](./verifier/evidence/before/kanban-pc.png) | ![Kanban after](./verifier/evidence/after/kanban-pc.png) |

Phone width, after at carried from de0993f: ![Kanban phone](./verifier/evidence/after/kanban-phone.png)

Triage with a selected P1 card, after at carried from de0993f: ![Triage](./verifier/evidence/after/triage-pc.png)

Panel of a backlog item and of a CR, after at carried from de0993f: ![Item panel](./verifier/evidence/after/panel-item-pc.png) ![CR panel](./verifier/evidence/after/panel-pc.png)

Costs, Batch and All projects, after at carried from de0993f: ![Costs](./verifier/evidence/after/costs-pc.png) ![Batch](./verifier/evidence/after/batch-pc.png) ![All projects](./verifier/evidence/after/all-projects-pc.png)

## Blast radius

Grade: **1**. CSS tokens and rules plus three small JS class additions in the board's web files; `git revert` restores the previous look.

## Autonomous decisions

- Panel head: it draws no card, so the `Pn` chip alone is its priority mark (no left border).
- Mark 5 kept its hue and was only darkened to reach 4.5:1 on its tint; it is 23.5 degrees from the ready hue but looks like no state.
- `--side` is also used by the Config table's header, which is now faintly tinted.

## Known gaps

- Home's PR rows and batch head build their state chip by hand, so they keep the grey chip; the other state chips are tinted.
- The Kanban's scrollbar itself is an overlay scrollbar in headless captures; it is proven by measured sizes, not shown.

<details>
<summary>Details</summary>

## Changes

- `css/shell.css`, `css/views/kanban.css`: the view of a Kanban becomes a bounded flex item so `height: 100%` resolves; header comment says seven columns.
- `css/tokens.css`: `--pri-*`, state and mark tints, `--side` tint, new mark values; `--state-*` value lines untouched.
- `css/tags.css`, `css/cards.css`, `js/ui/item-card.js`: priority chip and card left border; `js/ui/parts.js`, `js/ui/header.js`, `css/crumbs.css`, `css/views/batch-graph.css`: state tints on chips and badges.
- `css/components.css`, `css/views/costs.css`, `css/sidebar.css`, `css/picker.css`: marks, figure cards, active row, sidebar.
- `docs/web-board.md`: one sentence each for the Kanban and Triage.

Marks (old, new, hue, nearest state hue gap):

| Mark | Old | New | New hue | Nearest state (gap) |
| --- | --- | --- | --- | --- |
| 0 | `#c8401f` | `#a02e78` | 321.1 | blocked (30.4) |
| 1 | `#2f6f9f` | `#1a6c88` | 195.3 | working (26.3) |
| 2 | `#5b7a2a` | `#3a7222` | 102.0 | merged (50.2) |
| 3 | `#7a4aa8` | `#8a3aa8` | 283.6 | local (26.0) |
| 4 | `#a8691f` | `#666c12` | 64.0 | waits (27.7) |
| 5 | `#1f7a74` | `#1a736d` | 176.0 | ready (23.5, unmoved hue) |

Contrast (text on background):

| Pair | Ratio |
| --- | --- |
| P1 chip, white on `#1d5c63` | 7.60 |
| P2 chip, white on `#4a7e83` | 4.56 |
| P3 chip, `#123d42` on `#88acb0` | 4.84 |
| P4 chip, `#123d42` on `#cfe2e3` | 8.83 |
| Active nav row, `#123d42` on `#e9f1f1` | 10.34 |
| Mark letters on their tints, 0 to 5 | 5.34, 4.84, 4.77, 5.21, 4.66, 4.63 |

## Human decisions

- The priority gradient is the board's teal accent (P1 dark to P4 pale), not a warm one, which read like blocked, waits and draft.
- Pastel variant A: chips, avatars, figure cards and column headers; pages stay white; the sidebar is lightly tinted.
- Every Kanban column header takes one neutral pastel; the dots stay.
- Project marks that looked like a state colour move to other hues.

## Impacts

The board looks lighter and more colourful; priorities read at a glance; the Kanban's scrollbar is reachable.

## Test plan

- [x] No behaviour change in the CLI; board web files only
- [x] Local gates at `carried from de0993f`: `just check` (443 tests pass); CI at `carried from de0993f`: all jobs pass
- [x] Evidence: before at `33a2305`, after at `carried from de0993f`
- [x] Review: approved at `carried from de0993f`
- [x] Verified at `carried from de0993f`
- [x] CI green at `carried from de0993f`

## Internal references

- CR-326 board-kanban-priority-colours; work files `work/r1-tables.md`, `work/coder/r1.md`.

</details>
