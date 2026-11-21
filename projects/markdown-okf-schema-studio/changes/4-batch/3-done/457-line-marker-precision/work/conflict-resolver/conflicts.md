# Conflicts

- requirements/tiers/log.md (one hunk, `## 2026-11-21`): HEAD added "Impossible comment date refused (CR-459)", the CR added "Line marker precision (CR-457)". Kept both; CR-457 placed first (newest first, as CR-459 sits above CR-456). No BOM, LF kept.
- Rebase continued, message unchanged. New head: 3778f00a (parent b9aa1822 on eb3b6ecc).
- range-diff 7517dfd1..52cca97f vs origin/main..HEAD: commit 1 unchanged (=), commit 2 differs only by 2 lines in log.md.
- `just requirements-update` not run: coverage files do not differ (`okfreq update-coverage --check`: 0 files would change).
- Fast gate: `just check` run at 3778f00a, exit 0 (only W2 broken-cross-link warnings in requirements, no failure).
