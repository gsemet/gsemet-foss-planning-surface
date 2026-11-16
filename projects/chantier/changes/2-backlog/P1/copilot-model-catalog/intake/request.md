# Copilot model catalog from GitHub's own tables

Split from copilot-role-models on 2026-11-16 (its Q10, the user's choice): that CR ships the role
models with GPT-6.1 Terra added by hand; this one replaces chantier's hand-written Copilot model
list (`MODELS["copilot"]`) with a copy of GitHub's tables (`github/docs`,
`data/tables/copilot/`), kept in the repository and refreshed by a command (the CLI uses no
network), each identifier from the name rule and checked against the Copilot CLI reference's
"Supported models".

The grill is already done: copilot-role-models' 02-answers.md, Q3 to Q8 (the sources, the
identifier rule, Sol kept through `auto-model-selection.yml`, Luna `gpt-5.6-luna`, differences
reported and never refused, plans shown) and Q9 (no prices: they stay with
copilot-session-usage). Its first 03-change-spec.md (sections 2, 3 and the catalog tests) is the
starting draft.

model-defaults-board-config builds on it (checking the YAML's model ids, the board's model list).
