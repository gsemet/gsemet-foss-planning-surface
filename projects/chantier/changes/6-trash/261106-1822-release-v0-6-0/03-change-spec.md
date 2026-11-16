# Release v0.6.0

## Problem

`main` holds 27 commits since v0.5.0, and users of the plugin do not have them.

## Change

Follow the Release section of `CONTRIBUTING.md`, on the current head of `main`, with `just release
minor`: a new branch, the commit `release: v0.6.0`, a pull request merged by rebase once CI is green,
`just tag` on the merged commit, then `gh release create v0.6.0 --generate-notes`.

The user approves each irreversible action: the merge of the version's pull request, the tag and its
push, the publication.

## Out of scope

The `real` eval campaign: the user chose not to run it for this release, so the notes claim no run
with real agents.

## Done when

- CI is green on the exact head of `main` before the version commit.
- `just version-show` says 0.6.0 on `main`.
- The tag `v0.6.0` is on the merged release commit, and the GitHub release is published with its
  notes.
