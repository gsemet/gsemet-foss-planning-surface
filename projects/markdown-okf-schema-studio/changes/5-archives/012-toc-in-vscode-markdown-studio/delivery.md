# Report — toc-in-vscode-markdown-studio

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T12 | Table of contents in a right column below the toolbar: toolbar toggle, off by default, remembered per workspace; h1–h4 (including included files, excluding the properties table, admonitions and the sticky band); click scrolls to the heading; hidden on narrow panes | `ba11c89` |
| T13 | Each entry with sub-entries folds and unfolds (twisty, keyboard); the current section is highlighted (or its folded parent) and kept in view in the TOC; the open state survives a webview reload; a click right after a content refresh targets the live heading | `9afb00f` |

## Proof of completion

- T12: unit tests for the TOC builder, toggle and exclusions, visual fixture 30-toc; review APPROVE.
- T13: ten new unit/visual tests failed before the change (fold kept across rebuild, current entry
  follows scroll, folded parent highlighted, fractional heading top); review APPROVE in round 2.
- Phase 2 e2e (2026-10-16, `9afb00f`, clean tree): unit 863, contract 2, security 23; visual 151
  checks / 146 images; integration scroll, untrusted, trusted (incl. realInput, checkboxToggle),
  standalone and reload suites green, 0 failures.

## Open items

- The visual contrast check covers light and dark, not cream (the highlight tint is theme-relative).
- Fold keys of removed headings are never pruned (per panel, not persisted across restarts).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
