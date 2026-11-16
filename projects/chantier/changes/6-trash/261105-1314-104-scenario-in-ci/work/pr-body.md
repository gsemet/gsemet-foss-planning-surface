**Eval run: do not merge.** The maintainer decides what happens to this PR.

CI runs `just scenario` on Linux, so a change to the batch workflow no longer depends on someone running it by hand.

- `.github/workflows/ci.yml`: a new job, `just scenario (ubuntu-latest)`, on each pull request and each push to `main`, with the same setup and Git identity as the `check` job.
- `CONTRIBUTING.md` and `scenario/README.md` say that CI runs it.

Local checks on Windows: `just check` and `just scenario` pass. The new job's first run is the first time the scenario runs on Linux.
