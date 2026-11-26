# CR-509 before and after

- Before: base `5a73b6ebcf66ef80b412afcdbfd09c4defc028d8`. The measured "before" runs are heavy
  runs 45476952370 (`63ef752`) and 45713440510 (`17b779d`);
  `git diff --stat 17b779d5 5a73b6eb -- test/integration test/shared` prints nothing, so run
  45713440510 ran the base's real-window tests.
- After: pushed head `b24d3bf08f01ae0e72fe7d251b25833df558608c`, heavy runs 45734265223 and
  45734267839.
- No screenshot or video: test, CI and contributor documentation only. Evidence is text.
- Run downloads stay in `work/scratch/` (never published). `<scratch>` below is that folder.

## Pair 1: trusted launch durations

| Run | Commit | Launches | Setup to last step | `just ci-integration` step |
| --- | --- | --- | --- | --- |
| 45476952370 (before) | `63ef752` | 1 | 834.4 s | 1011 s |
| 45713440510 (before) | `17b779d` | 1 | 830.5 s | 1002 s |
| 45580228461 (before, failed) | `4a47151e` | 1 | LAUNCH TIMEOUT at 900 s | not read |
| 45734265223 (after) | `b24d3bf` | 2 | 421.6 s and 492.7 s | 1111 s |
| 45734267839 (after) | `b24d3bf` | 2 | 408.9 s and 453.3 s | 1056 s |

Reproduce: download each `integration` job log with `gh run view <run> --job <job> --log` into an
empty folder `<scratch>/verify-<run>/integration.log`, then
`python -I <scratch>/verify-parse.py`; step durations from
`gh api repos/gsemet/markdown-okf-schema-studio/actions/runs/<run>/jobs`.

## Pair 2: steps that run

- Before: 55 distinct `STEP done` names in one launch (run 45476952370).
- After, both runs: part 1 holds those names without `real-input` and `preview-editing`, in order
  (53); part 2 holds `setup`, `preview-smoke`, `real-input`, `preview-editing`; the union equals the
  55; only `setup` and `preview-smoke` run twice.

Reproduce: `python -I <scratch>/verify-parse.py`.

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

After, both runs: one line `TRUSTED LAUNCH: trusted-suite.js`, steps `setup`, `preview-smoke`,
`real-input`; no `STEP failed`, `LAUNCH TIMEOUT` or `LAUNCH HANG`.

Reproduce: `python -I <scratch>/verify-artifacts.py <scratch>`.

## Pair 5: frame lookup

- Before (base): `findCurrentFrame` calls `locator.count` on every frame of `page.frames()`
  (`git grep -n "page.frames()" 5a73b6eb -- test/integration/realInput/harness.ts`); run
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
