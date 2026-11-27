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

## The owner's request that widens this CR (2026-11-27, same session), verbatim

"Il faut rebase. Après en P1 tu mets une CR sur un plan d'optimisation des check locau et CI.
Parallisarion, test lourd que après merge ou optionnellelenr sur les PR"

So this CR is **a plan to optimise the local and CI checks**, with at least:

- parallel runs, locally and in CI;
- heavy tests run only after the merge, or on a pull request only when asked.

Related, already specified and in the same backlog: `split-heavy-ci-jobs` (the heavy `integration`
and `stress` jobs split in two parallel parts).

## Measured in CI and on this PC (2026-11-27)

- Pull request checks today (run 45947061700, jobs in minutes): static-windows 8.4, visual-2 7.8,
  visual 7.4, static 5, viewer-graph 1.7. The visual jobs run on every pull request; integration,
  acceptance and stress already run only on a push to `main` or on demand.
- Heavy run 45951664534 (22.9 min end to end): integration 19.4, stress 16.3, static-windows 12,
  visual 7.9, visual-2 7.8, static 3.9, viewer-graph 2.1, acceptance 1.4.
- `just check` (about 4 to 5 min on the owner's PC, 16 logical cores): its 15 steps run one after
  another; the Node tests already run files in parallel (unit about 53 s); pytest runs one test at a
  time (about 97 s, no pytest-xdist). A gain by parallel steps is estimated, not measured.

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
