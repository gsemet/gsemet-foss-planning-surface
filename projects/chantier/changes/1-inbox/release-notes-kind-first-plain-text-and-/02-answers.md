Short name: `release-notes-style`

1. release-notes-style-Q1: **Scope.** A: this CR changes chantier's `release-template.md` card. The amendment of the OKF repo's guideline (it ranks above the card) is filed into that project's inbox, for its own Chief of Staff; this CR does not touch it.
2. release-notes-style-Q2: **A fix with no image.** B (the user did not take the recommended A): the Release Driver captures the image itself, with the project's own capture means, before the notes are final.
3. release-notes-style-Q3: **Reading images.** A: the Release Driver reads each image it produced; `driver.md` names this as an exception to "a Driver never opens an image".
4. release-notes-style-Q4: **Mechanical refusals.** A: this CR changes the card only; the refusals (title version, word budgets, banned phrases, image size, empty fold) go in a separate CR on each project's `scripts/release_notes.py --check`.
