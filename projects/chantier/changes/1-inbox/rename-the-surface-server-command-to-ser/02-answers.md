# Answers (copied from the parent CR)

Copied 2026-11-22 from `remote-cli-commands-through-the-surface-/02-answers.md` (the parent CR,
split in three by remote-cli-Q11); the parent's file stays the record. Part A: the rename and
`webui`.

## remote-cli-Q1 (2026-11-22, the user): naming

Asked: `chantier board` starts the surface server today; which names? Answer: "Serve, live, webui":
`chantier serve` starts the surface server (today's `chantier board`), `chantier live` stays the
terminal client (the TUI), `chantier webui` is the web UI's command.

## remote-cli-Q3 (2026-11-22, the user): `chantier webui`

Answer (the recommended option): it prints the board's link with its key, and starts the server
when none runs.

## remote-cli-Q6 (2026-11-22, the user): placement

Answer: batch-30, right before CR-447 docs-gardening (CR-447 waits for it; the batch's end moves
later).

## remote-cli-Q11 (2026-11-22, the user): scope

Split into three stacked CRs in batch-30, before CR-447, in this order: A, the rename
`board`→`serve` and `webui` (this CR); B, the two keys (read-only and private); C, login,
profiles and the remote commands (needs B). Answer: "3 CR".

## remote-cli-Q14 (2026-11-22, the user): `webui` starts the server

`webui` starts the server when nothing runs, always, with no further yes (typing it is the yes);
AGENTS.md names it as a third starter of the server and hub. Answer: the recommended option.

## Chief of Staff's decision (2026-11-22)

A server `webui` starts stops 30 minutes after its last client, with no seat.

## remote-cli-Q17 (2026-11-22, the user), part (c)

From the second critique: "Pourquoi tu ne pourrais pas isolé l'environnement ? Sur une machine
donnée il peut y avoir n surfaces actives en même temps, elles seront dans plusieurs projets git
différent il faut juste qu'ils ne s'écrasent pas les port http etc". Read by the Chief of Staff,
part (c) for this CR: two surfaces' servers on one machine never clash: ports, keys and state stay
per surface; a default port already taken by another surface's server takes a free port and
prints it.

## Chief of Staff's decision (critic finding 8, 2026-11-22)

A `webui`-started server held open by the session's own watcher is named in the blocked-sync
message (`PID <n> serve`, started by `webui`); the user stops it by hand; this CR's sentence is
corrected.
