# Dropping a file from the VS Code Explorer inserts a link

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../5-archives/136-parity-grill/work/decisions.md))

## Expected

- Dropping a `.md` file from the Explorer onto the preview in edit mode inserts a link at the drop
  point: `[[name]]` when wiki links are active in the Extended mode, else
  `[Title](relative%20path.md)` (relative to the document, title from its first heading or name).
- Dropping an image inserts `![alt](relative/path.png)` (check the existing image drop first).
- A drop marker shows where the link lands, like the block move marker.

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.

## Why parked (2026-10-28)

See [00-request.md](intake/request.md#why-parked-2026-10-28).
