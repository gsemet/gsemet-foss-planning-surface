**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Change

`chantier open` and `chantier order add --note` take a plain path to a prepared CR folder or
specification. The `@` prefix is gone from these two commands, with no transition: a path
starting with `@` is a path that does not exist, and the error names it. PowerShell reads a
leading `@` as splatting, so the old form could not be passed unquoted there.

`chantier file` keeps `@<file>`.

The CLI's help and errors, `chief-of-staff.md`, the eval runbooks, the scenario and the tests
use the new form. `README.md` and `CONTRIBUTING.md` had no such use. `evals/results/` stays as it is.

## Checks

- `just check`
- `just scenario`, through `chantier gate`
