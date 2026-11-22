# CR-446 report: release v1.11.0

## Release

- Tag: `v1.11.0` on 5a84db8b (made by the `tag-release` job of the push-to-main CI run).
- Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.11.0 (published, not a draft).
  Assets: `markdown-okf-schema-studio.vsix`, `blank-lines-block.png`, `delete-block-button.png`,
  `line-marker-arrow.png`.
- Version PR: #456, merged by the owner at 07:59Z (head b28646f).

## CI runs

- 44880074434: heavy run on the top branch (before the merge).
- 44882733071: version push on `main`, success, every job green including `tag-release`, `release`,
  `pages / build-site` and `pages / deploy-pages` (`toc-loop` and `gallery` skipped as usual).
- 44883990209: Release VSIX (workflow_dispatch, main, 08:15Z, 48s), success. Marketplace publish,
  GitHub release attach and Open VSX publish green with no recovery dispatch.

## Registries

- VS Code Marketplace: vspackage URL 200 on the first poll after the release run.
- Open VSX: API URL 404 for about 1.5 minutes, then 200. Both serve 1.11.0.
- Pages: green. The live site was not opened.

## Issues

No issue closed by this release (no PR #445..#453 or #456 has a closing issue reference).

## Announcement thread

The owner's to post. Draft: `docs/releases-notes/2026-11-21-v1.11.0/tweet.md`.
