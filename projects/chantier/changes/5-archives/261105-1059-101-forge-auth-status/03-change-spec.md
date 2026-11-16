# The eval's fake forge answers `gh auth status`

## Change

- `evals/kit/forge.py`: `gh auth status` prints that the user is logged in to the fake forge and
  returns exit code 0. It needs no pull request state. The module's docstring says so.
- `evals/kit/audit.py`: `["auth", "status"]` joins `FORGE_ALLOWED`, so the audit does not report
  this call as a forbidden one.
- Every other call the fake forge refuses stays refused.

## Done when

- Run by hand with `FAKE_GH_STATE` and `LIVE_ORIGIN` set: `forge.py auth status` exits 0, and
  `forge.py pr close 1` still exits 1.
- `just check` passes, and CI is green on all three systems at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
