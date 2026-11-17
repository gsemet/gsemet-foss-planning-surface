# Report: release v1.9.1

Published on 2026-11-14.

- Tag: `v1.9.1` on `5a61b0c9` (`chore: version 1.9.1`, PR
  https://github.com/gsemet/markdown-okf-schema-studio/pull/400, merged by the owner by rebase at
  11:37:14Z).
- GitHub release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.1
  (reviewed notes, VSIX attached; no image).
- Content: 9 changes since 1.9.0, none user-visible (CR-324 to CR-327, PRs #396 to #399): the
  release dispatched from the version push, the version commit without `Signed-off-by`, the
  real-window test hardening, the stress deadline computed from its rounds (12 by default).

## Success criterion: met

The version push's **Release VSIX** run (event `workflow_dispatch`, branch `main`, dispatched by
the `release` job of `ci.yml`) published to Open VSX with trusted publishing on its first pass:
"Trusted publishing token issued ... Published GaetanSemet.markdown-okf-schema-studio v1.9.1".
**No recovery dispatch.** CR-324's fix is proven.

## CI runs

| Run | Commit | Result |
| --- | --- | --- |
| Heavy run on `main` before the deadline fix: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43582068953 | `0941cc09` | green on attempt 2 (attempt 1: stress red at round 10/20, real-input palette, Heading 2 prefix timeout; attempt 2 stress green in 24 min 41 s of the old 26-minute deadline, which led to CR-327) |
| Branch heavy run of the version PR, default repeat: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43588092081 | `3eee3d59` | green on attempt 1 (stress 15 min 12 s, 12 rounds) |
| PR CI of the version PR: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43588085877 | `3eee3d59` | green |
| Version push on `main`: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43590898224 | `5a61b0c9` | green on attempt 2. Attempt 1: integration red at `myst-blocks` (step after `toc`, after `readme-html`): "Edit mode did not switch to on: the toggle missed 3 clicks", host frame `hasFocus=false`, the signature of the known bug toc-edit-toggle-clicks-lost-after-readme-html; tag refused. Attempt 2 (re-run of the failed jobs, under `release go`): integration green, tag, release dispatch, Pages green. Stress green on attempt 1 in 13 min 29 s |
| Release VSIX, dispatched by the version push: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43593174902 | `5a61b0c9` | green: notes prepared, Marketplace published (OIDC), VSIX attached, Open VSX published (trusted publishing) |

## Registries

The Release VSIX run ended at 12:07:24Z (Marketplace published 12:07:13Z, Open VSX 12:07:21Z).

- VS Code Marketplace (gallery `vspackage` URL): HTTP 200 at the first check, 12:08:06Z, minute 1.
- Open VSX (`/api/GaetanSemet/markdown-okf-schema-studio/1.9.1`): 404 at 12:08, 12:09 (twice),
  HTTP 200 at 12:10:23Z, minute 3. The extension API answers latest version 1.9.1.
- Pages: https://gsemet.github.io/markdown-okf-schema-studio/ answers 200; `pages / deploy-pages`
  green at 12:09:14Z.

## Issues

No issue closed by this release (no closing references on PRs #396 to #400, no `issue:` line in
the changes of CR-323 to CR-327).

## Announcement

The thread is drafted in `docs/releases-notes/2026-11-14-v1.9.1/tweet.md` and not posted. Its post
1 and the notes say the release reaches both registries in the same run: true, no edit needed.
