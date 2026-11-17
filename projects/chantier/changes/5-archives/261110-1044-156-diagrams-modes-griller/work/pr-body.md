## Summary

The README and the docs showed one picture with two arrows for chantier's two ways of steering a batch, and the introduction did not carry what a new reader must know first. This PR draws the two modes as two pictures, shows the optional Griller (another session of yours that grills and specifies the backlog) wherever the Chief of Staff appears, and sets the README, the docs and the Chief of Staff's first-turn introduction straight around four messages: a Change Request sits one level above a tracker's issues; you talk to one person, the Chief of Staff; direct or Foreman mode; zero configuration. The release template now looks for screenshots in the merged PRs' Deliverables section.

## Deliverables

Renders of the changed drawings (PNG, made with headless Chrome from the SVGs in this PR):

how-chantier-works-simple-direct (`./how-chantier-works-simple-direct.png`)

how-chantier-works-simple-foreman (`./how-chantier-works-simple-foreman.png`)

how-chantier-works (`./how-chantier-works.png`)

cr-lifecycle-simple (`./cr-lifecycle-simple.png`)

cr-lifecycle (`./cr-lifecycle.png`)

cr-folder-lifecycle (`./cr-folder-lifecycle.png`)

batch-lifecycle (`./batch-lifecycle.png`)

- README: direct mode first, then Foreman mode, each with one line on when to pick it, then one plain sentence on the difference: in direct mode a CR joins a running batch only once every other CR is handled and the batch is paused; in Foreman mode it can join while the batch runs.
- Detailed diagram: the Foreman box is split in two halves, "Foreman mode" (nested session, natural conversation, not recommended in remote) and "direct mode" (the Chief of Staff plays the Foreman's role, works in a remote session, no grill during the batch: use a Griller session).
- The Griller, marked optional with a dashed outline and the word "optional", appears on both how-it-works diagrams, both CR lifecycles and the CR folder lifecycle; not on the batch lifecycle or the batch pace.

## Blast radius

Grade: 1. Documentation and two cards' text (the Chief of Staff's introduction and the release template's evidence line); no CLI, test or agent change. A `git revert` restores everything.

## Autonomous decisions

- The Griller is drawn with 🔥 and an "optional" tag; a GRILLER lane in the simple and detailed diagrams. The emoji and the band label stay open for the review of the renders.
- The detailed diagram's steering band is named "STEERING", since the direct half is not nested.
- In the direct simple diagram the empty nested-session lane is labelled "NO FOREMAN" with a short note, to keep both simple diagrams at the same width and positions.
- The Griller row sits below the You / Chief of Staff row, so the orders and asks arrows and the AGENTS.md arrow are re-routed to clear it.
- The Chief of Staff's first-turn introduction folds the former "Change Specification", "Batch", "Foreman" and "flow" bullets into the four messages; the "stack of PRs by default or independent" detail is dropped from it.
- The join-rule sentence added to the docs' configuration page does not mention the release CR exception, which `use-cases-direct.md` already states.

<details>
<summary>Details</summary>

## Changes

- `docs/how-chantier-works-simple.svg` (and its texts file) replaced by `-direct` and `-foreman` variants, each with its texts file.
- `docs/how-chantier-works.svg`, `cr-lifecycle-simple.svg`, `cr-lifecycle.svg`, `cr-folder-lifecycle.svg` and their texts files: Griller added, Foreman box split. `batch-lifecycle.svg` and its texts: "grill in a Griller session".
- `README.md`: four-message introduction, the two modes' diagrams and the difference sentence, the Change Requests section explains the tracker relation and names only `.agents/changes/`.
- `skills/chantier/references/session-start.md` section 4: bullets rewritten around the four messages.
- `skills/chantier/references/release-template.md`: Deliverables sections instead of Impacts sections.
- `skills/chief-of-staff/SKILL.md`: description no longer says the Chief of Staff needs Claude Desktop.
- `docs/tutorial-claude-code.md` (three skills), `docs/use-cases.md` (the join rule).

## Human decisions

- README shows both simple diagrams, direct first, then Foreman, each with a line on when to pick it.
- The Griller is shown, marked optional, on every diagram where the Chief of Staff appears, but not on the batch lifecycle or the batch pace.
- The Change Request / tracker explanation goes in the Change Requests section, not at the top of the README.
- The external planning area is not mentioned.
- The introduction keeps all four messages.
- The drawings are reviewed from PNG renders in this PR; no prototype step first.

## Impacts

Visible documentation change: the renders in Deliverables show the new drawings.

## Test plan

- [ ] New or changed tests: No behaviour change
- [ ] Local gates: `just check`, `just scenario`
- [ ] Evidence: the renders in Deliverables
- [ ] Review
- [ ] CI green

## Internal references

CR-156 diagrams-modes-griller (batch-09).

</details>
