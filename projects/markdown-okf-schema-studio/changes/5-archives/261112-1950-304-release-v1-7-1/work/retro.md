# Retro: release v1.7.1

- Local `just preflight` of the version commit failed at `ci-integration` because the screen was
  locked (window never active), and `ci-report` and `ci-gallery` failed from it; the proof came
  from an on-demand heavy run on the branch (43275294730), about 20 minutes more. Fix: let
  `ci-integration` detect a locked screen and stop with that cause before the run, and let the
  release driver dispatch the branch heavy run at once when the screen is locked.
- The changelog lines were written in the version commit instead of the stack PRs (owner's
  accepted deviation), so the notes and the changelog were written together late. Fix: have each
  CR Driver of a batch add its `## Unreleased` line in its PR, as step 2 of the procedure asks.
- The Marketplace listing still showed 1.7.0 three minutes after `vsce publish` reported 1.7.1
  published, while the gallery API already served the 1.7.1 VSIX. Fix: name in the procedure's
  step 6 the check of record (the gallery `vspackage` URL of the version) and the listing delay.
- A release with no closed issue still reads like it needs a step 8 approval. Fix: say in step 8
  that an empty list ends the step with a line in `report.md`.
