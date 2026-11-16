# Answers

## 2026-11-11

- Picked by the user as a CR of the next `real` eval campaign (the user chose it among the Chief of Staff's proposals). Its PR opens as a draft and is not merged.

- Grill: a ready CR sent back to its Driver (a rebase, a fix) is reopened by `take <cr> --note "<why>"`: it goes back to working and counts no round. The Driver passes both gates again at the new head, then hands back ready again. (The user chose "take la rouvre".)
- The eval is steered by a new Foreman session, which the user starts (the user chose "Session Foreman").

- Grilled enough: the user answered "Oui" to starting the spec-writers.
- The specification makes the PR open as a draft, with the first line of its body "**Eval run: do not merge.** The maintainer decides what happens to this PR." (`evals/real-foreman/RUNBOOK.md`).


## 2026-11-11, the spec-writer's open questions

- Q1: yes, `handback ready` refuses when the worktree's head differs from the head `ship` recorded; the Driver runs `ship` again, then the gates at the new head. (The user chose "Oui, il refuse".)
- Q2: yes, after the `take` the steering session resumes the Driver that handed the CR back; a new Driver only when the old one does not answer. (The user chose "Oui, il le reprend".)

- The resume covers a CR taken back from ready only; a CR taken back from blocked gets a new Driver. (The user chose "Ready seulement".)
- Go for the eval: "Oui, ouvre".

