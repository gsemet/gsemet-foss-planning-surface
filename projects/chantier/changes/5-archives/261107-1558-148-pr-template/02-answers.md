# Answers

- 2026-11-07, the user: a default PR template, easy to audit, that takes over the
  markdown-studio (markdown-okf-schema-studio) template, "car il était vraiment bon".
- 2026-11-07, the user: chantier has no template in its own `.github/`; it ships the template in
  its skill, as a reference.
- 2026-11-07, the user: the agent knows how to create a guideline and a template in the target
  project when the user asks for a customised version there.
- 2026-11-07, the user: batch-08's PRs stay on the old way; no rewrite of open PR bodies.
- 2026-11-07, the user: to the inbox, grilled later, then added to batch-08.
- 2026-11-07, the user: the Inspector alone checks that a PR description follows the template,
  reading `pr-body.md` with the diff; no CLI check.
- 2026-11-07, the user: only the CRs' PRs follow the template; the stack and release PRs keep
  their current form.
- 2026-11-07, the user: screenshots are attached by the method driver.md already describes for
  the Verifier's evidence.
- 2026-11-07, the user: the template and its rules live in a new reference,
  `skills/chantier/references/pr-template.md`, which driver.md and the Inspector's card name.
- 2026-11-07, the user: GitLab merge requests follow the same template; a project's own
  template (GitHub or GitLab) ranks above it.
- 2026-11-07, the user, on where a customised version goes in the user's project: "laisse
  l'agent le faire tout seul": the agent chooses where to write the guideline and the template.
- 2026-11-07, the user: priority P1.
- 2026-11-07, the user, on the restated shared understanding (template in
  references/pr-template.md; sections Summary, Deliverables, Changes, Impacts, Blast radius 1-3,
  Test plan, Autonomous decisions, every one filled or "None"; external reader, Internal
  references last; CR PRs on GitHub and GitLab only; project's own rules first; Driver applies,
  Inspector reviews pr-body.md; screenshots per driver.md; custom version on request, placed by
  the agent; open PRs not rewritten; P1): grilled enough.
- 2026-11-07, the user (spec-writer's open questions): the CR name ("CR-142 grill-rules") goes
  only in the "Internal references" section: not in the PR title, not in the body's text.
- 2026-11-07, the user: when the Inspector blocks only on `pr-body.md`, the Driver fixes the
  description and runs a new Inspector in the same round; no round is counted.
- 2026-11-07, the user: a customised template for a user's project is delivered as a CR: the
  Chief of Staff files it, a Driver delivers the guideline and the template by PR.
- Was open (all answered above): what "easy to audit" checks and who checks it (the Inspector on
  `pr-body.md`, a CLI check, or both); which card holds the rule (driver.md, a new reference
  file); the stack driver's and the release driver's PRs; GitLab MRs; the screenshot upload
  method (the side-branch blobs of markdown-studio or `gh pr edit --attach` of driver.md).
