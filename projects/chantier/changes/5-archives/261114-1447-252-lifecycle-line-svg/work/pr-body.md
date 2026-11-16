## Summary

The README's change request lifecycle section opens with diagrams that draw folders, lanes and loops. A reader who first wants the plain sequence (what happens to a request, in order, and who acts at each step) has no simple picture. This adds one diagram that shows only that: one line of ten steps, from your request to your merge, with a small line under each step naming who acts. Docs only; no behaviour changes.

## Deliverables

The new diagram, placed in the README just before the detailed lifecycle diagram, which stays for the details:

| Step | Who acts |
| --- | --- |
| Intent | you |
| Grill | Chief of Staff or Griller, with you |
| Spec | spec-writer |
| Spec critic (dashed, when impactful) | spec critic |
| Driver (Coder, Inspector, gate, CI) | CR driver |
| Verifier | Verifier |
| Ready locally (dashed, rare: no PR yet) | the driver hands back |
| PR in draft | the driver opens the PR |
| Ready to merge | the driver, or the stack driver, out of draft |
| you merge | you |

Choices: the three states of a PR end the line (violet dashed, brown, green); the user's decision points are not drawn, the detailed diagram just below shows them.

The README as rendered at the head: https://github.com/gsemet/chantier/blob/a4d342b490e06d496cac050a51ba1dbb4e5b5de0/README.md. The SVG itself: https://github.com/gsemet/chantier/blob/a4d342b490e06d496cac050a51ba1dbb4e5b5de0/docs/cr-lifecycle-line.svg (head a4d342b).

![A change request's life in one line: who acts at each step](https://github.com/gsemet/chantier/raw/a4d342b490e06d496cac050a51ba1dbb4e5b5de0/docs/cr-lifecycle-line.svg)

The roles in the diagram are chantier's agents: the Chief of Staff and the Griller grill the request with you, the spec-writer writes the specification, the spec critic reviews it, the CR driver builds and checks the change, the Verifier proves it, and the stack driver stacks the PRs.

## Blast radius

Grade: 1. Two new doc files and one README line; a `git revert` restores the previous README.

## Autonomous decisions

- The SVG is 1000 pixels wide, so on a 1000-pixel README column it shows at full size: step titles 17px and every small line 13.5px, with the texts wrapped inside taller boxes to keep ten steps in one row.

## Known gaps

- No local long gate: waived by the project for this change; GitHub CI at the head replaces it.

<details>
<summary>Details</summary>

## Changes

- `docs/cr-lifecycle-line.svg` (new): the one-row diagram, styled as `docs/cr-lifecycle-simple.svg`.
- `docs/cr-lifecycle-line-texts.md` (new): every text of the SVG, as the other diagrams' companions.
- `README.md`: one image line in "Change Requests Lifecycle", before `cr-lifecycle-simple.svg`.

## Human decisions

- The line sits at the head of the README's lifecycle section; the existing simple diagram stays.
- The steps end with the three PR states (ready locally, PR in draft, ready to merge), the first drawn dashed with "rare: no PR yet".
- The spec critic step is drawn dashed with "when impactful", icon 🧐.
- The user's decision points are not drawn; the line stays minimal.

## Impacts

A new picture at the top of the README's lifecycle section; nothing else.

## Test plan

- [x] No behaviour change
- [x] Local gates (carried from a0e759a): `just check` passes (biome, 69 tests, release-notes)
- [x] Evidence (at a4d342b): the SVG parses as XML, its viewBox matches its size, no 🔵, no folder name, every text is in the companion file
- [x] Review: approved at a4d342b
- [x] Verified at `a4d342b`
- [x] CI green at `a4d342b`: all 5 jobs pass (gh pr checks 190)

## Internal references

- CR-252 lifecycle-line
- Work files: `.agents/changes/4-batch/2-actives/252-lifecycle-line-svg/work/r1.md`; rendered image of the diagram: `work/r2.png` (not attached to the description)

</details>
