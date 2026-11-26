# CR-505 before and after

- Before: base `89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4` (head of the change below this one in the
  stack).
- After: pushed head `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`.
- The change has no user interface, so the pairs are command outputs. Every planned pair of the
  evidence plan (partial delivery) is below; the plan's "cannot be shown" items are listed at the end.
  A pair carried from an earlier capture says so, with the reason the move did not touch it.
- Placeholders: `<worktree>` the change's worktree at the head, `<base>` a detached worktree of the
  base (`<worktree>/.artifacts/vbase`, removed after the capture), `<scripts>` the Verifier's scripts
  and logs in `work/verifier/`.

## 1. Use case paths and scenario markers

Shows: five trust and security paths become accepted, 20 trust and security scenarios gain a marker,
no scenario is removed.

Reproduce: `okfreq trace requirements --json` in `<base>` and `<worktree>`
(`trace-base-89cae5f.log`, `trace-head-9d7e788a.log`), then `<scripts>/counts.py`
(`counts-9d7e788a.log`). Captured at `89cae5f` and `9d7e788`.

| Count | Before | After |
| --- | --- | --- |
| Use case paths / accepted / not accepted | 156 / 17 / 139 | 156 / 22 / 134 |
| SwRS scenarios / without a marker | 2633 / 722 | 2638 / 702 |
| Trust and security scenarios / with `@tests_req` | 94 / 74 | 94 / 94 |
| Trust and security paths accepted | 0 of 8 | 5 of 8 (001 S1, 004 S1, 006 S1, 009 S1, 009 S2) |

## 2. Runner, attempt selection, unpacking and workflow tests

Shows: the tooling tests exercise code the base does not have.

Reproduce: `uv run pytest test/build/test_workflows.py test/build/test_select_e2e_run.py
test/build/test_unpack_vsix.py` on the head, then the head's test files on an export of the base;
`git ls-tree` for the new sources.

