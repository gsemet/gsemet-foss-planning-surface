# Report — release-1-5-0

Status: **partial** (2026-11-06, branch `release/1-5-0`, PR #332, merge commit `aa0af6c9`). The owner accepted the state below and closed the release.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| Release | Version 1.5.0: tag `v1.5.0`, GitHub release with its notes and image, Marketplace 1.5.0 | `aa0af6c9` |

Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.5.0

## Proof of completion

- Heavy run on `main` before the version commit: 42189725818, `integration` and `stress` green on `30239846`.
- Version push: run 42195304770, every job green except `pages / deploy-pages`.
- Checked by the main session: tag on `aa0af6c9`; release not a draft, assets `comment-thread.png` and the VSIX; the image link of the notes loads (118 KB); Marketplace query returns 1.5.0.
- Process gaps: the changelog lines were not in the PRs of the stack, so they went into the version PR, after the heavy run.

## Open items

- **Pages not deployed**: the site still serves the 1.4.0 deployment. The first attempt stayed in `syncing_files` for 10 minutes (it took about 5 seconds for 1.4.0, same 94 MB artifact), and `actions/deploy-pages` gave up. The rerun got an empty status until its timeout, perhaps because it reused the cancelled deployment id `aa0af6c9`. GitHub status showed Pages operational; the cause is unknown. The next version push deploys the site again.
- Announcement thread: the owner posts it.
