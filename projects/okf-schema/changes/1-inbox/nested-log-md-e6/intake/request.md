# validate: a nested log.md fails with E6, but OKF 0.2 allows it

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

OKF 0.2 section 9: "A `log.md` file MAY appear at any level of the hierarchy to record the history
of changes to that scope." Section 3.1 gives the reserved filenames their meaning at any level.

Observed: a `computations/log.md` added to the spec's Appendix A bundle gives
`ERROR [E6] Reserved file '...' is not at bundle root (log.md must be at bundle root)` and
`validate` fails (`validator.py:1019-1026`). `docs/source/reference/validation-codes.md:138-145`
states the rule as if it were OKF. `okf-schema-vs-spec.md` does not list it.

The check's suggested fix: drop E6, or downgrade it to a warning and list it as an okf-schema
restriction.
