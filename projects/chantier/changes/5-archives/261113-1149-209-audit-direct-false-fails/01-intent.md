# Audit: two checks fail on lawful behaviour

## The request

From real-direct run 1 (2026-11-12, PR 137, findings 4 and 5): 4 of the audit's 6 FAILs were the
audit's own mistakes. Fix `evals/kit/audit.py` so both checks pass on what the cards allow.

## The problem

- **J3, the Verifier's detached worktree (3 FAILs).** `worker.md` lets one worker create one
  worktree: the Verifier, a detached worktree of the CR's base for its "before" capture (`git
  worktree add --detach <path> <base>`, removed at its end). `audit.py` checks "creates no
  worktree: the Driver did" for every worker, the Verifier included, with a pattern that matches
  any `git worktree add`. Three Verifiers of run 1 did what their card says and were failed.
- **C9, the report refresh with no epoch (1 FAIL).** `status-layout.md` and `chief-of-staff.md`
  require `status --refresh` with no epoch before a report; only the loop's wake carries
  `--epoch`. In direct mode the steering transcript is the Chief of Staff's, so it holds both
  kinds. `DIRECT_EPOCH_COMMANDS` matches every `status --refresh` and fails those with no epoch.
- A false FAIL costs a hand check at every run and hides the real ones: the run's two true slips
  (a Verifier's write to the host's scratchpad, the rules read before the claim) sat among four
  wrong lines, and the scorecard marks C9 and J3 "seen, wrong".

## What would fix it

- J3: a Verifier's `git worktree add --detach` is not a breach. Any other worktree creation by a
  worker, a QA driver or a review step still fails, and so does a Verifier's worktree that is
  not detached.
- C9: in a direct batch, a `status --refresh` with no epoch passes. Every other steering command
  of the list still needs its epoch.

Done when: the audit run again on run 1's workspace reports 2 FAILs (J3 scratchpad write, J14
rules), the four others pass, and the eval kit's dry run still passes.

## Out of scope

- The two real FAILs of run 1: the Verifier's scratchpad write (the Verifier's card) and J14
  (item `rules-after-claim`).
- Any card or CLI change: this is the eval kit alone.
- New checks (for instance that the Verifier removes its worktree), and the Copilot audit.
- The run 1 report, which is not rewritten.
