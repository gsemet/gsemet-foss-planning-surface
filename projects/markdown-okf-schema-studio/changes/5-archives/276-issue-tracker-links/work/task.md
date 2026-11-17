# Task

Specification: `03-change-spec.md` with `02-answers.md`. Only the PR in this project: the spec's
Chantier part is now an issue (gsemet/chantier#101, already opened by the Chief of Staff); never
touch the Chantier repository. Single CR, not a stack: the driver pushes and opens the PR **as a
draft** (`gh pr create --draft`), and runs `gh pr ready <n>` only at `ready`.
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/276`, branch
`change-requests/276-issue-tracker-links`, based on `origin/main`.

Files (the spec's five, nothing else): `.agents/guidelines/change-requests-lifecycle.guidelines.md`,
`.agents/guidelines/pull-request.guidelines.md`, `.agents/guidelines/release-process.guidelines.md`,
`.github/PULL_REQUEST_TEMPLATE.md`, `AGENTS.md`. Process and guidelines text only: no `src/`,
`test/`, `requirements/` or workflow change, no requirements log entry.

Documents the owner reads: follow `owner-review.guidelines.md`. Commit: `docs:` per the commit
guidelines.

Gates: `just check`; `just preflight` (static stage is enough if the rest is unchanged by a docs
change: say which stages ran). No heavy CI run needed (text only). Blast radius 1: Inspector on
Sonnet is enough.
