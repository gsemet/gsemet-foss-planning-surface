## Summary

After a version PR merges, `just tag` is run from the main checkout, which may still be on the previous version. `check-tag` reads the local version, so it refused and the release had to be tagged from the release worktree. `just tag` now fast-forwards the main checkout to `origin/main` first, never by force, and stops with a line saying what to do when it cannot.

## Deliverables

The `tag` recipe, before and after:

```text
before                                  after
git fetch origin main                   uv run --script scripts/version.py ff-main
uv run ... check-tag                    uv run ... check-tag
git tag ... origin/main                 git tag ... origin/main
git push origin ...                     git push origin ...
```

`ff-main` refuses, changing nothing, when the checkout is not on `main`, has tracked changes, the fetch fails, or main cannot fast-forward. Otherwise it prints `main checkout: fast-forwarded to <sha7>` (or `already at <sha7>`), adding `; uv.lock changed: sync pending` when the lock file changed.

The release procedure's main-checkout step stays out of the Release driver's hands: it hands `just tag` to the steering session, which runs it and takes the release back with a `tag done:` note.

## Blast radius

Grade: 1. Release tooling and cards only. Revert restores the previous recipe.

## Autonomous decisions

- The new tests live in a new file, `test_release_tag.py`, because the existing test file had no room under the repository's size limit.

## Known gaps

- `just tag` itself is not run in CI, because it pushes a tag; the steering session's hand-off is first proved at the next release.

<details>
<summary>Details</summary>

## Changes

- `scripts/version.py`: `ff_main` and the `ff-main` subcommand (`git merge --ff-only --no-overwrite-ignore origin/main`).
- `justfile`: the `tag` recipe starts with `ff-main`.
- `CONTRIBUTING.md`: Release step 4 describes the fast-forward and its refusals.
- `skills/chantier/references/driver.md`, `foreman.md`, `chief-of-staff.md`: the Release driver hands the main-checkout step to the steering session; take-back and refusal routes.
- `skills/chantier/scripts/cli/tests/test_release_tag.py`: `ff_main` cases, the recipe's order, the card phrases.

## Impacts

No visual change. Maintainers run `just tag` from a main checkout that is behind.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_release_tag.py`
- [x] Local gates at `9ff16d5`: `just check` pass (911 passed, 1 skipped), carried over the clean restack (patch unchanged)
- [x] Evidence: none, no visible change
- [x] Review: approved at `9ff16d5` (carried over the clean restack, patch unchanged; before that from `8311949`: rebase onto a new base, the second commit approved in round 3)
- [x] Verified at `9ff16d5` (carried over the clean restack)
- [x] CI green at `9ff16d5`

## Internal references

- CR-396 just-tag-fast-forwards-the-main-checkout

</details>
