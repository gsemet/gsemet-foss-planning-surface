# In edit mode a click on the footer of a link card leaves the document, and typing then lands in the target file

Severity High · Reproduced · Verdict Bug · Requirements: none found for the footer (header of the same card is covered by the c1-1 finding; SwRS-MDOKFSTUDIO-BLOCK-258 boundary says a linked title follows the link) · Area Grid cards · Side preview ·
c3-1 · Replay `scenarios/c3-1-link-card-footer-click-navigates.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/c3-1-currently.jpg) | In edit mode the footer opens its editor, as the header of the same card does (c1-1). |

Expected has no image: it needs a second clean window; the working case is the header of this card (`c1-1-link-card-not-editable.json`).
Measured: after the click the preview shows "Alpha target" (the `:link:` target), no textarea exists.

## Why this is wrong

In edit mode a click on text means "edit this". The footer of a `:link:` card in `fixtures-visual/46-grid-cards.md` instead follows the card's stretched link. The author, who expects an editor, types " F": the text goes into the front-matter editor of the target file `targets/alpha.md`, whose buffer becomes dirty with `--- F` as its first line (spy: `-1 +2 at L1, dirty`). A second file is silently damaged, in the file the author never meant to touch.

## Steps to reproduce

1. Fixture `fixtures-visual/46-grid-cards.md`, open the preview to the side, edit mode on.
2. Click the text "Footer of the card" in the "Linked card".
3. Type " F" and End: the target document's front matter receives it.

## Impact

A mis-navigation plus stray typing corrupts another document without any warning.

## Suggested direction

- (x) Treat the footer (and any `+++` part) of a link card like its header: a click opens the editor, Cmd/Ctrl-click follows the link
- ( ) Keep the link, but never let a navigation triggered in edit mode focus an editable field of the target

Uncheck to disagree: [ ]

## Test to add

Real-input E2E: edit mode on, click the footer of a link card, assert a textarea is open and the active file is unchanged.

Uncheck to disagree: [x]

## Done when

- [ ] The footer click opens an editor on the card's footer line.
- [ ] The replay scenario passes.
