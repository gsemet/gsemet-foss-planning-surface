# Replace from the preview

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- The find bar (`find-in-preview`) gets a replace field: Replace, Replace all, `$1` groups with
  regex. Each replacement edits only the matched source span (lossless), Replace all is one undo
  step. Disabled (with the reason) in read-only previews.
- Matches whose rendered text does not map one-to-one to the source (inside a formula, a link
  target, generated text) are skipped and counted ("3 matches cannot be replaced from the preview").

Depends on `find-in-preview`.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
