# Answers (copied from the parent CR)

Copied 2026-11-22 from `remote-cli-commands-through-the-surface-/02-answers.md` (the parent CR,
split in three by remote-cli-Q11); the parent's file stays the record. Part B: the two keys.

## remote-cli-Q9 (2026-11-22, the user): keys

Asked: with a profile, anyone holding the board link could run every command over plain HTTP on
the local network; a separate key for `cli.run`, or one key? Answer: "Il faut une clé publique en
lecture seule et une privée qui peut agir": two keys, a public one that only reads, and a private
one that can act. Read by the Chief of Staff: the read-only key opens the reads and subscriptions
(board view, `live`); the private key is needed for every write (backlog moves, `config.put`,
`cli.run`); `webui` prints both links, the private one for the user only.

Correction of the Q9 reading (2026-11-22): `project.file` only reads, so it is on the read side;
the planning file write is `backlog.file`, private key.

## remote-cli-Q11 (2026-11-22, the user): scope

Split into three stacked CRs in batch-30, before CR-447: A, the rename `board`→`serve` and
`webui`; B, the two keys (this CR); C, login, profiles and the remote commands (needs B). Answer:
"3 CR".

## Chief of Staff's decisions on the critic's points (2026-11-22)

- The read-only key opens an allow-list of read ops only; every other op, present or future
  (CR-449's `griller.send`/`griller.stop` included), needs the private key.

## Second critique, finding 7 (2026-11-22, the coordinator)

When CR-449 lands first, this CR also edits CR-449's panel strings (the web client's i18n), its
`docs/web-board.md` text and the Griller's card: "replaces both keys", "the private key".
