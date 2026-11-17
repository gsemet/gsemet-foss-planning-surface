# Report: release v1.9.0

Published on 2026-11-14.

- Tag: `v1.9.0` on `4b45b45e` (`chore: version 1.9.0`, PR
  https://github.com/gsemet/markdown-okf-schema-studio/pull/395, merged by the owner by rebase).
- GitHub release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.0
  (reviewed notes, VSIX and `floating-toolbar-four-by-four.png` attached).
- Content: 8 changes since 1.8.1 (CR-317 to CR-322, PRs #389 to #394).

## CI runs

| Run | Commit | Result |
| --- | --- | --- |
| Heavy run on `main` before the version commit: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43532691444 | `1191fb6c` | green on attempt 2 (attempt 1: integration flake at the toc step) |
| Branch heavy run of the version PR: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43536948441 | `f12ba53b` | green on attempt 2 (attempt 1: integration flake at real-input) |
| Version push on `main`: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43567601653 | `4b45b45e` | heavy jobs, tag, Marketplace, GitHub release and Pages green; Open VSX step red |
| Release VSIX dispatch with tag `v1.9.0`: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43569382533 | `4b45b45e` | green: Marketplace skipped the duplicate, GitHub release rewritten from the reviewed notes, Open VSX published |

## Registries

The release job ended at 07:03:34Z (version push); the recovery dispatch's Open VSX step ended at
07:05:42Z.

- VS Code Marketplace (gallery `vspackage` URL): HTTP 200 at the first check, 07:04:00Z, minute 1.
- Open VSX (`/api/GaetanSemet/markdown-okf-schema-studio/1.9.0`): 404 on the version push (step
  red). After the dispatch: 404 at 07:06 and 07:07, HTTP 200 at 07:08:12Z, minute 3 after its
  publish step. The extension API answers latest version 1.9.0.
- Pages: https://gsemet.github.io/markdown-okf-schema-studio/ answers 200; deployed by the version
  push (`pages / deploy-pages` green at 07:05:02Z).

## Open VSX recovery

The Open VSX step of the version push failed with "No trusted publisher matches the presented
token." The release job runs as a reusable workflow called by `ci.yml` (`uses:
./.github/workflows/release.yml`), so the OIDC token names `ci.yml` as the caller workflow, while
the trusted publisher on open-vsx.org is registered for `release.yml`. The recovery the
specification allows (one `workflow_dispatch` of **Release VSIX** with the tag, per CONTRIBUTING
"Recovery and Release Notes") ran from `release.yml` itself, and the publisher matched. Approved by
`chantier release go` within the grant.

Every future version push will fail the same way until the owner either registers `ci.yml` as a
trusted publisher on open-vsx.org as well, or the workflow is changed: see `retro.md`.

## Issues

No issue closed by this release (no closing references on PRs #389 to #395, no `issue:` line in
the changes of CR-317 to CR-323).

## Announcement

The thread is drafted in `docs/releases-notes/2026-11-14-v1.9.0/tweet.md` and not posted. Post 3
keeps its Open VSX link: the Open VSX publish succeeded.
