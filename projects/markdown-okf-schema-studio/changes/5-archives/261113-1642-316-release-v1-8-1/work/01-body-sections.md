## Summary

Version 1.8.1 of Markdown OKF-Schema Studio. The extension itself does not change: this patch
release is the first one published to the VS Code Marketplace with Trusted Publishing (GitHub
Actions OIDC): the release workflow no longer reads a stored Marketplace token, which
the owner deletes once this release succeeds. It proves the new publishing path before the next
feature release.

## Deliverables

The release folder the owner reviews, committed with the version:

| File | Content |
| --- | --- |
| `docs/releases-notes/2026-11-13-v1.8.1/release-notes.md` | The GitHub release notes (rendered below) |

No announcement thread and no picture for this release: there is nothing new for users to see
(the owner's decision for this patch).

## Changes

- `chore: version 1.8.1` from `just version 1.8.1` (set explicitly: since 1.8.0 only a `ci` and a
  `docs` commit landed): `package.json`, `package-lock.json`, the two plugin manifests and the
  GitHub Copilot catalog entry move from 1.8.0 to 1.8.1.
- `CHANGELOG.md`: a `## 1.8.1 - 2026-11-13` heading under `## Unreleased`; it holds no line, since
  no `feat` or `fix` commit landed since 1.8.0.
- The release folder above.

## Impacts

No visual change: this commit only changes version numbers, the changelog heading and the release
folder. The merge publishes 1.8.1 (tag, GitHub release with these notes, Marketplace, Pages)
through the version push on `main`, and the Marketplace step runs `vsce publish --oidc` for the
first time.

## Blast radius

Grade: 3

A release: once merged, CI tags v1.8.1 and publishes to the Marketplace. The extension code is the
one already on `main`. If the OIDC token exchange fails, the release job fails before the GitHub
release is written; the tag stays, and **Release VSIX** is dispatched again with the tag once the
cause is fixed (CONTRIBUTING, "Recovery and Release Notes").

## Test plan

- [x] New or changed tests (they fail on the previous code): no code change in this PR
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change; no `feat` or `fix` commit since v1.8.0
- [x] Local gates: `just release-notes-check` ok; `just preflight`: `ci-static` and
      `ci-visual` passed, the local real-window `ci-integration` failed on one step
      (`Heading 2` prefix: this machine's VS Code window lost focus), so `ci-report` and
      `ci-gallery` did not pass; the heavy run dispatched on this branch is the real-window proof
- [ ] Review: the owner reviews the release notes
- [x] CI green at this head; the heavy run of `main` HEAD b1907e9f is green (`integration`
      success, `stress` success; run 43450028473), and the heavy run dispatched on this branch is
      green at its exact head 08e3c0f8 (`integration` success, `stress` success; run 43456982844)

## Internal references

- Release change request: CR-316 release-v1-8-1 (batch-03).
