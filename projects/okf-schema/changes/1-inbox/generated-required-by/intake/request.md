# validate: generated requires at but never checks the required by

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

OKF 0.2 section 5.2: "`generated.by`: REQUIRED within `generated`." `generated.at` is not marked
required, and section 11 says consumers must not reject a bundle for missing optional fields.

Observed (`validator.py:471-477`):
- `generated: { by: human:me }` gives `ERROR [E7] ... 'generated' block but 'at' field is missing`,
  exit 1.
- `generated: { at: ... }` with no `by` gives no finding.
- `src/okf_schema/data/kb/_schema/Base.schema.yaml:26` has the same inversion (`required: [at]`).

Related: the actor form of `generated.by` and of `sources[].author` is not checked. CR
`trust-actor-forms` (batch-01) leaves both out of scope on purpose.

The check's suggested fix: E7 for a missing `by`; a missing `at` becomes a warning (W3 already
covers it).
