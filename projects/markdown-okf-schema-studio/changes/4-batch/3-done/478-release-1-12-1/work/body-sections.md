## Summary

Version 1.12.1 of Markdown OKF-Schema Studio. This pull request tops the stack that it releases (the raw-text opening fix below it); it carries the version commit, the changelog heading with the pull request of each line, and the release notes and announcement thread in `docs/releases-notes/2026-11-24-v1.12.1/`. The owner merges the whole stack with it, bottom up, by rebase.

## Deliverables

Release notes and announcement thread, rendered below. No images: a patch release, as 1.9.3.

## Changes

- `chore: version 1.12.1`: `package.json`, `package-lock.json`, the plugin manifests and the Copilot catalog.
- `CHANGELOG.md`: the `## 1.12.1 - 2026-11-24` heading; each line ends with its commit (when it is on `main`), pull request and issue.
- `docs/releases-notes/2026-11-24-v1.12.1/`: `release-notes.md` and `tweet.md`.

## Impacts

The merge starts the version push: heavy jobs, tag `v1.12.1`, GitHub release, Marketplace and Open VSX publications. The version is 1.12.1 although the stack carries a `feat` (the blank-line block per line, already on `main`), which Commitizen would number 1.13.0; the version is the owner's choice.

## Blast radius

Grade: **2**: the release publishes; a revert before the tag is a plain `git revert`, after it a new fix release.

## Test plan

- [x] New or changed tests (they fail on the previous code): none, release commit only
- [x] Requirements: No behaviour change
- [x] Changelog: the lines of the release moved under the 1.12.1 heading
- [ ] Local gates: `just preflight` (static stage on Windows)
- [ ] Review
- [ ] CI green, and the heavy run (`integration` and `stress`) green on this branch head
