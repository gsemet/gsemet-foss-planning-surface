## Summary

Release 0.19.0 publishes the changes merged since 0.18.1: `okf-schema show` prints concept files as stored, a new `okf-schema trust` command, and fixes to concept lookup, index summaries and the trust tier.

This pull request changes only the version (`pyproject.toml`, `uv.lock`) and `CHANGELOG.md`.

- The version is the one `just bump-version` computes from the commit history: a `feat:` commit gives a minor bump.
- The release notes list breaking changes in behaviour (`show` output, new W2 warnings). No commit carries `!` or a `BREAKING CHANGE:` footer. With that marker, the project's versioning rule would give a major version instead. The choice is the maintainer's.
- The new changelog entry sits under "Unreleased", as in earlier version pull requests.

## After the merge

- Main-branch CI tags `v0.19.0` and starts **Release**. Publication to PyPI needs no further approval.
- Release note generation with Copilot is not available (no credit), so that run is expected to fail after attempting PyPI publication, without creating the GitHub release.
- The notes below, written by hand and validated, are then supplied to **Release** through `release_notes`, once the maintainer approves that dispatch.

## Validation

- `just preflight` at `60d07fa`: pass (1269 passed, 12 skipped, coverage 95.72%, documentation built). Run on Windows with Python 3.13.
- `uv run python scripts/release_notes.py --validate` on the notes below: pass.

## Known gaps

- The docstrings of `show` and `show_bundle` date the concept lookup change to 0.18.2. It ships in 0.19.0.
- No picture for the announcement thread: the changes are command output, and no capture was made.
