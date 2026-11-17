# UX-26 — Status pages glue title and message, and user-facing text still says "Sphinx"

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Status pages, notifications, wording |
| Evidence | [r3-link-click.jpg](../evidence/r3-link-click.jpg) |

## Observed

- The missing-source page renders "**Preview source missing**Open a Markdown file to use the
  Sphinx preview." with no space or line break between title and message.
- The pipeline no longer uses Sphinx (myst-parser in process), but user-visible strings still say
  "Sphinx": "Open a Markdown file to use the Sphinx preview.", "Sphinx preview navigation blocked:
  …", "Sphinx preview could not open …".
- Internal attribute names (`data-sphinx-…`) are fine, but they leak into the accessible status
  region ("Preview ready" is announced, which is good).

## Where it comes from

`src/preview/webview.ts` status labels (L61) and `buildStatusWebviewHtml` (L108);
`src/extension.ts` L1512, L1576, L2232.

## Suggested direction

Put the title and message in separate block elements; replace "Sphinx preview" with "Markdown
OKF-Schema Studio" (or "the preview") in all user-facing strings; add a lint test that scans
`showWarningMessage`/status strings for "Sphinx".

## Done when

No user-facing string mentions Sphinx, and status pages read as two lines.
