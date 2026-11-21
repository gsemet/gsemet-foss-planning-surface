# Conflicts, CR-444 rebase onto the CR-443 branch

- `requirements/tiers/log.md` (commit "feat(editor): show blank-line runs ..."): both sides added a dated
  entry under `## 2026-11-21`. Kept both: the CR-444 entry first (newest-first convention, highest CR
  number on top), then the CR-443, CR-441, CR-440 entries unchanged. No BOM added; markers removed.
- No other conflict; the rebase ended with all 3 commits applied.

Fast gate: `just check` (run in the worktree), result: exit 0 (only existing okfreq W2 broken-cross-link
warnings). Raw log: `work/gate-check.log`.
