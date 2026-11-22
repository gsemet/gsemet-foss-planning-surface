# Change Specification: Release v0.15.1

## What it delivers

chantier 0.15.1 on GitHub: a version commit `release: v0.15.1` merged on `main`, the tag `v0.15.1`
pushed, and a GitHub release `v0.15.1` with the reviewed notes. It ships the session-folder fix and
nothing else.

## How

By the project's own procedure, `CONTRIBUTING.md` "Release", with `docs/release-process.md`:

1. After the batch's other CR is merged, on a new branch from an up-to-date `main` with green CI,
   write `docs/release-notes/<today>-v0.15.1/` (`release-notes.md`, `tweet.md`, no image needed) and
   the claims file `evals/results/claims-v0.15.1.md`. No eval ran for this release: the notes'
   "Not exercised by an eval" bullet lists the change's claims with their true result (`scenario only`
   or not exercised), as `docs/release-process.md` says.
2. `just release` (a patch), push the branch, open the PR, body from the release folder.
3. The steering session merges the PR by rebase once CI is green, under the grant recorded for this
   release (`order grant ... releases=1`). A red `scenario` job stops the merge: the Release driver
   hands back blocked and the user reads it on waking.
4. `just tag` from the main checkout, then `gh release create v0.15.1 --verify-tag ...` with the
   notes `--prepare` produced. The announcement (`tweet.md`) stays a draft: no agent posts it.

## Out of scope

Any eval, the local long gate, any change other than the release's files and the version bump, the
announcement's posting.

## Done when

`gh release view v0.15.1` shows the release, the tag is on the `release: v0.15.1` commit, `main` is
at 0.15.1, and the batch is paused.
