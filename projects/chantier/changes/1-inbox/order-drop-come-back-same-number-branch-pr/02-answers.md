# Answers

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)
- Origin: split from `order-drop-asks-where-the-cr-goes-trash-`, spec-critic finding 10. That CR writes `formerly.json` at the drop (with `pr_draft`); this CR reads and consumes it.
- The number (that CR's spec question 1): a CR moved out keeps its number; when it joins a later batch it gets the same number back (CR-381 stays CR-381); the number is never given to another CR.
- Its branch and PR (that CR's spec question 2): its new Driver picks up the existing branch and open PR, rebased on the new base; it starts fresh only when the branch is gone.
- Finding 1: a moved-out CR whose PR the user merges later: on "I merged #n" the Chief of Staff adds it to the open batch and records the merge (`order add`, then `order merged`); the Driver card treats a recorded PR found merged as "nothing to do, ask the Chief of Staff"; chief-of-staff.md names the route.
- Finding 6: a reopen resets every per-round and stack field (`stacked`, `head`, `pr_base`, `start_on`, `blocked_reason`, `attempts`, `phase_*`, `gate_waiver`); `pr_draft` is carried by `formerly.json`.
- Finding 8: reopen a closed PR before any push to its branch; "GitHub refuses to reopen after a force-push" is marked unproved.
- Depends on `order-drop-asks-where-the-cr-goes-trash-` (it writes `formerly.json`).
