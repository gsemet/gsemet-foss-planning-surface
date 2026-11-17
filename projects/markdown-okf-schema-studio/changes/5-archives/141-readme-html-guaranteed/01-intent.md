# README-style HTML renders and stays editable, like on GitHub

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- The HTML GitHub renders in READMEs works in the preview: `<div align="center">` (and `<p
  align>`), `<br>`, `<img src width height alt>`, `<a><img></a>` logos and badge rows, `<picture>`
  with `<source media="(prefers-color-scheme: dark)">`, `<details><summary>`, `<kbd>`, `<sub>`,
  `<sup>`. Markdown inside an HTML block after a blank line is rendered (GitHub behaviour).
- **Read (preview) mode** shows the final rendering, exactly like GitHub: the centred `div`, the
  logo at its size, the badge row.
- **Edit mode** shows each HTML element as an admonition-like block, the way XML comments and TODO
  comments are shown today, with the **literal opening tag as its title** (for example
  `<div align="center">`) and its content inside; a click edits the raw source. See
  [edit-mode-tag-in-block-title](../edit-mode-tag-in-block-title/01-intent.md) for the shared title rule.
- The rendering follows the theme.
- Test fixture (from the user):

  ````md
  <div align="center">

  <img src="app-icon.svg" alt="App" width="96" height="96">

  # Title

  </div>
  ````

- The sanitizer rules stay strict (no script, no event handlers); this is about what GitHub keeps.
- Proof: real-window screenshots of a README with a centred logo, a badge row and a centred
  title, compared with GitHub's rendering of the same file.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.

User precision (2026-10-27): "en mode preview on voit les div centrés etc. avec le rendu final, et en mode
édition on voit les balises HTML comme des admonitions (on fait déjà ça sur les commentaires XML et TODO)".
