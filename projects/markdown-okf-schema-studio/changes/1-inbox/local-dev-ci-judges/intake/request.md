# Local development stays quick and CI is the judge

# Local development stays quick and CI is the judge

## The owner's words (2026-11-27, Chief of Staff session of batch-09), verbatim

"Le just check fait combien de temps ? Parce que je pense pas que ce soit la source de problème . Il
faut un système où tu peux dev en local efficacement et la CI sanctionne. 1h de test visuel c'est
intéressant uniquement si ça apporte quelque chose"

## Measured on batch-09 (agents' wall time, from the transcripts, 2026-11-27)

| Minutes | CR-516 | CR-517 (not finished) |
| --- | --- | --- |
| All worker agents | 319 | 217 |
| Model (thinking and writing) | 99 | 92 |
| Old/new comparisons and other commands | 67 | 23 |
| Targeted browser tests and probes | 30 | 42 |
| `just check` (about 4 to 5 min a run) | 41 | 24 |
| Waits (background commands, sleep) | 34 | 32 |
| Whole visual stage, direct calls (3 runs of about 13 min, part counted in the waits) | 23 | 0 |
| `just preflight` | 14 | 0 |

On CR-516 the three local runs of `just ci-visual` (rounds 2, 3, 5) each gave 524 of 530 captures,
with the same 6 failures as on the unchanged head (this Windows host): they showed nothing about the
change.

## Where the rule comes from

`.agents/guidelines/change-requests-lifecycle.guidelines.md`, "Project bindings", "Visual evidence":
"the headless visual run of the local gates for the editor and the preview". Its "Early heavy CI"
rule pushes early only for a change that touches visual, integration or stress scenarios.

## Proposal of the Chief of Staff (not yet accepted)

1. Locally: the tests of the touched files, then `just check` once before the push.
2. Push after the first round: CI judges while the review runs.
3. The reviewer reads the CI result and does not run the suites again.
4. A proof worth keeping is a test in the repository; no long throwaway comparison unless the
   specification asks for it.
