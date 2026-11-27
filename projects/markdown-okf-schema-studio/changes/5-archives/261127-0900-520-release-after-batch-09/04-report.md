# CR-520 report: release v1.13.0

All times are UTC, on 2026-11-27.

## Release

- Tag: `v1.13.0` at `b9b29c5a` (`chore: version 1.13.0`), created by the `tag-release` job of the
  version push CI run.
- Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.13.0, published
  09:37:03, latest, not a draft, not a pre-release.
- Assets, each answering 200: the VSIX, `comment-render-speed.png`, `raw-copy-balance-edges.gif`,
  `admonition-block-edit-before-after.png`, `chart-hover.png`.
- Release body: the committed `release-notes.md`, with the image links pointing to the assets.
- Version PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/552, head `4222c324`, merged
  by the owner at 09:16:17.

## CI runs

- Heavy run on `main` before the version commit:
  [45958381383](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45958381383) on
  `b1e23cc`, every job green (`integration`, `stress`, `acceptance (trust-security)`).
- Version PR run:
  [45971675798](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45971675798) on
  `4222c324`, green, completed at 09:22:00, after the merge.
- Version push run:
  [45972312915](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45972312915) on
  `b9b29c5a`, every job green on the first attempt (`perf-547`, `toc-loop` and `gallery` skipped),
  `integration`, `stress`, `acceptance (trust-security)`, `tag-release`, `release` and the Pages
  build and deploy included. 09:16:19 to 09:38:59.
- Release VSIX run:
  [45975054311](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45975054311),
  success on the first attempt, 09:36:02 to 09:37:12. Open VSX needed no recovery dispatch.

## Registries

| Registry | Check of record | State |
| --- | --- | --- |
| VS Code Marketplace | `vspackage` of 1.13.0 | 200 at the first check, 09:39:24 |
| Open VSX | API of 1.13.0 | 404 at 09:39:24, 200 at 09:39:56 |

Both served 1.13.0 within 3 minutes of the end of the Release VSIX run.

## Issues

- Closed by a closing reference: none (PRs #549, #550 and #552 have none).
- Shipped in part: https://github.com/gsemet/markdown-okf-schema-studio/issues/547 (PRs #549 and
  #550, named by the changes CR-516 and CR-517). It was closed as completed from the repository
  owner's account at 09:16:38, 21 seconds after the merge of PR #552, with no closing PR or commit,
  although the comment posted on it at 07:56 says it stays open until its reporter has tried the
  release.
- Release comment on the issue: handled by the session that steered the release, which reports
  that the owner approved its text there, with the choice that leaves the issue closed, and that it
  posts it and reads it back. None was posted by this follow-up. Not yet on the issue when it was
  read back at 09:42, where the last comment is the one of 07:56.
- No other issue ships with this release (#485 was released and commented with 1.12.1).

## Clip

- Clip: `raw-copy-balance-edges`.
- Step 7 (owner only): not done at 09:40; the release body still shows the GIF.

## Left to the owner

- Upload `raw-copy-balance-edges.mp4` into the release body, in place of its GIF line.
- Post the announcement thread (`docs/releases-notes/2026-11-27-v1.13.0/tweet.md`), post 1 with
  the MP4.

## Note

The publication was followed by a separate session, after batch-10 was closed: no Driver ran the
steps after the merge, and chantier holds no `release published` record (see `retro.md`).
