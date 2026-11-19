# Answers

1. Q: Make a release? User, 2026-11-19: "Puis tu fais la release sans evals".
2. Q: The eval campaigns that CONTRIBUTING.md asks for before a release? User, same words: none.
   No campaign and no new run. The claims file `evals/results/claims-v0.14.0.md` marks each claim
   `scenario only` (proved by a named check of `just scenario` or `just test`) or `not exercised`.
   The notes' "For contributors" bullet lists them, and the PR says no eval ran.
3. Q: A release CR in batch-28 waits for every other CR, CR-381 and CR-382 included, which the
   user keeps for next week: take them out of the batch to release now? User, 2026-11-19: "Oui
   sort les du batch. Fait la 0.14.0 sans evals et clos le batch". CR-381 (#346) and CR-382 (#347)
   are dropped from batch-28 with their PRs left open as drafts; they join a later batch. Their
   work is not in v0.14.0.

## Settled by the Chief of Staff (2026-11-19, the user asks no questions)
- Version: v0.14.0, minor. There is new behaviour since v0.13.0 (factory mode and a batch opened
  with no CR, `chantier validate`, the board's Configuration page for the limits, the watcher
  woken by what the user does in the board, addressed events, one elected surface server for the
  board and the forge hub, a release finished after the user publishes it by hand), and nothing
  breaks a user's setup.
- Batch: batch-28, the batch whose work it ships (docs/release-process.md). Every other CR of the
  batch is merged, cancelled or dropped; the release joins with `order add --release`, from an
  up-to-date `main` (18b251d7 or later).
- Notes cover everything since v0.13.0 on `main`: every `feat:` and `fix:` commit exactly once.
- Highlights (two to four): factory mode (a batch opened with no CR, and a CR made ready joins it
  on its own); the board as the place to steer (the limits set from its Configuration page, and
  the watcher waking the session on what the user does there); one elected surface server for the
  board and the forge hub, with addressed events. The surface server is new and has no run on
  Windows yet; the notes say so, and the claims file and the "Not exercised by an eval." bullet
  name it.
- Images come from batch-28's real runs: the merged PRs' evidence screenshots, the batch's
  `STATUS.md`, `report.md`, `conversation.md` and CLI output, anonymised as
  docs/release-process.md says, with no local user path and no username. None invented. No docs
  SVG diagram.
- Grant: the user merges the version PR. Each irreversible step after that (tag, forge release)
  waits for the user's approval, asked with the merge go.
- Batch close: after the release is published, batch-28 closes; its retro is already done
  (2026-11-19, three points in the inbox).

4. Q: The host refused the release Driver's push and PR (ask A-43). User, 2026-11-19: "Oui tu peux
   pousser", then "Je ne suis pas à la maison débrouille toi pour que ce soit poussé". The Chief of
   Staff pushed the branch and opened PR #356; any later push of this version PR that the host
   refuses the Driver, the Chief of Staff runs itself. The merge, `just tag` and `gh release create`
   still each need the user's own word.
