# 125 — An unclosed fence in the middle of a document no longer hides the rest

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-unclosed-fence-swallows-document`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- An opening fence (backticks or colons, with or without a directive name) that has no closing fence before the next heading-level structure is rendered as its raw opening line; the rest of the document renders normally. Markdown says an unclosed fence runs to EOF: we deliberately depart from it in the preview only, and show a warning marker on the raw line naming the problem ("unclosed fence").
- The source is never changed.
- Tests: unit (parser), webview, and an e2e with the user's document; they fail on the current code.

- Round 1 APPROVED; requirements lint not run (okfreq too old) and shots are static Playwright captures: recorded in PR body.
