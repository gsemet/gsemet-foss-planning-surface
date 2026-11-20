# Driver context, second cut: the spec, the prompts, the CLI's outputs

Priority P2. Split out of `driver-context-budget` (2026-11-20), which cut the CR Driver's reading of `driver.md` and moved the closing hand-off to 115,000 tokens. It is the next step if a three-round CR still hands back `blocked context:` in the first batch that runs those cards.

What is left in a first-take CR Driver's context, measured on batch-29's 27 first takes (bytes, average per run, of 184 KB):

- the specification: 23 KB. The Driver reads it whole; it needs the goal, the scope, the decisions, the evidence and the list of file edits.
- its own tool calls: 29 KB (the workers' prompts, with the checklist copied into each Coder's prompt; `pr-body.md` written whole; the CLI's command line, about 230 characters at each call).
- `pr-template.md`: 11 KB, read whole when the body is written.
- the CLI's outputs: 9 KB; `take` and `handoff` print about 6 KB each, the same facts as the Driver's prompt (6 KB).
- `startup-manifest.json`: 4.4 KB, read whole at each start to find one role's lines.
- about a third of the context growth is in none of the bytes above (the model's own reasoning, the host's reminders).

Measure again after `driver-context-budget` is merged (the next batch's `events.jsonl`, `cost --by cr` and the Drivers' transcripts), then cut what still weighs. Some of these touch the CLI (what `take` and `handoff` print, the prompt's reading line), so the measured-cost rule of `AGENTS.md` applies with these figures.

Done when a CR that takes three rounds reaches `handback ready` in one Driver, in a real batch, with its peak context below 115,000 tokens.
