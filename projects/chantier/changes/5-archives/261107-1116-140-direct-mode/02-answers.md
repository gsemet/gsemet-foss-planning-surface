# Answers (grill with the user on the conditions, 2026-11-07)

## When

1. Who decides: the Chief of Staff may propose direct mode in the plan; the user's go approves
   it, like any batch.
2. When to propose it: a host that cannot start a Foreman, or few CRs.
3. Thresholds and limits: the same configuration as Foreman mode (slots, rounds, budget, the
   project's `chantier` section); no separate CR threshold for direct mode.

## How the batch runs

4. The batch is a normal batch: `open`, its slots, `land`, `close`, the same folders and
   `STATUS.md`. Several slots run in parallel as in Foreman mode: the only difference is that
   there is no Foreman. (The first wording, "not several in parallel", was corrected.)
5. The batch is strict: no dynamic additions (no `order add` of a new CR while it runs).
6. The Drivers run in the background. The Chief of Staff does the Foreman's job until the batch
   completes and refuses any grill or discussion meanwhile, to stay on the steering.

## What the Chief of Staff still accepts while it steers

7. "status?" and "what did it cost?": read-only.
8. Answers to a blocked CR of this batch (written to its `02-answers.md`, as today).
9. Orders on the batch itself: "I merged #42", "drop CR-140", "stop the batch".
10. Any other request is noted word for word and handed back at the end; an idea may be filed in
    the inbox at once (`file`, no grill).

## Switching mode

11. A batch may switch from direct to Foreman mode while it runs, but not on Remote Control,
    or only once the Foreman's working has been checked beforehand (the preflight's Foreman
    conditions pass) before the switch.

## Open, for the refinement

- Where the mode is recorded (the batch's record, so `status`, `close` and a resume know it).
- The cost: `close` prices a recorded Foreman transcript today; in direct mode the steering is
  the Chief of Staff's own session.
- Which preflight conditions direct mode keeps (P1 is the Foreman host's).
- The switch: how the Foreman takes over the running Drivers, and whether a Foreman batch may
  switch back to direct.
- The cards and the hard rules to change (`SKILL.md`, `chief-of-staff.md`, `routing.md`, the
  Foreman card read by the Chief of Staff in direct mode), on both hosts.
