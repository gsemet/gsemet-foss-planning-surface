## Summary

On a very wide screen (about 2900 px) the web board had several rough edges: the side panel stayed open when the view changed, hovering a Triage card made a horizontal scroll bar appear, Triage cards stretched across the whole window, a card's text could show raw `---` frontmatter, and the side panel was too narrow for a round file's table. This PR fixes them; the board is unchanged on a laptop and a phone apart from the frontmatter fix and the Triage cap.

## Deliverables

- **Triage cards capped, backlog as a grid.** Every Triage card (inbox, P1 to P4, 3-ready) has one width, at most 320 px (`--card-w`, a little wider than a 290 px Kanban card); at 1400 px every card, inbox, backlog and 3-ready, is 291 px; each backlog lane lays its cards side by side, as many per row as fit, in the same order as before. A group's frame spans a full row of the lane's grid, its members capped like any card. Picture: the updated docs/web-board/triage-pc.png, carried from f11132b.

![Triage carried from f11132b](./triage-pc.png)

| | Before | After |
| --- | --- | --- |
| Card width on a 2900 px window | over 1000 px | 320 px |
| Card width at 1400 px | column width | 291 px, all columns |
| Cards per row in a backlog lane | 1 | as many as fit |
| Side panel width | 680 px | 45% of the window, 680 px minimum |

- **Side panel.** It closes on any change of view (left bar, phone bar, view links, back and forward). On a wide window it takes 45% of the width with 680 px as a floor; a wide table or code block scrolls inside the file column instead of overflowing.
- **No hover scroll bar.** The tilt and shadow of a hovered card stay; the card's lane no longer shows a horizontal scroll bar.
- **Card text.** A YAML frontmatter at the start of a file is skipped when a card's description is computed.

## Blast radius

Grade: 1

Front-end CSS and one routing line, plus the description helper; a plain `git revert` restores the previous board.

## Autonomous decisions

- Card cap 320 px: the same order as a Kanban card, narrower than one and a half Kanban columns; below 1400 px cards shrink with their column.
- Panel share 45vw with the 680 px floor.
- Triage columns are capped at 30% of the width each for the inbox and 3-ready, so the backlog takes the rest.
- A group's frame spans a full row so its members stay together and its handle stays easy to hit.

## Known gaps

- Home's "see the batch" link is not shown at 375 px (no card to open there), and the phone's bottom bar was exercised by a scripted click.

<details>
<summary>Details</summary>

## Changes

- `board/web/js/core/router.js`: a change of view closes the panel.
- `board/web/css/views/triage.css`, `postit.css`, `tokens.css`: card cap, lane grid, no scroll bar on hover.
- `board/web/css/panel.css`, `components.css`: wider panel, sideways scrolling inside the file column.
- `board/backlog.py`: frontmatter skipped in `description`.
- `docs/web-board.md`, `docs/web-board/triage-pc.png`; a parametrized test of `description`.

## Human decisions

- Triage cards are capped to one width and the backlog is laid out as a grid of several cards per row, as the inbox item asked.
- The surface selector on the picker is a separate change, not part of this PR.

## Impacts

The Triage picture shows the capped cards. On a laptop (1400 px) a Triage card is now capped and a backlog lane may show two cards per row.

## Test plan

- [x] New or changed tests (they fail on the previous code: 4 of the 6 first cases failed on main)
- [x] Local gates carried from `f11132b`: `just check`
- [x] Evidence: before at `cb7690a`, after carried from `f11132b`
- [x] Review: carried from `f11132b`
- [x] Verified: carried from `f11132b`
- [x] CI green at `942e14d`: `just check` x3, eval-dry-run and `just scenario` (ubuntu-latest) pass

## Internal references

- CR-304 web board on a large screen; work files under the CR's `work/` folder.

</details>
