## Summary

Version 1.9.0 of Markdown OKF-Schema Studio. It ships the changes merged since 1.8.1: the floating
toolbar laid out as four rows of four, a grid of cards that stays whole inside a GitHub alert, two
click fixes for cards of a grid in a list item, and the first publication to Open VSX next to the
VS Code Marketplace.

## Deliverables

The release folder the owner reviews, committed with the version:

| File | Content |
| --- | --- |
| `docs/releases-notes/2026-11-14-v1.9.0/release-notes.md` | The GitHub release notes (rendered below) |
| `docs/releases-notes/2026-11-14-v1.9.0/tweet.md` | The three-post announcement thread (rendered below); posted by the owner only |
| `docs/releases-notes/2026-11-14-v1.9.0/floating-toolbar-four-by-four.png` | The hero picture of the notes and of post 1 |

## Changes

- `chore: version 1.9.0` from `just bump-version`: `package.json`, `package-lock.json`, the two
  plugin manifests and the GitHub Copilot catalog entry move from 1.8.1 to 1.9.0 (Commitizen
  computed 1.9.0 itself, from the `feat` of the toolbar).
- `CHANGELOG.md`: the four `## Unreleased` lines move under `## 1.9.0 - 2026-11-14`; nothing added.
- The release folder above.

## Impacts

No visual change in this commit: it only changes version numbers, the changelog heading and the
release folder. The merge publishes 1.9.0 (tag, GitHub release with these notes, VS Code
Marketplace, Open VSX for the first time, Pages) through the version push on `main`.

## Blast radius

Grade: 3

A release: once merged, CI tags v1.9.0 and publishes to the Marketplace and Open VSX. The extension
code is the one already on `main`; a bad release is fixed forward with a patch release.

## Test plan

- [x] New or changed tests (they fail on the previous code): no code change in this PR
- [x] Requirements: No behaviour change
- [x] Changelog: the version commit moves the `## Unreleased` lines under `## 1.9.0`; every `feat`
      and `fix` commit since v1.8.1 has its line
- [x] Local gates: `just release-notes-check` ok; `just preflight`: `ci-static` passed;
      `ci-visual` failed on one scenario (`v31-mark-editor-selection-light-900`, twice), an
      intermittent failure of this machine already seen before 1.8.1 and green in CI's `visual`
      job; the local real-window `ci-integration` failed at `tall-block-scroll` (this machine's
      window), so `ci-report` and `ci-gallery` did not pass; the heavy run below is the
      real-window proof
- [ ] Review: the owner reviews the release notes and the thread
- [x] CI green at this head, and the heavy run dispatched on this branch green at its exact head
      (run 43536948441: `integration` failed once at `real-input`, then green on the re-run of
      the failed jobs; attempt 2: `integration` success, `stress` success, `visual` success)

The heavy run of `main` 1191fb6c (run 43532691444) failed once at one `integration` step (`toc`:
the click on the Edit toggle never reached the page) and was green on its re-run of the failed
jobs (attempt 2: `integration` and `stress` success).

## Autonomous decisions

- The hero is a fresh capture of the 4 x 4 toolbar from the simulated visual suite (Cream theme,
  the capture made to check the toolbar change), cropped to a 4:3 frame; not a dedicated hero
  scenario. A dedicated one can replace it on request.
- The grid-in-alert fix is a highlight with a Markdown example and no picture (no capture of it
  exists; none is invented). The two list-item click fixes go in "All fixes".
- Open VSX is named in the notes (install link, one "Also on Open VSX" line) and in post 3 before
  its first publication. If the Open VSX step fails at the release, the "Also on Open VSX" line is
  removed from the published GitHub release by an edit, and post 3 keeps only the Marketplace link.

## Internal references

- Release change request: CR-323 release-v1-9-0 (batch-04).
