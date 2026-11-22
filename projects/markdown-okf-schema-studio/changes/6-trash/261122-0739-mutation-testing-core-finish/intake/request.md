# Mutation part 1 finish: whole src/core, fill holes, prudent removals

Mutation testing, part 1 finish: the whole of `src/core` (P1, before `mutation-testing-rest`).

Owner, 2026-11-22, after reading CR-450's results: "Combler, puis partie 2". Removal rule: "Prudente". 

## What CR-450 left

CR-450 (PR #461) built the tool (`just mutation-core`) and ran it on a sample: 51 of 162 files of
`src/core`, 6,007 mutants. Score at the start 70%; 1,289 holes, almost all killed by no test
anywhere; only 75 removal candidates out of about 1,400 core tests (about 5%). Round 3 added
`*.holes.test.ts` files on 25 clusters (319 of 416 holes killed). Not done: no test removed, the
suite grew from 1,396 to 1,475 tests, and every reading is on the sample. Evidence:
`4-batch/3-done/450-mutation-testing/evidence/` (`mutation-campaign-note.md`, `holes-core.md`,
`redundant-tests-core.md`, `r3-rerun.md`).

## Intent

1. One full run of `just mutation-core` on the whole of `src/core` (about 7.5 h by CR-450's
   measure, overnight, in the background).
2. Fill the holes that matter, by cluster, first the weakest folders (palette 3%, export 57%,
   edits 68.5%, paste 58.5%), and list the holes not worth a test (equivalent mutants, by reading).
3. Remove tests by the prudent rule only:
   - remove a test that kills no mutant on the full run (not "load-time coverage only");
   - merge near-duplicates into a table-driven test that keeps every assertion;
   - keep a focused unit test even when a broad test (render pipeline, features) kills the same
     mutants: a focused test says where it broke;
   - keep regression and boundary tests; a `@tests_req` marker moves only to a kept test of the
     same SwRS, and `just requirements-update` stays clean; no published requirement is removed.
4. Re-run the touched sub-folders: no sub-folder score drops.

## Done

- Score per sub-folder of the full run, before and after, in the PR.
- The unit suite of `test/core` is no larger than before this CR's new hole tests, net of the
  removals and merges, or the PR says why.
- The second-case lessons for chantier's `mutation-testing-driver` note (full run time, what the
  sample got wrong).
