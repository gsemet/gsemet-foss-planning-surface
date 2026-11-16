## Summary

The retro of the last batch found nine slips that a card's wording can prevent: a rebase run in the main checkout, a restack done one PR at a time, a smoke test writing into the live planning record, a write to `.git/info/exclude`, a commit pushed after the review, a lost first message to the steering session, an oversized bundled change, a stack offered for merge with open gaps, and asks left unread. This PR writes the rule that prevents each one into the cards. Card text only: no CLI, hook, type or test logic changes.

## Deliverables

| Slip | Rule now in the cards |
| --- | --- |
| Git run in the wrong checkout | Drivers and the conflict resolver run `git -C <worktree>`; the main checkout is read-only except the post-merge fast-forward |
| One-by-one restack after a stack merge | One planned pass: fetch and list heads once, rebase every remaining branch, push them back to back, one CI wait |
| Smoke test on the live planning record | Tests of the board's write paths use a scratch planning folder |
| `.git/info/exclude` written | A Driver and its workers write nothing in the repository's git folder |
| Commit pushed after the review | The commit must hold exactly what the Inspector reviewed, checked before and after the commit |
| First Driver message lost | Every Driver prompt carries a `Steering:` line with the address |
| Oversized bundled CR | The spec critic flags a bundle; the user is offered the split first |
| Stack offered with open gaps | The partial `stack-ready-to-merge` line carries each CR's gaps; the Chief of Staff quotes them and asks for a missing pane screenshot |
| Asks left unread | `asks --read A-<k>` runs in the turn the ask is relayed or acted on |

No visual change: no screenshot applies.

## Blast radius

Card text only, read by agents at their next start; a plain `git revert` restores the previous wording.

Grade: 1

## Autonomous decisions

- The `Steering:` paragraph of the prompt template names the host reference row, not a tool name, because a structure test forbids host tool names in the shared cards.
- The review-before-commit order is kept, as the docs diagrams show it; the added check compares the commit with the reviewed state, instead of moving the review after the commit.

## Known gaps

- The local long gate and the independent verification have not run yet; CI's `just scenario` at the head passed.
- The restack pass claim (a lease push after the fetch replaces the forge's rewrite) is unproved; it is marked so in the card, and the next native stack merge on GitHub settles it.

<details>
<summary>Details</summary>

## Changes

- `driver.md`: the `git -C <worktree>` bullet and updated examples; the git-folder rule; the four-step restack pass; the commit-matches-review check; the scratch-folder sentence; the `Steering:` rule.
- `worker.md`: conflict resolver's `git -C`; the scratch planning folder rule for tests and probes of the board's write paths.
- `concepts.md`: `Steering:` line in the prompt template.
- `foreman.md`, `chief-of-staff.md`: the `Steering:` line, gaps on the partial stack line and their handling, the bundle split, asks read in the same turn.
- `spec-critic.md`: a fourth check, the bundle.

## Impacts

No visual change. Drivers and the Chief of Staff behave as the new text says from their next start.

## Test plan

- [ ] New or changed tests (they fail on the previous code) No behaviour change
- [ ] Local gates at `42f13f0`: `just check` passes (72 tests); the long gate has not run locally yet
- [ ] Evidence: card text; no before/after
- [x] Review: approved at `9dde8c5` (the reviewed state, committed as `2a89015`, carried over a clean rebase to `42f13f0`)
- [ ] Verified at `<sha7>`
- [x] CI green at `42f13f0`: `just check` on three systems, `just eval-dry-run` and `just scenario` pass

## Internal references

- CR-263 "batch-17 retro, card fixes"

</details>
