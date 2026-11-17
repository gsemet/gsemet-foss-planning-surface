# Answers

## stack-state-Q1: how the state shows

2026-11-17, the user chose a combined label in one column, not the recommended two columns: e.g. `ready, PR draft (#251)`, `running`. The stack-driver card says the stack is made from the hand-back state (ready), whatever the PR's draft flag.

Spec critic: yes, it changes what `take stack` and `stack` print and the stack driver's card.

## Spec questions (2026-11-17)

- stack-state-Q2 (live Driver's word): `working`, the stored status, the same word everywhere (not `running`).
- stack-state-Q3 (out of draft): `PR out of draft` (not `PR ready`: "ready" is the ambiguous word this CR removes).
