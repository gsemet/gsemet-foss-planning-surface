# CR 230 round 1: Inspector review

Commit reviewed: 5c08be99 (wip) on origin/main acfbec73, worktree markdown-okf-schema-studio-wt-230.

VERDICT: APPROVE

## Correctness

- The restore runs last in `update()` (src/page/modules/widthMode.ts:180), after `removeAttribute(measuring)`
  (:170) and the wide mark, breakout and shift writes (:175-177). The old scrollLeft is read before `clear()`
  (:111-114), so it is the value the reader saw, before any uncap.
- Clamp: `Math.max(0, Math.min(left, scrollWidth - clientWidth))`, and a write only when it differs (:102-103).
  The value cannot go negative, and nothing is written when the browser kept the offset.
- Coverage of scroll boxes: the measuring CSS uncaps `> :where(table, .table-wrapper)` (contentLayoutStyles.ts:259).
  `scrolledBoxes` records each wrapper plus every `table, pre` inside it, which covers a table inside a
  `.table-wrapper`. Ineligible wrappers (editor open, relative-size figure) are not recorded, which matches
  "elements under edit untouched".
- Margin and Full: `wrappers` is `undefined` outside Auto, so the code reads and writes nothing; the behaviour is
  unchanged. The figure-holder pass is unchanged.
- Scroll handlers: an element scroll does not bubble to the non-capture window listener of scrollCore
  (scrollCore.ts:569), so a restore cannot start another layout pass. The capture listener in tableRowMove.ts:569
  only repositions the handles, which is wanted. A restore writes only when the browser had reset the offset,
  and that reset already fired a scroll event. No loop.
- Eligibility is now computed before `clear()`. It reads only the editing attribute, textarea and `data-okf-width`,
  none of which `clear()` touches, so the set of wrappers is the same as before.

## Gates (this base, out/ rebuilt)

| Gate | Result |
|---|---|
| `npm run compile` + runtimePageControls unit file | exit 0, 44/44 pass (T10b pass) |
| Same, with acfbec73 widthMode.ts | exit 1, 43/44, T10b fails `0 !== 300` |
| bundle + renderFixtures + capture v91 | exit 0, 1 scenario passed, 1 screenshot |
| Same, with acfbec73 widthMode.ts | exit 1: pass 1 `1670 -> 0 (max 1634, frames [1670, 1670, 0, ...])`, pass 2 `1634 -> 0` |
| `just check` (check-i1.log) | exit 0; node 3507/3507 and 73/73, pytest 153 passed, okfreq 1081 req, 0 errors, 26 warnings |
| `okfreq validate --check-links` (okfreq-i1.log) | exit 0, 0 errors, 26 W2 broken-link warnings, none in LAYOUT-023 (all from before this CR) |

The old file was restored with `git show HEAD:... >|`, and `git status --short` was empty afterwards.

## Requirements and collisions

- SwRS-MDOKFSTUDIO-LAYOUT-023 is `req_lifecycle: proposed` before and after. It is the only requirement file
  touched. The new scenario (same pixel offset, clamped, not proportional) matches the code. The verification
  notes and criteria were updated, and `tested_in_files` lists the two new test files.
- Markers: `@implements_req` on `restoreScroll` and `update`, and `@tests_req` on T10b, capture_width_scroll.py
  and widthScrollScenarios.ts.
- e2eGroups: 428 -> 429. v91 is used once.

## Findings

1. Non-blocking (performance), src/page/modules/widthMode.ts:111-114. Reading `scrollLeft` before `clear()`
   forces a layout flush when layout is dirty. `clear()` and the figure writes then invalidate it again, so
   `content.clientWidth` (:140) forces a second flush. This means one extra forced layout per `update()` in Auto
   (the update runs on every content patch). The extra reads are bounded: `scrollLeft` per wrapper and per
   descendant table/pre, and `scrollWidth`/`clientWidth` only for boxes with scrollLeft > 0. The read has to happen
   before the uncap, so I accept this. No change needed. If profiling of a long document ever shows a cost, skip
   the scan when no wrapper has a descendant or self that can scroll (for example, cache the overflow state from
   the last pass).
2. Non-blocking (test strength), test/page/runtimePageControls.test.ts T10b, ScrollingTable. The fake has
   `clientWidth = 0` (runtimeHarness.ts:72), so `restoreScroll` always computes `min(300, 1600)`. The
   "clamp to the new max" branch and the "no write when equal" branch are never exercised in the unit test, and
   the fake's own setter clamps anyway, so a broken clamp in `restoreScroll` would go unnoticed here. The real
   clamp is covered by v91 pass 1 (1670 -> 1634 kept at max). Fix: give `ScrollingTable` a `clientWidth` getter
   that returns `boxWidth()`, and add a case where the offset is past the new maximum and the expected value is
   that maximum.
3. Non-blocking (test method), test/visual/capture_width_scroll.py:17-33. Pass 1 sets scrollLeft
   programmatically from a MutationObserver at the moment the editor leaves the DOM (forced timing), rather than
   with real input. This is justified: repro-measures.md shows that the Playwright round trip lands after the rAF
   in headless (0/5), while the MutationObserver timing reproduces the slow CI frame (5/5). The comment in the file
   documents it. Pass 2 uses a real viewport resize. There is no retry loop, no raised timeout, and the assertions
   are not weakened (2 px tolerance against min(set, max)). Both passes fail on the old code.

No blocking findings.
