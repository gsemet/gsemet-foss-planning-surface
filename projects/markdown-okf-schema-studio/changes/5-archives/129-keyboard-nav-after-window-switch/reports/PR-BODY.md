## Summary

In edit mode, after leaving the window (or clicking the page margin) and coming back, the whole
preview page took the focus ring and Up/Down only scrolled the viewport instead of moving the block
selection. Keyboard navigation now keeps working, and the page itself never shows the focus ring.

## Deliverables

- The preview content root is treated as "the page" by the Up, Down, Enter and Shift+Arrow handlers,
  so a key pressed while it holds the focus moves the block selection.
- On window `focus` and `visibilitychange`, in edit mode with no editor open and the page holding
  the focus, the selection is restored: active selection, else last keyboard-selected block, else
  the block nearest the top of the viewport.
- The content root no longer draws a focus outline.

Before (whole page ringed) and after (only the selected block outlined), cream and dark themes:

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/f38f1ae703e0fce9f6f9b13f6ca12e6c1a029cc9/after-return-margin-before-cream.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/f38f1ae703e0fce9f6f9b13f6ca12e6c1a029cc9/after-return-margin-after-cream.png) |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/f38f1ae703e0fce9f6f9b13f6ca12e6c1a029cc9/after-return-margin-before-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/f38f1ae703e0fce9f6f9b13f6ca12e6c1a029cc9/after-return-margin-after-dark.png) |

## Changes

- `src/page/features/blockSelectionView.ts`: key target check, focus/visibility restore.
- `src/core/preview/styles/contentLayoutStyles.ts`: no outline on the content root.
- Tests: 5 unit tests (4 fail on the old code), real-window e2e `windowSwitchKeys` (margin click and
  other-editor-tab routes, both themes; fails on the old code).
- Requirement BLOCK-004, requirements log, user docs and changelog updated.

## Impacts

Edit-mode keyboard navigation only. Screenshots above.

## Blast radius

1 (page-side selection code and one CSS rule).

## Test plan

- `just check`: all steps pass (unit 2770/2770) except `requirements-lint`, which could not run locally (stale `okfreq` environment lacking `--check-links`); to be confirmed in CI.
- Real-window e2e `windowSwitchKeys` passes in cream and dark after the change, fails before.
- Limit: a real switch to another application cannot be driven from the test window, so that leg is covered by unit tests dispatching the window `focus` event.

## Autonomous decisions

- On focus return in edit mode the block selection is restored (last selected block, else the block nearest the top); the page itself never takes the block focus ring.
- Screenshots come from the margin-click route, since the content root could not be made to take focus on a tab return alone.

## Internal references

CR 129, backlog item `bug-keyboard-nav-lost-after-window-switch`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
