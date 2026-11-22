## Summary

On the board's Batch page, two full-width rows (the mode band and the "States and arrows" legend line) sat between the four figures and the view switch and took about 90 px of height for little content. They now sit in the page's title row, beside `Batch ‹ batch-name ›`. The view switch and the central view start about 90 px higher. Nothing is removed, except the legend's "hover for the legend" hint on a phone.

## Deliverables

- The title row now holds, in order: the mode pill (`<mode> · <steering>`), the legend pill with its hint, then the Stack / Series / Parallel switch pushed to the right end.
- The mode's one-sentence explanation is now a tooltip on the mode pill (shown on hover, focus and tap), at every width. Both pills show a help cursor.
- On a phone (760 px and below) the switch and the legend's hint are hidden; the two pills stay on one line, and a tip anchors at the slot's left edge so it never runs off the screen.

```
before:  Batch ‹ b ›                      [+ New]
         figures
         [mode band ........ Stack|Series|Parallel]
         [legend pill] hover for the legend
         [view switch]  central view
after:   Batch ‹ b › [mode] [legend] hover… ......... Stack|Series|Parallel
         figures
         [view switch]  central view
```

Batch page at 1400 x 860, before (base `33d1045`) and after (head `e2f8fdc`): the view switch's top goes from 353 px to 263 px (90 px higher); the figures' top stays at 143 px.

| Before `33d1045` | After `e2f8fdc` |
| --- | --- |
| ![before](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/evidence/batch-pc-before.png) | ![after](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/work/verifier/evidence/batch-pc-after.png) |

At 375 x 812, before and after at the same SHAs: the two pills share one line, the hint and the switch are hidden, there is no horizontal scroll (scrollWidth 375). On a phone the figures' top moves from 155 px to 176 px, because the pills take one new line.

| Before `33d1045` | After `e2f8fdc` |
| --- | --- |
| ![before](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/evidence/batch-phone-before.png) | ![after](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/work/verifier/evidence/batch-phone-after.png) |

Each tip opens whole above the figures' tiles at 1400 px and inside the viewport at 375 px:

| Mode tip | Legend tip |
| --- | --- |
| ![mode tip](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/work/verifier/evidence/batch-pc-tip-mpill-after.png) | ![legend tip](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/work/verifier/evidence/batch-pc-tip-lgpill-after.png) |

A closed batch shows the mode and the legend in the title row too: ![closed batch after](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/d91cd3e7a92099d2a800b66252a4c8792e9ee5f4/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact/work/verifier/evidence/closed-pc-after.png)

## Blast radius

Grade: **1**. One page of the web client (HTML slot, one new view module, one stylesheet, DESIGN.md, docs, one test); no server, protocol or CLI change. A plain `git revert` restores the previous layout.

## Autonomous decisions

- Restacked on the Kanban merge and on the dev-mode launch change below it in the stack; the title-row tests live in their own file, `tests/test_board_title_row.py`.

## Known gaps

- The "about 90 px" claim and the tip checks are measured on the demo at an earlier head, carried through the clean restacks to `e2f8fdc`, not on a live board.
- A batch opened with no CR yet starts in parallel mode, so its title row shows that mode; the picture of it is not in this description.

<details>
<summary>Details</summary>

## Changes

- `index.html`: a hidden `#batch-mode` slot in `.titlerow`; `js/main.js` paints it with `batchMode(state)`.
- `js/views/batch-head.js` (new): the mode pill, legend and switch moved out of `js/views/batch.js`.
- `css/views/batch.css`, `css/batch-nav.css`: the moved rules re-scoped under `.bmode`, the pills' tip rules, the phone block.
- `DESIGN.md`, `docs/web-board.md`: a section on the title row; the legend now sits in the title row.
- `docs/web-board/*.png` (batch-cards-pc, batch-gantt-pc, batch-pc, batch-phone, panel-pc, plus kanban-pc, triage-pc, editor-pc, new-pc, new-phone, triage-selection-phone that the Kanban merge had left stale): retaken; the phone picture leads with the PRs column, as the code draws it. `scripts/docs_screenshots.py`: the panel step opens the Kanban tab.
- `tests/test_board_title_row.py`: the title-row tests reading the shipped files.

## Human decisions

- Everything goes into the title row; the breadcrumb row and "+ New" stay untouched, and the switch follows its band at the row's right end.
- The mode's sentence is a tooltip alone, at every width, with no short form.
- Both pills show a help cursor.
- On a phone the legend's hint is hidden and the two pills stay.

## Impacts

The Batch page is shorter above its views; the mode sentence is a tooltip instead of an inline line.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_board_title_row`
- [x] Local gates: `just check`, `just eval-dry-run` and `just scenario` passed at this CR's earlier heads; not run again at `e2f8fdc` (a clean restack of the same patch); the pipeline runs them at the head
- [x] Evidence: before at `33d1045`; after: pictures from the Verifier at `e2f8fdc`
- [x] Review: restack judged at `e2f8fdc` (the patch approved earlier, carried through the restacks)
- [x] Verified at `e2f8fdc` (verdict VERIFIED; the browser claims carried from earlier heads)
- [x] CI green at `e2f8fdc` (5 checks)

## Internal references

CR-435 board-batch-compact.

</details>
