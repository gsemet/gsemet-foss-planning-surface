# Report — 275-release-1-6-0

Status: **done** (2026-11-10). Version 1.6.0 published: tag `v1.6.0` at `f4d11d38`, release https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.6.0 (VSIX, `svg-pictures.png`, `front-matter-values.png`), Marketplace 1.6.0, Pages deployed.

## Delivered

| CR | PR | Change |
| --- | --- | --- |
| 268 | #337 | A table cell left with Tab or an arrow shows the text just typed |
| 269 | #338 | A wide table keeps its width while a cell is edited |
| 270 | #339 | Inline Markdown hardening in cells |
| 272 | #340 | Inline SVG pictures (GitHub #336) |
| 273 | #341 | Front matter values `= this.field` (GitHub #334) |
| 275 | #342 | Version 1.6.0, notes, thread (merge `f4d11d38`) |

## Proof of completion

- Heavy run on `main` HEAD `ecb368e9`: run 42859219191, integration green; stress red on the first attempt (a focus and hang dump in `ci-stress`, scenario not identified), green after one `gh run rerun --failed`.
- Version push: run 42870003806 at `f4d11d38`: checks, integration, stress, tag-release, release and Pages all green. Tag read with `git ls-remote`, release with `gh release view`, Marketplace with the extension query (1.6.0 appeared about 10 minutes after `vsce publish`), Pages deployment at the tag commit, site HTTP 200.
- Notes and thread approved by the owner as in PR #342; no dedicated hero image (cropped captures of CR 272 and 273 used).

## Open items

- The stress flake of run 42859219191 attempt 1 is not diagnosed (CI rule 12).
- A changelog line for the table of contents fix (`ccaf35b8`) was missing and was added in the version commit.
- The announcement thread (`tweet.md`) is for the owner to post.
