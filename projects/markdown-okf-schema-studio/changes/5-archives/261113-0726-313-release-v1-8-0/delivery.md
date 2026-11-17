# Release v1.8.0

batch-02, stack, 8 of 8 change CRs merged by the owner by rebase (2026-11-13 06:14:48Z to
06:14:55Z), then the version PR. Batch cost $32.89, no budget (the Chief of Staff's own cost not
measured: no price for its model in chantier).

Written by the Chief of Staff from the Release driver's findings, relayed by the Foreman: the
harness refused the Release driver's Write of `report.md` ("Subagents should return findings as
text").

| CR | PR |
| --- | --- |
| CR-305 changelog-line-in-each-pr | https://github.com/gsemet/markdown-okf-schema-studio/pull/377 |
| CR-306 ci-report-object-object-message | https://github.com/gsemet/markdown-okf-schema-studio/pull/379 |
| CR-307 ci-integration-locked-screen | https://github.com/gsemet/markdown-okf-schema-studio/pull/376 |
| CR-308 card-in-blockquote-line-offset | https://github.com/gsemet/markdown-okf-schema-studio/pull/378 |
| CR-309 alert-followed-by-heading-taken-as-title | https://github.com/gsemet/markdown-okf-schema-studio/pull/380 |
| CR-310 export-html-drops-block-being-edited | https://github.com/gsemet/markdown-okf-schema-studio/pull/381 |
| CR-311 sticky-heading-long-title-wraps | https://github.com/gsemet/markdown-okf-schema-studio/pull/382 |
| CR-312 cmd-s-from-preview-focus | https://github.com/gsemet/markdown-okf-schema-studio/pull/383 |
| CR-313 release-v1-8-0 | https://github.com/gsemet/markdown-okf-schema-studio/pull/385 |

- Tag: `v1.8.0` at `5118466d` (`chore: version 1.8.0`, PR #385, merged by the owner by rebase at
  2026-11-13T06:59:12Z).
- GitHub release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.8.0,
  published 2026-11-13T07:22:55Z, not a draft, assets `markdown-okf-schema-studio.vsix` and
  `sticky-heading-one-line.png` (checked by the Chief of Staff).
- Marketplace: the gallery API serves the 1.8.0 VSIX (HTTP 200, checked by the Chief of Staff);
  the listing query still showed 1.7.1 shortly after, during the Marketplace's verification.
- Pages: the site answers 200 (Release driver, not re-checked).
- Issues: none closed by this release, so no "Released in" comment (empty-list rule).
- No announcement posted: `tweet.md` is the owner's.
- Not proved: the local `just preflight` real-window integration failed on `tall-block-scroll` at
  the version head (green in the branch heavy run).
- Side note: issue #336 (closed 2026-11-10) has no "Released in" comment, while #334 and #335 point
  to 1.6.0.

## CI runs

| Run | Commit | Event | Result |
| --- | --- | --- | --- |
| [43377379519](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43377379519) | `96b8b91d` (`main` before the version) | push | success |
| [43377939225](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43377939225) | `39d4a51e` (version PR branch) | heavy dispatch | success, `integration` and `stress` green |
| [43382475196](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43382475196) | `5118466d` (version push) | push | success: tag-release, release / package, pages green; toc-loop and gallery skipped |
