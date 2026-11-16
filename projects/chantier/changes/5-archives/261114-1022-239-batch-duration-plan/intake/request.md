Before the go, the Chief of Staff gives the batch's expected duration from measured times, and promises no delivery time without it.

The user (2026-11-14), after two nights without the promised stack: "je suis très déçu, tu n'as pas fait ce qu'il fallait pour livrer une stack cette nuit. C'est la deuxième nuit que ça ne marche pas."

What happened (batch-17): the Chief of Staff said "you should have a stack when you wake up" with no estimate. The batch held 13 CRs with a dependency chain six deep (CR-221 → CR-237 → CR-222 → CR-225 → CR-226/227 → CR-228); each level takes one to three hours (rounds, long gate, CI, Verifier); CR-221 alone took about 6 hours (8 rounds). It could not fit in a night.

Wanted:
- preflight (or a `plan` command) computes the critical path in time: the median of a round, a long gate, a CI run, a Verifier, read from the archived batches' records; the wait on the gate lock counted;
- it prints "this batch takes about X hours; critical path: <CRs>";
- the Chief of Staff states a delivery time only from that figure, and offers to cut the batch when the path is longer than the time the user gives (a night).
Justification as a new CLI tool (AGENTS.md: from measured cost): two failed nights.
## After the critic's review (Fable, 2026-11-14)

Drop the estimator: medians from archives do not exist for a new user and would not have predicted an 8-round CR; a new `plan` command is speculation by AGENTS.md's own rule. Keep a floor from facts the record already holds: the dependency chain's depth, and the CRs times the gate's time under one lock (13 × 35 min is about 7.6 h before any round). Card rule: the Chief of Staff states no delivery time without that floor, and offers to cut the batch when the floor exceeds the time the user gives.