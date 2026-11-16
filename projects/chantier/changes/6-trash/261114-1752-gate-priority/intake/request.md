# Gate queue and push order: put the user's next merge first

Filed 2026-11-14 by the Chief of Staff, on the user's word: a CR for after batch-17.

Two rules in the cards slow down the PR the user will merge next:

1. Long gates run in arrival order (`concepts.md`, "Long gates run one at a time, in arrival
   order"; `driver.md`, the long gate). The CR whose merge comes next for the user (the stack's
   lowest open PR, then its children once restacked on main) should take the first place in the
   queue; queued gates yield to it; a gate already running is never stopped.
2. The Driver pushes only after the long gate (`driver.md`, "Rebase first, so the long gate passes
   on the head you push"). For a PR that already exists, after a rebase or a restack, the Driver
   should push at once with `--force-with-lease`, the PR kept in draft, so CI runs while the gate
   waits in the queue; the PR leaves draft only when the long gate and CI have both passed at the
   same head. A new PR still waits for its long gate, as `AGENTS.md` requires.

The principle missing from the cards: what unblocks the user's next merge goes first.

## Evidence (batch-17)

- CR-237 (PR #171) rebased cleanly onto main at about 11:24, waited for CR-225's running gate,
  started its own at 11:53, passed at 12:29, and was pushed only then: CI started at 12:30.
  About an hour lost on the PR the user was waiting to merge.
- The Foreman applied both rules by direct order of the Chief of Staff during the batch, then
  extended rule 2 to CR-240, which had no PR yet, against `AGENTS.md`; corrected before any PR
  was opened.
