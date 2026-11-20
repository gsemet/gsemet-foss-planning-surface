# Conflicts, CR-430

Rebase onto origin/main 145f1953: one conflicted file, `requirements/tiers/log.md`, one hunk
(2026-11-20 section). Choice: kept both entries, CR-429's (main) first, then CR-430's, before the
CR-350 entry; markers removed, a blank line between. No BOM (file starts `# U`).

`just requirements-update`: nothing changed (0 indexes, 0 projections); nothing to amend.

Fast gate: `just check` -> exit 0. Also `just requirements-lint` -> exit 0 (92 StRS, 578 SwRS
citations valid; 93 use case diagrams parse). Only W2 broken cross-link warnings on PALETTE-264 (pre-existing, not failures).
