# Conflicts, CR-305 rebase onto CR-304

Commit ad35ccf (selector shows the surface):
- web/js/i18n/en.js and fr.js: base added nav.config, nav.prs (en), nav.overview; the CR removed
  nothing there. Kept the base's nav lines; kept the CR's project.folder/project.repo and its
  removal of project.all/project.all_sub (no use left in web/).

Commit f3af2c0 (picker count wraps):
- scripts/docs_screenshots.py: base added the clone/chantier.yaml block after the one-line `git`
  tuple; the CR reformatted the tuple one item per line. Kept both: multi-line tuple, then the
  clone block.

No BOM added. Rebase completed; nothing pushed.

Fast gate: `just check` (ruff format/check, mypy, uv lock --check, biome, pytest 367 passed,
release-notes check): pass.
