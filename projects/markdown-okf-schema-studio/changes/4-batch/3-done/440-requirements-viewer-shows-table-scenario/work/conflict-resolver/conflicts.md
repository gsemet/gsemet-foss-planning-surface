# Conflicts, CR-440 rebase onto CR-439 branch

One conflicted file: `requirements/tiers/log.md`, section `## 2026-11-21`. Both sides added an entry.

- Hunk: CR-439 entry (HEAD side) versus CR-440 entry (CR side). Choice: keep both entries whole, CR-440 (newer) first, then CR-439, one blank line between, matching the file's newest-first order. No text changed. No BOM (file still starts `# U`), no conflict markers left.
- Staged `requirements/tiers/log.md`, `rebase --continue` succeeded; branch is 5 ahead, 1 behind its origin (not pushed).

Fast gate: `just check` (in the worktree), exit 0, passed (requirements indexes, coverage, main paths and diagrams checks clean). Log: `check.log` in this folder.
