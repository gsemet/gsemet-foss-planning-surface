# Answers

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)
- Grilled enough: the intent is the grill. The user's go, 2026-11-20: "relance un foreman avec les inbox et les p1"; this CR joins batch-29 (factory, stack) once specified.

## Settled by the Chief of Staff (2026-11-20, the user asks no questions), for the specification
1. Aim: one Driver per CR in the common case. Measure first where a Driver's context grows (what
   it reads, what workers hand back; `driver.md` and the worker cards), and cut that: worker
   hand-backs stay short (path to a file plus a few lines), the Driver reads files by section, not
   whole.
2. Also make the closing step (PR body, ticks, hand-back) restartable by design: a fresh Driver
   resumes from the record and files with no rereading of the round history. Prefer card changes;
   a CLI change only for a measured token cost (AGENTS.md: CLI scope).
3. No new role and no new agent file unless the measure shows card changes cannot reach the aim;
   if one seems needed, name it as an open question.
4. Evidence: what a later batch's `cost --explain` should show (restarts per CR), and the
   scenario/test impact if any.
- Spec open question 1: 100,000 tokens is the threshold for closing in place, as proposed from the measure.
- Spec open question 2: `cost --explain` does not print the restart split in this CR (no measured agent token cost); the retro sorts restarts from the notes. Out of scope.
