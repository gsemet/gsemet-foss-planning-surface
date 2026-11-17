## Summary

Version 1.8.0 of Markdown OKF-Schema Studio. It ships the changes merged since 1.7.1: save with
Cmd+S (Ctrl+S) from the preview, GitHub alerts that keep their title when they start with a
heading, a sticky heading band that keeps each level on one line, an HTML export that keeps an
edit in progress, and a click fix for cards of a grid inside a quote.

## Deliverables

The release folder the owner reviews, committed with the version:

| File | Content |
| --- | --- |
| `docs/releases-notes/2026-11-13-v1.8.0/release-notes.md` | The GitHub release notes (rendered below) |
| `docs/releases-notes/2026-11-13-v1.8.0/tweet.md` | The three-post announcement thread (rendered below); posted by the owner only |
| `docs/releases-notes/2026-11-13-v1.8.0/sticky-heading-one-line.png` | The picture of the notes and of post 1 |

## Changes

- `chore: version 1.8.0` from `just bump-version`: `package.json`, `package-lock.json`, the two
  plugin manifests and the GitHub Copilot catalog entry move from 1.7.1 to 1.8.0.
- `CHANGELOG.md`: the `## Unreleased` lines move under `## 1.8.0 - 2026-11-13`; nothing added.
- The release folder above.

## Impacts

No visual change in this commit: it only changes version numbers, the changelog heading and the
release folder. The merge publishes 1.8.0 (tag, GitHub release with these notes, Marketplace,
Pages) through the version push on `main`.

## Blast radius

Grade: 3

A release: once merged, CI tags v1.8.0 and publishes to the Marketplace. The extension code is the
one already on `main`; a bad release is fixed forward with a patch release.

## Test plan

- [x] New or changed tests (they fail on the previous code): no code change in this PR
- [x] Requirements: No behaviour change
- [x] Changelog: the version commit moves the `## Unreleased` lines under `## 1.8.0`; every `feat`
      and `fix` commit since v1.7.1 has its line
- [x] Local gates: `just release-notes-check` ok; `just preflight`: `ci-static` and `ci-visual`
      passed, the local real-window `ci-integration` failed on one step (`tall-block-scroll`) of
      this machine's VS Code window, so `ci-report` and `ci-gallery` did not pass; the heavy run
      below is the real-window proof
- [ ] Review: the owner reviews the release notes and the thread
- [x] CI green at this head, and the heavy run dispatched on this branch green at its exact head
      (`integration` success, `stress` success; run 43377939225)

## Autonomous decisions

- The picture is an existing capture of the sticky band from the visual suite, cropped to a
  landscape frame, not a dedicated hero scenario: the guideline accepts an existing capture for a
  small release. A dedicated hero image (a real document with the sticky band or an alert) can
  replace it on request.
- "Export keeps your edit in progress" goes in "Smoother editing" and the grid-in-quote click fix
  in "All fixes"; the three headline changes have their own sections.

## Internal references

- Release change request: CR-313 release-v1-8-0 (batch-02).
