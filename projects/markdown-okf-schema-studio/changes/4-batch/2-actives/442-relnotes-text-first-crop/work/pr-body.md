## Summary

Release notes highlights now read text first: a heading saying what you can now do, at most two sentences, then the picture. The picture is cropped to the part of the screen where the change happens, so the eye lands on the change and not on the toolbar or the content around it. The rule is written in the release guideline so the next release follows it.

## Deliverables

The release guideline's "Release notes" section changes in six places, shown here as the order of a highlight before and after:

| | Before | After |
| --- | --- | --- |
| Highlight order | heading, picture, at most two sentences | heading, at most two sentences, picture |
| Picture that shows the whole change | no text under it | no sentence: heading, then picture |
| Crop | not said | picture cropped on the change; both halves of a joined before / after image cropped to the same region at the same scale; a gesture capture keeps the element and what it acts on |

Also changed to match: the section intro (no more "in pictures first"), the highlight item of "Structure", and one sentence in "Images" saying the captures are cropped before they are joined.

## Changes

- `.agents/guidelines/release-process.guidelines.md`, section `## Release notes` only: intro, three bullets of "Writing" (reworded order, whole-change rule, two new crop bullets), item 3 of "Structure", one sentence in "Images".
- No change to past release notes, `scripts/release_notes.py`, tests, the justfile or CI.

## Impacts

No visual change. The next release's notes follow the new order and crop.

## Blast radius

Grade: 1. A wording change in one guideline; a plain `git revert` restores the previous text.

## Autonomous decisions

None.

## Known gaps

None.

## Test plan

- [x] New or changed tests: none, a guideline wording change
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [ ] Local gates: `just check` at the round's state: pass; `just preflight` pending
- [ ] Review
- [ ] CI green

## Internal references

CR-442 relnotes-crop.
