# Intent: add several CRs to a paused batch

## The problem

Today, `order add` on a paused batch sets it running at once (`commands.py`, "was paused: running
again"). A running direct batch is strict, so a second `order add` is refused. Only one CR can
join a direct batch per pause.

This was seen in batch-09 on 2026-11-10: the user asked to add `status-command` and
`planning-repo`, and only the first joined. The batch could not be paused again either, because
the new CR was queued.

## The intent

- While a batch is paused, `order add` can be run any number of times. Each run adds one CR and
  leaves the batch paused.
- The batch runs again when the first added CR starts (`take`).
- The rule is the same in direct and Foreman mode.
- The strict refusal on a running direct batch stays as it is, release exception included. Its
  message names only the pause, not Foreman mode.

## Where it shows

- the CLI (`commands.py`: `order add`, `take`);
- the structure test `test_a_direct_batch_is_recorded_shown_and_strict`;
- the scenario;
- the cards that describe the pause: `concepts.md` ("a paused batch … takes new CRs, which set it
  running again") and `chief-of-staff.md` ("The running batch is strict").
