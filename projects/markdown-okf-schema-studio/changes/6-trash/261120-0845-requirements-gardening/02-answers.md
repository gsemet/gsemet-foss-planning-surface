# Answers

## 2026-11-17, owner

- Q: Delete the retired requirements (61 deprecated, 508 superseded)?
  A: No. Published requirements are not deleted; they stay as `superseded` / `deprecated` (IDs, links and the viewer's history kept). Merges and splits use `okfreq supersede` / `archive`.
- Q: Split the work as proposed in evidence/audit-synthesis.md, minus the deletion CR?
  A: Yes. Filed in the inbox: req-use-case-diagrams, req-marker-gate, then six restructure CRs req-garden-{block-table, review-frontmatter, palette-theme-layout, toolbar-lifecycle, core-diagrams-trust, myst-code-gfm}, which depend on the first two.
- This CR stays as the record of the audit and the decisions; its evidence is the source of the eight CRs.

## 2026-11-17, owner (series garden-Q1..Q5, asked once for the six req-garden CRs)

1. garden-Q1: **Approved StRS text.** A. Agreed in advance for the corrections each specification plans; one commit per corrected approved StRS, reviewed by the owner on the PR (the Driver records the re-approval the project rules ask for, and names these commits in the PR body).
2. garden-Q2: **Generated links and an added diagram on an approved StRS.** A. No re-approval: generated `derived_by`/Links are not authored text; an added diagram is editorial, reviewed on the PR.
3. garden-Q3: **Shared rules cited in Main paths.** A. A small CR, req-main-paths-depends-on, lands before the six: a Main path may cite an SwRS the StRS lists in `depends_on`. The six CRs then cite shared rules (LIFE-169/170, LIFE-026/049/069, BLOCK-041/058/109, TRUST-001/005/065, ...) with `depends_on` instead of deriving them, including in Main paths; this replaces the specifications that kept those derivations because of the old rule.
4. garden-Q4: **Implemented drafts.** A. StRS TOOLBAR-002, TOOLBAR-003 and their draft SwRS go to `proposed`.
5. garden-Q5: **Other open questions of the specifications.** A. Take each specification's recommendation; the Driver settles placements between sibling CRs and lists those choices in the PR body.
