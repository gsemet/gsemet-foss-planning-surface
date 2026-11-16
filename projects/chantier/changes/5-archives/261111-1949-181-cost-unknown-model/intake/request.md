# `cost` prices a model it does not know as "unknown"

Batch-10's Foreman, at pause (2026-11-11): the Chief of Staff's cost was "unknown, because the
price table has no 'claude-fable-5-2' (your session model changed since A-2)". The session ran
Fable subagents (a critic, a spec-writer, an advisor) on the user's word.

- What happens: one model missing from the CLI's price table makes the whole line unknown.
- Open for the grill: add the model's price; whether `cost` prices the known part and names the
  unknown model instead of dropping the whole figure; how a new model's price gets in without a
  release.
