# The Foreman runs as a long task in the chantier server

The user wants the Foreman detached from a session and held by the chantier server as a long-running task: a complete orchestrator that can last for days and manage several hundred agents (their words in `intake/request.md`). Not grilled yet: the goal, what runs in the server, how the user talks to it and its permissions are open.

## What the logs show (read-only, 2026-11-25, this machine)

Claude Code transcripts of the Foreman sessions of chantier (batches 05 to 31) and of markdown-okf-schema-studio (batches 06, 07, 09), eval runs left out of the figures below. Durations are from the first to the last record, idle time included.

- A Foreman session lasts up to 79 h (Studio batch-06); chantier batch-31 was at 70 h and Studio batch-09 at 63 h, both still running.
- Agents under one Foreman session (Drivers and their workers): 321 to 522 on each of nine large batches, 522 the most (chantier batch-30); at most 20 agent lifetimes overlap.
- The Foreman's own load: up to 1,175 model calls, 604 wakes and 9 compactions in one session, with about 180k tokens of context on average.
- Its tools are mostly shell commands (the chantier CLI), `SendMessage`, `Agent` and `ScheduleWakeup`; it also uses Claude Desktop's own tools (task list, wrap-up, session title and messages).
- Cost, from `1-inbox/foreman-idle-wakes/experiments/foreman-cost-study.md`: the Foreman is 10 to 36 % of a batch's spend; about a third of its cost is inherent to the events it handles, 17 to 19 % are idle wakes, the rest comes from calls per event, context size and model.

## What it would change in the project rules

`AGENTS.md` (local and `origin/main`) says the surface server never edits a batch and never messages an agent, the forge hub records nothing in a batch, the CLI knows no role, and a role's contract lives in the cards. A Foreman held by the server changes at least some of these.

## A trial the same day

A headless `claude -p` run on this machine appeared in the other sessions' list, received a message and answered; it had `Agent` and `SendMessage` and none of Claude Desktop's session tools. A headless run lasting days, and its wake-ups, are not tried.

## Related items

- `1-inbox/foreman-idle-wakes`: paused on the user's word (measure first, decide after).
- `1-inbox/simplify-cards-and-prompts`: batch-31 rewrites the cards, the Foreman's included (CR-507).
- `2-backlog/P3`: `night-watch-independent`, `surface-chief-of-staff`, `foreman-session-not-linked`, `batch-takeover`.
