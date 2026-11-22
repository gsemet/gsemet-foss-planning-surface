
## remote-cli-Q1 (2026-11-22, the user): naming

Asked: `chantier board` starts the surface server today; which names? Answer: "Serve, live, webui":
`chantier serve` starts the surface server (today's `chantier board`), `chantier live` stays the
terminal client (the TUI), `chantier webui` is the web UI's command.

## remote-cli-Q2 (2026-11-22, the user): scope of the remote commands

Asked: today's API only (read, backlog, config, file an idea, plus the TUI), or also the batch
commands (take, round, handback...) through the server, which changes AGENTS.md's rule that the
server never edits a batch? Answer: "Aussi les commandes de batch": the batch commands too, in
this CR; the AGENTS.md rule changes with it.

## remote-cli-Q3 (2026-11-22, the user): `chantier webui`

Answer (the recommended option): it prints the board's link with its key, and starts the server
when none runs.

## remote-cli-Q4 (2026-11-22, the user): how a remote agent runs a command

Asked: the same command with `--url <link>`, or a dedicated `remote` group? Answer: "Il faut un
system de login comme gh. Une fois fait les commandes se rappelle du serveur (on peut avoir un
système de profile avec un par défaut )": a login, like `gh auth login`; once logged in, the
commands remember the server; profiles, one of them the default.

## remote-cli-Q5 (2026-11-22, the user): which commands run remotely

Answer: "Toutes": every CLI command, `order`, `open` and `cancel` included.

## remote-cli-Q6 (2026-11-22, the user): placement

Answer: batch-30, right before CR-447 docs-gardening (CR-447 waits for it; the batch's end moves
later).

## remote-cli-Q7 (2026-11-22, the user): local or remote after a login

Answer (the recommended option): with an active default profile, every command goes to the
server; `--profile local` (or `chantier logout`) runs it locally again. On the server's own
machine no login is needed: everything stays local, as today.

## remote-cli-Q8 (2026-11-22, the user): where the profiles live

Answer (the recommended option): one file in the user's config folder (`~/.config/chantier/`,
`%APPDATA%\chantier\` on Windows), like `gh`; a named exception to AGENTS.md's rule that chantier
writes only in the planning folder.
