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

How copilot-session-usage rebuilds the identifiers (read by the Chief of Staff on 2026-11-16, on
the user's word, in `src/copilot_session_usage/_internal/core.py` of gsemet/copilot-session-usage):
its `pricing refresh` downloads GitHub's `models-and-pricing.yml` and keys each row by
`_normalize_model_name(model)`: drop footnote markers (`[^...]`), drop `(preview)`, keep other
parentheticals, lower case, each run of spaces becomes `-`, dots kept (`GPT-6.1 Terra` →
`gpt-6.1-terra`, `Claude Sonnet 5[^promo]` → `claude-sonnet-5`). A model id read from a log is
matched exactly, else by the longest table key it starts with (a versioned id finds its family),
else `default`. This is the same rule as copilot-role-models' Q5; the catalog uses this one
rule, and the same cleaning of the display name. Seen in passing: its docstring says
`Claude Opus 4.8 (fast mode) (preview)` → `claude-opus-4.8-fast-mode`, but the code gives
`claude-opus-4.8-(fast-mode)` (parentheses kept); reported on the user's yes as
https://github.com/gsemet/copilot-session-usage/issues/67, never a workaround here.

model-defaults-board-config builds on it (checking the YAML's model ids, the board's model list).
