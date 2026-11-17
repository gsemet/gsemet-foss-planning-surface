# Per-block side-by-side diff with the last commit

Type: feat · Priority: P1 · Filed 2026-10-27 from the parity grill with the user ([decisions](../../../4-archives/136-parity-grill/decisions.md))

## Expected

- Default unchanged: the green bar on the left of each block changed since the last commit.
- A new toggle in the floating toolbar turns each changed block into a small **side-by-side diff**:
  the block as in HEAD on the left, as now on the right, both rendered, with added and removed
  words marked. Unchanged blocks stay as they are, so the page shows several small diffs.
- Added blocks show an empty left side; deleted blocks reappear with an empty right side.
- Mode: the user's answer was cut after "que en mode …"; assumption to confirm in the grill of the
  CR: read mode only (the toggle is disabled in edit mode).

Proof: unit tests of the parser/renderer, a webview or e2e test of the interaction, and before/after real-window screenshots (cream + one dark theme). The source file is never rewritten outside the edited span.

## Why parked (2026-10-28)

See [00-request.md](00-request.md#why-parked-2026-10-28).
