## Summary

Release 1.11.0: the version commit (bump, changelog heading, release notes folder with its three cropped pictures). It is a minor release because the stack under it ships features: the Delete block button, the blank-lines block, and Studio opening at a searched line. The stack is merged: this branch sits on `main` and targets it. It stays a draft until the owner's word.

## Deliverables

The release notes and the announcement thread are rendered below, from the files in `docs/releases-notes/2026-11-21-v1.11.0/`. The three pictures are cropped from the captures of the merged changes to the place where each change happens. Nothing is tagged or published by this PR: the owner merges it, and the tag, the GitHub release and the Marketplace publication follow only on the owner's word.

## Changes

- `chore: version 1.11.0`: `package.json`, `package-lock.json`, `plugin.json`, `.claude-plugin/plugin.json`, `.github/plugin/marketplace.json`.
- `CHANGELOG.md`: the `## Unreleased` lines moved under `## 1.11.0 - 2026-11-21`.
- `docs/releases-notes/2026-11-21-v1.11.0/`: `release-notes.md`, `tweet.md` and the pictures.

## Impacts

No visual change in the extension by itself. It publishes the changes of the stack below it.

## Blast radius

Grade: 3

Release: the merge starts the tag and the publication. Nothing is published before the owner's word; rollback after the tag is a new patch version.

## Test plan

- [x] New or changed tests: none, a version commit
- [x] Requirements: No behaviour change
- [x] Changelog: the lines of the stack moved under 1.11.0
- [x] Local gates: `just release-notes-check` ok; `just preflight` (static stage on Windows) run through the project's gate
- [ ] Review
- [ ] CI green: the heavy run (`integration`, `stress`) is dispatched on this branch
