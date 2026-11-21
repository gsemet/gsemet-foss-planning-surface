# Mutation campaign note (CR-450, spec 4.11)

Complete except the section "After the round 3 re-run", filled in round 3.

## Command and tools

- Command: `just mutation-core` (default: no `sample` argument and `STUDIO_MUTATION_FILES` set to the 51 sample files, see below). It runs, in order: `npm run compile`, the TS 7 checker self-test, the core phase (`scripts/stryker.config.mjs`, tests of `test/core` only, bail off), `node scripts/mutation-report.mjs --others-ranges`, the others phase (`scripts/stryker.others.config.mjs`, tests of the other layers, on the holes' ranges only), then `node scripts/mutation-report.mjs`, which writes `out/reports/mutation/summary.md` and `summary.json`.
- StrykerJS 10.1.1 with our plugins: the `node:test` runner `mdokf-node-test` (per-test coverage), the TS 7 checker `mdokf-ts7` (typescript 7.0.2, whole program, one mutant per check, 8 checker processes) and the ignorer `mdokf-messages`. `tsconfigFile` is an absent file name, so Stryker core never imports `typescript`.
- Machine: Windows 11 Home, 16 logical processors, Node 24, run from a git worktree. Concurrency 15 (7 test runner processes and 8 checker processes).
- The run lived in the background of the Driver session (its log: `work/logs/r2-just.log`). It follows the Driver brief, which asks for a background run polled with an until-loop, although the Coder card says no background shell.

## Scope: a recorded sample

A full run of `src/core` was not attempted in round 2. The sample is 51 of the 2,629 files Stryker could see, from every one of the 19 sub-folders of `src/core`, 6,007 mutants (budget: at most about 6,000). Files per sub-folder: comments 2 (commentModel, inlineThread), configuration 6, directives 1, edits 1, export 1, find 1, frontmatter 6, mapping 6, myst 1, navigation 2, palette 2 (emoji, paletteIcons), paste 1 (htmlToMarkdown), preview 5, protocol 3, render 4, scroll 1, security 1, state 6, syntax 1 (51 files). The exact list is in `work/logs/r2-sample-files.txt`, and the table "Sample" at the top of `out/reports/mutation/summary.md` gives the mutant count of each file.

Consequences, all printed in the summary and in the evidence files:

- Every reading is "on the sample". The report reader only judges tests whose test file is named after a sampled source file of the same sub-folder; the others are counted, not listed (101 zero-kill, 722 redundant, 101 reaching no sampled mutant).
- A judged test may also kill mutants of unsampled files: no removal is final before a run of the whole sub-folder.

## How the report was read

- Score = (Killed + Timeout) / (Killed + Timeout + Survived + NoCoverage); CompileError and Ignored mutants are out of the denominator. Overall: 70.0% (6,007 mutants: 2,611 Killed, 398 Timeout, 1,104 Survived, 185 NoCoverage, 1,700 CompileError, 9 Ignored).
- Holes = Survived + NoCoverage of the core phase: 1,289. The others phase labels each one: killed by a test of another layer ("killed only by another layer", 35) or not ("no test kills it", 1,254).
- Zero-kill test: reaches killable mutants and kills none. Redundant test: all the mutants it kills are also killed by a keeper (greedy set cover, sole killers first, then the largest gain). Not judged: reaches only Ignored, Timeout or CompileError mutants (mt-Q11).
- Decision on Timeouts of the others phase (the run needed it: 15 Timeouts there, 9 holes touched): a Timeout in another layer is not counted as a kill. The hole keeps the label "no test kills it" and the report says "timed out in another layer (not counted as a kill)". Reason: a timeout in a mutant of an infinite loop is a signal that something stopped, not that an assertion failed; the core phase does count its Timeouts as detected (Stryker convention), which is a stricter reading on the others side and keeps the label cautious.
- Decision on load-time coverage (new, from the data): a module's load-time mutants (constants, tables) are credited to every test of a file (mt-Q9), so a test that reaches only such mutants has zero kills by construction. 97 of the 118 judged zero-kill tests are in `previewStyles.test` and 109 of the 118 are of that kind. The evidence marks them "not judged" (an extension of mt-Q11, to be moved into the reader in round 3 if kept).
- Equivalent mutants were found by reading, not by proof: two so far (see `holes-core.md`).

## Proposed removal rules (not applied)

1. A removal candidate is a judged test that is zero-kill (not load-time only) or redundant. A not-judged test is never a candidate.
2. A test that carries `@tests_req` is removed only if a test that stays carries the same SwRS; the marker moves in the same commit and `just requirements-update` must show no loss. The evidence file marks the last carrier of an SwRS "keep".
3. A merge of near-duplicates keeps the intent of every assertion (table-driven test with one row per input).
4. Regression tests (a bug, a CR, a stability fix) and boundary tests (cap, limit, exact, edge) are kept even when redundant.
5. No removal is made from a sample: it needs the run of the whole sub-folder, then the rules above.
6. After each removal batch, re-run the sub-folder: the score must not fall.

## Time taken

| Step | Time |
| --- | --- |
| TS 7 checker self-test | 255 ms to open the project, 0 baseline errors |
| Core phase: instrument 51 files, 6,007 mutants | 2 s |
| Core phase: dry run (1,396 tests, 144 test files) | 1 min 6 s (net 41 s, overhead 25 s) |
| Core phase: mutation testing | 66 min 15 s (about 0.66 s of wall time per mutant, 15 workers) |
| Others phase: 41 files, 2,132 mutants on the holes' ranges, dry run of 2,940 tests | 3 min 7 s dry run, 24 min 16 s mutation testing (about 0.68 s per mutant) |
| Whole `just mutation-core` | 91 min 5 s |

- Check time per mutant: about 1.8 s for one TS 7 check in one process (16 checks timed alone, noisy); with 8 processes the checker alone bounds the core phase at about 23 minutes, so the test side is the longer part. Compile errors were 1,700 of the 6,007 mutants (28%): they cost a check and no test run.
- Test time per mutant: the 1,396-test dry run takes 41 s net, but a mutant runs only the covering tests of its file, so the average is a fraction of a second. The wall time per mutant already includes both.
- Projection: at 0.91 s per mutant (both phases) all of `src/core` (about 29,000 mutants, estimated from 6,007 mutants for 51 of the files) would take about 7.4 h. A run by sub-folder is therefore feasible, and a full run fits in an overnight run. The projection before the run (4.8 h for 6,000 mutants) was too high: the per-test coverage keeps most mutants to a few tests.
- A Stryker incremental file exists (`stryker-incremental.json`): a re-run after changes to tests only redoes the mutants whose covering tests changed.

## What a Mutation Testing Driver should do differently

- Name the sample in the brief and keep it: the reader's fairness rule depends on it. Prefer a sample drawn by sub-folder, then the full run per sub-folder.
- Never edit `test/` or `src/` while a campaign runs: the sandbox copy is made at the start, but the reader reads `test/core` at the end for the SwRS of each test, and an edit mid-run would shift names.
- Run `just mutation-core` in the background and poll; the progress reporter downgrades to append-only (no TTY), the log grows by one line per few mutants; the whole run is above the 10 minutes a foreground command can wait.
- Read the load-time warning before acting on zero-kill: judge a zero-kill test only when it reaches mutants other tests of its file do not.
- Do round 3 on the numbered clusters of `holes-core.md`, not on single mutants: most holes sit in a few functions.
- Re-run only the touched sub-folders for the after figures, with the same sample files for the sub-folders that were sampled, to compare like with like.

## After the round 3 re-run

To fill in round 3: score per sub-folder, holes by label, number of new tests, wall time, compared with `r2-summary.md`.
