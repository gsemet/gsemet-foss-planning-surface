# Answers: outside-contributions-archive (Part G)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Malformed names:** only names in the outside form are checked; a malformed one is an error
   (exit 3). Every other archive name stays unchecked.
2. **In-project mode:** the feature works there too, in `.agents/changes/5-archives/`, with no
   writer and nothing refused.
3. **The time in the name:** the PR's merge time in UTC, as a CR's archive, so archives stay in
   merge order.
4. **When nothing is written:** the Chief of Staff says so in one line for a PR not merged, a PR
   a batch's CR names, or a PR that already has an outside archive.

The rule goes in chantier's `validate`, not in the surface's `scripts/validate-bundles.py`, as
the specification argues. No spec critic: the change is small and adds no CLI tool.
