A Driver's opening reads cost less

Measured on batch-16's transcripts (by the spec-writer of driver-context-budget, 2026-11-13): a Driver
spends about 58k tokens on its opening reads (cards, rules, specification) before any work, out of a
budget of 130k once CR-236 lands.

Wanted: find which reads a Driver needs whole and which it can read by section or leave to its workers
(e.g. the project rules, concepts.md, the full specification), and cut the opening cost; measure before
and after on a real batch.