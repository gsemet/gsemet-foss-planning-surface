# Answers

## 2026-11-14: a fix of the v1.9.1 release

Owner, 2026-11-14: « fait tout ça dans le batch en cours et fait un release 1.9.1 », and the
overnight grant O-11 (releases=2, fixes=on). This is a fix for the release CR (CR-323, second
release), merged before the version PR. Priority P1.

Decided by the Chief of Staff (no user impact, CI only):

- The default stress run on the version push must finish with a clear margin (at least a third)
  under its launch deadline and under the job's `timeout-minutes`, on the current 17 scenarios.
- Preferred: the launch deadline scales with the work (rounds times scenarios, from a measured
  per-scenario cost), with a ceiling under the job limit; the spec-writer may pick another way (a
  lower default repeat, a narrower default list) that meets the same goal. No scenario is dropped
  from the stress list.
- The REPEAT guidance in the recipe's comment, CONTRIBUTING.md and ci.guidelines.md is updated to
  the real figures.
- Proof: a heavy run on the branch with the default repeat, green, with its stress duration
  reported against the deadline.
