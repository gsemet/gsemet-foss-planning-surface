Short name: `notes-kind`

1. notes-kind-Q1 (2026-11-24): **Grill stopped by the owner.** The CR stays in the backlog (P2), ungrilled; it does not join batch-09. Open points for a later grill: the shape of a patch note, mechanical checks in `release_notes.py --check`, the image bounds against CR-482's clip-GIF exception, the reach of the 1.12.1 rewrite.
Destination: backlog P2.

2. 2026-11-27, owner: « et tu mettras release-notes-kind-first dans le batch aussi » (the batch then running, batch-11). The grill resumes.

Destination: running batch batch-11.

## Facts read before the grill resumed (2026-11-27, not decisions)

- chantier's CR-475 (`release-notes-kind-first-plain-text-and`) merged on 2026-11-24: its `release-template.md` card holds the five kinds, the labelled lines, the word budgets (as a judgement, no script check) and a ten-question self-check.
- This project's guideline still asks for the title `X.Y`, a subtitle of verbs and « what you can now do » headings; it already holds the clip GIF exception to cropping.
- `scripts/release_notes.py --check` checks only that the title names `X.Y` and that each image sits next to the notes.

## Series 1, 2026-11-27, owner

- `notes-kind-Q2` (shape of a fix release's note): « Même structure » : today's structure, the headings in the tone of the kind (« Fixed: … » in a fix release, never « what you can now do »), as chantier's card.
- `notes-kind-Q3` (script checks): « Non » : the agent's own reading only; `release_notes.py --check` is not extended.
- `notes-kind-Q4` (clip GIFs and the new image sizes): « Dispensés » : clip GIFs are exempt from the sizes, as they already are from cropping.
- `notes-kind-Q5` (rewrite of the 1.12.1 note): « Pas de réécriture » : only the rule changes. This replaces the request's « The 1.12.1 note itself also needs a rewrite ».
- Told to the owner with the series, with no objection in the answers: the guideline also gets the rule the owner gave for 1.13.0 (« il faut mettre en avant que le rendu est plus rapide dans la release note », figures estimated if need be): a performance gain the user can see is a highlight with figures, never only a folded line.

## After the first specification, 2026-11-27

- `notes-kind-Q6` (owner; the hero image in the release notes): « Post X seul » : the hero image serves post 1 of the announcement thread only; the first highlight of the notes takes a picture cropped within the new bounds.
- Chief of Staff, routine gap: in a fix release the smaller changes are headed `## 🛠 Other fixes`, as the specification has it.

- Spec critic: no (a project guideline only, aligned on a card already checked and merged in chantier; a wrong point is fixed by an edit, no product behaviour).
