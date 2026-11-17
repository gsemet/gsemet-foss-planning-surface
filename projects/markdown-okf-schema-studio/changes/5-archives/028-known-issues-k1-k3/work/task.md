# T1 — Fix K1 overflow and K3 Mermaid error duplication

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-028 (branch `fix/mermaid-error-and-overflow` from origin/main). Work ONLY there;
`node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read
`00-request.md` (decisions), `00-intent-backlog.md` (symptoms and measurements) and `rules.md`.

## K3 — Mermaid error duplication

- `src/webview/mermaidPreview.ts` ~line 91: the catch does `diagram.prepend(error)` on every
  render, so each theme switch adds one more "Unable to render Mermaid diagram" line.
- Fix: one error element per diagram (replace the existing one, never stack). Keep the source text
  visible below as today. Add a collapsible `<details>` (closed by default) with the parser's error
  message (`err.message`, as text, never as HTML). Style it in the stylesheet
  (src/preview/previewStyles.ts), readable in light, dark, cream and current theme.
- A diagram fixed by the user after an error must render the image and drop the error.

## K1 — overflow

- A long unbroken word overflows its paragraph and a long bare URL (autolink) makes the whole page
  scroll horizontally (1093 px at 900, 1058 px at 460). Fixture `test/visual/fixtures/35-cjk-rtl.md`.
- Fix in the stylesheet (likely `overflow-wrap: anywhere` on paragraphs, list items, table cells,
  links; check which selectors already have it). The page must never scroll horizontally because of
  text; code blocks keep their own horizontal scroll.

## Tests (write first, they must fail on the unchanged code)

- Unit test (test/webview/…): render an invalid diagram twice (or trigger the re-render path) and
  assert exactly one `.myst-mermaid-error` and one `<details>` holding the parser message.
- Stylesheet unit test (test/webview/previewStyles.test.ts style) for the overflow rule.
- Visual scenarios (test/visual/scenarios.ts): remove `knownIssue: "P9-B4-K3"` from v08/v09 and add
  an assertion that there is exactly one error line after a theme switch if the harness allows it;
  on v17/v18 keep only `P9-B4-K2`. Add a NEW visual scenario without `knownIssue` that renders long
  unbroken words and long bare URLs at 460 and 900 px and asserts document scrollWidth <= viewport
  width and each paragraph's scrollWidth <= its clientWidth (new fixture if 35-cjk-rtl mixes RTL).
- Screenshots for the PR: the Mermaid error with its details (light and dark, open details if
  possible) and the overflow scenario at 460 px, from `just visual`.

## Docs

CHANGELOG Unreleased bullets (user-facing): long words and URLs wrap instead of widening the page;
an invalid Mermaid diagram shows one error with the parser's reason. README only if it documents
Mermaid errors.

## Gates (foreground, windowless only)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. No integration/e2e/preflight
locally.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/028-known-issues-k1-k3/reports/T1-r<round>.md`.
