---
type: cr-answers
description: The user's word on round-one-host-default-matrix, and the behaviour choices the Chief of Staff settled with no grill.
---

# Answers

## The user's word (2026-11-17)

The user, after the retro of batch-24: "remet les 5 dans le batch et on continue" (put the five
retro points back in the batch and go on). This CR is one of the five; it was not grilled. The
choices below fill what the request leaves open.

## Settled choices (2026-11-17)

- **matrix-Q1: when a CR has a matrix.** Settled by the Chief of Staff: a CR has a host and
  default matrix when what it changes behaves differently on Claude Code and on Copilot, or with a
  shipped default and with a value the user configured (CR-331 had both). The Spec-writer judges
  it and names the matrix in the specification; a CR with neither has no matrix, and nothing of
  this CR applies to it.
- **matrix-Q2: what a cell is.** Settled by the Chief of Staff: one cell per combination that
  applies (each host, by shipped default or by configured value, and a host's refusal where one
  exists), each with the result it must show and the real flow that proves it: the CLI's own
  commands from a real state, the shipped-default cell with no user file. A record or
  configuration shape built by hand, which the real flow does not produce, proves no cell (the
  round-5 lesson of CR-331).
- **matrix-Q3: who carries it in round 1.** Settled by the Chief of Staff: the Driver copies the
  matrix into the evidence plan, and from round 1 into the Coder's checklist (one line per cell)
  and into the Inspector's prompt. A cell with no test, or tested only on a hand-built shape, is a
  blocking item for the Inspector.
- **matrix-Q4: when the Verifier probes it.** Settled by the Chief of Staff: after each round's
  commit, while the CR has never been pushed, before the rebase and the long gate (so before
  round 1's push and `ship`), a Verifier start probes every cell at the committed head. Its
  `NOT VERIFIED` is the next round, under the same round limit (`order rounds` stays the user's);
  the probe grants no round and uses none.
- **matrix-Q5: what the probe records.** Settled by the Chief of Staff: the probe writes
  `work/verifier/matrix-r<n>.md` with a `Head:` line, runs no `$CHANTIER verdict` and no gate,
  captures no before/after and checks no PR description. The Verifier at the pushed head still
  runs as today and is given the last probe file with the move, so it judges again the cells the
  move touched and carries the others.
- **matrix-Q6: a specification that names no matrix.** Settled by the Chief of Staff: the Driver
  answers for the evidence plan; when a specification written before this change names none but
  the CR plainly depends on the host or on shipped defaults, the Driver writes the matrix into the
  plan and the rest follows.
- **matrix-Q7: scope.** Settled by the Chief of Staff: cards only, no CLI change (the CLI already
  takes `phase <cr> verifier <detail>` at any step and knows no role); no agent file changes.
