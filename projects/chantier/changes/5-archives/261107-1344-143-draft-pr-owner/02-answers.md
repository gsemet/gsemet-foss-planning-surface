# Answers (grill of 2026-11-07)

- **The steering session owns it** (the Foreman, or the Chief of Staff in direct mode). When
  `order merged` records the dependency's merge, the steering session sends each CR that waited
  for it back to a Driver with `take <cr> --note "rebase: <dependency> merged"`; the Driver
  rebases on the default branch, retargets the PR there and turns it ready once it can merge.
- The CLI adds nothing for this: the rule lives in the steering card.

- 2026-11-07, the user: grilled enough; joins batch-08 now ("C", "Relance le batch avec toutes ses CR").
