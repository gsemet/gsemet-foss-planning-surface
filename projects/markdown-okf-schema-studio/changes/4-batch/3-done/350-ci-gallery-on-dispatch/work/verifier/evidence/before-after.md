# Before and after, CR-350

Before: base `abeb761a9ea8815888f2bb59d3e114ef83979598` (CR-349's branch head).
After: pushed head `768570c0f6c317b0bacdb9360a96e50f3c136dd6`.
No visual change: no screenshots (CI workflow only).

## Pair 1: a heavy dispatch, `-f heavy=true`

| | Run | Head | integration | report | release-check | gallery | `studio-site-attempt-1` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before | 44651923296 | abeb761 | success | success | skipped | skipped | absent |
| After | 44652636266 | 768570c | success | success | skipped | success | present (108988467 bytes, 2209 files) |

Reproduce:

```sh
gh run view <run> --repo gsemet/markdown-okf-schema-studio --json headSha,event,conclusion,jobs
gh api repos/gsemet/markdown-okf-schema-studio/actions/runs/<run>/artifacts --jq '[.artifacts[].name]'
gh run download 44652636266 --repo gsemet/markdown-okf-schema-studio -n studio-site-attempt-1 -D <new folder>
```

The before run is the Driver's comparison dispatch on the base; its dispatch inputs (whether
`-f gallery` was passed) are not readable from the API. The file listing of the after artifact is
`work/verifier/site-artifact-listing.log` (not published: `*.log`).

## Pair 2: the strengthened skip-propagation test, on the base workflow and on the head workflow

Captured by the second Verifier pass (a detached worktree of the base fails on Windows path
length, `Filename too long`, first pass). Instead, the test of the pushed head
(`test_every_job_after_a_skippable_job_opts_out_of_the_implicit_success`, from
`test/build/test_workflows.py` at 768570c) is run with its `CI` path pointed at the base's
`.github/workflows/ci.yml` (exported with `git show abeb761:.github/workflows/ci.yml`; blob
`0254a4b960c0b2a2e8c6052cc1cad08b9ae4bb87`, equal to `git rev-parse abeb761:.github/workflows/ci.yml`),
then at the head's.

| | Workflow | Result |
| --- | --- | --- |
| Before | ci.yml at abeb761 | `FAILED against base-ci.yml: gallery: needs a skippable job but has no !cancelled()` (exit 1) |
| After | ci.yml at 768570c | `PASSED against ci.yml` (exit 0) |

Reproduce, from the worktree at 768570c, with a probe that does
`sys.path.insert(0, "<worktree>/test/build")`, `import test_workflows as t`,
`t.CI = Path(<workflow>)`, then calls the test function:

```sh
git show abeb761:.github/workflows/ci.yml > <scratch>/base-ci.yml
uv run --no-sync python <scratch>/probe_base.py . <scratch>/base-ci.yml
uv run --no-sync python <scratch>/probe_base.py . .github/workflows/ci.yml
```
