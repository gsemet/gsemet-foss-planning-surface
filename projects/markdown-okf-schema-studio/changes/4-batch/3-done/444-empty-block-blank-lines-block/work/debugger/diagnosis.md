# Diagnosis: ci-visual red at ccf9ff75 (CR-444)

## Reproduction
- CI: run 44859320198, log `work/ci-44859320198.log`. Local: `just ci-visual` (needs Linux/Chromium; not run in full here).
- Minimal probe (run): `uv run --no-sync python -I work/debugger/probe.py`
  - without marker: scrollY 6232, `#content > :last-child` box {y:542,h:18}
  - with `<div hidden data-okf-blank-runs="">` last: scrollY 40, box None

## Cause
`blankRunsMarker()` (src/core/render/renderPipeline.ts:241,254-257) now appends
`<div hidden data-okf-blank-runs="...">` to EVERY render, even with no runs, as the last child of
`#sphinx-myst-preview-content`. It is `display: none`. The visual harness assumes the last child is real content:
1. `test/visual/capture_page_checks.py:40` (scroll kind "bottom"): `main.lastElementChild.scrollIntoView({block:'end'})`.
   On a display:none element this does nothing, so the page never scrolls to the bottom (only `scrollBy(40)`).
   Bottom screenshots (v03, v10, v20, myst v05, review v01 ...) then show the wrong frame: the "failed:" lines.
2. `test/visual/capture_final_checks.py:386`: `#content > :last-child` bounding_box() is None for a hidden element:
   "last content or bottom padding is missing from final frame: None" (8 pages, see log lines 581-588).
3. v20 assertion "last paragraph lies inside the viewport" (scenarioAssertions.ts:109) fails as a consequence of 1 (not scrolled).
Not CSS: no margin/spacing change (rule `[data-okf-blank-runs]{display:none}`); no page last-element logic in src/ uses last-child on the content root.
block-editing v09/v10 and review v01 are the same "bottom"/final-frame path (scroll to the end, then last-child check).

## Base
Base 6154eb1b has no `data-okf-blank-runs` anywhere in src (`git grep`), and its CI runs 44850923095/44850923505 are success.
So these scenarios pass on the base; the regression comes from commit 67ecf991 (marker introduced).

## Place to fix (no fix made)
Test side (simplest, the marker is by design the last element): in capture_page_checks.py:40 and capture_final_checks.py:386
use the last VISIBLE child, e.g. `main.querySelector(':scope > :not([data-okf-blank-runs]):last-of-type')` is wrong for mixed types;
better: `[...main.children].filter(e => !e.hidden && !e.hasAttribute('data-okf-blank-runs')).pop()`
(Playwright: `#content > :nth-last-child(2)` only when the marker exists; prefer the JS filter).
Alternative product side: emit the marker only when runs exist (still breaks pages with runs) or place it outside the content root.
Grep other harness users of lastElementChild/last-child on the content root after the fix.
