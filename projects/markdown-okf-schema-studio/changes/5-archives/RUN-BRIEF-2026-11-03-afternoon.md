# Foreman brief — run 2026-11-03 (afternoon): close every P1 and P2, then release 1.3.0

Written and kept current by the main session (`.claude/worktrees/angry-noether-edbfbb`). Read it
at every tick. The guideline in force is
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.claude/worktrees/angry-noether-edbfbb/.agents/guidelines/change-requests-lifecycle.guidelines.md`
(identical to `main` 6f8fd56d).

## Run settings

- Base: `origin/main` ac32bda4. Stack mode for every CR (guideline "Stacked PRs").
- Open-PR cap: 4, every PR of the stack counted.
- Live CR drivers: at most 4 at a time; start the next CR in the order below when one returns.
- Round limit: 3 per CR.
- Permissions: the foreman shares the main session's worktree, so it writes the files under
  `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/` through Bash
  scripts only, and nothing else of the main checkout.
- No agent merges, and no agent enables auto-merge. If a PR has auto-merge on, report it.
- Real VS Code window tests never run locally; CI runs them.
- Drivers start their coder and reviewer in the foreground, one at a time, never in the
  background (a driver that returns before its coder leaves the round orphaned).

## CRs (PRD folder `03-requests/NNN-<slug>`, worktree `../markdown-okf-schema-studio-wt-NNN`,
## branch `change-requests/NNN-<slug>`)

Start order for drivers, and stack order bottom to top:

| Order | CR | Slug | Priority | Note |
| --- | --- | --- | --- | --- |
| 1 | 251 | restricted-images-test-gaps | P2 | test only |
| 2 | 253 | atomic-save-test-flake | P2 | test only; may end with no change |
| 3 | 249 | myst-block-break-in-directive-crashes-render | P2 | crash fix |
| 4 | 247 | open-md-in-preview | P1 | |
| 5 | 250 | toc-rail-polish | P2 | |
| 6 | 252 | table-move-e2e-test | P2 | test only |
| 7 | 243 | bug-missing-slash-for-version-admonitions | P1 | adjacent to 244 (same files) |
| 8 | 244 | admonition-type-picker | P1 | |
| 9 | 245 | missing-columns-button | P1 | adjacent to 246 |
| 10 | 246 | myst-code-block-editor | P1 | |
| 11 | 242 | bug-margin-breaking | P1 | large, visual; screenshots |
| 12 | 248 | syntax-coverage-audit | P1 | start only after 243-246 are committed |

A CR that goes red or needs rework moves to the top of the stack (guideline ordering rule 5).

## Owner decisions

Each CR's decisions are in its `00-request.md`. Each CR adds one user-facing line to
`CHANGELOG.md` under `## Unreleased`, except the test-only CRs.

## After the run

When every CR is landed, report it. The main session prepares release 1.3.0; the foreman does
not touch the version or the changelog beyond the CRs' own lines.

## Owner decisions (2026-11-03, later)

- 245: the Grid form gets per-card header, footer and link now (one more round on 245, before 248).
- 247: a reload of the same document keeps edit mode; only another or a new document opens in preview.
- 243, 244, 245: a simulated visual scenario and light/dark screenshots in each PR body are required.
- 242: the minimum prose column width is 24ch (owner approved).
- 242: rounds: 5 (owner approved) for the red v26/v27 visual scenarios.
- 242: round 5 = fixture 63 input change only (owner approved), with before/after screenshots; follow-up P2 "breakout-scroll-handles-scenario" filed.
