# Feature session — state

Resume rule: read this file first, then `journal.md` (last entries), then act on the first
step whose status is not `done`. Update this file and append to `journal.md` after every step.

Repo: `~/Projects/DevTools/markdown-okf-schema-studio`, branch `dev/gsemet`, start commit `9df67aa`.
Landing format: each backlog item moves to `.agents/changes/archives/NNN-<name>/` (intent files +
`report.md`: status, delivered table with commits, proof of completion, open items); next number 007.
Commits: Conventional, scopes vscode/render/editor/frontmatter, `Assisted-by:` trailer, no
Co-Authored-By. Completion gate: `just preflight` (never `just dev`/`update`: they install).

Models: analysis Haiku (simple) / Sonnet (complex); task breakdown Opus high effort;
implementer Sonnet 5.5; reviewer Sonnet 5.5; strictly sequential, one commit per task.

## Steps

| # | Step | Status | Output |
| --- | --- | --- | --- |
| S1 | Haiku analyses, 5 groups (A margins/copy/settings, B block editing, C toolbar/TOC/TODO/diff, D palette, E autodetect/comments/test infra) | done | `analysis/A..E-haiku.md` |
| S2 | Sonnet deep analyses: D palette+toolbar, B block ops (move, image, multi-select, paste), E diff/comments/autodetect/TODO | done | `analysis/*-sonnet.md` |
| S3 | Questions to the user, answers recorded | done | `decisions.md` |
| S4 | Expected changes presented to the user | done | `CHANGES.md` |
| S5 | Opus (high) task breakdown by phase | done | `PLAN.md`, `tasks/Txx.md` |
| S6 | User approval of the plan (O1–O13, T26/T30) | done | `decisions.md` |
| S7 | Implementation, task by task (see PLAN.md task table) — current: T45 done r2 | running | commits, `reports/`, `reviews/` |
| S7b | Post-plan fixes P1–P10 (post-plan.md; order P5+P6, P4, P3, P1, P2+P7, P8, P11, P9-T1, PR (U33/U35 → pr/STATE.md), P10, P9 B5/T2/F) | in-progress | commits |
| S8 | Archive landing per feature + final verification | done (PR #11 merged 2026-10-22) | `archives/NNN-*/report.md` |

## Feature scope (backlog items)

copy-code-block, bug-one-line-top-margin-missing, vscode-setting-rework, move-block-up-down,
edit-inline-image, toolbar back/next/zoom/margin (P1), todo-comments, clever-margin-break,
toc-in-vscode-markdown-studio, paste-image-in-edit-mode, show-incoming-diff,
block-edition-palette (P1, phased), myst-autodetect (warnings), multibloc-selection,
local-comment-mode. Check only: rendering-difference-on-windows.

Orchestrator tools (persistent): `tools/track.py <Txx> <status> <round> <commit|-> "<text>"`,
`tools/gate.sh <name> "<levels B T S R F E>"` (log in `reports/<name>-gate.log`, refuses if a VS Code
test runs), `tools/commit.sh <Txx> <msgfile>` (explicit staging; README.md and CHANGELOG.md staged
hunk by hunk at -U0, leaving out the user's own edits). Shared rules: `implementer-rules.md`,
`reviewer-rules.md`.
