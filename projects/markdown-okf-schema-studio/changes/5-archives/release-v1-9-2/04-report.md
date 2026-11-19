# Report: release 1.9.2

- Tag: `v1.9.2` on 7185a976 (`chore: version 1.9.2`, PR #422, merged by the owner on
  2026-11-19T12:40:13Z).
- Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.2 (notes and
  VSIX attached).
- Heavy run on `main` HEAD 1d5db15b: CI run 44519875389. `integration` failed once in
  `preview-editing` (the test reads a badge highlight that lasts 1.5 s twice, and the second read
  timed out), green on the single re-run of the failed jobs; `stress` green.
- Version push: CI run 44526032547, all jobs green (integration, stress, tag-release, release,
  pages). Release VSIX: run 44528571415, green, no recovery dispatch.
- Registries: VS Code Marketplace served 1.9.2 at minute 1; Open VSX served 1.9.2 at minute 1.
- Issues closed by the release: #420 (PR #421).
