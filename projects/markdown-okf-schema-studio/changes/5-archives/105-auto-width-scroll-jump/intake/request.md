# 105 — Auto width: preview jumps back when scrolling past wide tables

## Intent

User report: on `.agents/changes/03-requests/ORCHESTRATOR.md`, in Auto width with edit mode on,
the preview pulls the scroll back to the top as soon as the user scrolls; resizing the window
sometimes makes it go away.

## Root cause

A wide table with row handles flip-flopped every frame between "broken out" and "row-shift
capped". Each flip fired the ResizeObserver → `stabilizeLayout` → `applyAnchor`, which restored
the scroll anchor.

## Fix

- `src/page/modules/widthMode.ts`: a wrapper with row handles breaks out only up to
  `pane - reserved - 2 × handleGutter`.
- `src/core/preview/styles/contentLayoutStyles.ts`: the measuring rule lifts every cap
  (`max-width: none !important`).
- SwRS LAYOUT-023 updated, unit tests added.

## Decisions

- Fixed directly in the session (no grill), commit `82bc0a5`.
- No screenshots: the fix is a scroll behaviour, not visible on a still image.
