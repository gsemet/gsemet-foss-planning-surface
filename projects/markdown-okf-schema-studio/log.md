## 2026-11-09

- Bundle created; schemas shared from `_schemas/`.
- Filed from GitHub: #334 frontmatter-keys-in-body, #335 tab-clears-new-row-first-cell.

## 2026-11-17

- Change requests moved here from the project's `.agents/changes/`, as they were; not yet in
  chantier 0.11's layout (68 intents nested in archive sub-folders, no `summary.json`, links to the
  old stage names).
- The surface's `_schemas/` removed: chantier owns the format; `just validate` places CRs and runs
  `chantier summary lint`.
- Migrated to chantier 0.11's CR layout: the request in `intake/`, the run's files in `work/`,
  images in `evidence/`, studies in `experiments/`, an archive's report as its `delivery.md`;
  follow-up intents nested in archives renamed `intent.md`; links rewritten to the new places and
  stage names (906). 56 active CRs got their `summary.json`; #334 and #335 carry their `issue:`
  line.
