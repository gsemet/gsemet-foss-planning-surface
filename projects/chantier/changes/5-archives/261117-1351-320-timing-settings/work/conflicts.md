# Conflicts: rebase of CR-320 onto cr-319 (9bb941f)

1. skills/chantier/references/concepts.md (escalation table, "A CR blocked twice" row): base added
   "a Driver stopped from outside never counts either"; CR changed "its one re-run" to "its re-runs".
   Choice: base row kept whole, with "after its re-runs" taken from the CR.
2. skills/chantier/scripts/cli/src/chantier/board/web/css/tokens.css: base replaced the colour block
   (--blue, --green, ... --teal) with --chip-2, --pill, --band, --caption, etc.; the CR had added
   `--teal`. Choice: base block kept; `--teal` dropped. Follow-up: the CR's css/views/config-timing.css
   used `var(--teal)` (same value as base's `--accent`, #1d5c63), changed to `var(--accent)`.

Rebase finished (new commit 17b1c6b, message kept). No BOM added (files start as before).

Gate: `just check` -> pass (ruff, mypy, uv lock, biome, 410 pytest passed, release notes ok).
