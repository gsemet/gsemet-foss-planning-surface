## Summary

Release 1.7.1. Everything merged since 1.7.0 is on the published site: the requirements viewer with
the map of each use case, the main paths of the use cases, one cream look for the whole site and
the share picture cards. The site is published only on a version tag, so this release is what puts
those pages online. The extension itself does not change.

## Deliverables

```text
docs/releases-notes/2026-11-12-v1.7.1/
├── release-notes.md              the GitHub release notes (rendered below)
├── tweet.md                      the three-post announcement thread (rendered below)
├── requirements-viewer-map.png   hero: the map of a use case in the requirements viewer
└── share-card-gallery.png        the share card of the screenshot gallery
```

## Changes

- `just version 1.7.1`: `package.json`, `package-lock.json`, `plugin.json`,
  `.claude-plugin/plugin.json`, `.github/plugin/marketplace.json`.
- `CHANGELOG.md`: the `## 1.7.1 - 2026-11-12` section. Its lines are written in this commit rather
  than in the merged pull requests, on the owner's decision for this release (documentation only,
  so no new heavy run of `main` was needed).
- The release notes folder above. The hero is a capture of the site built from the reports of the
  heavy run of `main` (`just site-from-run 43262188098`), the exact site this tag publishes.

## Impacts

No change to the extension. On merge, CI tags `v1.7.1`, publishes the extension to the
Marketplace, creates the GitHub release with these notes, and deploys the site to GitHub Pages.

## Blast radius

Grade: 3. A release: tag, Marketplace publication and Pages deploy. Before the merge, closing the
PR undoes everything; after it, a fix ships as a new version.

## Test plan

- [x] New or changed tests: none, a release
- [x] Requirements: no behaviour change
- [x] Local gates: `just preflight` at this head: `ci-static` (with the release notes check) and
      `ci-visual` passed; the real VS Code stage could not run on the locked screen of the machine,
      so `ci-integration`, then `ci-report` and `ci-gallery`, failed. Its proof is the heavy run
      dispatched on this branch, below.
- [x] Heavy run on this branch's head `786fe7b0`: run 43275294730, `integration` and `stress`
      success, the whole run green
- [x] Heavy run green on `main` HEAD `cf51f12f` (run 43262188098: `integration` and `stress` success)
- [ ] Review: the owner reviews the notes and the thread
- [x] CI green (pull request run 43275285258)

## Internal references

- Change request CR-304 release-v1-7-1 of batch-01; the merged changes are PRs #371 to #374.
