Audit the move of chantier's planning to the planning surface (read-only)

The user (2026-11-13): "we will organise together the move to the planning surface
https://github.com/gsemet/gsemet-foss-planning-surface. First, look without changing it at everything
that might not work. A dedicated CR, done AFTER the rework (CR-221) and the backend with sync
(CR-222, CR-227)."

The surface is in the environment: C:/Users/gaeta/Projets/gsemet-foss-planning-surface.

Scope: read-only. List every gap between what chantier writes and what the surface expects, and say
for each who changes (chantier or the surface) and how. A first look already shows some:
- the surface's AGENTS.md makes every `projects/<name>/` an OKF bundle, checked by `just validate`
  (okf-schema against `_schemas/`): a frontmatter `type` and `description` in every Markdown file, an
  `index.md` in every folder, UTF-8 without BOM, `log.md` at the bundle root only; chantier writes
  plain Markdown (STATUS.md, 03-change-spec.md, retro.md, work/ files) with no frontmatter;
- stage folders differ: the surface uses `3-stash` and `4-batches/1-pending|2-actives|3-done`;
  chantier uses `3-ready` and `4-batch/`;
- a CR folder is `<issue>-<slug>` with `intake/` holding the tracker's raw JSON, and `01-intent.md`
  is `type: cr-intent` with OKF 0.2 provenance;
- `scripts/ai-autosync-git.py` and `.agents/autosync.toml` are to be replaced by chantier commands
  (CR-227), and the surface's autosync guidelines rewritten for them;
- `projects/chantier/` already holds a `changes/` tree and a `checkout.yml`: compare with
  chantier's external-surface mode.

Done: a written gap list in the CR, each gap with its owner and fix, and the follow-up CRs filed.
Nothing in the surface changes in this CR.