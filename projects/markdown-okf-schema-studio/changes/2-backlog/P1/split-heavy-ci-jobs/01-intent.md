# The heavy CI finishes much faster

The two long jobs of the heavy CI run, `integration` (about 18 min) and `stress` (about 16 min), are
each split into jobs that run in parallel, so a heavy run of a branch or of `main` ends in about half
the time. The owner asks for it now, to go fast: it comes right after CR-517 in batch-09, before the
CRs that wait.

## Done when

- A heavy run of the branch is green, and each job that comes from the split lasts about 10 min or
  less; the run's whole duration and each job's are written in the PR, next to the runs measured
  before (`request.md`).
- The same tests run, as many times as before: every real-window suite once, every stress scenario the
  same number of rounds. Nothing is removed, skipped or made weaker to gain time.
- The same gates hold: a red `integration` part blocks `checks` and a release tag; `stress` stays
  advisory, except on a version change; `checks` keeps its name.
- `just ci-integration`, `just ci-stress` and `just preflight` still run everything on one machine.

## Not in this CR

The pull-request jobs, the visual jobs, `acceptance`, and any change to a test or to the product to
make it quicker.
