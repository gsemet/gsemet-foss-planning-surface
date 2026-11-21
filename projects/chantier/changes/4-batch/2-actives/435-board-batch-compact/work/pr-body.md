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

Before/after pictures: **UNVERIFIED:** not yet attached (see Known gaps).

## Blast radius

Grade: **1**. One page of the web client (HTML slot, one new view module, one stylesheet, DESIGN.md, docs, one test); no server, protocol or CLI change. A plain `git revert` restores the previous layout.

## Autonomous decisions

- Built on the current `main`: the Kanban tab and the factory wording that other pending changes touch are not in this branch, so the change uses the tab bar and `steeringWord` as `main` has them; a rebase onto those changes is expected to conflict only textually in `batch.js`, `batch.css` and `docs/web-board.md`.

## Known gaps

- **UNVERIFIED:** before/after pictures and the tip-stacking measurements (a tip drawn whole above the figures' tiles; no horizontal scroll at 375 px) are not yet produced.
- The docs screenshots are not retaken yet.

<details>
<summary>Details</summary>

## Changes

- `index.html`: a hidden `#batch-mode` slot in `.titlerow`; `js/main.js` paints it with `batchMode(state)`.
- `js/views/batch-head.js` (new): the mode pill, legend and switch moved out of `js/views/batch.js`.
- `css/views/batch.css`, `css/batch-nav.css`: the moved rules re-scoped under `.bmode`, the pills' tip rules, the phone block.
- `DESIGN.md`, `docs/web-board.md`: a section on the title row; the legend now sits in the title row.
- `tests/test_board_design.py`: one parametrized test reading the shipped files.

## Human decisions

- Everything goes into the title row; the breadcrumb row and "+ New" stay untouched, and the switch follows its band at the row's right end.
- The mode's sentence is a tooltip alone, at every width, with no short form.
- Both pills show a help cursor.
- On a phone the legend's hint is hidden and the two pills stay.

## Impacts

The Batch page is shorter above its views; the mode sentence is a tooltip instead of an inline line.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates
- [ ] Evidence
- [ ] Review
- [ ] Verified
- [ ] CI green

## Internal references

CR-435 board-batch-compact.

</details>
