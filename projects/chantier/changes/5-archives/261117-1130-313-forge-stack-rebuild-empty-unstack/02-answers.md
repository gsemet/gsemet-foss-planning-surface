# Answers

## rebuild-Q1: in this batch

2026-11-17, the user chose the recommended answer: P1, in the next batch: an empty body on a 2xx unstack reply is a success and `rebuild` goes on; a `rebuild` that fails after the unstack says plainly that the stack is dissolved and to run `forge-stack create`.

Spec critic: yes, it changes the CLI's forge behaviour and what it tells the stack driver.

## Spec questions (2026-11-17)

- rebuild-Q2 (stack driver runs create): yes, when a refused `rebuild` ends with the new dissolved line, the stack driver runs `forge-stack create` itself; one-sentence change in driver.md (~744-750).
- rebuild-Q3 (which command): the line names `forge-stack create`, and chief-of-staff.md (~1070-1072) is changed so the Chief of Staff runs the command the line names.
- rebuild-Q4 (create accepted, reply unreadable): the dissolved line only when `retarget` failed or the create call was refused; for a create call that succeeded with a reply that cannot be read, a line saying the stack's state is unknown and to run `forge-stack show`.
