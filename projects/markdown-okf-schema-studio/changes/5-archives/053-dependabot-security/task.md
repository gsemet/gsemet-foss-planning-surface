# T1 — 053-dependabot-security

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-053 (branch `changes-requests/053-dependabot-security` from origin/main; rebase on the latest origin/main before starting).
Work ONLY there. Read `00-request.md` (decisions = the spec) and `rules.md`.

## Change

`pyproject.toml` (requires-python, pillow), `uv.lock` (relock with `UV_NO_CONFIG=1`), any script
or CI step that pins Python 3.10, and code adapted to Pillow 13 if its changelog requires it.

## Docs

CHANGELOG Unreleased bullet only if a developer-visible requirement changes (Python 3.11 minimum
for the docs/build tools). README / CONTRIBUTING where the Python version is documented.

## Gates

`just check`, `just visual`, `uv run --group docs pytest test/build`.

## Report

/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/053-dependabot-security/reports/T1-r<round>.md
