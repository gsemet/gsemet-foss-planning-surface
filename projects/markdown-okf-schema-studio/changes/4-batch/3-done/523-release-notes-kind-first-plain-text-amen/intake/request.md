# Release notes: kind-first plain text, amend the guideline

Amend .agents/guidelines/release-process.guidelines.md: release notes state the release kind first and use plain, short text.

Why: the 1.12.1 note (urgent fix release) reads like a feature release. The guideline asks for a verb subtitle and a "what you can now do" heading whatever ships, and it ranks above chantier's release-template card, so the card alone cannot fix this repo's notes. A Fable audit of every note of the repo (2026-11-24): fixes worded as new abilities in 7 of 19 notes, bad news hidden or softened in 6, whole-page or oversized images in 6 of 11, mechanism told instead of consequence in 5.

Amend: kind first (feature, fix, restore, breaking, internal; subtitle names it; full version in the title); "Fixed:", "Restored:", "Removed:", "Changed:", "Known issue:" lines in the visible part; one sentence per item; word budgets (subtitle 16, item 20, visible part 120 for a patch, 250 for a feature); image protocol (only visible changes, crop to the changed element, 900-1200 px wide, at most 600 px high, joined before/after, alt text as caption). The user-facing text rules are filed as chantier's CR "release-notes-kind-first-plain-text-and-"; keep the two in step. The 1.12.1 note itself also needs a rewrite on these rules.
