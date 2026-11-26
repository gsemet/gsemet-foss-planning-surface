# CR-505 before and after

- Before: base `3478f0992688c7a354d11106145793fc83590506` (`origin/main`).
- After: pushed head `5a8a59398692a0d497ad88c18e5f142de1411638`.
- The change has no user interface, so the pairs are command outputs. Every planned pair of the
  evidence plan (partial delivery) was captured; its "cannot be shown" items are listed at the end.
- Placeholders: `<worktree>` the change's worktree at the head, `<base>` a detached worktree of the
  base, `<scripts>` the Verifier's scripts in `work/verifier/`.

## 1. Use case paths and scenario markers

Shows: five trust and security paths become accepted, 20 trust and security scenarios gain a marker,
no scenario is removed.

Reproduce: `okfreq trace requirements --json` in `<base>` and `<worktree>`, then `<scripts>/counts.py`.

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

- Before: `test_select_e2e_run.py` fails to collect (`module 'select_e2e_run' has no attribute
  'ACCEPTANCE_ARTIFACT'`); the two other files give `34 failed, 72 passed`; `test/shared/runnerArgs.ts`,
  `scripts/select-acceptance-attempts.mjs` and `scripts/unpack_vsix.py` do not exist.
- After: `149 passed`; the selected Node tests (runner, attempt selection, security, new scenario tests)
  give `tests 288, pass 288, fail 0, skipped 0`.

## 3. Acceptance files

Shows: one marker per path function, declared paths only, no `@tests_req` on a StRS.

Reproduce: `git ls-tree -r --name-only <sha> -- test/integration/acceptance`;
`git grep -n "@accepts_req\|@tests_req StRS" <sha> -- test/integration/acceptance`; `just check-markers`.

- Before: no file under `test/integration/acceptance/`.
- After: `support.ts`, `trust-security.acceptance.ts`, `trust-security.restricted.acceptance.ts`,
  `trust-security.vsix.acceptance.ts`; five `@accepts_req` lines (four in the trusted file, one in the
  Restricted Mode file), none in the built-VSIX file, no `@tests_req StRS`.
  `check-markers: 11 companion file(s), 459 in-force SwRS marked, 12 files on the marker baseline`.

## 4. Preflight on Windows

Shows: the static stage runs and the skip line names acceptance.

Reproduce: `just preflight` on Windows (log `work/gates/preflight-5a8a5939.log`);
`git grep -n "stages skipped on Windows" <base sha> <head sha> -- justfile`.

- Before (recipe text at the base): `preflight: visual, viewer-graph, integration, report and gallery
  stages skipped on Windows; CI runs them`.
- After (run at the head): `preflight: visual, viewer-graph, integration, acceptance, report and
  gallery stages skipped on Windows; CI runs them`, `exit=0`.

## 5. CI acceptance job

Shows: a heavy `acceptance` job exists and its first shard passes under its limits.

Reproduce (read only): `gh api repos/<repo>/actions/runs/45774743144/attempts/1/jobs`; download the
artifact `e2e-acceptance-trust-security-attempt-1` and read
`acceptance/trust-security/acceptance-manifest.json`.

- Before: no `acceptance` job in `ci.yml` at the base.
- After: run 45774743144 at the head, attempt 1: job 87 s, test step 59 s, success. Manifest:
  `status passed`, `scope trust-security`, `revision 5a8a5939...`, `dirty False`, three launches
  passed (trusted 26458 ms, restricted 7929 ms, vsix 15627 ms).

## 6. Newest attempt of a shard

Shows: the report keeps the newest attempt of a re-run shard.

Reproduce (read only): `work/ci-45774743144-report-attempt3.log`; the run's artifact list.

- Before: no acceptance stage and no `select-acceptance-attempts.mjs` at the base.
- After: artifacts `e2e-acceptance-trust-security-attempt-1` and `-attempt-3` both live; log
  `acceptance trust-security: kept attempt 3 (e2e-acceptance-trust-security-attempt-3)`.
  The planned `-attempt-2` is attempt 3 here: attempt 2 re-ran the failed jobs of the run.

## 7. Coverage mode kept

Shows: the tracked mode is unchanged and no gate was added.

Reproduce: `git grep -n strs_test_coverage_mode <base sha> <head sha> -- requirements/config.yml`;
`git diff --stat <base sha> <head sha> -- requirements/config.yml`.

- Before and after: `requirements/config.yml:8:strs_test_coverage_mode: linked-swrs-and-validation-test`;
  empty diff.

## 8. New coverage mode, on an export

Shows: the bundle validates in the new mode, and the delivered group's missing use cases go from six to two.

Reproduce: from `<worktree>`, `python -I <scripts>/w004.py . <sha> <empty folder outside the
repository>` (log `work/verifier/w004.log`).

| | Before | After |
| --- | --- | --- |
| Summary | `1228 requirements, 0 errors, 104 warnings` | `1228 requirements, 0 errors, 100 warnings` |
| Use cases without an acceptance test (W004) | 78 | 74 |
| Trust and security among them | TRUST 001, 004, 006, 009, 012, 014 | TRUST 012, 014 |

## 9. Pull request description

- Before: the description posted on pull request 532 describes an earlier state (real VS Code tests
  "UNVERIFIED", gates and review at `0feab1d9`, evidence and CI pending, stacked on pull request 524).
- After: the description posted on pull request 532 at `5a8a593` (updated `2026-11-26T08:54:30Z`, equal to `work/pr-body.md`); judged in `work/verify.md`.

## Cannot be shown (limits of the evidence plan)

- A local real VS Code run: the machine of this change runs the static stage only.
- Parallel shards: one group only.
- Merging the attempts of several groups on CI: one group only (covered by unit tests).
- The plan's checks 1 to 3 and the owner steps 1 to 4: they belong to the coverage-mode switch, not
  delivered here.
- Release tagging and Pages reuse on a real push to `main`: covered by the workflow tests only.
