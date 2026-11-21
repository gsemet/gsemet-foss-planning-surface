# Round 2 summary figures (CR-450), for the PR body

Real run of `just mutation-core` on a sample of 51 of the files of `src/core` (every one of the 19 sub-folders), 6,007 mutants, 1,396 tests of `test/core`. Everything is "on the sample". Details: `mutation-campaign-note.md`, `redundant-tests-core.md`, `holes-core.md`.

## Mutants (core phase)

| Killed | Timeout | Survived | NoCoverage | CompileError | Ignored | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 2,611 | 398 | 1,104 | 185 | 1,700 | 9 | 6,007 |

Overall score 70.0%. Compile errors: 1,700 (28% of the mutants; TS 7 checker, no test run for them). Others phase: 2,132 mutants on the holes' ranges (180 Killed, 15 Timeout, 623 Survived, 1,138 NoCoverage, 174 CompileError, 2 Ignored).

## Score per sub-folder

| folder | score | killed | survived | no coverage | timeout | compile error | ignored | holes only another layer kills | score with other layers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| comments | 80.0% | 295 | 74 | 5 | 21 | 203 | 0 | 1 | 80.3% |
| configuration | 92.9% | 52 | 4 | 0 | 0 | 32 | 0 | 1 | 94.6% |
| directives | 86.2% | 18 | 2 | 2 | 7 | 13 | 3 | 0 | 86.2% |
| edits | 68.5% | 37 | 14 | 3 | 0 | 16 | 2 | 0 | 68.5% |
| export | 57.1% | 12 | 9 | 0 | 0 | 9 | 0 | 0 | 57.1% |
| find | 78.6% | 50 | 11 | 4 | 5 | 27 | 0 | 0 | 78.6% |
| frontmatter | 52.1% | 309 | 221 | 80 | 19 | 328 | 2 | 2 | 52.5% |
| mapping | 62.3% | 214 | 132 | 6 | 14 | 62 | 0 | 4 | 63.4% |
| myst | 80.2% | 50 | 12 | 4 | 15 | 52 | 0 | 0 | 80.2% |
| navigation | 72.1% | 172 | 67 | 5 | 14 | 101 | 0 | 1 | 72.5% |
| palette | 3.3% | 2 | 58 | 0 | 0 | 12 | 0 | 17 | 31.7% |
| paste | 54.6% | 415 | 292 | 54 | 1 | 237 | 0 | 0 | 54.6% |
| preview | 82.9% | 215 | 47 | 0 | 13 | 111 | 0 | 1 | 83.3% |
| protocol | 77.5% | 145 | 42 | 0 | 0 | 134 | 1 | 0 | 77.5% |
| render | 85.7% | 202 | 34 | 8 | 49 | 161 | 0 | 1 | 86.0% |
| scroll | 67.8% | 142 | 62 | 6 | 1 | 43 | 0 | 0 | 67.8% |
| security | 97.8% | 64 | 2 | 4 | 197 | 25 | 0 | 0 | 97.8% |
| state | 90.0% | 203 | 19 | 4 | 4 | 123 | 1 | 7 | 93.0% |
| syntax | 96.3% | 14 | 2 | 0 | 38 | 11 | 0 | 0 | 96.3% |


The palette score (3.3%) is the emoji and icon tables: 128 data-literal mutants, not a test gap in the usual sense. The frontmatter and paste sub-folders (52% and 55%) hold the most holes.

## Holes

| | holes |
| --- | --- |
| all (Survived + NoCoverage) | 1,289 |
| no test kills it | 1,254 (1,252 after the 2 equivalents) |
| killed only by another layer | 35 |
| equivalent (listed apart, found by reading) | 2 |
| in the 25 test-worthy clusters for round 3 | 415 |
| timed out in another layer, not counted as a kill | 9 |

## Tests

| | tests |
| --- | --- |
| tests that ran | 1,396 |
| judged zero-kill | 118 (109 of them load-time only, so not judged; 97 in `previewStyles.test`) |
| judged redundant | 108 |
| not judged by the reader (mt-Q11) | 27 (plus the 109 load-time zero-kill ones: 136 in all) |
| removal candidates after the regression, boundary and SwRS-carrier marks | 75 |
| kept: regression 20, boundary 5, last carrier of an SwRS 17 | 42 |
| left out of the judgement (outside the sample) | 101 zero-kill, 722 redundant, 101 reaching no sampled mutant |

## Run time

| Phase | Time |
| --- | --- |
| Core phase (dry run 1 min 6 s, mutation testing 66 min 15 s) | about 67 min 30 s |
| Others phase (dry run 3 min 7 s, mutation testing 24 min 16 s) | about 27 min 30 s |
| Reader and checks | seconds |
| Whole `just mutation-core` | 91 min 5 s |

Concurrency 15 (7 test runners, 8 checker processes), Windows 11, 16 logical processors, Node 24. About 0.91 s per mutant overall: all of `src/core` (about 29,000 mutants) is estimated at about 7.4 h.
