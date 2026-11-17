# Fold and unfold sections in the preview

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- A chevron next to each heading (shown on hover and for the focused heading) folds the section
  until the next heading of the same or a higher level. Keyboard: a shortcut toggles the current
  section; "Fold all" / "Unfold all" in the toolbar or command palette.
- The fold state is a view state (per document, kept across reloads), never written to the file.
  Search (`find-in-preview`) and navigation to an anchor unfold the target.
- Works in read and edit mode; editing a block inside a folded section is impossible until unfolded.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.
