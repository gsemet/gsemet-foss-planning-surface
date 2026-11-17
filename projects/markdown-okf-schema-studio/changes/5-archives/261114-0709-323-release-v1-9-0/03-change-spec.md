# Change Specification: release v1.9.0

Written by the Chief of Staff (a release CR's specification is the Chief of Staff's). Completed at
the confirmation, from what was merged.

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`) and
"How to Release" in `CONTRIBUTING.md`. They rank above this file. Run `just dev` first in the new
worktree.

## Decisions

- Version: **1.9.0**, a minor from v1.8.1: CR-318 is a `feat` (the floating toolbar in four rows of
  four); the rest are fixes, docs and the Open VSX publish.
- Delivery: the version PR is the top of the batch's stack, per the guideline; the branch heavy run
  is green on its exact head before it turns ready; the owner merges by rebase; the version push on
  `main` stays the final gate and makes the tag.
- Release notes and the announcement thread (`tweet.md`, three posts) per the guideline; the owner
  posts, agents never do. Lead with the toolbar; the grid fixes in plain words; one line that the
  extension is now also on Open VSX (for VSCodium, Cursor and other compatible editors), only if
  the Open VSX publish succeeded at the time the notes are final, else no mention.
- Hero image: recommended for a minor; a fresh capture of the floating toolbar in its 4 x 4 layout
  (the README hero still shows the old five-row toolbar: do not reuse it).
- Grant: default. Every irreversible action waits for the owner's approval.

## Check of record

- The release job's "Publish to VS Code Marketplace" step ran with `--oidc` and succeeded; the
  Marketplace serves 1.9.0 (gallery API).
- The Open VSX step ran with trusted publishing and succeeded:
  `GET https://open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio` answers version 1.9.0.
  Note which workflow Open VSX matched (`release.yml` is registered; if the exchange fails on a
  workflow mismatch, report it: the owner can change the registration, nothing is worked around).
- On a failed Open VSX step: the Marketplace step runs before it; report the state, recover per
  CONTRIBUTING "Recovery and Release Notes" on the owner's word.
- GitHub release published with the VSIX; Pages answers 200; "Released in" comments on the issues
  the release closes (none expected).

## Settled at the confirmation

Settled by the Chief of Staff on 2026-11-14, under the owner's overnight grant (02-answers.md):

- What is merged since v1.8.1 (origin/main 1191fb6c): CR-317 #389 (30fd3f52, docs), CR-318 #390
  (8d7b052e feat, 0a48496b test), CR-320 #391 (d8ff17d3), CR-319 #392 (5a5f6745), CR-321 #393
  (f50b2059), CR-322 #394 (6c511d75 ci, 1191fb6c docs). Nothing else.
- Version 1.9.0, set explicitly (`just version 1.9.0`) if the commitizen guess differs.
- CHANGELOG: the four `## Unreleased` lines as they stand (CR-317 and CR-322 have none: docs/ci).
- Release notes: the guideline's two install links (VS Code Marketplace, Open VSX), as CR-322
  changed it.
- Hero image: a fresh capture of the 4 x 4 floating toolbar; if none can be made unattended, no
  hero image (recommended, not required) and say so in the report.
- No docs diagram. Announcement thread drafted, not posted; post 3 adds the Open VSX link only if
  the Open VSX publish succeeded.
- Open VSX: if the trusted publishing exchange fails, recover once with a `workflow_dispatch` of
  **Release VSIX** (`release.yml`) with the tag, per CONTRIBUTING; if that also fails, report it
  for the owner, nothing else.
- Watch both registries for 10 to 15 minutes after the release job, per the guideline.
