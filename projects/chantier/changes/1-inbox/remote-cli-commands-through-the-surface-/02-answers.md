
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

## remote-cli-Q9 (2026-11-22, the user): keys

Asked: with a profile, anyone holding the board link could run every command over plain HTTP on
the local network; a separate key for `cli.run`, or one key? Answer: "Il faut une clé publique en
lecture seule et une privée qui peut agir": two keys, a public one that only reads, and a private
one that can act. Read by the Chief of Staff: the read-only key opens the reads and subscriptions
(board view, `live`); the private key is needed for every write (backlog moves, `config.put`,
`project.file`, `cli.run`); `webui` prints both links, the private one for the user only.

## remote-cli-Q10 (2026-11-22, the user): whose machine a remote command reads

Answer (the recommended option): everything runs on the server's machine (worktrees, transcripts,
paths for `round`, `verdict`, `handback`, `cost`, `file @path`); reads on the client's machine are
a later CR.

## Chief of Staff's decisions on the writer's other open points (2026-11-22)

- `watch`, `gate` and `lease … hold` refused under a profile, `preflight` on the server: kept.
- `login` makes the new profile the default (the last login wins, like `gh`); `--no-default`
  stores it without.
- A server `webui` starts stops 30 minutes after its last client, with no seat: kept.

## remote-cli-Q11..Q14 (2026-11-22, the user), from the spec-critic's findings

- Q11, scope: split into three stacked CRs in batch-30, before CR-447, in this order: A, the rename
  `board`→`serve` and `webui`; B, the two keys (read-only and private); C, this CR: login,
  profiles and the remote commands (needs B). Answer: "3 CR".
- Q12, printed launch forms through a profile (the Driver block's `cli:`, the `watch:` line):
  the server sends its launch form with the answer and the client replaces it with its own, so a
  Driver started from a remote client works. Answer: the recommended option.
- Q13, `file @<path>` through the server can copy any file of the server's user into the plan:
  kept ("Garder": the private key is the user's).
- Q14, `webui` starts the server when nothing runs, always, with no further yes (typing it is the
  yes); AGENTS.md names it as a third starter of the server and hub. Answer: the recommended option.

Correction of the Q9 reading: `project.file` only reads, so it is on the read side; the planning
file write is `backlog.file`, private key.

## Chief of Staff's decisions on the critic's other points (2026-11-22)

- The read-only key opens an allow-list of read ops only; every other op, present or future
  (CR-449's `griller.send`/`griller.stop` included), needs the private key.
- A `cli.run` counts as a client for the idle stop's 30 minutes.
