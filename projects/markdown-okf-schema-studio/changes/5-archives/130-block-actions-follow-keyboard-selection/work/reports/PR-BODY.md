## Summary

In edit mode, the block actions (the "+", move-up and move-down buttons) could stay on the block
last hovered by the mouse while the keyboard selection had moved to another block, so two blocks
looked active at once. The actions now show on one block only: the one whose input moved last
(keyboard selection or mouse hover). A mouse move hides the selection ring; a keyboard selection
move hides the hover. Move up / down act on the block the actions are shown on.

## Deliverables

Before (selection ring on one block, actions left on another) and after, in a real VS Code window.
Keyboard moved last, then mouse moved last:

| Before | After |
| --- | --- |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/before-keyboard-moved-last-cream.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/after-keyboard-moved-last-cream.png) |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/before-keyboard-moved-last-dark.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/after-keyboard-moved-last-dark.png) |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/before-pointer-moved-last-cream.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/after-pointer-moved-last-cream.png) |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/before-pointer-moved-last-dark.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/684dc07ae22e9846eb35e845e5c258e409e771a2/after-pointer-moved-last-dark.png) |

```text
root[data-sphinx-preview-actions-owner] = keyboard | pointer
keyboard -> actions under the selection, pointer -> selection ring hidden
```

## Changes

- Page runtime tracks the last mover on the preview root and styles the bar and ring from it.
- Requirement BLOCK-109 and its log entry updated; user guide (`docs/user/editing.md`) documents it.

## Impacts

Edit-mode block selection and block actions only. Cream and dark themes verified.

## Blast radius

1 (page-side edit-mode focus and styles).

## Test plan

- New unit test and style test; new real-window e2e (`blockActionsFollowSelection`) that fails on
  the previous code and passes now.
- `just check`: unit 2767/2767, contracts 2/2, security 48/48, Python 31/31 pass. The last step
  (`requirements-lint --check-links`) fails on this machine because the installed `okfreq` lacks
  that option; it fails the same way without this change.

## Autonomous decisions

- Whichever moved last (keyboard selection or mouse hover) owns the block actions; the other
  indicator goes away.
- Stacked right above the keyboard-navigation fix, which touches the same focus code.

## Internal references

CR 130 (block-actions-follow-keyboard-selection); depends on CR 129.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
