## Summary

Everything merged since 1.12.1 is on `main` but reaches no user before a release. This is version 1.13.0, a minor release because it adds new features. Merging it publishes it.

## Deliverables

- The version commit `chore: version 1.13.0`, with the changelog heading and a commit reference on each line.
- The release notes, the announcement thread draft and their images in `docs/releases-notes/2026-11-27-v1.13.0/`, shown below.

## Changes

- Version 1.13.0 in the npm manifest, the lock file, the two plugin manifests and the plugin catalog.
- `CHANGELOG.md`: the `Unreleased` lines move under `1.13.0 - 2026-11-27`.
- Pictures: `admonition-block-edit-before-after.png` joins the before and after captures of the merged change, both cropped to the same region at the same scale (composed with Pillow); `chart-hover.png` is a crop of a capture of the hover box. The clip's GIF and MP4 are copies of the approved clip `raw-copy-balance-edges`.
- No dedicated hero scenario, to keep code out of the version commit. The clip is the picture of the thread.

## Impacts

Users get the changes listed in the release notes below. This pull request itself changes no behaviour.

## Blast radius

A merge publishes to both extension registries; a published version cannot be withdrawn by a revert, only followed by a new version.

Grade: 3

## Test plan

- [ ] New or changed tests (they fail on the previous code): none, version and notes only
- [x] Requirements: no behaviour change
- [x] Changelog: the lines move under the version heading
- [x] Local gates: `just preflight` passed (on Windows, the static stage only; CI runs the others), `just release-notes-check` passed
- [x] Heavy CI of the released code: run [45958381383](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45958381383) on `b1e23cc`, every job green
- [ ] Review: the owner reviews the notes folder
- [ ] CI green

## Internal references

CR-520.
