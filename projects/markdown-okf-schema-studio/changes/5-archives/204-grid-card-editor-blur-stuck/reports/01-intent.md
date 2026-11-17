# Block editor in a grid card sometimes does not close on blur; the page stays stuck

GitHub issue #227 (filed 2026-10-31). While editing a card of the #225 grid, clicking outside the
block editor did not save and close it; the page stayed in edit mode, Done/Cancel partly hidden by
the palette. Not reproduced deterministically.

Suspects: focus moving into the palette that overlaps the text box (#225), or the blur commit
suspension.

Owner decisions (2026-10-31):
- Reproduce first, in a real window (heavy CI) and headless, on the issue's grid document.
- Blur outside the editor (text box AND palette) must always save and close it.
- BLOCK-047 stays: a whole-window blur commits and closes (owner decision 2026-10-29).
- If not reproducible once the #225/#226 layout fix is in, report the attempts; no speculative fix.
