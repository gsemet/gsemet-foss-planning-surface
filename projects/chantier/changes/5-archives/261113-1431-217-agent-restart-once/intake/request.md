An agent that ends or is refused (host API error, a mode switch, a first-line refusal) is restarted unclearly: silently, or twice. Fix: the cards say that each such end is one restart from the recorded state, and a refused start is either resumed or restarted, never both.

Merged on 2026-11-13 from the batch-15 retro items below (the user's word: "regroupe en moins de CR").

## From `host-error-driver-restart`

Batch-15: CR-213's first Driver was ended by a host API 403 (Cloudflare) right after its long gate; the Foreman restarted it and a second Driver finished. Measure what such an end loses (the gate's result, the round), and say in the cards that a host failure is a restart from the recorded state, not a silent end.

## From `mode-switch-restarts-crs`

Batch-15: switching the batch from direct to Foreman mode lost the epoch-1 Drivers of CR-196 to CR-199 when the direct session stopped; the Foreman restarted them by the restart path. The switch's card says that a switch restarts every live CR.

## From `one-spec-writer-per-cr`

Batch-15: the spec-writer refused a prompt without its first line; the Chief of Staff resent the line by SendMessage, which resumed that agent, and also started a second one: two spec-writers wrote the same 03-change-spec.md. After a first-line refusal, the card says whether a message resumes the agent or a new start is needed (one of them, never both), and the CLI or card guards one spec-writer per CR.
