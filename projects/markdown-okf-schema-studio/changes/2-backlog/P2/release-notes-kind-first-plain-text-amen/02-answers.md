Short name: `notes-kind`

1. notes-kind-Q1 (2026-11-24): **Grill stopped by the owner.** The CR stays in the backlog (P2), ungrilled; it does not join batch-09. Open points for a later grill: the shape of a patch note, mechanical checks in `release_notes.py --check`, the image bounds against CR-482's clip-GIF exception, the reach of the 1.12.1 rewrite.
Destination: backlog P2.

2. 2026-11-27, owner: « et tu mettras release-notes-kind-first dans le batch aussi » (the batch then running, batch-11). The grill resumes.

Destination: running batch batch-11.

## Facts read before the grill resumed (2026-11-27, not decisions)

- chantier's CR-475 (`release-notes-kind-first-plain-text-and`) merged on 2026-11-24: its `release-template.md` card holds the five kinds, the labelled lines, the word budgets (as a judgement, no script check) and a ten-question self-check.
- This project's guideline still asks for the title `X.Y`, a subtitle of verbs and « what you can now do » headings; it already holds the clip GIF exception to cropping.
- `scripts/release_notes.py --check` checks only that the title names `X.Y` and that each image sits next to the notes.
