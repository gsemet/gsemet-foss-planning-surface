# close and pause see a finished agent as finished

`close` (and the quiet check behind it, `rails.py` `running()`, `QUIET_SECONDS = 300`) refuses while any batch transcript was written in the last 5 minutes. It judges by file age, not by whether the agent ended: in both runs it refused 4 times on agents that had already handed back (530 s slept in all), and run 2's final cost rose from $11.47 to $11.91 because the prompt cache expired during the wait. It also misses a silent tool call longer than 5 minutes.

Judge by the transcript's end instead: all 94 finished agent transcripts of the two runs end with their hand-back and its result; an assistant tool call with no result yet means the agent still runs, whatever the file's age. Refuse only when an agent still runs or its transcript cannot be read (naming the file). The user's word, 2026-11-15: read the transcript rather than wait 5 minutes; a round trip to ask the agent only as a last resort (a finished subagent cannot be messaged, and the CLI messages no agent).

The same detector can later serve "a Driver ended with no recorded hand-back" (batch-18 retro, 4 occurrences).

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
