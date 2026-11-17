# Task T1 — Fix the writing skill wording

Worktree `../markdown-okf-schema-studio-wt-158`, branch `change-requests/158-writing-skill-okf-definitions`.
Edit SKILL.md only (plus the test if a name assertion must follow, without weakening it). Keep
CORE-073 (proposed) anchored; `just requirements-update`; dated `tiers/log.md` entry if the
requirement text changes. Find installed copies (`find ~ -maxdepth 7 -path '*skills/writing-for-markdown-okf-schema-studio/SKILL.md' -not -path '*/markdown-okf-schema-studio*'`) and any install
recipe in the justfile/docs; refresh copies or report where none exist. Gates: `just check`; normal
CI; heavy CI dispatched.
