## Summary

A heading too long for the sticky heading band used to wrap onto a second line. At 130 to 160 % zoom with a sticky depth of 1, the band grew taller than configured and covered the first line of the section under it. Each heading level now stays on one line, cut with an ellipsis.

## Deliverables

Before and after, in CSS of the `[data-sphinx-preview-sticky-headings]` band:

```css
/* before */ white-space: pre-wrap; overflow-wrap: anywhere;
/* after  */ white-space: pre; overflow: hidden; text-overflow: ellipsis;
```

The band stays one text node with one line per level, so nothing in `stickyHeadings.ts` changes. The band still ignores the pointer; the full title stays readable in the heading and in the table of contents.

## Changes

- Band style in `pageChromeStyles.ts`.
- Visual checks: `expectStickyGrowth` becomes `expectStickyEllipsis` (one rendered line per level, ellipsis style, text cut); new `expectSectionStartVisible` (the first block of the section starts at or below the band).
- New visual scenario (160 % zoom, Cream, depth 1) with its own fixture, in a new file because `scenarioDefinitions2.ts` hit the file size limit. The scenario-count test goes from 473 to 474.
- Requirements: SwRS TOOLBAR-025 and StRS TOOLBAR-004 amended, log entry, changelog line.

Changed assertions and why:
- `previewStyles.test.ts` (band style): `pre-wrap` and `overflow-wrap: anywhere` become `pre`, `overflow: hidden`, `text-overflow: ellipsis`, no `overflow-wrap: anywhere`. The band no longer wraps.
- `check_sticky_headings`: the "does not expand beyond one line per level" growth check becomes the ellipsis check, with rendered lines equal to levels shown.
- Floating-controls overlap checks (`check_final_frame`, `check_sticky_headings`): text rectangles are clamped to the band's visible text edge, because with `overflow: hidden` the full rectangles run past the clipped edge and failed falsely. Text drawn over the toolbar is still caught.
- Scenario v05: now proves the ellipsis (new slug and wording); `expectedStickyHeadings` keeps the full text.
- SwRS TOOLBAR-025: scenario "Long heading path wraps" replaced by "Long heading cut with an ellipsis".

## Impacts

Before (v05 at 460 px, depth 3: the band wraps over many lines):

![before](./before-v05-sticky-wrapped-growth-dark-460.png)

After (v05: one line per level, cut with an ellipsis):

![after v05](./after-v05-sticky-long-path-ellipsis-dark-460.png)

After (new scenario, 160 % zoom, Cream, depth 1: one line with an ellipsis, the section stays visible):

![after v44](./after-v44-sticky-long-title-zoom-160-cream-900.png)

## Blast radius

Grade: **1**. One CSS rule and its tests; a plain `git revert` restores wrapping.

## Autonomous decisions

- The scenario-count assertion in `e2eGroups.test.ts` was raised by one, and the overlap-check clamping was added; neither was in the specification.
- The new scenario lives in `stickyLongTitleScenarios.ts` (file size limit).

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Local gates: `just check`, `just requirements-lint`, visual toolbar-navigation group
- [x] Review
- [x] CI green

## Internal references

CR-311 sticky-heading-long-title-wraps (batch-02).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
