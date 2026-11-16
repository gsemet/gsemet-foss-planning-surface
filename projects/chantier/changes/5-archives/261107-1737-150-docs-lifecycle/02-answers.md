# Answers

- 2026-11-07, the user: P1, to follow batch-lifecycle and pr-template: update the docs SVG
  diagrams with the batch lifecycle and the direct mode (no Foreman).
- 2026-11-07, the user: the same for the docs, with all of today's changes.
- 2026-11-07, the user: the docs explain that direct mode is less dynamic but keeps the same
  lifecycle.
- 2026-11-07, the user: the docs explain that direct mode allows no grill in the same session;
  the user can open another session themself to grill and put their own ideas in the backlog
  beside the batch.
- 2026-11-07, the user: this CR starts once batch-lifecycle and pr-template are merged, so the
  docs use their final words (paused, `pause`, the PR template).
- 2026-11-07, the user: a new diagram shows the batch lifecycle (running → paused → closed on
  the user's word), with its texts file, named in the README.
- 2026-11-07, the user: direct mode is a variant on the same diagram: how-chantier-works shows
  both modes (with a Foreman, or the Chief of Staff steering the batch itself).
- 2026-11-07, the user: the README, `use-cases.md`, `tutorial-claude-code.md` and every page of
  `docs/` that is out of date take today's changes (direct mode, init, spec-writer, paused
  batch, the board's slots, the PR template).
- 2026-11-07, the user: "pour les svg montre moi les nouvelles versions avant de lancer la PR":
  the Driver shows the user the new and changed SVGs (rendered, through the Chief of Staff)
  before it opens the PR, and waits for the user's go.
- 2026-11-07, the user, on that review (asked again): the SVGs are reviewed before the CR
  starts, not before its PR: the Chief of Staff has a prototype of the new and changed SVGs
  drawn in a temporary folder, shows them rendered, the user's corrections go into the
  specification, and the approved SVGs are the reference the Driver delivers. This replaces the
  Driver's stop before the PR.
- 2026-11-07: batch-lifecycle (PR #86, ac5e453) and pr-template (PR #85, c913e43) are merged;
  this CR can start.
- 2026-11-07, the user (spec-writer's open questions): `docs/batch-pace.svg` is left untouched
  in this CR.
- 2026-11-07, the user: `docs/how-chantier-works-simple.svg` is updated to show both modes, gets
  a `-texts.md` companion and is named in the README.
- 2026-11-07, the user: batch-08's budget goes to $40.
- 2026-11-07, the user: "fait un document use case par configuration": one use-case document
  per configuration (at least Foreman mode and direct mode); the spec-writer names the
  configurations and the files.
- 2026-11-07, the user: the five SVG prototypes are approved as they are; they are frozen in
  `work/approved-svgs/` (SVG and rendered PNG each) and are the Driver's reference.
- 2026-11-07, the user: the new `batch-lifecycle.svg` is not named in the README in this CR;
  the user adds it there later. The other SVGs keep their README links.
- 2026-11-07, the user: the CR waits in P1 backlog, complete, until the user starts it.
- 2026-11-07, on the Copilot wording: "Copilot SDK host" and "Copilot agent session" name the
  same host; the docs use one name, the one the CLI's preflight checks (agent session).
