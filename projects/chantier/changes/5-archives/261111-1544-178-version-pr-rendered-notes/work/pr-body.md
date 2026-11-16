## Summary

A release is approved in its version PR, but the release notes and the announcement thread were only drafts in files, which is hard to review, on a phone especially. The release guidance now has the release procedure show both in the PR's body, rendered, under the PR's own description. The same PR fixes a wording defect: the agent that runs a change was told to read its worker `team:` lines with a command that also counts an attempt; it now reads them with `handoff`, a read-only command.

## Deliverables

The version PR's body, as the release guidance now describes it:

| Part | Content |
| --- | --- |
| PR description | the procedure's own, unchanged |
| `---` rule, then notes | `release-notes.md`, rendered |
| `---` rule, then thread | `tweet.md`, under a heading saying it is a draft the user posts |

- The draft files stay the source; the body is a copy, refreshed when the PR opens, at each draft change and before the merge is asked. It is never copied back.
- An image shows in the body only once it is on the forge, else it is named in prose; what the forge's size limit leaves out is named by its path.
- A project procedure that says where notes are reviewed is followed as written; a release with no PR keeps the drafts alone.
- The `team:` lines are read with `handoff`; `round` is run only to start a round.

## Blast radius

Grade: 1. Text in two guidance cards and two docs; no code, CLI or agent file changes. A `git revert` restores the previous wording.

## Autonomous decisions

- The optional `CONTRIBUTING.md` phrase ("in the PR's body and its files") was made, as it keeps the release steps consistent with the cards.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: "Your means" reads `team:` lines with `handoff`; the release section gains four bullets (body layout, source and refresh, images, size limit) and the release PR bullet refreshes the body first.
- `skills/chantier/references/release-template.md`: "Where they go" and the image rule cover the PR's body.
- `docs/release-process.md`: the version PR's body shows the notes then the thread; images linked at the PR's head commit on GitHub.
- `CONTRIBUTING.md`: release step 3 says the user reviews in the PR's body and its files.

## Human decisions

- The body shows notes then thread, each after a `---` rule, as the default under a project's own procedure.
- The files stay the source; the body is a copy refreshed before the merge, never copied back.
- The thread is headed as a draft the user posts; no agent posts it.
- Images show only once on the forge (an image pushed with the PR's branch counts); a new upload keeps its approval step.
- Size overflow is named by path, never cut silently.

## Impacts

No visual change. Releases will show the notes and thread in the PR's body.

## Test plan

- [ ] New or changed tests: No behaviour change (cards and docs only)
- [x] Local gates at `963d576`: `just check` and `just scenario` pass
- [x] Evidence: text checks of the cards against the specification, at `963d576` (no screenshots: text only)
- [x] Review: approved at `963d576` (same content as reviewed)
- [x] Verified at `963d576`
- [x] CI green at `963d576`

## Internal references

- CR-178 version-pr-rendered-notes; also carries point 2 of cr-171-retro-fixes.

</details>


