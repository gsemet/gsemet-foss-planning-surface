# CR-509 before and after

- Before: base `3478f0992688c7a354d11106145793fc83590506`, main push run 45773405420. Older
  measured "before" runs: 45476952370 (`63ef752`) and 45713440510 (`17b779d`); between `17b779d5`
  and the base, `test/integration` and `test/shared` differ only in comments and in the move of
  the schema steps of `previewEditing.test.ts` to their own file.
- After: pushed head `89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`, heavy runs 45794678556 and
  45795351595.
- No screenshot or video: test, CI and contributor documentation only. Evidence is text.
- Run downloads stay in `work/scratch/` (never published). `<scratch>` below is that folder.

## Pair 1: trusted launch durations

| Run | Commit | Launches | Setup to last step | `just ci-integration` step |
| --- | --- | --- | --- | --- |
| 45773405420 (before, base) | `3478f09` | 1 | 851.8 s | 1023 s |
| 45476952370 (before) | `63ef752` | 1 | 834.4 s | 1011 s |
| 45713440510 (before) | `17b779d` | 1 | 830.5 s | 1002 s |
| 45580228461 (before, failed) | `4a47151e` | 1 | LAUNCH TIMEOUT at 900 s | not read |
| 45794678556 (after) | `89cae5f` | 2 | 423.8 s and 493.5 s | 1112 s |
| 45795351595 (after) | `89cae5f` | 2 | 387.1 s and 419.4 s | 969 s |

Reproduce: download each `integration` job log with `gh run view <run> --job <job> --log` into
`<scratch>/artifacts-<run>/integration.log` (and `stress.log` for the stress job), then
`python -I <work>/verifier/verify_runs_89cae5f.py <scratch>` for the after runs (it reads the
reference log of run 45476952370 in `<scratch>/verify-45476952370/`). For run 45773405420, time
from `STEP start: setup` to `STEP done: workspace-disposal`. Step durations from
`gh api repos/gsemet/markdown-okf-schema-studio/actions/jobs/<job>`.

## Pair 2: steps that run

- Before: 55 distinct `STEP done` names in one launch (run 45476952370; 55 in run 45773405420).
- After, both runs: part 1 holds those names without `real-input` and `preview-editing`, in order
  (53); part 2 holds `setup`, `preview-smoke`, `real-input`, `preview-editing`; the union equals the
  55; only `setup` and `preview-smoke` run twice.

Reproduce: the script of pair 1.

## Pair 3: new unit tests

- Before (old behaviour, mimicked by stand-ins in a throwaway copy of the compiled tests): 9 tests,
  0 pass, 9 fail.
- After (head): 9 tests, 9 pass, 0 fail.

Reproduce, from the worktree at head: `npm run compile`;
`node --test out/test/build/trustedParts.test.js out/test/build/webviewFrames.test.js`; then
`cp -r out/test out/verify-red-test`,
`python -I <scratch>/verify-red-standins.py out/verify-red-test`, run the same two test files from
`out/verify-red-test/build/`, and delete `out/verify-red-test`.

## Pair 4: stress stays one launch

After, both runs: one line `TRUSTED LAUNCH: trusted-suite.js`, three trusted steps done, ending
with `real-input`; no `STEP failed`, `LAUNCH TIMEOUT` or `LAUNCH HANG`.

Reproduce: the script of pair 1.

## Pair 5: frame lookup

- Before (base): `findCurrentFrame` calls `locator.count` on every frame of `page.frames()`
  (`git grep -n "page.frames()" 3478f099 -- test/integration/realInput/harness.ts`); run
  45706313890 attempt 2: `STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not
  return within 10000 ms (frame )`.
- After (head): frames are picked by `url()` before any other call (code and unit tests of pair 3);
  the open-at-line steps pass in both runs.

## Not captured

- A real-window run on this machine: Windows, where the local gates skip the real VS Code stage.
- Proof that the frame lookup failure is gone: it failed once, two green runs cannot show it, and
  the open-at-line steps are not stress scenarios.
- The new frame list in a timeout message from a real window: no run at the head had such a
  timeout. It is proven by the unit test of `FrameLookupLog` and by reading `waitFor` only.
