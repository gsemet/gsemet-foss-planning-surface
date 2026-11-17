# Change specification: a Main path may cite an SwRS the StRS depends on

Origin: CR requirements-gardening, owner answer garden-Q3 (2026-11-17); `02-answers.md` here.

## Goal

Shared rules (for example LIFE-169/170, BLOCK-041/058) are cited by many StRS. Today a StRS that cites one in its `### Main paths` must also derive it, so the rule shows as a child of up to 10 StRS. After this CR a StRS may cite in its Main paths an SwRS it lists in its own `depends_on`, so the six req-garden CRs can move shared rules to `depends_on`.

## What changes (repository markdown-okf-schema-studio)

1. `scripts/check_main_paths.py`: a cited SwRS is valid when it exists, is active (`draft`, `proposed`, `approved`) and either derives from the citing StRS (as today) or is listed in that StRS's `depends_on`. The error message names both ways. The module docstring says the same.
2. `requirements/guidelines/project.guidelines.md`, "Main paths of a StRS": the bullet "Every cited SwRS ... has that StRS in its `derives_from`" becomes "... has that StRS in its `derives_from`, or is listed in that StRS's `depends_on` (a shared rule the use case relies on)". One sentence says a shared rule is cited with `depends_on` rather than derived by every StRS that relies on it.
3. Tests of the checker (the existing test of `check_main_paths.py` if there is one; else a new unit test under `test/build/` or the project's Python tests, the Driver picks the place the project uses): a StRS citing an SwRS through `depends_on` passes; a StRS citing an active SwRS it neither derives nor depends on fails with the message; a `depends_on` SwRS that is superseded fails.
4. No requirement is moved in this CR: the six req-garden CRs do that. `okfreq` already accepts `depends_on` on a StRS (proved on a copy of the bundle by the req-garden-block-table specification: `okfreq validate` 0 errors, a "Depends on" group in the Links).
5. A dated entry in `requirements/tiers/log.md` only if the project's rules ask for one for a guideline change; `just requirements-lint` and `just preflight` pass.

## Out of scope

Moving any SwRS, the req-garden CRs' work, okfreq itself.

## Evidence

The checker's tests; `just requirements-lint` (its last line, unchanged count); `just preflight`.
