# T18 review — round 2

Base: fa73a7f · Reviewed diff: 7 T18 files (scrollSync.ts, previewStyles.ts, scrollSync.test.ts,
previewStyles.test.ts, realInput.test.ts, scenarios.ts, capture.py)

## Gates
compile/unit/types: PASS. trusted: PASS (55 s, includes RI-T18). visual: PASS vs T00 baseline, 0 new
failure lines, 4 baseline lines now pass. The strict capture check is active in this run. The report
shows it failing against the round-1 code (2 new lines, 08-okf-schema dark/light).

## Done-when
- [x] Toolbar in flow above the table, labels, status text: unit tests, RI-T18, screenshots.
- [x] Selected cell outlined: `edit-table-wrapped-light-460.png` (2px blue outline), capture.py check.
- [x] The toolbar is fully visible when it appears (UX-14 amendment). In `edit-table-wrapped-light-460.png`
  the bar sits below the band and the controls pill. All four labels are readable, and the status
  wraps ("Saving Markdown…") without hiding it. capture.py checks this per button with
  `elementFromPoint` and with `barTop >= usableTop - 1`.
- [x] 900 px: unchanged from round 1, gate PASS.

## Protected features checked
- P-E5 (table operations): handlers unchanged. The existing table tests pass in the unit gate.
- R7 / scroll sync: the re-reveal in `applyAnchor` runs only inside the `editAnchor?.element` branch,
  and only when `activeBlockEdit.tableMenu` and `selectedCell` exist and the measured bar height
  differs from `edit.tableMenuHeight`. With no table edit open, it is a no-op. During normal scrolling
  and cell switches that keep the bar height, it is also a no-op. When it does run, the reveal uses
  `programmaticScroll`, so `expectedScroll` drops the event and the source editor does not move. It
  scrolls only up, only by the missing amount, and only if the selected cell stays in the viewport.
  `editAnchor.viewportTop` is updated, so the next `applyAnchor` does not undo the reveal. A unit
  test covers this: one reveal, then an unchanged-size pass that does not move the page. The
  `anchor` line is refreshed (round-1 MINOR 3 fixed).
- P-E8: the toolbar exists only in the edit path. P-S4: labels use `textContent`.
- conventions §2: the new runtime code has no backticks, no `${`, and no global `setTimeout`.
  Browser APIs use optional calls.

## Findings
1. [MINOR] scrollSync.ts:applyAnchor — when a cell switch changes the status wrap (for example from
   "Header · …" to "Row n of m · …"), the bar height changes and the page can scroll up a few pixels.
   This happens only when the bar is under the band, so it is the intended behaviour. No change is
   required. Optional follow-up: add a unit test where a cell switch leaves the bar height unchanged
   and assert `scrollY` stays put.
2. [NIT] capture.py: `controlsBottom` is still returned but unused. The per-button hit test covers
   the controls overlap, so this is harmless.

Round-1 BLOCKER 1 (strict capture check) is fixed. BLOCKER 2 (bar hidden at 460 px) is fixed.
MINOR 3 and NIT 4 are fixed.

## Existing assertions changed
- Same as round 1 (all OK). capture.py "aligned with its active cell" now has the usable-top check
  and the per-button hit test, which makes it stronger than the original. OK.

VERDICT: PASS
