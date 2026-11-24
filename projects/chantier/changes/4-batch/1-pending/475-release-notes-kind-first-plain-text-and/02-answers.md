Short name: `release-notes-style`

1. release-notes-style-Q1: **Scope.** A: this CR changes chantier's `release-template.md` card. The amendment of the OKF repo's guideline (it ranks above the card) is filed into that project's inbox, for its own Chief of Staff; this CR does not touch it.
2. release-notes-style-Q2: **A fix with no image.** B (the user did not take the recommended A): the Release Driver captures the image itself, with the project's own capture means, before the notes are final.
3. release-notes-style-Q3: **Reading images.** A: the Release Driver reads each image it produced; `driver.md` names this as an exception to "a Driver never opens an image".
4. release-notes-style-Q4: **Mechanical refusals.** A: this CR changes the card only; the refusals (title version, word budgets, banned phrases, image size, empty fold) go in a separate CR on each project's `scripts/release_notes.py --check`.
5. release-notes-style-Q5: **Capture impossible.** B (not the recommended A): the Release Driver publishes without the image and names the gap in the version PR's Known gaps ("no picture for <change>: <why>"); the note says nothing about it. Q2 B still holds: it tries the project's own capture means first.
6. release-notes-style-Q6: **Patch that needs feature wording.** A: the note takes the tone of the real kind; the version PR says the version is probably wrong, and the user decides.
7. release-notes-style-Q7: **Word budgets.** A: the audit's figures, as judgement in the card: subtitle 16 words, item 20, highlight 40, visible part 120 (fix, restore, internal) or 250 (feature).
8. release-notes-style-Q8: **Grilled enough.** B (not the recommended A): specify, for the running batch batch-31.
Destination: running batch batch-31.
9. release-notes-style-Q9: **docs/release-process.md.** A: this CR aligns its three lines with the card (highlight headings by kind, line 47; known issues out of "For contributors" into the visible part, lines 53-54; the title with the full version, line 38). A doc change, no script change.
10. release-notes-style-Q10: **An image outside the bounds.** A: counts as "capture impossible" (Q5): no image, a line in the version PR's Known gaps.
11. release-notes-style-Q11: **Mixed kinds, breaking budget.** A: the subtitle names the first kind in the order breaking, feature, restore, fix, internal; a breaking release's visible part is 250 words at most.
12. release-notes-style-Q12: **No version PR.** A: the missing picture is named in a `note` and in the hand-back report.
13. release-notes-style-Q13: **Line 39 of docs/release-process.md.** A: this CR aligns it too: the header line names the kind first, then the main changes in that kind's words, not "as verbs".
