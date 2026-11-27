# Release notes: kind-first plain text, amend the guideline

Type: docs · Priority: P2 · Filed 2026-11-24 from the chantier CR `release-notes-style` (chantier batch-31, CR-475)

## Problem

The 1.12.1 note (an urgent fix release) reads like a feature release: emoji highlights, "what
you can now do" headings, a bold verb line. The guideline
`.agents/guidelines/release-process.guidelines.md` ("Release notes") asks for that shape whatever
ships, and it ranks above chantier's `release-template.md` card, so the card's new rules cannot
fix this repository's notes on their own.

A Fable audit of every note of the repository (2026-11-24): fixes worded as new abilities in 7 of
19 notes, bad news hidden or softened in 6, whole-page or oversized images in 6 of 11, mechanism
told instead of consequence in 5.

## Expected

- The guideline's "Release notes" says the release kind first (feature, fix, restore, breaking,
  internal): the subtitle names it, the title carries the full version.
- The visible part uses "Fixed:", "Restored:", "Removed:", "Changed:", "Known issue:" lines, one
  sentence per item, within word budgets (subtitle 16, item 20, visible part 120 for a patch, 250
  for a feature).
- An image protocol: only visible changes, cropped to the changed element, 900-1200 px wide, at
  most 600 px high, before and after joined, alt text as the caption.
- The rules stay in step with chantier's `release-notes-style` (CR-475 of chantier batch-31).

## Decided (owner, 2026-11-27, `02-answers.md`)

- For the batch running on that day, batch-11.
- A fix release keeps today's structure; its headings take the tone of its kind ("Fixed: …", never
  "what you can now do"), as chantier's card (`notes-kind-Q2`).
- No new script check: `release_notes.py --check` is not extended (`notes-kind-Q3`).
- Clip GIFs are exempt from the new image sizes, as from cropping (`notes-kind-Q4`).
- The 1.12.1 note is not rewritten (`notes-kind-Q5`).
- A performance gain the user can see is a highlight with figures, never only a folded line (the
  owner's rule for 1.13.0, told with the series, no objection).

## To grill

Nothing open.

## Related

- CR-482 (`feature-clip`, batch-09), decision feature-clip-Q14: a clip GIF is not cropped, by an
  exception written into the same guideline.
- The video gallery CR (`pages-video-gallery`), for the same batch, edits the feature clip
  guideline.
