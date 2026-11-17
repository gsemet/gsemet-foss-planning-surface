# Report — requirements-okfreq

Requirements baseline with okfreq: every behaviour of the extension is specified as it is today,
anchored to the code by `@implements_req` / `@tests_req` markers.

## Delivered

| PR | Content |
| --- | --- |
| [#55](https://github.com/gsemet/markdown-okf-schema-studio/pull/55) | okfreq installed in the project (`requirements` dependency group), justfile targets |
| [#56](https://github.com/gsemet/markdown-okf-schema-studio/pull/56) | Batch 1: rendering-core, code-blocks, gfm, myst |
| [#57](https://github.com/gsemet/markdown-okf-schema-studio/pull/57) | Rule: requirements are anchored to the code |
| [#58](https://github.com/gsemet/markdown-okf-schema-studio/pull/58) | `.agents/constitution.md`, AGENTS.md under 100 lines, load triggers |
| [#59](https://github.com/gsemet/markdown-okf-schema-studio/pull/59), [#60](https://github.com/gsemet/markdown-okf-schema-studio/pull/60) | Batch 2: diagrams, frontmatter-schema, frontmatter-editing, layout-width, and follow-up |
| [#62](https://github.com/gsemet/markdown-okf-schema-studio/pull/62) | Complete baseline, one commit: 16 scopes, 76 StRS / 364 SwRS (one SwRS per observable behaviour), markers in code and tests, tests for every SwRS, superseded ids for the earlier finer baseline |

## Proof of completion

- 16 scopes, 364 active SwRS, 76 StRS (1863 / 228 before the tile restructuring, kept as superseded or retired ids, see `reduction/`); `okfreq validate --prose --check-links`, `lint --check`,
  `update-coverage --check` clean.
- Every non-exempt SwRS has an implementation and a test marker (3 declarative exemptions); 69 of
  76 StRS have a stakeholder validation test. okfreq's own StRS figure counts superseded SwRS
  (reported upstream in gsemet/okf-schema graph-viewer request).
- `just check` green; `just preflight` green (the real VS Code integration stage passed on the
  third run after two focus-related timeouts); PR #62 checks green.
- Completeness audit: `reviews/completeness.md`; gaps: `gap-report.md`.

## Open items

- Known issues found by the baseline are filed in the backlog (none fixed here, by design):
  - P1: restricted-mode-capability, palette-stale-after-autosave.
  - P2: trust-grant-refresh, include-empty-argument, inline-link-opens-editor,
    refused-open-empty-frame, stale-request-no-answer, block-editor-save-races,
    block-edit-line-endings, table-insert-splits-table, table-cell-paste-linebreak,
    switch-back-state-lost, watcher-ignore-absolute-path, page-security-hardening, plus the batch 1
    items (paste-*, copy-button-*, label-rename-dead-click, currency-dollar-preview-check).
  - P3: table-editor-polish, link-navigation-fixes, toolbar-band-fixes, preference-write-failure,
    readonly-reason-wording, comments-button-hides-threads, lifecycle-small-fixes,
    block-editing-small-fixes, requirements-test-quality, checkbox-refusal-feedback,
    empty-yaml-schema (waits for gsemet/okf-schema#41), field-editor-error-then-block-click,
    doc-download-empty-link, docs-includes-restricted-mode, html-colour-grammar,
    requirements-report-site.
- Follow-ups: code simplification PR (`reduction/code-simplification.md`); requirements page on the
  site (CR 060, PR #63); okfreq id reuse (gsemet/okf-schema#42); `okfreq-setup` skill
  (gsemet/okf-schema#43, merged).
