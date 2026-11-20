## Summary

Release notes put a highlight's picture before its text, and a picture could show a whole window
with the change lost in it. Chantier's own release process also asked each highlight for a usage
example, a doc link and a "why it matters" sentence, which the generic release template forbids.
A highlight now reads heading, at most two sentences, then the picture, and each picture shows only
the part where the change happens. Chantier's release process keeps what is its own and points to
the template for how notes are written.

## Deliverables

Text-only change; the new order of a highlight and the crop rule, as shipped:

| | Before | After |
| --- | --- | --- |
| A highlight | heading, picture, at most two sentences | heading, at most two sentences, picture |
| Picture shows the whole change | no text under it | the highlight is the heading and the picture, no text |
| A picture's content | not said | only the part where the change happens; both halves of a before/after at the same region and scale |
| A picture that cannot be cropped | not said | stays whole, a `note` says so, no other image is made up |

Choices: the crop rule holds for every source of a picture; the template names no tool; the
release process file keeps only the count and heading form of a highlight, and the template owns
the writing rules.

## Blast radius

Grade: 1. Two Markdown files; a `git revert` restores the previous wording. `release_notes.py` and
the published notes are untouched.

## Autonomous decisions

- The introduction of the release process file lists "the release folder, the structure of the
  notes, the links, the anonymisation, the batch" as what is chantier's own, to keep the split
  accurate to the sections that stay.

## Known gaps

- No screenshot or run proves the new rules in practice: the first release notes written with them
  (text before the picture, the pictures cropped) are what proves them.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/release-template.md`: "A highlight" reorders to heading, text,
  picture; "Visible evidence" gains the four crop points.
- `docs/release-process.md`: the introduction states which file holds what; "Release notes" item 3
  links the template's "A highlight" and "Writing rules" and drops its five sub-bullets; "Visuals"
  gains one sentence on the crop.

## Impacts

No visual change. Future release notes follow the new order and crop rule.

## Test plan

- [x] New or changed tests: No behaviour change
- [x] Local gates at `867cabc`: `just check` pass; `just check` pass on three systems and `just scenario (ubuntu-latest)` pass in CI
- [x] Evidence: no visual change (grep and read checks of the shipped files, at `867cabc`)
- [x] Review: approved at `4ed0d56` (committed as `867cabc`)
- [x] Verified at `867cabc`
- [x] CI green at `867cabc`

## Internal references

- CR-424 release-highlight-text-first, a follow-up of CR-413 (release-notes-writing-rules, PR #378).

</details>
