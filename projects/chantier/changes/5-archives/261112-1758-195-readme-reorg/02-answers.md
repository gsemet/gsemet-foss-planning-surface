# Answers (grill, 2026-11-12)

- Timing: after the reproducible-evals work (batch-13) is done.
- Introduction, the CR: a Change Request is a folder whose content varies, from one line of
  text to several HTML prototypes; the agents read it and find the request's intent. In one
  sentence alone (no list of examples): CRs are fungible in the plan, they can be handled,
  split, and so on.
- Introduction, working in batches: chantier is not continuous delivery (1 intent = 1 PR =
  1 release). It is n CRs → m PRs (normally close to n) → p batches (1, 2, 3…) → 1 release.
- Direct or Foreman, why pick one: direct is simpler to use remotely, from a phone; Foreman
  lets you grill future topics with the Chief of Staff "naturally" while the Foreman runs the
  batch.
- "Zero configuration" becomes "respect the project's rules": your changes must be able to land
  without chantier; chantier is there to industrialise.
- The diagrams of "How chantier works": the detailed one first, then Foreman, then direct.
- The rest (sections, images) is good. The end is too detailed and moves to docs/, leaving a
  link: the detailed use (the CR board, the remote board, the gates, your own agents, the
  models, the planning folder's layout), Supported hosts (hosts, forges, Windows), Costs and
  budgets. "What is Chantier?" stays in the README.
- Grilled enough (user, 2026-11-12, after the restatement): "Ok".
- Go (user, 2026-11-12, relayed by the parent session, verbatim): "Fait tout ça": runs in a
  parallel batch with four retro items; its specification is final; the cards' references are
  updated, so the long gate (`just scenario`) runs.
