# Spell check in edit mode, with a toolbar toggle and a language

Type: feat · Priority: P3 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../5-archives/136-parity-grill/work/decisions.md))

## Expected

- In edit mode only, the block editors (text boxes, table cells) are spell-checked.
- The floating toolbar gets a toggle (on/off) and a language choice; both are remembered (setting
  plus per-workspace view state). Read mode is never spell-checked.
- Check feasibility first: VS Code webviews may not expose Chromium's spell checker or let the
  language be chosen. If not, the CR records the finding and proposes the alternative (a bundled
  dictionary-based checker; a new dependency needs the user's approval) before building.
- A dedicated CR (user decision), not mixed with the editor rewrite.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
