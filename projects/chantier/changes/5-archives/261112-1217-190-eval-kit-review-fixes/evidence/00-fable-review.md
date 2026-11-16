# The fable review of CR-188 and CR-189 (2026-11-12, read-only, at 4e111ac)

Kept as received by the Chief of Staff; W is the CR-189 head (now `main` at d72df44).

## Blocking or near-blocking

- **A1. The audit fails on a correct `full` run.** `rails.py` `release_merged` (240-244) clears
  the release CR's `pr`; `evals/kit/audit.py` `sandbox_checks` (650-661) builds `ours` only from
  CRs that still have a `pr`, so the merged release PR, whose title carries the prefix, counts as a
  stray merge: C12 FAIL, exit 1. The release PR also gets no J5 check (628-630 skip it). Fix: take
  the release PR number from the `ship` events or the `merged: <pr>` note.
- **A2. `reset --yes` ends in "verification failed" from the second campaign on.** `remote_refs()`
  (224-230) returns every ref and `verify()` (293-303) demands only `refs/heads/main`; GitHub keeps
  `refs/pull/N/head` forever. Fix: compare only `refs/heads/*` and `refs/tags/*`. Also unproved:
  closing PRs, deleting branches, tags and releases never ran against real objects.
- **A3. The host may refuse the merges and the release's irreversible steps.** The operator's raw
  `gh pr merge`, the Release driver's tag push and `gh release create` have no allow rule, and
  `setup.py` writes no `.claude/settings.local.json` for sandbox campaigns ("Merge Without Review",
  "Create Public Surface" seen before). Fix: a named kit merge script, or allow rules written by
  `setup.py` into the workspace's ignored settings file.
- **A4. `full`: the release PR is likely to go red on `uv.lock`.** The bump changes `uv.lock`
  (`sandbox/uv.lock` 67-69 `version = "0.1.0"`); `RELEASING.md` step 3 and the "Files" of
  `sandbox-crs/release-v0-2-0` and `release-v0-3-0` name three files only; the Driver stages by
  name; the warning in `full/RUNBOOK.md` (70-72) reaches only the operator. Fix: add `uv.lock` to
  the two release CRs' "Files" and steps (no change of the base).

## Risks

- **B1. Budget.** Every feature touches `app.py` and `README.md`; in parallel each merge sends
  every open PR back for a rebase. No runbook says what the operator does on a `budget:` ask.
- **B2. The 10-message limit in `full`:** 15-20 operator sends; a `ping` in the Foreman's session
  does not reset the operator's count; one ping may not be enough.
- **B3. The limit in real-foreman:** the quick runbooks carry no fallback text like `full`'s.
- **B4. Red checks do not block a merge** on the unprotected `main`, though `evals/README.md`
  (79-83) says they do.
- **B5. Judge strictness** on contiguous text (`Rating: none`, `Unknown status: &lt;b&gt;`). Low.
- **B6. Role conflict:** the Chief of Staff card says "Never merge"; the runbooks tell the
  operator to merge.
- `evals/README.md` line 21 says "9 feature CRs plus a release" for batch 1; code and runbook say
  8 + release.

## Verdicts

- `full`: will not work as it stands (A1, A4, A3, B2, B1).
- `real-foreman`: will work with risks (A3, B1, B3, A2 from the second run, B4).
- `real-direct`: will work with risks (A3, B1, B6, A2, the unproved direct-mode host lines).
- Not checked: `evals/copilot/RUNBOOK.md`.
