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

## batch-takeover-Q4: scope

2026-11-16, the user chose the recommended answer: the whole retro point. `pause` accepts a batch
whose remaining CRs are stopped or blocked by the user; the CR keeps its existing PR branch (no
second push of one head to two branches); the stale batch-20 record (`running` in
`5-archives/batches`) is closed as superseded.