- Before, carried from `3478f09`: the new base adds no change to `.github/`, `scripts/`, `justfile`,
  `test/security/`, `requirements/` or `src/` (`git diff --stat 3478f09 89cae5f -- ...`: empty), and
  this change's patch is the same. `test_select_e2e_run.py` fails to collect (`module
  'select_e2e_run' has no attribute 'ACCEPTANCE_ARTIFACT'`); the two other files give `34 failed, 72
  passed`.
- Before, captured at `89cae5f`: `git ls-tree` finds none of `test/shared/runnerArgs.ts`,
  `scripts/select-acceptance-attempts.mjs`, `scripts/unpack_vsix.py`.
- After, captured at `9d7e788`: `149 passed` (`pytest-9d7e788a.log`); the selected Node tests
  (runner, attempt selection, trusted parts, webview frames, security, scenario tests) give `tests
  342, pass 342, fail 0, skipped 0` (`node-tests-9d7e788a.log`).

## 3. Acceptance files

Shows: one marker per path function, declared paths only, no `@tests_req` on a StRS.

Reproduce: `git ls-tree -r --name-only <sha> -- test/integration/acceptance`;
`git grep -n "@accepts_req\|@tests_req StRS" <sha> -- test/integration/acceptance`; `just
check-markers`.

- Before (`89cae5f`): no file under `test/integration/acceptance/`.
- After (`9d7e788`): `support.ts`, `trust-security.acceptance.ts`,
  `trust-security.restricted.acceptance.ts`, `trust-security.vsix.acceptance.ts`; five
  `@accepts_req` lines (lines 41, 123, 176, 222 of the trusted file, line 36 of the Restricted Mode
  file), none in the built-VSIX file, no `@tests_req StRS`. `check-markers: 11 companion file(s),
  459 in-force SwRS marked, 12 files on the marker baseline` (`check-markers-9d7e788a.log`).

## 4. Preflight on Windows

Shows: the static stage runs and the skip line names acceptance.

Reproduce: `just preflight` on Windows (log `work/gates/preflight-9d7e788a.log`);
`git grep -n "stages skipped on Windows" <base sha> <head sha> -- justfile`.

- Before (recipe text at `89cae5f`, line 471): `preflight: visual, viewer-graph, integration, report
  and gallery stages skipped on Windows; CI runs them`.
- After (run at `9d7e788`, log lines 5889 and 5890): `ci-static: passed`, then `preflight: visual,
  viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`.

## 5. CI acceptance job

Shows: a heavy `acceptance` job exists and its first shard passes under its limits.

Reproduce (read only): `gh run view 45794286167`; the log `work/ci-45794286167-acceptance.log`;
download the artifact `e2e-acceptance-trust-security-attempt-1` and read
`acceptance/trust-security/acceptance-manifest.json` with `<scripts>/manifest.py`.

- Before (`89cae5f`): no `acceptance` job in `ci.yml` (`git grep acceptance <base sha> --
  .github/workflows/ci.yml`: no match).
- After (run 45794286167 at `9d7e788`, attempt 1): job 82 s, test step 52 s, success. Manifest:
  `status passed`, `scope trust-security`, `revision 9d7e788a...`, `dirty false`, three launches
  passed (30037 ms, 5813 ms, 10249 ms: trusted, Restricted Mode, built VSIX).

## 6. Newest attempt of a shard

Shows: the report keeps the newest attempt of a re-run shard.

Reproduce (read only): `work/ci-45774743144-report-attempt3.log`; the artifact list of run
45774743144.

- Before: no acceptance stage and no `select-acceptance-attempts.mjs` at the base (captured at
  `89cae5f`, pairs 2 and 5).
- After, carried from `5a8a593`: the move changes neither `scripts/select-acceptance-attempts.mjs`
  nor `.github/` (`git diff --stat 5a8a593 9d7e788`: neither listed). Artifacts
  `e2e-acceptance-trust-security-attempt-1` and `-attempt-3` both existed; log line 418 `acceptance
  trust-security: kept attempt 3 (e2e-acceptance-trust-security-attempt-3)`. The planned
  `-attempt-2` is attempt 3 here: attempt 2 re-ran the failed jobs of the run.

## 7. Coverage mode kept

Shows: the tracked mode is unchanged and no gate was added.

Reproduce: `git grep -n strs_test_coverage_mode <base sha> <head sha> -- requirements/config.yml`;
`git diff --stat <base sha> <head sha> -- requirements/config.yml`.

- Before (`89cae5f`) and after (`9d7e788`): `requirements/config.yml:8:strs_test_coverage_mode:
  linked-swrs-and-validation-test`; empty diff.

## 8. New coverage mode, on a copy

Shows: the bundle validates in the new mode, and the delivered group's missing use cases go from six
to two.

Reproduce: from `<worktree>`, `python -I <scripts>/newmode.py . <sha> <work folder>/scratch/<new
folder> <scripts>` (logs `newmode-current-<sha7>.log`, `newmode-new-<sha7>.log`). The copy leaves out
52 files whose path would pass 259 characters (under `.agents/skills/markdown-studio-exploratory-qa*`
and `docs/demo-video/clips`, none under `requirements/`); on the copy, the tracked mode gives the 26
warnings of the in-tree lint at the head.

| | Before (`89cae5f`) | After (`9d7e788`) |
| --- | --- | --- |
| Summary | `1228 requirements, 0 errors, 104 warnings` | `1228 requirements, 0 errors, 100 warnings` |
| Use cases without an acceptance test (W004) | 78 | 74 |
| Trust and security among them | TRUST 001, 004, 006, 009, 012, 014 | TRUST 012, 014 |

## 9. Pull request description

- Before: the description posted on pull request 532 at `5a8a593` (updated `2026-11-26T09:19:30Z`,
  `posted-body-5.md`), naming the old head and the old CI runs.
- After: the description posted at `9d7e788` (updated `2026-11-26T10:06:51Z`, `posted-body-6.md`);
  judged in `work/verify.md`.

## Cannot be shown (limits of the evidence plan)

- A local real VS Code run: the machine of this change runs the static stage only.
- Parallel shards: one group only.
- Merging the attempts of several groups on CI: one group only (covered by unit tests).
- The plan's checks 1 to 3 and the owner steps 1 to 4: they belong to the coverage-mode switch, not
  delivered here.
- Release tagging and Pages reuse on a real push to `main`: covered by the workflow tests only.
