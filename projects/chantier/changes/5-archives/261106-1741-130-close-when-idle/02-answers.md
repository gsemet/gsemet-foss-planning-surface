# Answers

The user's answers, 2026-11-06:

1. What proves an agent is no longer active: the recorded state and the transcripts. `close` refuses
   if the state shows work, or if a transcript was written in the last few minutes.
2. `order add` on a landed batch: it reopens the batch, and `land` runs again at the end.
3. The cost is final at `close`, once nothing runs; `land` prints it as not final.

Found after these answers, on batch-06: `land` builds its summary before it records its time, so a
second `land` priced up to the first one. `STATUS.md` kept $49.38 in its Cost section under a header
of $53.12.
