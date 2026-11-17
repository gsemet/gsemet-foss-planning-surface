# Find in the preview (Ctrl+F / Cmd+F)

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- Ctrl+F (Cmd+F) in the preview opens a find bar: match case, whole word, regular expression,
  next/previous (Enter, Shift+Enter, F3), match count, all matches highlighted, Escape closes.
- Matches in rendered text (tables, admonitions, folded sections unfold), not in hidden source.
- The find bar follows the theme and the keyboard rules of the toolbar (focus, Tab order).
- The shortcut must not break VS Code's own find when the text editor has focus.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
