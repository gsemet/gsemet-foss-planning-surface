# T1 — 046-light-animations

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-046 (branch `feat/light-animations` from origin/main; rebase on the latest origin/main before starting).
Work ONLY there. Read `00-request.md` (decisions = the spec), the other files of this folder, and
`rules.md`.

## Tests (write first; they must fail on the unchanged code where that applies)

Unit tests next to their neighbours; visual scenarios in test/visual/scenarios.ts (group,
description, locks, assertions, next free id per group) and/or real-window scenarios when the
behaviour needs a real editor.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`; real-window under the lock
(rules.md) when the CR needs it.

## Report

/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/046-light-animations/reports/T1-r<round>.md
