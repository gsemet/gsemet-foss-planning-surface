# chantier live in Rich: tables, dates, Ready and Agents boxes

Short name: `live-rich`. Owner's words of 2026-11-23, relayed from okf-schema.

Rework the terminal client `chantier live` (`clients/tui/`) with Rich: real tables and boxes, `--once` still printing a plain-text screen. Each Flow line shows its date and time in the local zone (the zone in the header); the key `t` switches the time column to the rounded time since the event and back. Layout: Projects top left, Agents below it in its own box (the project's active sessions, with role and CR), Flow in the centre, Ready above Tasks on the right (the PRs or MRs ready, each with its state in the board's colours and a clickable link where the terminal allows), the Ready list read from the server's published API, never from `gh` or `glab`. The spec checks the observed `none` in Agents, the observed time gap, and the Rich dependency.
