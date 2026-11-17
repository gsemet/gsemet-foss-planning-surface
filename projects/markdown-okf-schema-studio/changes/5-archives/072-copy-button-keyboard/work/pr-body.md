## Summary

The Copy code button of a code block appeared only when the pointer was over the block, so a
keyboard or screen-reader user could not copy code. The button is now reachable with Tab.

## Deliverable showcase

```text
Tab        -> code block gets a focus ring, "Copy code" button appears in its corner
Tab        -> focus moves to the button (focus ring)
Enter/Space-> raw code copied, button shows the check mark ("Copied")
Shift+Tab  -> back to the block
focus away -> button hidden
```

Two new visual scenarios (light and dark) show the focus state.

## Changes

- Copyable code blocks get `tabindex="0"` (reapplied after each live content patch); blocks being
  edited, block editors and diagram sources are skipped.
- `focusin` on a block shows the button; Tab and Shift+Tab move between block and button;
  `focusout` hides it. A scroll that settles keeps the button while the block or button has focus.
- Focus ring styles for the block and the button.

## Impacts

Keyboard and screen-reader users can copy code. Pointer behaviour is unchanged; code blocks are now
tab stops. See the two new visual scenarios for the focus state in light and dark.

## Blast radius

Grade: 1. Local to the copy button module and its styles; `git revert` restores the previous behaviour.

## Test plan

- [x] New unit tests for tab stop, focus reveal, Tab/Shift+Tab, keyboard copy and scroll settle
- [x] Requirements: code-blocks SwRS updated (Known issue removed, keyboard scenarios added), StRS
      updated, `just requirements-update`
- [x] Local gates: `just check` (2601 unit tests, contract, security, requirements lint), `just ci-visual` (2 new scenarios)
- [ ] Review
- [ ] CI green

## Internal references

- CR 072 (copy-button-keyboard)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
