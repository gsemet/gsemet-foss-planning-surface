# 122 — Strict requirement schemas with supersession and related links

Type: chore · Priority: P1 · From: user request (no backlog item)

## Intent (user)

"j'ai release une nouvelle version de okf-schema, qui supporte les superseded_by etc, donc normalement tu peux retirer les additionalProperties de requirements/tiers/_schema/base.schema.yaml" — then "met le dans le stack de cette nuit". Goal: requirement schemas reject unknown frontmatter keys.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Requires okf-schema 0.15.0 on PyPI (`okfreq supersede`, `superseded_by` list, generated `supersedes`, `relates_to`). If `pip index versions okf-schema` / PyPI JSON does not show 0.15.0 yet, the driver sets `status: blocked` with question "publish okf-schema 0.15.0" and does nothing else.
- Recipe verified by the main session on a copy with okf-schema main (validate, lint --check --check-links, update-coverage --check all green, 1013 requirements, 0 errors): bump `okf-schema>=0.15.0` in pyproject.toml + uv.lock; in `requirements/tiers/_schema/base.schema.yaml` add the `superseded_by`, `supersedes`, `relates_to` blocks copied from okf-schema's `examples/okfreq-examples/requirements/tiers/_schema/base.schema.yaml` and drop `additionalProperties: true`; add top-level `unevaluatedProperties: false` to `strs.schema.yaml` and `swrs.schema.yaml` (additionalProperties: false in the base would reject tier fields under allOf); convert every scalar `superseded_by: X` to `[X]` (508 files); remove `annotation_exemption` / `exemption_reason` from StRS files (53, they are SwRS-only fields); add `supersedes` to `generated_fields` in `requirements/config.yml` if listed explicitly; run `okfreq update-coverage requirements` (about 262 files get `supersedes`).
- Mechanical change: a script in the report, not hand edits. No product code change. Requirements guideline updated if it documents the scalar form.
- Placed on top of the stack: it touches hundreds of requirement files, so it rebases last.

## Unblocked (2026-10-28)

- The user published okf-schema 0.16.0 on PyPI (supersedes the 0.15.0 prerequisite). Use
  `okf-schema>=0.16.0`. Re-verify the recipe against 0.16.0 (its example base schema may have
  moved since 0.15.0) before the mechanical change. Relaunched from origin/main, in parallel,
  not stacked; not part of the 1.0.0 scope.
