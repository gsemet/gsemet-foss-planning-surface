## Summary

Release notes written from the old template were long: each highlight carried a usage example, a doc link, a "why it matters" line and often a description of the old behaviour the picture already showed. This PR changes the release-notes template so the notes are shorter and plainer. A highlight is a heading saying what you can now do, a picture, and at most two sentences; a change that replaces a visible behaviour shows the before and the after side by side in one picture.

## Deliverables

The structure of a highlight in the release notes, old and new:

| | Old template | New template |
| --- | --- | --- |
| Heading | what changes for the reader | what you can now do |
| Content | usage or call example, evidence, doc link, why it matters | one picture, at most two sentences |
| Replaced behaviour | described in text | before and after side by side in one image, not described again |
| Whole change shown by the picture | text anyway | no text under it |
| Setting | not specified | "the setting `full.name`", with its default and where to turn it on |

Choices made: the notes keep their title, one line of verbs, two to four highlights, one-line smaller changes and folded fixes; a short list of banned wording ("Before:" / "Now:" labels, invented scenes, punchy fragments, praise words, a closing "why it matters" line); every changelog line appears once, visible or folded.

## Blast radius

Grade: 1

Only the wording of one card changes (`skills/chantier/references/release-template.md`); a plain `git revert` restores the old template. The project's own release procedure still ranks above the template.

## Autonomous decisions

- The two rule groups got their own subsections ("Writing rules", "A highlight") under "The notes", to keep the specification's wording findable. No behaviour depends on it.

## Known gaps

- `docs/release-process.md` (lines 47 to 51) still asks for a usage example, a doc link and a "why it matters" sentence per highlight. It ranks above the template for this project and is outside the request's scope; it is left for a follow-up.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/release-template.md`, "The notes": new structure (title, one line of verbs, two to four highlights, one-line smaller changes, fixes and details folded), a "Writing rules" subsection, an "A highlight" subsection, and the coverage rule.
- Same file, "Visible evidence": each highlight shows one image, the before and after side by side when a visible behaviour is replaced, built from the Verifier's before/after.

## Impacts

Release notes written from now on follow the new form. No visual change in the product.

## Test plan

- [ ] No behaviour change (a card text change; no test applies)
- [ ] Local gates at `<sha7>`: `just check` (pending the commit; passed on the worktree before it)
- [ ] Evidence: none, a text-only change
- [ ] Review: approved at `<sha7>` (pending)
- [ ] Verified at `<sha7>` (pending)
- [ ] CI green at `<sha7>` (pending)

## Internal references

- CR-413 release-notes-writing-rules

</details>
