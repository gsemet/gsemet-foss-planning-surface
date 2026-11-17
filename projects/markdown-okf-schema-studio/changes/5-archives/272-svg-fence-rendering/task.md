# Task

Specification: `03-change-spec.md` with `02-answers.md`. Single CR, not a stack: the driver pushes and
opens the PR. Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/272`,
branch `change-requests/272-svg-fence-rendering`, based on `origin/main`.

Start from: how the `mermaid` and `plantuml` fences are rendered and edited (`src/core/render`, the
diagram SwRS in `requirements/tiers/swrs/diagrams/`), the raw HTML allow-list (`SwRS-MDOKFSTUDIO-CORE-056`,
`GFM-031`, the HTML sanitizer in `src/core`), the theme tokens (`src/core/preview/themeTokens.ts`,
`src/core/preview/styles/pageChromeStyles.ts`), the width mode (`src/page/modules/widthMode.ts`), the CSP
(`src/core/security/csp.ts`), and the writing skill with its rendering test.

Layering (constitution, section 2): the sanitizer belongs in `src/core` (pure), no new dependency unless
the task truly needs one (then say so in the report: an agent adds a dependency only when the task allows
it; this task allows a well-known SVG/HTML sanitizer from npm only if the existing sanitizer cannot be
extended). No dependency-cruiser exception.

Tests first: sanitizer unit tests (each hostile case), render tests (fence, raw block, inline `<svg>`
dropped, variables defined per theme), a visual scenario (fence + raw block, light and dark). The writing
skill's example test covers the new examples.

Gates: `just check`; the headless visual capture of the diagrams and rendering groups (no real VS Code window
locally: a QA campaign holds them; CI runs the real-window tests); a heavy CI run on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
Before and after screenshots, light and dark, named in the report.
