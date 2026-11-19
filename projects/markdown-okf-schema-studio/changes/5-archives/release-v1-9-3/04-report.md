# Release 1.9.3 report

- Tag: v1.9.3 (version commit 24c9eef0, PR #425 merged by rebase at the owner's request).
- Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.3, published
  2026-11-19T18:12:36Z.
- CI runs:
  - Heavy run of `main` a0821ac5 (PR #424): 44569980384, `integration` and `stress` green.
  - Version push 24c9eef0: 44575797652. `integration` red twice on `paste-url` ("Timed out waiting
    for the workspace to remember edit mode off"), green on the second re-run, which the owner
    chose; `stress`, tag-release, release dispatch and Pages green.
  - Release VSIX: 44585200057, green with no recovery dispatch.
- Registries: the Marketplace vspackage and Open VSX API both return 200 for 1.9.3. They were
  checked once, about 1 h 48 min after publication, so the minute each began serving is not known.
- Issues closed: none. PR #424 refers to #423, which stays open for the follow-ups.
