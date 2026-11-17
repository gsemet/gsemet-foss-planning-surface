# Gate requirement markers: a source marker on every SwRS, markers on the code and test they name

From the requirements gardening audit, CR requirements-gardening (projects/markdown-okf-schema-studio/changes, evidence/audit-synthesis.md), systemic findings 1 and 8.

- Fail the static checks when an in-force, non-exempt SwRS has no @implements_req marker (DIAG-128 went through: its code at src exportSnapshot.ts:84 carries TOOLBAR-137). Fix DIAG-128 in the same CR.
- Stop marker lists that point at no code or test: header blocks of many IDs (test/page/modules/editActions.test.ts:9-48, test/session okfFrontmatter.test.ts:29-43) and the companion file test/integration/realInput/markers.ts:4-65. Decide the rule (for example a cap of IDs per marker comment, or markers only in a test body or on a declaration) with the owner during the grill; existing offenders are moved by the restructure CRs, so the gate may start as a ratchet.
- Remove the stale @tests_req LAYOUT-021 at test/session/diagReq.viewState.requirements.test.ts:107.
