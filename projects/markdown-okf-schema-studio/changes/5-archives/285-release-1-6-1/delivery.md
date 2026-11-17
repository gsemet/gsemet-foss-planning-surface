# Report — 285-release-1-6-1

Status: **done** (2026-11-11). Version 1.6.1 published: tag `v1.6.1` at `96a86e46`, release https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.6.1 (VSIX, `cell-editor-narrow-before.png`, `cell-editor-narrow-after.png`), Marketplace 1.6.1 (`vsce publish` log), Pages deployed.

## Delivered

| CR | PR | Change |
| --- | --- | --- |
| 278, 279, 277 | #346, #347, #348 | Table fixes from QA 271 |
| 280 | #350 | Undo/redo of a row deletion restores its comment mark |
| 282 | #351 | Cell editor fits a narrow pane |
| 281 | #352 | One click reaches a property field |
| 283, 284 | #345, #353 | Process: PR template, Verifier step |
| 285 | #354 | Version 1.6.1, notes, thread (merge `96a86e46`) |

## Proof of completion

- Heavy run on `main` HEAD `2e9cf0b9`: run 43005192087 green.
- Version push: run 43012439055 at `96a86e46`: checks, integration, stress, tag-release, release/package and Pages all green. Release read with `gh release view`; the publish step logged "Published GaetanSemet.markdown-okf-schema-studio v1.6.1" (the Marketplace page lags a few minutes).
- Notes and thread approved by the owner in PR #354; no hero image.

## Open items

- The announcement thread (`tweet.md`) is for the owner to post.
- Release worktree, local and remote branch `release/1.6.1` not removed (classifier refusal).
- Owner request: the next release PR shows the notes and the tweet in its body (P1 backlog `release-pr-body-renders-notes`).
