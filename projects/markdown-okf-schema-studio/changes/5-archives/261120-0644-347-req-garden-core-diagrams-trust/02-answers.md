# Answers

## 2026-11-17, owner

- "Ne supprime pas les requirements publiées effectivement. Le reste me semble bien": published requirements are never deleted; merges and splits use okfreq supersede / archive. The split into this CR and its siblings is approved.
- "Tu peux lancer tout ce que tu m'as dis, avec le foreman réutilisé et finissant sur une stack de PR": launched without the owner reviewing the specification; the specification follows the audit report of this CR's group (CR requirements-gardening, evidence/).
- Decisions the owner keeps (to bring back, not to take alone): re-approval of any approved StRS whose text changes; draft -> proposed; a proposed merge or split the Driver doubts.
- Spec critic: no, it changes requirement text, markers and tests, no product behaviour.
- 2026-11-17, Chief of Staff (from the spec critic of req-use-case-diagrams): that CR adds one proposed SwRS for the use-case diagram on the site, derived from TRUST-014 with its marker in a companion file. It is one of the site SwRS this CR reparents (with CORE-069, CORE-080..086) and whose marker it moves.

## 2026-11-17, owner (series garden-Q1..Q5, asked once for the six req-garden CRs)

1. garden-Q1: **Approved StRS text.** A. Agreed in advance for the corrections each specification plans; one commit per corrected approved StRS, reviewed by the owner on the PR (the Driver records the re-approval the project rules ask for, and names these commits in the PR body).
2. garden-Q2: **Generated links and an added diagram on an approved StRS.** A. No re-approval: generated `derived_by`/Links are not authored text; an added diagram is editorial, reviewed on the PR.
3. garden-Q3: **Shared rules cited in Main paths.** A. A small CR, req-main-paths-depends-on, lands before the six: a Main path may cite an SwRS the StRS lists in `depends_on`. The six CRs then cite shared rules (LIFE-169/170, LIFE-026/049/069, BLOCK-041/058/109, TRUST-001/005/065, ...) with `depends_on` instead of deriving them, including in Main paths; this replaces the specifications that kept those derivations because of the old rule.
4. garden-Q4: **Implemented drafts.** A. StRS TOOLBAR-002, TOOLBAR-003 and their draft SwRS go to `proposed`.
5. garden-Q5: **Other open questions of the specifications.** A. Take each specification's recommendation; the Driver settles placements between sibling CRs and lists those choices in the PR body.
