# UX-22 — `project-relative` links resolve from the Git root, so nested bundles show only errors

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (fixed by setting `projectRoot`) |
| Area | `x-okf-link` resolution |
| Evidence | [r3-swrs.jpg](../../evidence/r3-swrs.jpg) (red `[E10]`), [r3-projectroot.jpg](../../evidence/r3-projectroot.jpg) (after setting) |

## Use case

A team keeps several OKF bundles in one repository (here `okf/okfreq-examples/` next to other
knowledge bases). An author opens a requirement and expects its implementation and test links to
work.

## Observed

`implemented_in_files: [src/export.py]` and `tested_in_files: [tests/test_export.py]` are red with
`[E10] target 'src/export.py' does not resolve to a file`. The files exist under
`okf/okfreq-examples/src/` and `okf/okfreq-examples/tests/`, and the bundle's
`requirements/config.yml` declares `scopes.Core.source_dirs: [src]` and `test_dirs: [tests]`.
The extension resolves project-relative paths from the workspace Git root.

Setting `"markdownOkfSchemaStudio.frontmatter.projectRoot": "okf/okfreq-examples"` fixes it
(applied live, good), but the setting is a single value for the whole workspace, so two bundles
with different project roots cannot both work. The error message does not say which root was tried.

## Expected

The project root is derived per document: from the bundle's own configuration (`config.yml`, or an
`x-okf-*` hint in the schema directory), or at least from the nearest ancestor that contains the
schema directory's project markers, before falling back to the Git root.

## Suggested direction

Resolve roots per schema directory, cache them, and include the root in diagnostics:
"`src/export.py` not found under `okf/okfreq-examples/` (project root from config.yml)". Keep the
setting as an override, ideally as a glob → root map.

## Done when

The okfreq example renders without errors in a multi-bundle workspace with no settings.
