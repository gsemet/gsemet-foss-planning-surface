# Report — frontmatter-diff-line

Status: **done** (2026-10-28, branch `change-requests/155-frontmatter-diff-line`,
PR [#169](https://github.com/gsemet/markdown-okf-schema-studio/pull/169), merge commit `55b5c371`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | One change bar per changed or added front matter field row; a removed field marks the whole properties table; new SwRS-MDOKFSTUDIO-REVIEW-215 (`proposed`); docs (settings, README, CHANGELOG) | `85942140` |

## Proof of completion

- Tests added: 12 unit tests (9 failed before, 3 cover cases that already worked), 2 visual
  scenarios `review-annotations/v27` (light) and `v28` (dark), both failed before.
- Local gate: `just check` green (3067 + 69 tests, 0 fail); `okfreq validate --check-links` exit 0.
- CI: normal run [40694048877](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40694048877) green.
  Heavy run [40691765772](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40691765772)
  (old head) stopped at the known `tableMoves` regression (fixed by #167).
- Screenshots: branch `change-requests/155-frontmatter-diff-line-assets` (commit `ebcfb949`),
  before/after light/dark.
- Rounds: 1/3 (coder r1, reviewer r1 APPROVE).

## Open items

- Reviewer's non-blocking notes →
  [02-backlog/P3/frontmatter-diff-bars-followups](../../2-backlog/P3/frontmatter-diff-bars-followups/01-intent.md).
