# Intent

`chantier cost` prices the Foreman's session and its subagents, not the Chief of Staff's session,
so a batch's real cost is hidden.

Measured on 2026-11-06 for batch `cr-board`, with `costs.usage` on the Chief of Staff's transcript
from the batch's opening: $8.69 over 118 calls and 48 wakes, peak context 367k, against about $10
for the whole batch. The Foreman: $2.24 over 56 calls and 17 wakes, peak context 138k.

Nothing new is needed to price it on Claude: the same transcript format, the same `usage`. To
settle: how the batch learns the Chief of Staff's transcript, the window of a session that spans
several batches and work outside them, its subagents, Copilot, and whether it counts against the
batch's budget.
