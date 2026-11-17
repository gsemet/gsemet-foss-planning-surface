# Report — 209-grid-card-title-editor-wrong-line

Status: **done locally** (2026-10-31, branch change-requests/209-grid-card-title-editor-wrong-line,
commit 1d1c2da8 on a0ee07e4; not pushed, no PR — separate PR on main, Foreman rebases and opens it).

## Delivered
- `src/core/render/mystGridToctree.ts`: card titles and `:header:`/`:footer:` options parsed inline
  only (leading "2." literal), snippet positions stripped, title part mapped data-line/data-end-line
  to the directive line (skipped with `:link:`), options to their own line. Grid and standalone cards.
- Tests: `test/core/render/gridCardTitleSourceLine.test.ts` 7 tests (6 fail on unchanged code, the
  link-card guard passes both); `alertSourceLines.test.ts` one expected tuple added (intended change);
  visual v25/v26 assert the editor holds "2. Status projection".
- Requirements: new SwRS-MDOKFSTUDIO-BLOCK-258 (proposed); MYST-100 option row; StRS-BLOCK-001
  generated lines (not locked); BLOCK-257 unchanged.

## Gates
just check exit 0 (unit 3288/0, contracts 71/0); okfreq validate 1071 reqs, 0 errors, 21 pre-existing
link warnings; visual 12 grid/card scenarios pass (v23–v26, myst v22–v24, v41–v45).

## Reviews
Inspector r1 CHANGES REQUESTED (W002 on BLOCK-257 from `<title>` placeholders, markers, tests,
one-behaviour split) -> r2 APPROVE. See reviews/T1-r1.md, reviews/T1-r2.md.

## Proof
/private/tmp/claude-502/cr209-driver/shots/{before,after}-title-{cream,dark}.png (before: editor in
card 2 holds "# Grid card editing", Line 1; after: ":::{grid-item-card} 2. Status projection", Line 8).

## Follow-ups
- Backlog: a grid/card inside a blockquote maps every line one too early (pre-existing).
- BLOCK-258 nominal scenario says "Done replaces line 8 only"; no end-to-end test of Done in this change.
