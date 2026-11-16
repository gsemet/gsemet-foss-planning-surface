# Build the eval sandbox project

## Goal

The eval campaigns get a frozen project to run on: the public repository
https://github.com/gsemet/chantier-eval-sandbox. This CR writes that project into chantier's eval
kit, gives the kit one command that turns it into the same initial commit every time (fixed
author, committer, dates and message, so the same SHA-1), records that SHA-1, and gives the kit
one reviewed command that resets the sandbox to that commit. Running the reset publishes the project
on the sandbox, and its CI is green there at the recorded SHA-1.

The project is what a chantier user's project looks like: a small Python web app run with uv, with
a backend in the standard library only and hand-written HTML. It has tests, a fast GitHub Actions
CI, an `AGENTS.md` with its gates, and a release procedure that ends in a tag and a GitHub
release. Every eval starts from that one known SHA-1.

This is the first of two CRs. The second, `reproducible-evals`, builds the campaigns on it and
uses these interfaces, named exactly in "Interfaces for `reproducible-evals`" below.

No tracker issue.

## Decisions carried from the answers (`02-answers.md`, 2026-11-12)

- The sandbox is https://github.com/gsemet/chantier-eval-sandbox: public, `main` not protected.
  The user said "fais-en ce que tu veux".
- The project is Python with uv and has CI. It is a web app with a Python backend and hand-written
  HTML. No Node: only uv and hand-written HTML (and CSS). The CI is fast. The eval CRs on it must
  be real coding without being long.
- The app exists and works before any eval. Every eval starts from a known SHA-1.
- Order of work: this CR first, then `reproducible-evals`.
- A scripted procedure force-pushes the sandbox back to its initial state. Evals merge PRs and make
  releases there, so the reset also cleans up the releases.
- `main` is not protected, so the reset can force-push. The force push lives only in a clearly
  defined, reviewed kit command, never in an ad-hoc command.
- Merged PRs may stay on the sandbox.
- A batch can end with a release on the sandbox (both `full` batches do, in `reproducible-evals`),
  so the project carries its own release procedure: version, notes, tag, GitHub release.
- Q5: `just check` rebuilds the sandbox's initial commit and compares it with `sandbox.json`
  ("Oui, un test"). This is one structure test, so CI proves the same SHA-1 on Linux, macOS and
  Windows.
