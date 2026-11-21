# Conflicts, rebase of CR-448 onto origin/main a106fa7

- CHANGELOG.md (Unreleased): kept both entries, CR-458's first (from main), then CR-448's, before the CR-447 entry.
- requirements/tiers/log.md (2026-11-21): kept both sections, CR-458 then CR-448, blank line between.

No byte-order mark in either file. New head: c01f2cade9b97f86b02443d16a7c8f907b99c855.

Fast gate: the project's rules name none; ran `just requirements-lint` in the worktree: passed (use case diagrams: 94 StRS checked, all parse).
