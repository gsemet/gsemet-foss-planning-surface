# Raw block and cell editor: show bold, italic and inline code styled, like Obsidian

Type: feat · Priority: P3 · Asked 2026-10-27

## Intent (user)

When I edit a block (or a table cell), the text is raw and I see the `**` of bold and the `*` / `_`
of italic. That is fine, but like Obsidian I would like the bold or italic text to be shown in bold
or italic inside this raw editor: it makes the raw block easier to read. Only bold and italic get
this mini-formatting.

Addition (user, 2026-10-27): inline code too (`` `CHUNK_SIZE` ``).

![A raw block editor with a **bold** sentence shown as plain text](evidence/image.png)

## Expected

- In the block editor and the table cell editor, text between `**…**` / `__…__` shows in bold and
  text between `*…*` / `_…_` in italic; `***…***` both; text between backticks (`` `…` ``,
  also with longer backtick runs) gets the preview's inline code look (monospace font, background). The markers stay visible and editable, as
  typed; the source text is never changed.
- Nothing else is styled (no headings, links, code blocks, other colours).
- Same rules as the Markdown renderer: no bold or italic inside inline code or code blocks, `snake_case`
  words and `2 * 3 * 4` are not italic, escaped `\*` is not a marker.
- Caret, selection, undo/redo, IME, paste, the VS Code shortcuts (CR 119) and keyboard editing
  (CR 120) behave exactly as today. Typing stays fluid on a long block.

## Technical note: study first (user, 2026-10-27)

Study how Obsidian does it before choosing; the text box is probably fully replaced. Obsidian's
editor is built on **CodeMirror 6**: a `contenteditable`-based editor whose Markdown syntax tree
(Lezer) drives *decorations* (marks styling ranges, widgets hiding markers in Live Preview). A plain
`<textarea>` cannot style part of its text.

Step 1 of the CR is a short study (written to `reports/study.md`) comparing, with a throw-away spike:

1. **CodeMirror 6** (`@codemirror/view`, `@codemirror/state`, `@codemirror/lang-markdown`) replacing
   the block and cell `<textarea>`: real styled ranges, no caret drift; cost: bundle size, a new
   editor API behind every existing feature (CR 119 shortcuts, CR 120 keyboard editing, slash
   palette, paste, autosave, Ctrl/Cmd+Enter, Esc, IME, undo history, tests that drive `textarea`).
2. **Mirror layer** behind a transparent-text `<textarea>`: small change, but bold widens glyphs
   and the caret drifts unless widths are kept.

The study states how Obsidian behaves (markers kept visible in Source mode, hidden away from the
caret in Live Preview; here they always stay visible), the bundle size delta, CSP / Restricted Mode
impact, and a recommendation. The main session validates the choice with the user before step 2
(implementation). Adding the CodeMirror 6 dependencies is allowed by this CR if chosen.

## Proof

- Before/after screenshots in a real VS Code window (cream and dark), on the user's example.
- Tests: styled ranges for bold, italic, both, inline code, bold markers inside inline code (none), `snake_case`, escapes; caret
  position after typing at the end of a long bold line matches the text; scroll stays in sync.

## Added 2026-10-27 (parity grill): multi-caret with Ctrl+D

The user wants **Ctrl+D (Cmd+D on macOS) for multiple carets in edit mode**, like VS Code: add a
caret at the next occurrence of the selection. A textarea cannot hold several carets, so this goes
with the CodeMirror 6 block editor studied by this item (user decision: merge it here).
