# A model per role on each host

Split from model-defaults-board-config on 2026-11-16 (its Q18, the user's choice), second of a stack of three, on top of it: each host declares whether it starts a named agent with a model given at the start (Claude Code yes; Copilot no until proved); where it cannot, a generic agent with the role's contract rebuilt and the model; `model-policy: required` removed from `chantier-coder` only, with the eval probe; `cost --explain`. Its grill is model-defaults-board-config's 02-answers.md (Q3, Q5 to Q10, Q12, Q13, Q17).
