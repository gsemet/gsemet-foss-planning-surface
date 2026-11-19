# The eval audit's J1 accepts the QA driver's first line

Intent: the eval audit (`evals/kit/audit.py`) recognises a QA driver started with its own first
line (`chantier qa-driver for <folder> of batch <batch>, in the project <root>.`) and audits it as
the Driver it is, instead of failing J1 as it did the Chief of Staff's subagents before
eval-audit-no-false-fails, as `intake/request.md` says. No run has shown the FAIL yet: the fix is
proved by a dry-run case. Filed 2026-11-15 by the Chief of Staff, sorted later (not for the
release of that week); specified 2026-11-18.
