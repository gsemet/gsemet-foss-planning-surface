Short name: `release-0-13`

# Answers

1. Q: Make a release? User, 2026-11-18: "fait une release sans evals".
2. Q: The eval campaigns that CONTRIBUTING.md asks for before a release? User, same words: none.
   No campaign and no new run. The claims file `evals/results/claims-v0.13.0.md` marks each claim
   `scenario only` (proved by a named check of `just scenario` or `just test`) or `not exercised`.
   The notes' "For contributors" bullet lists them, and the PR says no eval ran.

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- Version: v0.13.0, minor. There is new behaviour since v0.12.0 (the forge hub and `chantier
  watch`, a Foreman batch switched to direct mode with CRs in flight, a CR Driver started in its
  worktree, the batch's shape in the pane, the archive kept out of the PR by default, a session
  that stops when its CLI cannot run, a project logo), and nothing breaks a user's setup. The
  archive's new default (off on an external surface) is named in the notes as a change of default.
- Batch: batch-27, the batch whose work it ships (docs/release-process.md). Batch-27 is paused
  with its seven CRs merged; the release joins it with `order add --release`, from an up-to-date
  `main`. Batch-26's work, merged since v0.12.0 too, is shipped by the same release.
- Notes cover everything since v0.12.0 on `main`: every `feat:` and `fix:` commit exactly once.
- Highlights: the forge hub and `chantier watch` (a merge wakes the steering session, measured at
  about 27 s on 2026-11-18), the switch of a Foreman batch to direct mode with CRs in flight, and
  the archive kept out of the PR unless the project says yes.
- The watch highlight (spec critic, 2026-11-18): the host references still mark the session's
  wake by the watcher unproved. The notes keep the highlight but say it is on Claude Code only,
  observed once (about 27 s, 2026-11-18) and still on trial, and unproved on Copilot; the claims
  file and the "Not exercised by an eval." bullet name it. Marking the host row proved is not
  this release's work.
- Images come from batch-26's and batch-27's real runs: the merged PRs' evidence screenshots, the
  batch's `STATUS.md`, `report.md`, `conversation.md` and CLI output, anonymised as
  docs/release-process.md says, with no local user path and no username. None invented. No docs
  SVG diagram.
- Grant: the user merges the version PR. Each irreversible step after that (tag, forge release)
  waits for the user's approval.
