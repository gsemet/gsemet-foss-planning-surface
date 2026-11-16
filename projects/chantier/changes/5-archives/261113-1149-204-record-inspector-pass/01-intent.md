# A Driver records each Inspector pass before the PR body cites it

## The problem

In real-direct run 1 (2026-11-12, PR 137) the Verifier said `NOT VERIFIED` three times for one
cause: the PR description said the change was reviewed and approved (`Review: approved at
<sha7>`), and nothing in the CR's record showed that pass. Each time cost a Verifier pass and a
description fix, on a change that was sound.

## Where it shows

- `skills/chantier/references/worker.md`, Inspector: it is read-only and "writes nothing: its
  reply is its output". The approval exists only in the Driver's context.
- `skills/chantier/references/driver.md`, "CR driver": the only recorded approval is the note
  after a round's commit (`r<n> approved at <head>, committed as <sha>`). The other passes leave
  no trace: a body-only re-inspection in the same round, the inspection of a rebase that changed
  the patch, a review step of the `Team:`, the stack driver's inspector after a move. And nothing
  orders the note before the body is written.
- `skills/chantier/references/pr-template.md`, Test plan: the `Review: approved at <sha7>` box
  cites the pass.
- `skills/chantier/references/worker.md`, Verifier: a claim of the description "with no proof in
  `verify.md`, the gates or the evidence is `NOT VERIFIED`", and the Inspector's notes are not
  proof. So the Review box has nowhere to be proven from, unless the record holds the pass.

## What would fix it

- driver.md: every `APPROVE` an Inspector (or a review step) returns is recorded at once with
  `$CHANTIER note`, with what the JSON says (the verdict, its `head`) and what was reviewed (the
  round, the body alone, a move), and the commit once there is one. The Review box of
  `pr-body.md` is filled or updated only from such a note, with its SHA.
- worker.md, Verifier: the Review box is judged against that note in the CR's record (`log`,
  `handoff`): present with the same SHA, the claim holds; absent or another SHA, `NOT VERIFIED`
  as today.
- pr-template.md: the Review box names the SHA of a recorded pass.

## Out of scope

- A CLI record of the Inspector's verdict (a `verdict`-like command) or a `handback` check on it.
- The Inspector writing anything: it stays read-only.
- What the Inspector reviews, and when a new inspection is needed after a move.
- The agent files of both hosts.
