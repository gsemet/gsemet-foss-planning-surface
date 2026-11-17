# Task

Specification: `03-change-spec.md` with `02-answers.md`. Single CR, outside the P2 stack: the
driver pushes and opens the PR **as a draft** (`gh pr create --draft`), and runs `gh pr ready <n>`
only at `ready`. PR body from `.github/PULL_REQUEST_TEMPLATE.md` per `pull-request.guidelines.md`.
No GitHub issue: no `Fixes`, no issue comment. Never touch the Chantier repository.
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/284`, branch
`change-requests/284-verifier-step`, based on `origin/main`.

Files: `.agents/guidelines/change-requests-lifecycle.guidelines.md` and
`.agents/guidelines/pull-request.guidelines.md` (and `AGENTS.md` only if the spec says so). Process
text only: no `src/`, `test/`, `requirements/` or workflow change, no requirements log entry.

Documents the owner reads: follow `owner-review.guidelines.md`. Commit: `docs:` per the commit
guidelines.

Gates: `just check`; `just preflight` (static stage is enough for a text change: say which stages
ran). No heavy CI run (text only). Blast radius 1: Inspector on Sonnet.
