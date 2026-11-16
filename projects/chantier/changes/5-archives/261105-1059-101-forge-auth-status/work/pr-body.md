**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Change

- `evals/kit/forge.py`: `gh auth status` prints that the user is logged in to the fake forge and
  exits 0. It needs no pull request state, and the module's docstring says so.
- `evals/kit/audit.py`: `["auth", "status"]` joins `FORGE_ALLOWED`, so the audit does not report
  this call as a forbidden one.
- Every other call the fake forge refuses stays refused.

## Checks

- By hand, with `FAKE_GH_STATE` and `LIVE_ORIGIN` set: `forge.py auth status` exits 0, and
  `forge.py pr close 1` exits 1.
- `just check` passes.
