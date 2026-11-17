# Pasting a URL makes a link, an image URL an image

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- In a block editor, pasting a URL over selected text gives `[text](url)`; pasting a URL alone
  gives `<url>` or a bare autolink (GFM); an image URL (`.png`, `.jpg`, `.gif`, `.svg`, `.webp`)
  gives `![](url)`. Ctrl+Shift+V pastes the raw text.
- Check first what already exists (rich paste, image paste) and keep it; record the before state.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
