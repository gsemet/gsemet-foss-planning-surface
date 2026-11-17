## Summary

Three small defects of the pinned heading band, the table-of-contents fold buttons and the
"mark editor selection" outline made the preview point at the wrong thing: a collapsed heading
appeared as a parent in the band, the band listed headings that the table of contents never shows,
a folded entry still read "Fold", and a cursor in a long block outlined the next block.

## Deliverables

The band and the outline now follow the same rules as the table of contents and the text editor.

```text
Band, before:  # Title / ## Collapsed (height 0) / ### Part      (note headings also followed)
Band, after:   # Title / ### Part                                 (running text only)

Fold button:   "Fold Setup" in both states  ->  "Fold Setup" open, "Unfold Setup" folded

Outline, cursor on line 17, code block on lines 7-20, paragraph on line 22
  before: the paragraph (line 22 is nearer to 17 than line 7)
  after:  the code block (it contains line 17)
```

![Cursor in a long code block, light](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/d2981bdeeacaa5b99b1b227469c58e6dd57e8a3f/v37-mark-containing-block-light-900.png)
![Cursor in a long code block, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/d2981bdeeacaa5b99b1b227469c58e6dd57e8a3f/v38-mark-containing-block-dark-900.png)
![Sticky band with a heading inside a note, light](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/d2981bdeeacaa5b99b1b227469c58e6dd57e8a3f/v39-sticky-running-text-light-900.png)
![Sticky band with a heading inside a note, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/d2981bdeeacaa5b99b1b227469c58e6dd57e8a3f/v40-sticky-running-text-dark-900.png)

## Changes

- Sticky band: headings without height and headings inside admonitions or the properties table are
  skipped when the band is built, so they are neither the current heading nor a parent line.
- Table of contents: the fold button's accessible name follows the state (Fold / Unfold).
- Editor-selection mark: the block that contains the cursor line wins (the innermost one when
  blocks nest); a line between blocks takes the block with the nearest edge.
- Requirements: three Known issue lines removed and the matching scenarios reworded or added in the
  toolbar scope; the toolbar-over-text note is unchanged on purpose.

## Impacts

Visible: the outline on a cursor in a long block (screenshots above, light and dark) and the
band that ignores a heading inside a note (v39 light and v40 dark scenarios; the band shows
"# Fleet handbook / ## Overview" while the reading line is in the note's own heading). Existing
assertion changed: the band test that expected a heading inside an admonition to appear now uses a
heading in a normal section, because the requirement is the opposite (those headings are no longer
followed); the test name changed too.

## Blast radius

Grade: **1**. Three local functions in the page runtime; a `git revert` restores the old behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): unit tests for the zero-height parent, admonition headings, Fold/Unfold name and containing block fail on the old source and
      pass now; 6 new unit tests in all (also: a line between two blocks, nested blocks); 4 new visual scenarios (cursor block and band, light and dark)
- [x] Requirements: SwRS toolbar 018, 040, 128 and three StRS updated, markers kept,
      `just requirements-update` run (validate, lint, coverage clean)
- [x] Local gates: `just check` (2673 unit tests, contract, security, requirements) and
      `just ci-visual` (363 scenarios, 252 screenshots) pass
- [ ] Review
- [ ] CI green

## Internal references

- Change request 102 (toolbar-band-fixes); decision: the toolbar over the text and the find widget
  is ignored and its Known issue stays.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
