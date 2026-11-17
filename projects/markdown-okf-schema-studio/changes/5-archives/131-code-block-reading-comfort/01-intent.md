# Code blocks: reading comfort (VS Code-grade highlighting, dark background, line numbers)

Type: feat · Priority: P1 · Asked 2026-10-27, scoped with the user (grill session)

## Intent (user)

Improve the visual rendering of documents like the one in the screenshot, starting with `<pre>` and
`<code>` (inline and block). It is already rather nice, but we can do better. The goal is reading
comfort.

![A technical report with code blocks in the cream theme](image.png)

- Multi-line blocks: show line numbers, with a setting to turn them on or off (no toolbar switch).
- Syntax highlighting is rather poor. Code blocks can stay on a dark grey background, with a setting
  "gray dark code background in cream and white theme".

## Decisions (user, 2026-10-27)

- **Highlighting**: replace highlight.js by **Shiki** (TextMate grammars, same tokens as the VS Code
  editor), theme **Dark+** in every preview theme.
  - **JavaScript regex engine, no WASM** (Restricted Mode and strict CSP keep working).
  - Bundle the common languages only (python, typescript, javascript, json, yaml, bash/shell, c, cpp,
    rust, go, java, sql, toml, diff, markdown, html, css, xml, ini, dockerfile, powershell, …).
    A language that is not bundled renders as plain text, never as an error.
  - Adding the `shiki` dependency is allowed by this CR.
- **Dark code background**: new boolean setting, **on by default**. Code blocks use the Dark+ dark
  background in the cream and white preview themes too. Inline code keeps its current look (out of
  scope).
- **Line numbers**: new boolean setting, **on by default**.
  - Only for blocks of 2 lines or more.
  - Never copied: neither the copy button nor a mouse selection picks them up.
  - MyST options win over the setting, block by block: `:linenos:`, `:lineno-start:`, and
    `:emphasize-lines:` (highlighted lines) on `{code-block}` / `{code}`.
- Settings live under the existing `markdownOkfSchemaStudio.preview.*` prefix, `scope: resource`,
  documented in `docs/user/settings.md` and the SwRS.

## Out of scope

- Inline code styling, a language label in the block header, wrap vs horizontal scroll for long lines.

## Proof

- Before/after screenshots in a real VS Code window, cream, white and dark preview themes, on a
  document like the screenshot (Python, YAML, shell blocks, one `{code-block}` with `:linenos:`,
  `:lineno-start:` and `:emphasize-lines:`).
- Tests: tokens coloured for each bundled language; unknown language falls back to text; line
  numbers absent from copied text (copy button and selection); settings on/off; MyST options win;
  WCAG AA contrast of code text and line numbers on the dark background; Restricted Mode renders.
- Report the VSIX size before and after.