- Q6: the sandbox's release keeps the maintainer's approval of the notes ("Garder
  l'approbation"). In `full`, the operator gives that approval.

## What changes

All of it is in this repository (`gsemet/chantier`): the eval kit under `evals/`, plus one
structure test in `skills/chantier/scripts/cli/tests/test_structure.py`. The sandbox repository
changes only through the reset command (see "Evidence"). The plugin, the cards, the CLI's code,
`hooks/`, `types/` and the scenario are untouched.

### 1. The sandbox project's source: `evals/kit/sandbox/`

This folder holds the project, file for file, as it will stand in the sandbox's initial commit.
The project is **shelf**, a small reading list served on the web. It is not the to-do list of
`kit/fixture/`, so the two kits are never confused.

The tree:

```text
evals/kit/sandbox/
├── .github/workflows/ci.yml
├── .gitignore
├── .python-version          ← 3.12
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE                  ← chantier's own licence text
├── README.md
├── RELEASING.md
├── pyproject.toml
├── uv.lock
├── scripts/release_check.py
├── src/shelf/
│   ├── __init__.py          ← __version__ = "0.1.0"
│   ├── __main__.py          ← `python -m shelf [--host H] [--port P]`
│   ├── app.py               ← the WSGI application and its routes
│   ├── models.py            ← the item, its statuses, the validation of a new item
│   ├── store.py             ← load/save the items in a JSON file
│   ├── views.py             ← renders the templates (string.Template, html.escape)
│   ├── templates/           ← hand-written HTML: base.html, index.html, item.html, error.html
│   └── static/style.css     ← hand-written CSS
└── tests/
    ├── conftest.py          ← the data-file fixture and the `client` fixture
    ├── test_store.py
    ├── test_items.py
    ├── test_pages.py
    └── test_server.py
```

The Driver chooses the module boundaries in detail. The shape above is required: a few modules
with clear seams, so that an eval CR (a page, a route, a filter, a validation, an export) touches
the backend, an HTML template and the tests.

**Constraints:**

- **Dependencies.** The runtime uses the standard library only: `wsgiref` for the server,
  `string.Template` and `html.escape` for the pages, `json` for the store. There is no template
  engine, no web framework, no JavaScript build and no Node. The one dev dependency is
  `pytest>=8`, in `[dependency-groups] dev`. `[tool.uv] package = false`, and
  `[tool.pytest.ini_options] pythonpath = ["src"]`, as in `kit/fixture/pyproject.toml`.
  `requires-python = ">=3.11"`, and `.python-version` pins 3.12 so CI and the Drivers use one
  interpreter. `uv.lock` is committed. It is made with `uv lock` in the folder and is checked by
  `uv sync --locked`.
- **Storage.** The items live in a JSON file: the path that `SHELF_DATA` names, else `shelf.json`
  in the current folder. That file is in the sandbox's `.gitignore`, along with `.venv/`,
  `__pycache__/`, `.pytest_cache/` and `.claude/settings.local.json`. A missing file is an empty
  shelf. A save is atomic: write a temporary file, then replace.
- **Item.** Each item has `id` (int, from 1), `title` (str, required, 1–200 characters after
  trimming), `url` (str, optional; when given it starts with `http://` or `https://`), `status`
  (`to-read`, `reading` or `done`; the default is `to-read`) and `added` (an ISO date, `YYYY-MM-DD`,
  from the server's clock).
- **Routes.** Each one is listed in the README's "Routes" table:

  | Method | Path | Does |
  | --- | --- | --- |
  | GET | `/` | the list of items (title linked to its page, status, date added) and the add form |
  | POST | `/items` | adds an item from the form (`title`, `url`). On success: 303 to `/`. On invalid input: 400, the list page again with the error message and the values entered |
  | GET | `/items/<id>` | the item's page; 404 page if unknown |
  | POST | `/items/<id>/status` | sets `status` from the form. 303 to the item's page; 400 on an unknown status; 404 on an unknown item |
  | GET | `/static/style.css` | the stylesheet |
  | GET | `/healthz` | `{"status": "ok", "version": "<version>"}` as JSON |

  Any other path gets the 404 page. A known path with the wrong method gets 405. Every page shows
  the version in its footer. All user text is HTML-escaped. There is no JavaScript.
- **Left out on purpose.** These leave room for the eval CRs, which `reproducible-evals` chooses:
  delete, edit, tags, search or filter, sort, a JSON list API, CSV export, pagination, statistics,
  notes or ratings. None of them exists in the base, and the README promises none of them.
- **Run.** `uv run python -m shelf` serves on `http://127.0.0.1:8000`. `--host` and `--port` change
  that. It prints the URL at start and stops cleanly on Ctrl-C.
- **Tests.** There is a test for every behaviour above: the store, each route's success and error,
  escaping, the 404 and 405 pages, `/healthz`. `test_server.py` has one smoke test: a real
  `wsgiref` server on `127.0.0.1` port 0, in a thread, answering `/healthz`. It runs on Linux,
  macOS and Windows. The whole suite takes a few seconds.
- **Test fixtures.** Hidden tests in `reproducible-evals` will rely on these, so they are part of
  the interface. In `tests/conftest.py`:
  - an autouse fixture sets `SHELF_DATA` to a file in `tmp_path`, so every test starts with an
    empty shelf;
  - a `client` fixture calls the WSGI app directly, with no socket. It offers
    `client.get(path)` and `client.post(path, data: dict)`, and each returns a response with
    `.status` (int), `.headers` (dict, header names in lower case) and `.text` (str). A redirect is
    returned as it is, not followed. `client.get` accepts a query string in `path` (for example
    `/?status=done`): the part after `?` goes to the app as `QUERY_STRING`, and the part before it
    as `PATH_INFO`. `client.post` sends `data` form-encoded as the body
    (`CONTENT_TYPE` `application/x-www-form-urlencoded`, with `CONTENT_LENGTH` set).
- **Size.** The project stays small: about 300–450 lines of Python in `src/`, and about
  15–25 tests.
- **Text.** Every file is UTF-8 without a byte-order mark, ends lines with LF, and is in English.
  None of chantier's root `.gitignore` patterns may hide a sandbox file: the root ignores `lib/`,
  `build/`, `dist/`, `*.spec`, `.env` and others, so name no file or folder that way.

**`AGENTS.md`** (the sandbox's rules, read by chantier's `$CHANTIER rules` in an eval) says, in
this order:

- what shelf is, and that everything runs with `uv`;
- run it: `uv run python -m shelf`;
- fast gate (after each change): `uv run pytest -q -x`;
- long gate (before a pull request): `uv run --locked pytest -q`;
- default branch `main`; Conventional Commits (`feat: …`, `fix: …`); pull requests merge by rebase
  (`gh pr merge --rebase`);
- the code lives in `src/shelf/`, with a test for every behaviour in `tests/`; the HTML is
  hand-written in `src/shelf/templates/`; no JavaScript framework, no Node, and no new runtime
  dependency;
- every route and page is in the README's "Routes" table, and a change to a route updates it;
- a `## chantier` section with `- release: RELEASING.md` (as in `kit/fixture/AGENTS.md`).

The sandbox's `AGENTS.md` declares no review steps. Per-run settings (PR title prefixes, review
agents) are `reproducible-evals`' to place outside the frozen commit.

**`RELEASING.md`** (the release procedure). Run these steps in order, from a branch on a fresh
`main`. If anything in the code changes, start again from step 1:

1. **Heavy check:** `uv run python scripts/release_check.py` must end with
   `release check passed`.
2. **Notes:** write one bullet per user-visible change since the previous version's entry in
   `CHANGELOG.md`. A maintainer approves them before they go anywhere. This step stays (Q6); in
   the `full` campaign, the operator gives the approval.
3. **Release commit:** set the version in `pyproject.toml` and in `src/shelf/__init__.py`, add the
   approved notes at the top of `CHANGELOG.md` under `## <version>`, run step 1 again, and commit
   `release: v<version>`. Open a pull request.
4. **CI** is green on that pull request.
5. **Merge** it by rebase.
6. **Tag** the merged commit: `git fetch origin main`, then `git tag v<version> origin/main`, then
   `git push origin v<version>`.
7. **GitHub release:** `gh release create v<version> --title "v<version>" --notes-file <file>`,
   where the file holds that version's `CHANGELOG.md` section.
8. **Check:** `git ls-remote --tags origin` lists the tag, and `gh release view v<version>` shows
   the notes.

Steps 5 to 7 cannot be undone (on the sandbox, only the kit's reset undoes them).

**`scripts/release_check.py`** runs `uv run --locked pytest -q`, then checks three things:
`pyproject.toml`'s version equals `shelf.__version__`; the first `## ` heading of `CHANGELOG.md`
is that version; and `/healthz` of the WSGI app (called in-process) reports it. It prints
`release check passed` and exits 0, or prints one `FAIL …` line per failure and exits 1.

**`CHANGELOG.md`** starts with `## 0.1.0`, which describes the first version in a few bullets.
The base has no tag and no GitHub release, so the first eval release is `v0.2.0`.

**`README.md`** gives what shelf is, how to run it, how to test it, the "Routes" table, where the
data lives (`SHELF_DATA`), and one line saying that this repository is chantier's eval sandbox and
that its `main` is reset by chantier's eval kit, so PRs and releases there do not last.

**`.github/workflows/ci.yml`** runs on `push` to `main` and on `pull_request`, with
`permissions: contents: read`. It has one job, `test`, on `ubuntu-latest`:
`actions/checkout@v4`, `astral-sh/setup-uv@v6` (cache enabled), then `uv run --locked pytest -q`.
The target is under two minutes from queue to green. One OS is enough for the sandbox: the
portability check is chantier's, not the sandbox's.

### 2. The kit command: `evals/kit/sandbox.py`

It uses the standard library only and runs on POSIX and Windows. It is called as
`uv run --no-project python evals/kit/sandbox.py <command>`. Its exit codes: 0 ok, 1 usage,
2 precondition, 4 external (git or gh failed; the tool's error text is printed).

The repository is a constant in the script, `gsemet/chantier-eval-sandbox` (URL
`https://github.com/gsemet/chantier-eval-sandbox.git`). No argument or environment variable
changes it, and the script touches no other repository.

**`build [<dest>] [--record]`**: builds the initial commit.

- It reads every file under `evals/kit/sandbox/`, skipping `.venv/`, `__pycache__/`,
  `.pytest_cache/`, `*.pyc` and `shelf.json`.
- It turns CRLF into LF, so the same files on a Windows checkout with `core.autocrlf=true` and on
  Linux give the same blobs. It gives every file the mode `100644`.
- It writes the objects itself (`git hash-object -w --no-filters`, `git mktree`, and the commit
  object written by the kit through `git hash-object -t commit -w`, or the same in pure Python).
  The commit therefore depends on none of the user's git config: no autocrlf, no signing, no
  template, no hooks.
- The commit is a root commit, with no parent. Its fixed values are constants in the script:
  - author and committer: `chantier eval kit <eval@example.com>`;
  - author date and committer date: `2026-11-12T00:00:00+00:00`;
  - message: `feat: shelf 0.1.0, the chantier eval sandbox` (one line, then a newline).
- With `<dest>` (it must not exist), it leaves a git repository there whose `main` is that commit,
  checked out. Without `<dest>`, it builds in a temporary folder and removes it.
- It prints `base <40-hex sha>` and the number of files.
- It compares the SHA-1 with `evals/kit/sandbox.json`. If they differ, it exits 2 and prints both
  SHA-1s and `run build --record and commit sandbox.json`. With `--record`, it writes the SHA-1
  there instead and exits 0. `build --record` is the only command that writes in this repository.

**`evals/kit/sandbox.json`**: the record, written by `build --record` only:

```json
{"repository": "gsemet/chantier-eval-sandbox", "base": "<40-hex sha>"}
```

**`reset [--yes]`**: puts the sandbox back at the recorded base. This is the only force push on
the sandbox.

1. **Preconditions** (exit 2, naming which one failed):
   - `gh auth status` passes, and its token has the `workflow` scope (needed to push
     `.github/workflows/`);
   - the repository's default branch is `main` (`gh repo view <repo> --json defaultBranchRef`);
   - `build` (in a temporary folder) gives exactly `sandbox.json`'s `base`.

   The push uses git's credentials for github.com (`gh auth setup-git`). When one is missing, the
   script says so and does not set it up itself.
2. **Survey.** It lists `main`'s current SHA-1, the open PRs (number, title, branch), the branches
   other than `main`, the tags and the GitHub releases.
3. **Plan.** It prints one line per action, in the order it will run them:
   1. close each open PR;
   2. delete each release;
   3. delete each tag that is left;
   4. delete each branch other than `main`;
   5. force-push the base to `main`, only if `main` is not already there.

   An empty plan prints `sandbox already at <sha>: nothing to do`. **Without `--yes` it stops
   there: it changes nothing and exits 0.**
4. **With `--yes`** it runs the plan in that order, printing each line before running it:
   - `gh pr close <n> --repo <repo>`;
   - `gh release delete <tag> --repo <repo> --yes`;
   - the tag and branch deletions with `git push <url> --delete <ref>`;
   - `git push --force <url> <base>:refs/heads/main`, run from the repository `build` made.

   It stops at the first failure with exit 4 and the tool's error text. It does not retry and does
   not work around the failure.
5. **Verify.** `git ls-remote <url>` shows exactly one ref, `refs/heads/main` at `base` (HEAD
   aside), and no tag; there is no open PR and no release. It prints
   `sandbox reset: main at <sha>` and exits 0. Any difference exits 4 and names it.

Merged and closed PRs, and the Actions run history, stay on the sandbox, as the answers allow.

### 3. Docs: `evals/README.md`

- **The kit table** gets two rows:
  - `kit/sandbox/`: shelf, the sandbox project, the source of the sandbox's initial commit;
  - `kit/sandbox.py`: `build` (the deterministic initial commit, its SHA-1 recorded in
    `kit/sandbox.json`) and `reset` (the sandbox back at that commit; the only force push).
- **A short "The sandbox" section** says:
  - the repository and the recorded base;
  - how to change the project: edit `kit/sandbox/`, run `build --record`, commit `sandbox.json` in
    the same PR (else `just check` is red), run `reset --yes` once that PR is reviewed;
  - that nothing else changes the sandbox.
- The campaigns table and the runbooks are not changed (that is `reproducible-evals`).

### 4. The structure test: `skills/chantier/scripts/cli/tests/test_structure.py` (Q5)

This adds one test, `test_the_eval_sandbox_builds_its_recorded_base`. It finds the repository
root from the test file, as the other tests do, and runs
`evals/kit/sandbox.py build` with the test's own Python (`sys.executable`). The build needs no
`<dest>` and never takes `--record`. The test asserts three things:

- the exit code is 0;
- the printed `base <sha>` equals `evals/kit/sandbox.json`'s `base`;
- that `base` is 40 hex characters.

It needs only `git`, which the tests already use, and takes a few seconds at most. `just check`
runs it on the three OSes of chantier's CI. The Windows runner's checkout uses CRLF, so CI proves
that the LF normalisation gives the same SHA-1 everywhere. An edit of `evals/kit/sandbox/`
without `build --record` turns `just check` red. This is the intended guard, and `evals/README.md`'s
"The sandbox" section says so. No other test is added.

## Interfaces for `reproducible-evals`

These are the names the second CR builds on. Keep them exactly:

- **The kit folder of the project:** `evals/kit/sandbox/`. Package `shelf`, in `src/shelf/`.
  Templates in `src/shelf/templates/`, tests in `tests/`, and the `client` and `SHELF_DATA`
  fixtures in `tests/conftest.py`. `client.get(path)` takes a query string in `path` (for example
  `/?status=done`, passed as `QUERY_STRING`). `client.post(path, data)` sends `data` form-encoded
  (`application/x-www-form-urlencoded`) as the body. Both return `.status`, `.headers` and `.text`.
- **The initial commit:** `uv run --no-project python evals/kit/sandbox.py build [<dest>] [--record]`.
  The SHA-1 is in `evals/kit/sandbox.json`, key `base`. `just check` guards it.
- **The reset:** `uv run --no-project python evals/kit/sandbox.py reset` (plan only), then `… reset --yes`.
  It takes no repository argument.
- **The sandbox's long gate:** `uv run --locked pytest -q` (fast gate `uv run pytest -q -x`).
  The CI job is `test` in `.github/workflows/ci.yml`.
- **The release procedure:** `RELEASING.md`, named by `- release: RELEASING.md` in the sandbox's
  `AGENTS.md`. The version lives in `pyproject.toml` and `src/shelf/__init__.py`, the notes in
  `CHANGELOG.md` (approved by a maintainer; in `full`, the operator), the tags are `v<version>`,
  and there is a GitHub release per version. The heavy check is
  `uv run python scripts/release_check.py`. The base is 0.1.0, with no tag.

## Out of scope

All of these are in `reproducible-evals`:

- the frozen CRs and the hidden tests;
- the campaigns (`full`, the rebuilt `real-foreman` and `real-direct`, `copilot` on the sandbox),
  their runbooks and the PR-title convention;
- changes to `audit.py` and `setup.py`.

Also out of scope:

- `kit/fixture/` and `claude-planted`, which stay as they are;
- any change to the plugin, the cards or the CLI's code (the one structure test of section 4
  aside);
- any change to the sandbox other than through `reset --yes`.

## Evidence

The CR changes the eval kit and adds one structure test, not the CLI, the cards or the scenario.
So AGENTS.md asks for no `just scenario`, and the long gate is `just check`.

1. **`just check` passes** in the worktree at the pushed head, with
   `test_the_eval_sandbox_builds_its_recorded_base` among the tests it runs. The PR's CI is green
   on all three OSes, Windows and its CRLF checkout included: this is the cross-OS proof of the
   base SHA-1 (Q5).
2. **Determinism.** Run `uv run --no-project python evals/kit/sandbox.py build <tmp>/a`, then the
   same with `<tmp>/b`. Both print the same `base <sha>`, equal to `sandbox.json`, and neither
   exits non-zero. `git -C <tmp>/a cat-file -p HEAD` shows the fixed author, committer, dates and
   message and no parent. This is run on the Driver's Windows checkout (CRLF working tree), which
   tests the LF normalisation.
3. **The project works**, run in `<tmp>/a`:
   - `uv sync --locked`, then `uv run --locked pytest -q` (passes; the time is quoted);
   - `uv run python scripts/release_check.py`, which ends with `release check passed`;
   - `uv run python -m shelf --port 8765` in a background shell. A GET of `/` (200, with the
     form), `/healthz` (the JSON with `0.1.0`), `/items/99` (404), and a POST of `/items` with an
     empty title (400) and with a valid one (303), then `/` showing it. These are quoted with
     their outputs; the Verifier captures them.
4. **Reset, plan.** `uv run --no-project python evals/kit/sandbox.py reset` prints the plan
   against today's sandbox: `main` at `8e84ddace885dee69b633134e5384d9e9534348f` (the README
   commit), no PR, branch, tag or release. The plan is a single force push, and nothing changes.
5. **Reset, run.** This happens once the Inspector has passed the round, at the PR's head:
   - `… reset --yes` force-pushes `main` and prints `sandbox reset: main at <base>`;
   - `git ls-remote https://github.com/gsemet/chantier-eval-sandbox.git` shows only `main` at
     `base`;
   - a second `… reset --yes` prints `nothing to do` (it is idempotent).

   If the host or its classifier refuses the force push, that refusal goes to the parent with its
   exact text (rule 7). Nothing else pushes to the sandbox.
6. **CI green on the sandbox at `base`.** Find the run with
   `gh run list --repo gsemet/chantier-eval-sandbox --commit <base>`, wait for it with
   `gh run watch <id> --repo gsemet/chantier-eval-sandbox --exit-status` in a background shell,
   and quote its conclusion and duration (target: under two minutes).
7. **Not provable here.** The reset's clean-up of PRs, branches, tags and releases cannot be shown
   on today's sandbox without changing it by another route, which is not allowed. The PR says so.
   The first `reset --yes` after a `reproducible-evals` campaign proves it, and that CR's report
   records it.

The PR body's Deliverables section quotes items 1 (the three OSes' CI), 2, 3, 5 and 6.
