# Stack CI: the merge-commit check accepts the forge's chained test merge

Make `check-no-merge-commits` pass on a pull request above the bottom of a GitHub native stack,
whose checked-out test merge is a chain of forge merges, and keep it failing for every merge commit
a branch really carries.

Why: any new CI run of such a pull request is red, so the batch's stack cannot be completed.

In scope: `scripts/check-no-merge-commits.sh` (and the `justfile` line that passes it the base, if
the diagnosis needs it), its tests, the guideline or requirement text the project asks for.

Out of scope: any other CI job, disabling or loosening the check, the stack's other changes.
