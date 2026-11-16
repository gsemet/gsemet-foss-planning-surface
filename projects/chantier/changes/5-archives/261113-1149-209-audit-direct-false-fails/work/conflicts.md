# Conflicts: CR-209 restack onto CR-208 head 2da9cf5

evals/SCORECARD.md, row C9: the base added "and `cancel` without `--epoch` is refused (exit 2)"; the CR changed "`status --refresh` on a wake" and the audit column (a direct batch's `status --refresh` with no epoch is the report refresh and passes). Kept the CR's row and carried in the base's cancel clause.

evals/kit/audit.py: merged automatically (CR-196's and this CR's edits do not overlap); no hunk to resolve.

Fast gate: `just check` passed (58 tests).
