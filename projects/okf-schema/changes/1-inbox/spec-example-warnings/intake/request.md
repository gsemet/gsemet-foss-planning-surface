# validate: W7 and W13 warn on the spec example; W12 message is broken

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

These are warnings (exit 0), not spec violations. Observed on the bundle of the spec's Appendix A:
- W7 "block-style lists" on every document, because the spec writes `sources:` as a block list. The
  docstring at `validator.py:691-692` says `sources` and `verified` are exempt; the code
  (`validator.py:711-718`) does not exempt them.
- W13 on `resource: dashboards/exec-revenue`, which Appendix A uses as a source.

Message bug: the W12 message prints a literal `'{ref_id}'` (`validator.py:550`, missing `f`
prefix). The same bug in the W10 message is fixed by CR `trust-actor-forms` (batch-01).
