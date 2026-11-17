# Task

Specification: `03-change-spec.md` with `02-answers.md`. Part of a stack of six CRs, bottom to
top: 278, 279, 277, 280, 282, 281. This CR is based on `change-requests/282-table-cell-editor-clamp-to-pane`; the stack driver orders, restacks
and ships. The PR opens **as a draft** (`gh pr create --draft`) and turns ready on its own
(`gh pr ready <n>`) as soon as it is mergeable itself: CI green at its head, review approved
(owner's rule: each PR of a stack turns ready on its own).
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/281`, branch `change-requests/281-frontmatter-click-lost-below-open-editor`.

Starting test: the QA 271 replay(s) and fixtures the spec names, taken from local branch
`qa/271-table-campaign-replays` (87307e8f) with `git checkout 87307e8f -- <paths>`; never push
that branch. New SwRS IDs: re-check the next free number against the CRs below in the stack.

Layering (constitution, section 2). No new dependency. Inspector: Sonnet (blast radius 1).

Tests first (see the spec). Gates as listed in the spec: `just check`; headless visual of the
group(s); no real VS Code window locally (CI runs them); a heavy CI run on the branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`). Before and after screenshots if the page
changes visibly.
