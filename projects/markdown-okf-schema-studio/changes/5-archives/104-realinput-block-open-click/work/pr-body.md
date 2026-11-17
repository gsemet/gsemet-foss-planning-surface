## Summary

The manual heavy CI job (real VS Code window) fails in its `integration` stage at the typing and
undo scenario: "Timed out waiting for the block editor to close before the undo". The scenario types
in a paragraph and then clicks a heading to leave it. Since a click on another block opens that
block once the first save has rendered, the heading now opens its own editor, and the scenario
waited for no editor to be open. The scenario now closes that editor with Escape before it checks
that one undo restores the paragraph. No product code changes.

## Deliverables

```text
before: type in paragraph -> click heading -> [heading editor stays open] -> wait for no editor (timeout)
after:  type in paragraph -> click heading -> heading editor opens -> Escape -> one undo restores the paragraph
```

Evidence of the cause (heavy CI, same branch, only this commit differs): with the block-open change
reverted the `integration` job passes; with it, and without this test change, the job fails at that
scenario.

## Changes

- `test/integration/realInput.test.ts`: the typing and undo scenario waits for the heading's editor and
  closes it with Escape; a small `escapeBlockEditor` helper replaces eleven copies of "press Escape,
  wait for no editor" so the file does not grow (the size ratchet only allows it to shrink).
- Verification note of the block-editor requirement and the update log name the scenario.

## Impacts

Test only. The scenario's intent (typing is one undo step) is unchanged.

## Blast radius

Grade: 1 (one integration test file and requirement text; a plain `git revert` restores it).

## Test plan

- [x] New or changed tests: the typing and undo scenario; the heavy CI `integration` job is the check
- [x] Requirements: verification note of the block-editor requirement and update log; `okfreq` clean
- [x] Local gates: `just check`
- [ ] Review
- [ ] CI green (heavy integration run linked in the final comment of this PR)

## Internal references

CR 104; regression came with the click-opens-after-save change (576d768).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
