# 244 — Pick an admonition's type from a list above it

Type: feat · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-244`, branch `change-requests/244-admonition-type-picker`.
Part of the stacked run of 2026-11-03 (afternoon), before release 1.3.0.

## Intent

See [01-intent.md](../01-intent.md)

## Owner decisions (2026-11-03)

- When the caret is on the type of an admonition (GFM alert `> [!NOTE]` and MyST `:::{note}`), a list of types with their icons shows above it; a pick replaces the type only. GFM shows the five GFM types; MyST shows the list of CR 243.
- Keyboard: arrows move, Enter picks, Escape closes.
- 2026-11-03 (later): light and dark screenshots of the type picker (GFM and MyST) in the PR body, from a simulated visual scenario.
