# Task

Specification: `03-change-spec.md` with `02-answers.md`. Single CR, not a stack: the driver pushes and
opens the PR. Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/273`,
branch `change-requests/273-frontmatter-this-field`, based on `origin/main`.

Start from: how the front matter is parsed and shown (`src/core/frontmatter/`, `frontmatterParse.ts`,
the properties table renderer), how inline code is rendered (`src/core/render`, the render passes of
`mystRenderer.ts`), how a front matter edit refreshes the page (`src/core/frontmatter/frontmatterChanges.ts`,
`src/core/edits/frontmatterEdit.ts`), the SwRS groups `frontmatter-editing`, `frontmatter-schema` and
`rendering-core`, and the writing skill with its rendering test.

Layering (constitution, section 2): the resolution belongs in `src/core` (pure). No new dependency.
No dependency-cruiser exception.

Tests first: render tests (string, number, boolean, list, object, missing key, no front matter,
`=this.x` without space, hostile value, inline code that only looks close), a refresh test, a visual
scenario (value and missing key, light and dark). The writing skill's example test covers the new example.

Gates: `just check`; the headless visual capture of the rendering and front matter groups (no real VS
Code window locally: CI runs the real-window tests); a heavy CI run on the branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`).
Before and after screenshots, light and dark, named in the report.
