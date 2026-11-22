# Answers

1. Q: Make a release today? User, 2026-11-22: "Il faudra faire les evals et une release ajd",
   then, after the eval: "Oui fait tout on va faire une release".
2. Q: Which eval? The real-foreman campaign, run 4 of 2026-11-22 (sandbox batch-01, five CRs, one
   native stack merge, $9.88, passed with findings). Its report is
   `evals/results/real-foreman-2026-11-22-run4.md` (PR #436). The claims file cites it for each
   claim that run exercised; every other claim is `scenario only` or `not exercised`.

## Settled by the Chief of Staff (2026-11-22, the user prefers simple options)
- Version: v0.15.0, minor. New behaviour since v0.14.0 and nothing that breaks a user's setup:
  the web board grows into the place to steer (Inbox, History, Dashboard, Help, batch graph and
  Kanban, the Griller's discussion panel), the surface server serves an API over a WebSocket with
  a private and a public read-only key, CLI commands run remotely through it (`login`, `webui`,
  `serve`), `chantier live`, typed waits, leases, forge connectors, the writer that publishes the
  plan, stack batches that keep their shape.
- Batch: batch-30, the batch whose work it ships (docs/release-process.md); every other CR of it
  is merged. It joins with `order add --release`, from an up-to-date `main`.
- Notes cover everything since v0.14.0 on `main`: every `feat:` and `fix:` commit exactly once.
- Highlights (two to four): the web board as the place to steer, the Griller in the board
  included; the CLI run remotely through the surface server, with a private and a public key;
  the forge followed for you (the hub reading only what is awaited, typed waits, the writer
  publishing the plan). The release Driver may merge or reorder them for the reader.
- Images come from batch-30's real runs: the merged PRs' evidence screenshots, the batch's
  `STATUS.md`, `report.md`, `conversation.md` and CLI output, anonymised as
  docs/release-process.md says. None invented. No docs SVG diagram.
- Grant: the default. The user merges the version PR; each irreversible step after it (`just
  tag`, `gh release create`) waits for the user's word, asked with the merge go.
- A push or PR the host refuses the Driver, the Chief of Staff runs itself (the user's standing
  rule).
