## Summary

Eval campaigns need a frozen project to run on. This adds that project to the eval kit: "shelf", a small reading list served on the web (Python and uv, standard library only, hand-written HTML), with tests, a fast CI, its own `AGENTS.md` and a release procedure. The kit also gets one command that builds the project into the same initial commit every time (same SHA-1 on every machine) and one reviewed command that resets the public sandbox repository, `gsemet/chantier-eval-sandbox`, to that commit.

## Deliverables

The kit gains two commands and one recorded SHA-1:

```text
uv run --no-project python evals/kit/sandbox.py build [<dest>] [--record]
uv run --no-project python evals/kit/sandbox.py reset [--yes]     # plan only without --yes
evals/kit/sandbox.json    {"repository": "gsemet/chantier-eval-sandbox", "base": "<sha>"}
```

- `build` writes the git objects itself (LF line endings, mode 100644, fixed author, committer, dates and message, no parent), so the commit depends on none of the user's git config. `just check` rebuilds it and compares it with `sandbox.json`, so CI proves the same SHA-1 on Linux, macOS and Windows.
- `reset` is the only force push on the sandbox. It surveys the sandbox, prints its plan (close PRs, delete releases, tags and branches, force-push the base to `main`) and changes nothing without `--yes`. Its pushes use the user's own git credentials.

```text
evals/kit/sandbox/
  src/shelf/   app.py models.py store.py views.py templates/ static/style.css
  tests/       conftest.py (SHELF_DATA and `client` fixtures) test_*.py
  scripts/release_check.py   RELEASING.md   CHANGELOG.md   AGENTS.md   .github/workflows/ci.yml
```

Choices: the app leaves delete, edit, tags, search, sort, export and the like out on purpose, to leave room for eval changes; the project's `pyproject.toml` uses a `hatchling` build backend so that `uv run python -m shelf` finds the package.

Evidence at `90718bd`:

- Two builds into separate folders on a Windows checkout (CRLF working tree) both print `base 6e87a361c1b192e6d081c162f0cb2cc28bb72b25` and `27 files`, equal to `sandbox.json`; the commit is a root commit with author and committer `chantier eval kit <eval@example.com>`, date 2026-11-12T00:00:00Z.
- In the built copy: `uv run --locked pytest -q` gives 28 passed in 0.16s, `release_check.py` ends with `release check passed`, and a real server answers `/` 200, `/healthz` `{"status": "ok", "version": "0.1.0"}`, `/items/99` 404, `POST /items` with an empty title 400 and with a valid one 303.
- `sandbox.py reset --yes` was run once at this head: it force-pushed `main` from `8e84dda` to the base and printed `sandbox reset: main at 6e87a361c1b192e6d081c162f0cb2cc28bb72b25`; `git ls-remote` of the sandbox then shows only `main` at that SHA-1, and a second `reset --yes` prints `nothing to do`.
- The sandbox's CI at that SHA-1 passed in 15 seconds.
- This PR's CI is green on Linux, macOS and Windows, which proves the same base SHA-1 on all three.

**UNVERIFIED:** the reset's clean-up of PRs, branches, tags and releases cannot be shown on today's sandbox (nothing there to clean) and is proved by the first reset after a campaign.

## Blast radius

Grade: 1. Only the eval kit and one structure test change; the plugin, the CLI and the cards are untouched. A `git revert` restores the repository; the sandbox itself changes only when someone runs `reset --yes`.

## Autonomous decisions

- `package = false` is replaced by a `hatchling` build backend in the sandbox's `pyproject.toml`: with `package = false`, `uv run python -m shelf` fails with `No module named shelf` on a `src` layout.
- The reset's credential check accepts any configured git credential helper, not only the one `gh auth setup-git` sets.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/sandbox/`: the shelf project, `uv.lock` included.
- `evals/kit/sandbox.py` and `evals/kit/sandbox.json`: `build`, `reset` and the record.
- `evals/README.md`: two kit rows and a "The sandbox" section.
- `skills/chantier/scripts/cli/tests/test_structure.py`: `test_the_eval_sandbox_builds_its_recorded_base`.

## Human decisions

- The sandbox is a public repository whose `main` is not protected, so a scripted reset can force-push.
- The reset lives in one reviewed kit command, never in an ad-hoc command.
- `just check` rebuilds the initial commit and compares it with the record.
- The sandbox's release procedure keeps the maintainer's approval of the notes.

## Impacts

No visual change. A change to `evals/kit/sandbox/` now needs `build --record` and the new `sandbox.json` in the same PR, or `just check` is red.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_the_eval_sandbox_builds_its_recorded_base`
- [x] Local gates at `90718bd`: `just check` passed (47 tests)
- [x] Evidence at `90718bd`: determinism, the project's own tests and server, reset plan and reset run (Deliverables)
- [x] Review: approved at `90718bd` (round 2)
- [x] Verified at `90718bd`
- [x] CI green at `90718bd`: `just check` on three OSes and `just scenario`

## Internal references

- CR-188 build-the-eval-sandbox-project; second of two, `reproducible-evals`, builds on it.

</details>
