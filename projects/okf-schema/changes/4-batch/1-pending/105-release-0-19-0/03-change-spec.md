# Release 0.19.0

Publish `okf-schema` 0.19.0 with the changes merged on `main` since `v0.18.1`. This item
prepares the version pull request; the user merges it, and CI tags and publishes.

## Goal

The user's words: "J'ai mergé. Fait une release".

After this item:

- `okf-schema` 0.19.0 is on PyPI.
- The GitHub release `v0.19.0` exists, with user-facing notes and the distributions.

## Decisions carried from `02-answers.md`

- The project's procedure is followed as written: `CONTRIBUTING.md`, "How to Release" and
  "Recovery and Release Notes".
- The version is the one `just bump-version` computes. A `feat:` commit is in the range, so the
  expected result is 0.19.0. If the command computes another version, say so before opening the
  pull request.
- The user merges the version pull request. No irreversible step is approved in advance.
- Comments on issues 56, 57 and 58 are the steering session's step, after publication.

## Current behavior (checked on 4353782)

- Commits in `v0.18.1..origin/main`: a371f73 `fix(show)`, 62cdc32 `fix(validate)`, 1a742d7
  `docs`, f182faf `fix(index)`, 127a56c `docs(changelog)`, bd47920 `docs(changelog)`, 4353782
  `feat(cli)`.
- Latest tag and GitHub release: `v0.18.1`. Its version commit reached `main` by a pull request
  (number 67, branch `release/v0.18.1`, title `chore: version 0.18.1`).
- On a push to `main`, CI (`.github/workflows/ci.yml`, job `tag-release`) tags a changed
  version after the preflight jobs pass, then dispatches `publish.yml`.
- The `pypi` environment has no protection rule: publication starts with no further approval.
- In the 0.18.1 publication, the CI-started run failed at note generation (`gh copilot` exit
  status 1). PyPI publication was attempted and no GitHub release was created. A second
  dispatch with manually written notes succeeded.

## What changes

1. On the release branch, from `origin/main`, with the release tags fetched: `just bump-version`.
   It updates `pyproject.toml` and `uv.lock` and makes the signed-off commit
   `chore: version X.Y.Z`.
2. Follow what the previous version pull request did to `CHANGELOG.md` (read it on the forge):
   the "Unreleased" entries move under the released version, when the repository's procedure and
   history do so. `just preflight` regenerates `CHANGELOG.md`; review its diff.
3. Validate the version commit: `just preflight`, then `git show --stat HEAD`.
4. Open the version pull request against `main`, titled `chore: version X.Y.Z`.
5. Prepare user-facing notes for the exact release range and validate them with
   `uv run python scripts/release_notes.py --validate <file>`. Keep the file in this item's
   `work/` folder: it is the recovery input if note generation fails again.

## After the user's merge

- Check that main-branch CI passes, that tag `vX.Y.Z` is on the merged commit and that the
  **Release** workflow ran.
- Check the version on PyPI and the GitHub release.
- If note generation fails: check the PyPI step's result first. Dispatching **Release** with
  `release_notes` publishes, so it waits for the user's approval:
  `gh workflow run publish.yml --ref main -f tag=vX.Y.Z -F release_notes=@<file>`.
- Never move a tag and never bump again to retry.

## Out of scope

- Any change to the code, the workflows or the release procedure.
- Merging the version pull request.

## Evidence

- `just preflight` at the version commit.
- The links of the pull request, the tag, the workflow run, the PyPI version and the GitHub
  release.
