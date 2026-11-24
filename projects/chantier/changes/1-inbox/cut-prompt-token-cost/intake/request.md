# Cut the prompts' token cost without losing quality

Cut the token cost of running chantier: slim the prompts (cards, agents, startup reads) without losing the quality of what is delivered.

Trigger: CR-471 (PR 450, merged 2026-11-24) cut the role cards into pieces but the Chief of Staff's start reading grew by 21,049 bytes (Claude 177,821 to 198,870, ratio 0.47 to 0.52): the any-moment rules (forge permissions, offering options and refusals, compacting, tips, the floor) became one new 19,819-byte piece, chief-of-staff-any.md, read by the entry action. Foreman +739, Stack Driver +1,362, Release Driver +415, CR/QA Driver +58.

User's direction (2026-11-24), to grill at the end of batch-31, once everything has landed:
- Chantier's prompts are huge; a large part can be inferred by modern models (Opus, Sonnet) and need not be written.
- Look for duplication across cards, and for information handed to a role that is not for that role.
- Retros may have added rules for problems too insignificant to justify their tokens: audit rules added by retros and drop the trivial ones.
- Goal: minimise the token cost of an execution (start reads and per-action reads), with no loss in the quality of the deliverables.
- Measure before and after (startup bytes and tokens per role, per action) and check quality with the existing evals.

Leads: the Fable readings of CR-471 (in its spec, section 5, and work/fable-readings-findings.md), and the inbox item driver-card-leads-left-by-role-cards-sti.
