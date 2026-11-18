Short name: `release-pr-recorded`

# Answers

1. Q: File it and run it now? User, 2026-11-18: "les deux. garde le batch ouvert et enchaine sur
   ces 2 bugs" (both retro points, in batch-27, now).

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- A release CR's version PR is recorded in its record as any CR's PR is, so `handoff`, `status`,
  `STATUS.json`, the board and the forge hub see it.
- The spec-writer finds the cause (the Release driver's path never records the PR, or the CLI drops
  it for a release CR) and the fix goes where the cause is: the cards if the Driver skips a
  recording step, the CLI if it refuses or drops it.
- Already-archived release CRs (CR-352, CR-366) are not rewritten.
- A test of the CLI's refusals covers it if the fix is in the CLI.
- (spec critic, 2026-11-18) The board: a row whose PR is already merged (`pr_merged`) is left out
  of the open-PR lists and counts (home's open PRs, the PRs nav count, the merge order). This
  brings `board/web/` and its `DESIGN.md` into scope.
- (spec critic, 2026-11-18) The lines agents read (`handoff`, `stack`) show a release PR already
  merged with a mark: `PR: <link> (merged)`. `status`, `STATUS.json` and the board show the
  plain link.
