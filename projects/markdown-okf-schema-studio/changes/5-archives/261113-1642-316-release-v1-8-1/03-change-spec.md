# Change Specification: release v1.8.1

Written by the Chief of Staff (a release CR's specification is the Chief of Staff's). Completed at
the confirmation, from what was merged.

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`) and
"How to Release" in `CONTRIBUTING.md`. They rank above this file.

## Decisions (from 02-answers.md)

- Version: **1.8.1**, a patch from v1.8.0: the only change is how the extension is published
  (CR `marketplace-trusted-publishing`, VS Code Marketplace Trusted Publishing with GitHub OIDC).
- Purpose: the proof of the OIDC publish before the next feature release.
- Delivery: the version PR is the top of the batch's stack, per the guideline; the owner merges by
  rebase, in order; the version push on `main` stays the final gate and makes the tag.
- Release notes: short, for a user: this release changes nothing in the extension; it changes how
  it is published (no stored Marketplace token). No mention of Open VSX.
- Grant: default. Every irreversible action waits for the owner's approval.

## Check of record

- The release job's "Publish to VS Code Marketplace" step ran with `--oidc` and succeeded; no
  token step exists.
- The Marketplace serves 1.8.1 (gallery API), and the policy "Release workflow" (or a second
  policy for `ci.yml`, if the owner adds one) shows a "Last used" date.
- On a failed exchange: the job fails before the GitHub release is written; recovery per
  CONTRIBUTING "Recovery and Release Notes" (fix, then dispatch **Release VSIX** with the tag).
  This is reported, not worked around.

## Settled at the confirmation (owner, 2026-11-13)

- Version set explicitly: `just version 1.8.1` (since v1.8.0 only a `ci:` and a `docs:` commit; the
  commitizen guess may not bump on them). Every versioned file of `scripts/version.py` says 1.8.0 on
  `origin/main` before it.
- CHANGELOG: per the guideline; `## Unreleased` is empty (CI commits get no line), so the 1.8.1
  section is empty, or holds one maintenance line if the procedure requires one.
- No hero image (patch release, nothing visible). No docs diagram.
- No announcement thread: no `tweet.md` (an owner's exception to the guideline's three posts: the
  release has nothing to tell users).
- Two Marketplace policies exist: "Release workflow" (`release.yml`) and "CI workflow (calls
  release.yml)" (`ci.yml`), both environment `release`. The check of record notes which shows a
  "Last used" date. `VSCE_PAT` stays; the owner deletes it after this release succeeds.
- What is merged: PR 387 (CR-315, b1907e9f) and fd8adb9e (docs). Not from this batch: nothing else.
