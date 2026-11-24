## Summary

A bug-fix release's notes read like a feature release's: a revert shown as a new feature, fixes worded as new abilities, bad news buried, oversized images. The release template asked for verbs in the subtitle and a "what you can now do" heading whatever shipped. This change teaches the Release Driver to write the notes kind first, one plain sentence per change, bad news on labelled lines, within word budgets, with images framed on the changed element, and to check the result with a ten-question self-check.

## Deliverables

- `release-template.md`: the title carries the full version (`X.Y.Z`) and a subtitle that names the release's kind first (feature, fix, restore, breaking, internal; mixed kinds in the order breaking, feature, restore, fix, internal). New subsections: The kind, One line per change, Bad news (`Removed:`, `Changed:`, `Known issue:` lines in the visible part), Length (budgets of 16, 20, 40 words, and 120 or 250 for the visible part), the banned constructions with before/after pairs, and the ten-question Self-check. "A highlight" heading says the change in its kind's words.
- `release-template.md`, "Visible evidence": the image protocol (crop to the changed element, 900 to 1200 px wide, at most 600 px high, alt text as caption, the Release Driver reads each image it produced, a missing picture named in Known gaps and never in the notes).
- `driver-pr-extras.md`: the "never opens an image file" bullet names the Release Driver's exception.
- `docs/release-process.md`: four lines of the structure list aligned (full-version title, kind-first header line, highlight heading, known issues out of "For contributors").
- New structure test `test_release_template_card.py` over the shipped files.

Reading check, a dry run of the new rules on an urgent release that holds a revert and block-editing fixes (a restore and fixes: the subtitle names the restore first) (text only):

- Subtitle (12 words): **Restores pasting whole blocks that 1.12.0 broke, and fixes block editing**
- `Fixed: the cursor stays in the block you are editing.`
- `Restored: pasting whole blocks, which 1.12.0 broke.`
- `Known issue: undo after a paste restores the text but not the cursor position.`

Self-check answers: 1 yes (the subtitle starts with the kind); 2 yes (`X.Y.Z` in the title); 3 yes (no "you can now" heading); 4 yes (each fix starts with "Fixed:"); 5 yes (the restore names 1.12.0); 6 yes (the known issue is a labelled line in the visible part); 7 yes (one sentence each, within 120 words); 8 yes (consequences, no mechanism); 9 yes (no image: nothing visible to frame, and no sentence about it); 10 yes (a patch version matches a fix release).

## Blast radius

The change is card text, one doc and one test; no CLI code.

Grade: 1

## Autonomous decisions

- The "never opens an image file" bullet now lives in `driver-pr-extras.md` (moved there by an earlier change); the exception was added there.

## Known gaps

- No screenshot is owed: the change shows nothing visible.
- The long gate (`just scenario`) is green only once CI reports it at the head.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/release-template.md`, `skills/chantier/references/driver-pr-extras.md`, `docs/release-process.md`, `skills/chantier/scripts/cli/tests/test_release_template_card.py`.

## Human decisions

- Card only: the mechanical refusals (title version, budgets, banned phrases, image size) belong to a separate change on each project's release-notes check script.
- A release's real kind sets the tone even when the version does not match; the version PR says so and the user decides.
- Mixed kinds are named in the order breaking, feature, restore, fix, internal; a breaking release's visible part is at most 250 words.
- A picture that cannot be captured or cropped within bounds goes out without it, with the gap in the version PR's Known gaps (or a note and the hand-back when no version PR).

## Impacts

No visual change. Future release notes start with the release's kind and carry labelled bad-news lines.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `6773a4d`: `just check`
- [x] Evidence: reading check (the 1.12.1 situation) at `6773a4d`
- [x] Review: approved at `6773a4d`
- [x] Verified at `6773a4d`
- [x] CI green at `6773a4d`

## Internal references

CR-475 release-notes-style.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
