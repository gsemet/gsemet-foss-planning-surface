# Owner's answers (2026-11-10, "ok" to every recommendation)

| Question | Decision |
| --- | --- |
| Scope | The `svg` fence and raw `<svg>` that fills a whole block. A `<svg>` inside a sentence stays dropped. |
| How | Option B: the sanitized SVG is inlined in the page. The sanitizer removes scripts, `foreignObject`, `on…` handlers, external links and `<style>`, and scopes or renames `id`s. |
| Variables | Studio defines a small vocabulary from its theme: `--surface`, `--background`, `--bg` (block background); `--border`; `--text`, `--foreground`, `--fg`; `--muted` (secondary text); `--accent`, `--primary`; named colours `--red`, `--green`, `--blue`, `--orange`, each for light and dark. An undefined variable uses its `var()` fallback, else the text colour. |
| Size | The SVG keeps its `viewBox` and declared width, capped at the column, eligible for the Auto breakout like an image. |
| Edit | A click opens the block's source editor, as for Mermaid; raw `<svg>` edits as an HTML block. |
| Writing skill | Describes what is possible in the same PR: both forms, the variable list and meaning, what the sanitizer removes, when a file with `{figure}` is still the better choice. |
| Form | One PR, P2, after CR 270; it may take in QA campaign 271 findings if they touch the same code. |

## Issue link (owner, 2026-11-10)

The PR body says `Fixes #336` so GitHub links and closes the issue, and a comment on the issue links the PR when it opens.
