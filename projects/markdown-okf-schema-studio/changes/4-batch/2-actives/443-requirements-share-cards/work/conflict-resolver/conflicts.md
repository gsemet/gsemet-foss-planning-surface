# Conflicts: CR-443 rebase onto CR-442 branch (7ad44734)

- `requirements/tiers/log.md` (2026-11-21 section): both sides added entries. Kept both; the CR-443 entry goes first (newest), then CR-441, CR-440, CR-439 unchanged.
- `test/site/requirementsViewer/pages.ts` (imports): base added `pathColour` to the layout import, CR-443 added `plainText, shareDescription` to the socialCard import. Kept both.

No BOM added (files start as before). Rebase finished successfully; nothing pushed.

Fast gate: `just check` in the worktree: exit 0 (only existing W2 broken-cross-link warnings in requirements; checks, diagrams and main paths pass).
