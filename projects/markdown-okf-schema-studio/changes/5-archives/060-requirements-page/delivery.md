# Report — requirements-page

## Delivered

- [#63](https://github.com/gsemet/markdown-okf-schema-studio/pull/63): a "Requirements" page on the
  project site (`requirements.html`): what the requirements are, why, how they work (chain
  diagram and real `@implements_req` / `@tests_req` snippets read at build time), stats from the
  okfreq report (active requirements only), and a "browse" placeholder. README links to it; the
  site gained a dark theme. SwRS-MDOKFSTUDIO-CORE-069.

## Proof of completion

- `just check` green; `just preflight` green (integration stage passed on retry after a focus
  timeout); PR checks green; merged.

## Open items

- The link goes live with the next release (Pages deploys on tags).
- Requirement browser: backlog `P3/requirements-report-site`, and okfreq-side data in
  gsemet/okf-schema `.github/changes/backlog/graph-viewer`.
