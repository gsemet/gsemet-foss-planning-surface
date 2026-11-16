# Parallel mode: pay less for each merge

## The request

In a parallel batch each merge sends the other open CRs back to rebase, run the long gate and CI
again and verify again. Batch-11 paid this several times (its retro). Measure it, and see whether
ready CRs can be merged in an order that limits rebases. Also seen in real-direct run 1
(2026-11-12, PR 137, finding 9): CR-101 delete-item paid three rebases, each with a
conflict-resolver ($3.32 of $9.22). The plan could chain CRs that all touch the same files
(there, the README's Routes table and the item template).

## The problem

- The rule today (`foreman.md`, "Parallel"; `chief-of-staff.md`; `driver.md`): after each merge,
  every CR with a PR still open goes back to a Driver; "conflict or not, its checks run again at
  the new head": rebase, push, long gate, CI, Verifier. With n PRs open, n merges cost about
  n²/2 such passes.
- What the records already say:
  - Batch-11 retro: CR-181, CR-176 and CR-182 went back after a merge; two of the three patches
    were identical or clean after the rebase. For CR-184 and CR-185 the rebase was clean or
    context-only, and "the gate re-run, not the rebase, was the cost (about 13 minutes of the long
    gate each time)". Its own note: a PR the forge reports mergeable needs no rebase note.
  - Batch-14 retro: one gate lock queued four long gates behind one another; the re-gates after
    each merge fed that queue.
  - Real-direct run 1: five CRs that all append to the same README table. Every rebase of the
    slow CR conflicted; three conflict-resolvers, and one resolution added a byte-order mark that
    cost a round.
- So there are two different costs: (a) checks run again on a rebase that changed nothing in the
  CR's patch (the common case, paid in gate minutes and Verifier calls); (b) real conflicts on a
  hot spot that every CR of the batch edits (paid in conflict-resolvers and rounds).
- The order of merges does not help much by itself: among PRs that overlap, each merge still
  moves the others, whatever the order. What helps is not sending back a PR the merge did not
  touch (a), and not starting side by side CRs known to edit the same lines (b).

## What would fix it

1. **Measure first, from what is recorded.** A table in the CR's PR, from batch-11's and run 1's
   `events.jsonl` and `cost --by cr`: per merge, the CRs sent back, whether the rebase changed
   the patch, and what the pass cost (gate minutes, agents started, dollars). No new CLI command.
2. **A ready PR the merge did not touch stays ready** (open for the user, below): the steering
   session reads the forge before it sends a rebase note.
3. **The plan proposes a chain for a known hot spot** (open for the user, below): CRs whose
   specifications edit the same lines, such as one shared table. The cards already allow it
   ("you may propose a queue with no real dependency … the plan gives the reason", and the
   Foreman's chain); they also say "touching the same file is no reason to wait". The change is
   to name the hot-spot case, not to chain on a shared file.

## Out of scope

- A merge-order advice line in the reports: no measured gain (above).
- Series and stack batches, and the stack driver's restack.
- A new CLI tool or a refusal in `rails.py`: the judgement is the steering session's, the forge
  read is the agents'.
- The batch-wide gate lock (item `stop-own-gate`), the race of a rebase note with a ready
  hand-back (item `rebase-note-check-status`), byte-order marks (item `check-rejects-bom`).
- A project whose rules ask for an up-to-date branch before a merge: its rules rank above, and
  every PR is rebased as today.
