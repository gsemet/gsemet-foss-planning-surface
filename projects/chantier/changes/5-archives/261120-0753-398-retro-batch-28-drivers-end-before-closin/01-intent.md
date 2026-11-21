# retro batch-28: Drivers end before closing, 43 restarts

From batch-28's retro (2026-11-19), kept by the retro critic.

`cost --batch batch-28 --explain`: 62 cr-driver agents for 19 CRs, of which 43 were restarted on a
CR that already had a Driver; Drivers are 26% of the batch's spend ($29.76 of $116.26). Driver
peak contexts were 100k-128k tokens (`cost --by cr`). The Drivers of CR-379, 381, 382, 383 (round
4), 385 and 387 stopped before the last steps (PR body, ticks, hand-back), and a fresh Driver did
the closing step each time.

Long-term fix to study: a Driver hands its closing step to a fresh short-lived agent by design, or
keeps its context smaller (what it reads, what workers send back), so a CR needs one Driver.
