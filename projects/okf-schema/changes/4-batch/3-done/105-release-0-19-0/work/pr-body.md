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

---

## New Features
- New `okf-schema trust --path BUNDLE CONCEPT_PATH` command: it prints the trust tier of a concept (`unverified`, `machine-confirmed` or `human-reviewed`) and `stale: true` once `stale_after` is reached, and writes no file. See the [trust command reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-trust).
- The Python API result of `show_bundle` now has `raw`, the exact stored text of the concept file. See the [show reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).

## Breaking Changes
- `okf-schema show` now prints the concept file byte for byte, in any encoding, with nothing added: comments, quoting and line endings are kept, and the `trust:` and `stale:` lines are gone. Scripts that read those lines must call `okf-schema trust` with the same `--path` and concept. See the [show reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).
- `okf-schema show` no longer parses the file: invalid YAML or a file that is not valid UTF-8 is printed with exit code 0. Use `okf-schema validate` to check a file.
- Validation now reports broken links in `index.md` and `log.md` as W2, so `validate --strict` can start failing; `okfkb validate` and `okfreq validate` report them too. Run `okf-schema index` or fix the links by hand. See [W2](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/validation-codes.md#w2-broken-cross-link).

## Bug Fixes
- `okf-schema show` finds a concept with or without `.md` or a leading `/`, from any terminal folder, and accepts an absolute path inside the bundle. See [how a concept name is read](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).
- `okf-schema show` and `show_bundle` refuse paths and symbolic links that leave the bundle, and a directory gives a plain error instead of a traceback.
- `okf-schema index` no longer copies into a parent index a link that only works from the subdirectory. Run it again to repair damaged summaries; summaries you wrote are kept. See the [index reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-index).
- A new subdirectory summary comes from the introduction of its `index.md`, never from a list entry or a heading, with its links adjusted for the parent index. An introduction already copied is not refreshed: delete the entry line and run `index` again.
- Valid links with an anchor or percent-encoding are no longer reported as broken or counted as broken by `stats`.
- The trust tier now counts every OKF 0.2 actor form: an agent such as `reference_agent/gemini-2.5-pro` reads as `machine-confirmed`. Any non-empty actor other than `human:<id>` counts as machine, including unrecognized ones. See [W10](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/validation-codes.md#w10-unrecognized-actor-string-in-verifiedby).
- W10 now warns only about actors in no recognized form, lists the accepted forms and names the faulty entry.

---

## Announcement thread (draft, to post yourself)

**1/3**

okf-schema 0.19.0 changes how you read a concept. `okf-schema show` now prints the file exactly as stored, comments, quoting and line endings included. The trust tier and staleness moved to a new command, `okf-schema trust`, so update any script that read them from `show`. And `okf-schema index` no longer writes broken links into subdirectory summaries.

**2/3**

Release notes: https://github.com/gsemet/okf-schema/releases/tag/v0.19.0

**3/3**

Install or update with `pip install -U okf-schema`, free under the MIT license: https://pypi.org/project/okf-schema/

🤖 Generated with [Claude Code](https://claude.com/claude-code)
