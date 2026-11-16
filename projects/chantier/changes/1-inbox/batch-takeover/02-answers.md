---
type: cr-answers
description: The user's answers to the grill of taking over a batch opened on another machine.
---

# Answers

## batch-takeover-Q1: how the batch's state reaches the other machine

2026-11-16, the user's words (French, translated): "There must be an active record that is not
published (gitignore) and another one updated only at the start and at the pause." So two
records: the batch's live record stays local and ignored by git, as today; a second, published
record (in the surface) is written only at the batch's open and at its pause. A takeover reads
the published one.

## batch-takeover-Q2: when a takeover is allowed

2026-11-16, the user chose the recommended answer: allowed when the batch is paused, or when the
other machine has been silent for a while; otherwise refused with its last activity named, and
allowed only on the user's explicit confirmation.

## batch-takeover-Q3: the costs

2026-11-16, the user's words (French, translated): "It must go in the pause file." The cost
priced to date on the machine that pauses is written in the published record at the pause; a
takeover carries it over.

## batch-takeover-Q5: a batch that is not paused

2026-11-16, the user chose the recommended answer: since the published record changes only at the
open and the pause (Q1), another machine cannot see the first one's silence, so Q2's "silent for
a while" is dropped. A paused batch is taken over at once; a batch not paused is refused with its
open time and machine named, and taken over only when the user confirms the other machine has
stopped.

## batch-takeover-Q6: a machine stopped without a pause

2026-11-16, the user chose the recommended answer: the takeover starts from the record published
at the open, plus what the forge and the surface show (the PRs, the branches, the CRs' pushed
documents); the rounds, notes and costs never published are named "lost on <machine>", never
estimated.

## The specification's open questions (first run), 2026-11-16

- Q7, the user chose the recommended answer: a paused batch that starts again (its first `take`
  or `order qa`) counts as a start: the published record is written again as running, so another
  machine cannot take it over without the user's confirmation.
- Q9, the user chose the recommended answer: the published record holds the brief, the CRs' notes
  and the events (no worktree paths, no session ids), so a takeover finds everything.
- Q8, the user chose the recommended answer: machine A's leftover local copy is replaced when
  needed: A takes the batch back with `takeover` once it is paused again, and A's `open` replaces
  the leftover copy of a batch closed elsewhere, after saying so.

## Grilled enough

2026-11-16, after the Chief of Staff's restatement, the user: grilled enough; the spec-writer
writes the specification. Spec critic: yes.

## batch-takeover-Q4: scope

2026-11-16, the user chose the recommended answer: the whole retro point. `pause` accepts a batch
whose remaining CRs are stopped or blocked by the user; the CR keeps its existing PR branch (no
second push of one head to two branches); the stale batch-20 record (`running` in
`5-archives/batches`) is closed as superseded.
