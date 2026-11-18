# Bug: handoff and the record show PR none for a merged release PR

`handoff CR-366` printed `PR: none; head -` although the version PR 331 was opened, green and
merged, and the CR's `STATUS.json` has `pr: null`. The same happened for CR-352 (v0.12.0). The
batch's `status` line for CR-366 shows `-` where a CR's PR link goes. A release CR's record should
hold its version PR like any other CR's.

Source: batch-27's retro (CR-366), kept by the retro critic.
