# Conflicts: CR-380 rebased on CR-379's branch (commit 924d0d71)

- types/index.d.ts, ChantierBatch: kept base's `spent_usd: number | null` and added CR-380's `spent_at?: string | null`.
- hooks/register.tsx, batch title line: kept base's noCr branch (title "none yet", "paused, no CR yet", "No CR yet." body) and added CR-380's `spentOld` (age, only when spent_usd is not null) at the end of the title.
- hooks/register.test.tsx: both tests kept (base's crs_total test, CR-380's spend-age test).
- views/batch.js: base's imports (noCrYet, steeringFactoryWord) plus `spentAge` import (base's rename of steeringWord kept).
- views/home-batch.js: imports as above; in the mini card kept base's `none`/`figure` logic and added `old = spentAge(...)` shown after the meter.
No two product intents in conflict.

Fast gate: `just check` run in the worktree: pass (mypy, biome, 760 pytest passed 1 skipped, release-notes ok).
Also: `just mod`: pass (86 pass, 0 fail). `just eval-dry-run`: pass (18 of 18 cases as expected).
Note: spend-age.js (web board) reads `cost_at`, the hooks pane reads `spent_at` (STATUS.json); both fields exist in the base, left as they were.
