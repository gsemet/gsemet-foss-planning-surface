# Conflicts: CR-479 rebase on origin/main

## requirements/tiers/log.md (one hunk)

- HEAD side: "Every final save ends (CR-475)" entry. CR side: "Open Preview and Refresh Preview complete once the page shows the document (CR-479 heavy-red)" entry. Both under `## 2026-11-23`.
- Choice: keep both, unchanged text. The file lists newest first (CR-475 above CR-474 above CR-473), so CR-479 goes first, then CR-475. No BOM (file starts "# U" as before).

Rebase continued; resulting subject: `fix(render): finish Open Preview once the page shows the document` (no "# "; body and Assisted-by trailer kept).

## Gates

- `just requirements-lint`: pass.
- Fast gate `just check`: FAILS at check-limits: `test/integration/previewEditing.test.ts: 1503 lines, over the 1500-line limit of test/; split it`. origin/main has this file at exactly 1500 lines; the CR adds 3 lines. Not a rebase conflict: the CR must trim or move 3 lines (or split the file). Later steps of `just check` did not run. Raw log: work/conflict-resolver/check.log.
