## Summary

Three small defects in block editing and the citation picker: AltGr plus an arrow key was read as
the block-move shortcut on some keyboard layouts, the check that refuses a paste next to an included
block ran only in the page, and the citation list claimed more entries existed when exactly 20
bibliography files were found.

## Deliverables

```text
AltGr + Up/Down in the block text box   before: block moves   after: caret moves (native)
paste after the closing fence of {include}   before: host accepts   after: host refuses
exactly 20 .bib files                   before: "More entries exist"   after: complete list
```

## Changes

- `blockMoves.ts`: the move chord ignores key events that report the AltGraph modifier.
- `sourceEdits.ts`: `checkBlocksPaste` refuses a paste after any line from the opening fence to the
  closing fence of an `{include}` directive, not only its opening line.
- `bibScan.ts`: the search asks for one file more than the cap (21) and marks the list truncated only
  when that extra file exists.
- Requirements BLOCK-127, BLOCK-130 and PALETTE-183 state the new behaviour; their Known issue lines
  are removed.

## Impacts

No visual change. AltGr layouts keep word-free caret movement in the editor; a complete list of 20
bibliography files no longer shows the "More entries" note.

## Blast radius

Grade: 1. Three isolated checks; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New tests that fail on the previous code (verified by stashing `src`): AltGr chord, paste after
      the closing fence (backtick and colon fences), exactly 20 versus 21 bibliography files. No
      existing assertion changed intent; the BLOCK-127 paste test gained assertions.
- [x] Requirements: SwRS updated, markers in tests, `okfreq` validate, lint and update-coverage clean
- [x] Local gates: `just check` green; unit, page, core and session suites 2430 passed, 0 failed
- [ ] Review
- [ ] CI green

## Internal references

- CR 097 (block-editing-small-fixes); SwRS BLOCK-127, BLOCK-130, PALETTE-183.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
