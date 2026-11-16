# CI runs the scenario on Linux

## Change

- `.github/workflows/ci.yml`: a new job, `just scenario (ubuntu-latest)`, runs `just scenario` on
  each pull request and each push to `main`, with a Git identity as the `check` job has.
- Whatever fails on Linux is fixed at its cause in the scenario or the CLI. No test is skipped or
  loosened to get green.
- `CONTRIBUTING.md` and `scenario/README.md` say that CI runs it.

## Done when

- The new job is green at the PR's head, on both forges, with every step passing.
- The `check` jobs stay green on all three systems.
- `just check` passes.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
