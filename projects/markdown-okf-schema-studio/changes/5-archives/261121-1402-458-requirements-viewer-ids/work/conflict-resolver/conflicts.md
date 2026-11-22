# Conflicts: CR-458 rebased onto origin/main

- CHANGELOG.md, `## Unreleased`: kept both bullets. The CR-458 bullet (full IDs and ID search) first, then the CR-447 bullet from origin/main.
- requirements/tiers/log.md, `## 2026-11-21`: kept both. Added `### Requirements viewer full IDs and ID search (CR-458)` (its Added/Changed lines) above `### Copy, cut and paste on a list followed by blank lines (CR-447)` with its lines. Dropped the stale `### Real-window paste-url ... (CR-454)` heading, which came only from the rewritten former base and had no body in the CR commit.
- No BOM added (both files start with `# `). Rebase continued and finished.

Fast gate: `just check` -> exit 0 (only existing W2 broken cross-link warnings). `just requirements-update` -> 0 indexes, 0 projections updated, no diff. Log: work/conflict-resolver/check.log
