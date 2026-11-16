# Reproducible eval campaigns on the sandbox

## Goal

Two eval runs should measure the same thing: only the variable under test (the chantier plugin)
changes from one run to the next. Until now the real campaigns (`real-foreman`, `real-direct`)
took fresh inbox items on this repository and its `main` of the day, and their PRs were gone the
next day. After this CR every real campaign runs on the frozen sandbox project that
`eval-sandbox-app` built (shelf, on https://github.com/gsemet/chantier-eval-sandbox):

- it starts from the same recorded commit (the kit's reset puts the sandbox back first);
- it takes the same already-specified CRs (frozen CRs in the kit, no grill to replay);
- a judge runs hidden tests on each PR's head, so the audit says whether the work is right, not
  only whether the rails held;
- the report names the chantier version and commit, the sandbox's base SHA-1, the campaign, the
  mode and the models, so two reports compare line by line, costs included;
- every PR a run opens carries the run's number, date and campaign in its title.

A new campaign, `full`, runs two batches end to end, releases included, with no human step: the
operator plays the user (the reset and the setup are its preparation, before the run, not steps
of it). `real-foreman` and `real-direct` become quick campaigns of 5 frozen CRs
with the mode chosen at launch; `copilot` takes one frozen CR. Dogfooding on this repository stays
normal work, not an eval. `claude-planted` is unchanged.

Second of two CRs: it runs after `eval-sandbox-app`, whose branch is this CR's base. No tracker
issue.

## Decisions carried from the answers (`02-answers.md`, 2026-11-12) and the intent

- The sandbox is https://github.com/gsemet/chantier-eval-sandbox, public, `main` not protected.
  The project is shelf (Python with uv, standard-library backend, hand-written HTML, fast CI),
  delivered by `eval-sandbox-app`. Every eval starts from its known SHA-1.
- The only force push on the sandbox is `evals/kit/sandbox.py reset --yes`; nothing in this CR
  force-pushes, and no runbook gives an ad-hoc force push.
- Merged PRs may stay on the sandbox; every PR title a run opens carries the run's number, date
  and campaign type.
- **full**: 2 batches, 4 slots, Foreman mode, no human step: the operator plays the user (gos,
  merges, approvals, confirmations). Batch 1: 8 feature CRs plus a release CR, the last, which
  waits for all the others; during the coding a 10th CR is injected with `order add`, and the
  release waits for it too. Batch 2: 2 feature CRs plus a release CR, the last. Both releases are
  made on the sandbox by its own `RELEASING.md`; the next reset cleans them up.
- **real-foreman, real-direct**: one batch of 5 CRs, no release, the mode chosen at launch
  (`--mode stack|parallel|series`), the same 5 CRs in every mode.
- **copilot** takes one frozen CR.
- **The CRs (Q3, decided by the Chief of Staff):** 11 feature CRs and 2 release CRs for shelf;
  small features that each touch the backend, the hand-written HTML and the tests; batch 1's 8
  include the 5 of the quick campaigns; the injected 10th and batch 2's 2 are distinct. Some touch
  the same files on purpose, so rebases after a merge happen; none depends on another. Each runs
  in a few rounds at most.
- **The judge (Q4, decided by the Chief of Staff):** hidden test files per feature CR, kept in
  the kit and never pushed to the sandbox, run by the audit against the PR's head in a clean clone
  of the sandbox with the project's own test command; a pass, a fail or "not run" per CR. A release
  CR is judged by what the sandbox shows: the version, the tag, the GitHub release, the notes.
- **Q6 (folded into `eval-sandbox-app`):** the sandbox's release keeps the maintainer's approval of
  the notes; in `full` the operator gives it.
- **Q5** (a structure test of the base SHA-1) is `eval-sandbox-app`'s; this CR adds nothing to it.
- An eval's workspace is outside this repository, and the main checkout does not change during an
  eval (AGENTS.md).
- Claude Desktop's 10-message limit: the runbooks say how the operator lives with it (the host's
  turn notes and `status`).
- **Q7:** in `real-foreman` and `real-direct` too, the operator plays the user in full, merges
  included.
- **Q8:** in `full`, past the 10-message limit, when the Foreman's heartbeat has ended, the user
  types one line (`ping`) in the Foreman's session; the report counts it as the run's one human
  step. It is the only possible human step during a `full` run.
- **Q9:** `evals/README.md`'s "which campaign" names `full` before each release, with both quick
  campaigns.
- **Q10:** `eval-sandbox-app`'s specification states the `client` fixture's query string
  (`QUERY_STRING`) and form-encoded POST body.

## What this CR builds on (from `eval-sandbox-app`, used as named there)

- `evals/kit/sandbox/`: the shelf project; package `shelf` in `src/shelf/`, templates in
  `src/shelf/templates/` (`base.html`, `index.html`, `item.html`, `error.html`), CSS in
  `src/shelf/static/style.css`, tests in `tests/` with the `client` fixture and the autouse
  `SHELF_DATA` fixture in `tests/conftest.py`.
- `uv run --no-project python evals/kit/sandbox.py build [<dest>] [--record]`; the base SHA-1 in
  `evals/kit/sandbox.json`, key `base`.
- `uv run --no-project python evals/kit/sandbox.py reset` (plan only), then `reset --yes`.
- The sandbox's long gate `uv run --locked pytest -q`, fast gate `uv run pytest -q -x`, CI job
  `test` in `.github/workflows/ci.yml`.
- `RELEASING.md` (named by `- release: RELEASING.md` in the sandbox's `AGENTS.md`), the version in
  `pyproject.toml` and `src/shelf/__init__.py`, notes in `CHANGELOG.md`, tags `v<version>`, one
  GitHub release per version, heavy check `uv run python scripts/release_check.py`. Base 0.1.0, no
  tag: the first eval release is `v0.2.0`.

The hidden tests rely on two properties of the `client` fixture that `eval-sandbox-app` states
(Q10): `client.get(path)` accepts a path with a query string (`/?q=a`,
split into `PATH_INFO` and `QUERY_STRING`), and `client.post(path, data)` sends `data` as an
`application/x-www-form-urlencoded` body. A redirect's target is read from
`response.headers["location"]`.

## What changes

Everything is under `evals/`, plus one structure test and two lines of docs outside it (see 7).
The plugin, the cards, the CLI, `hooks/`, `types/` and the scenario are untouched. The sandbox
changes only through campaigns and `reset --yes`; this CR's evidence opens no PR there.

### 1. The frozen CRs: `evals/kit/sandbox-crs/<slug>/`

One folder per CR, in the form of `evals/kit/crs/` (which stays `claude-planted`'s):
`intake/request.md` (one or two lines, as a user would write the request), `01-intent.md` (the
request summarised), `02-answers.md` (the decisions, as if grilled: every choice the
specification makes that a user would make), `03-change-spec.md` (the specification: "Change"
then "Done when"). No `depends.json`. No hidden test is ever in these folders. Every file is
UTF-8 without a byte-order mark, LF line ends, English. None of chantier's root `.gitignore`
patterns may hide a file there.

Every feature CR's "Done when" ends with these common lines:

- each behaviour of "Change" has a test, in the test file named, using the `client` fixture;
- the README's "Routes" table lists every new route and every new query parameter of `/`;
- all user text is HTML-escaped; no JavaScript; no new runtime dependency; a known path with the
  wrong method gets 405, like the base routes;
- the fast gate (`uv run pytest -q -x`) and the long gate (`uv run --locked pytest -q`) pass.

**The set.** Letters are for this document only; the slug is the folder's name.

| | Slug | In | Asks of shelf | Files it touches (in `src/shelf/` unless said) |
| --- | --- | --- | --- | --- |
| A | `delete-item` | quick, batch 1, copilot | delete an item | `store.py`, `app.py`, `templates/item.html`, `README.md`, `tests/test_items.py` |
| B | `edit-item` | quick, batch 1 | edit an item's title and URL | `models.py`, `app.py`, `views.py`, `templates/edit.html` (new), `templates/item.html`, `README.md`, `tests/test_items.py` |
| C | `status-filter` | quick, batch 1 | filter the list by status | `app.py`, `views.py`, `templates/index.html`, `README.md`, `tests/test_pages.py` |
| D | `json-api` | quick, batch 1 | read the items as JSON | `app.py`, `api.py` (new), `templates/index.html`, `README.md`, `tests/test_api.py` (new) |
| E | `stats-page` | quick, batch 1 | a statistics page | `app.py`, `views.py`, `templates/stats.html` (new), `templates/base.html`, `README.md`, `tests/test_pages.py` |
| F | `csv-export` | batch 1 | export the shelf as CSV | `app.py`, `export.py` (new), `templates/index.html`, `README.md`, `tests/test_export.py` (new) |
| G | `item-notes` | batch 1 | free-text notes on an item | `models.py`, `store.py`, `app.py`, `templates/item.html`, `static/style.css`, `README.md`, `tests/test_items.py` |
| H | `title-search` | batch 1 | search the titles | `app.py`, `views.py`, `templates/index.html`, `README.md`, `tests/test_pages.py` |
| I | `item-rating` | batch 1, injected 10th | rate an item from 1 to 5 | `models.py`, `store.py`, `app.py`, `templates/item.html`, `templates/index.html`, `README.md`, `tests/test_items.py` |
| J | `sort-list` | batch 2 | sort the list | `app.py`, `views.py`, `templates/index.html`, `README.md`, `tests/test_pages.py` |
| K | `duplicate-url` | batch 2 | refuse an item whose URL is already on the shelf | `models.py`, `app.py`, `templates/index.html`, `templates/edit.html`, `README.md`, `tests/test_items.py` |
| L | `release-v0-2-0` | batch 1, last | release 0.2.0 | `pyproject.toml`, `src/shelf/__init__.py`, `CHANGELOG.md` (by `RELEASING.md`) |
| M | `release-v0-3-0` | batch 2, last | release 0.3.0 | the same |

- **The quick campaigns' set:** A, B, C, D, E (`real-foreman`, `real-direct`, in every mode).
- **Batch 1 of `full`:** A to H, then L (opened with `--release 9`); **the injected 10th:** I.
- **Batch 2 of `full`:** J, K, then M (opened with `--release 3`).
- **`copilot`:** A.

The "files it touches" column is the expected footprint, written into each specification as
"Files"; a Coder may add a helper module, never a dependency. On purpose: every feature touches
`app.py` and `README.md`; C, D, F, H, I, J, K touch `index.html`; A, B, G, I touch `item.html`; B,
G, I, K touch `models.py`.

**Each feature CR's "Change"**, to be written into its `03-change-spec.md` as stated (exact texts,
attribute values and class names below are part of the specification; a Coder meets them without
seeing the hidden tests):

- **A `delete-item`.**
  - The item page has `<form method="post" action="/items/<id>/delete">` with a button `Delete`.
  - `POST /items/<id>/delete` removes the item and answers 303 to `/`. An unknown id: the 404
    page. `GET` on that path: 405.
  - After a delete, the item is gone from `/` and `/items/<id>` is 404; the other items stay.
  - An id is never given twice: an item added after a delete gets an id higher than any id the
    shelf ever gave, the deleted one included (the store keeps the next id).
- **B `edit-item`.**
  - `GET /items/<id>/edit`: a page with `<form method="post" action="/items/<id>/edit">`, inputs
    `name="title"` and `name="url"` holding the current values (escaped). An unknown id: 404.
  - `POST /items/<id>/edit` (`title`, `url`) is validated exactly as adding (title 1-200
    characters after trimming; URL empty or starting with `http://` or `https://`), by one
    validation function in `models.py` that adding uses too. Valid: title and URL saved
    (trimmed), status and date added unchanged, 303 to `/items/<id>`. Invalid: 400, the edit page
    again with the error message and the values entered; nothing saved. Unknown id: 404.
  - The item page links to `/items/<id>/edit` with the text `Edit`.
- **C `status-filter`.**
  - `GET /?status=<s>`, `<s>` one of `to-read`, `reading`, `done`: only the items with that
    status. `status` absent or empty: all items. Any other value: 400, with the message
    `Unknown status: <value>` (the value escaped).
  - Above the list, `<nav class="filters">` with four links in this order: `All` (`/`), `To read`
    (`/?status=to-read`), `Reading` (`/?status=reading`), `Done` (`/?status=done`). The link of
    the current filter (`All` with no filter) has `aria-current="page"`; no other link of that
    nav has it.
  - A filter that matches nothing shows `No items with this status.`.
- **D `json-api`.**
  - `GET /api/items`: 200, `Content-Type: application/json; charset=utf-8`, a JSON array of all
    items in id order. Each item is an object with at least `id` (integer), `title` (string),
    `url` (string, or `null` when the item has none), `status` (string) and `added`
    (`YYYY-MM-DD`).
  - `GET /api/items/<id>`: that object. Unknown id: 404, body `{"error": "not found"}`, same
    content type.
  - Any other method on these paths: 405. Titles are given as entered, not HTML-escaped.
  - The list page links to `/api/items` with the text `JSON`.
- **E `stats-page`.**
  - `GET /stats`: a page whose `<h1>` is `Statistics`, with `<table class="stats">` of four rows
    in this order: `To read`, `Reading`, `Done`, `Total`; each row a `<th>` holding the label and
    a `<td>` holding the count. An empty shelf shows four zeros.
  - The navigation in `base.html`, on every page, links to `/stats` with the text `Statistics`.
  - `POST /stats`: 405. The page shows the version in its footer, like every page.
- **F `csv-export`.**
  - `GET /export.csv`: 200, `Content-Type: text/csv; charset=utf-8`,
    `Content-Disposition: attachment; filename="shelf.csv"`. The body is written with Python's
    `csv` module, default dialect (comma, minimal quoting, `\r\n` line ends): the header
    `id,title,url,status,added`, then one row per item in id order; `url` empty when the item has
    none. Exactly these five columns.
  - The list page links to `/export.csv` with the text `Export CSV`. `POST /export.csv`: 405.
- **G `item-notes`.**
  - Each item has `notes`, a text, empty by default; an item stored before this change reads as
    empty notes. At most 2000 characters, counted after removing leading and trailing whitespace.
  - The item page shows the notes in an element with class `notes`, escaped, with their line
    breaks kept (`.notes { white-space: pre-wrap; }` in `style.css`), and has
    `<form method="post" action="/items/<id>/notes">` with `<textarea name="notes">` holding the
    current notes (escaped) and a button `Save notes`.
  - `POST /items/<id>/notes` (`notes`): saves them trimmed, 303 to `/items/<id>`. Over 2000
    characters: 400, the item page with `Notes are limited to 2000 characters.`, nothing saved.
    Unknown id: 404. `GET` on that path: 405.
- **H `title-search`.**
  - `GET /?q=<text>`: the items whose title contains the text, trimmed, ignoring case. `q` absent
    or blank: all items.
  - The list page has `<form method="get" action="/">` with `<input name="q">`, whose `value` is
    the current query (escaped), and a button `Search`.
  - A query that matches nothing shows `No items match "<query>".` (the query escaped).
- **I `item-rating`.**
  - Each item has an optional `rating`, a whole number from 1 to 5, none by default; an item
    stored before this change has none.
  - The item page shows `Rating: <n>/5`, or `Rating: none`, and has
    `<form method="post" action="/items/<id>/rating">` with `<select name="rating">` whose options
    are `""` (text `No rating`), then `1` to `5`; the current one is `selected`.
  - The list page shows `<n>/5` in the row of each rated item.
  - `POST /items/<id>/rating` (`rating`): `""` clears it, `1` to `5` sets it, 303 to
    `/items/<id>`. Any other value: 400, the item page with
    `Rating must be a whole number from 1 to 5.`, nothing saved. Unknown id: 404.
- **J `sort-list`.**
  - `GET /?sort=<order>`: `oldest` (id ascending; also when `sort` is absent or empty), `newest`
    (id descending), `title` (title A to Z ignoring case, ties by id). Any other value: 400, with
    `Unknown sort: <value>` (escaped).
  - The list page has `<nav class="sort">` with three links: `Oldest` (`/?sort=oldest`), `Newest`
    (`/?sort=newest`), `Title` (`/?sort=title`); the current one (`Oldest` when absent) has
    `aria-current="page"`, no other link of that nav has it.
  - The sort combines with the list page's other query parameters, when the page has some (in
    0.2.0, the status filter and the search): its links keep them, and their links keep the sort.
- **K `duplicate-url`.**
  - Adding an item (`POST /items`) whose URL is already another item's: 400, the list page with
    the values entered and the message `Already on the shelf:` followed by a link to the existing
    item (`href="/items/<id>"`, its title as the link's text); nothing added. Two URLs are the
    same when they are equal after trimming, ignoring the case of the scheme and the host and one
    trailing `/`. An item with no URL never clashes.
  - The same check on the edit form (`POST /items/<id>/edit`, released in 0.2.0), where an item's
    own URL is not a clash.

**The release CRs.** `release-v0-2-0` and `release-v0-3-0` follow `evals/kit/crs/release-v0-2-0`
in form. Their specification: the version (`0.2.0`, `0.3.0`); the scope, everything merged on
`main`; the procedure, `RELEASING.md` at the repository's root; the maintainer approves the notes
before they go anywhere (Q6; in an eval the operator is the maintainer). "Done when": the tag
`v<version>` is on the origin, a GitHub release `v<version>` holds that version's `CHANGELOG.md`
section, the version is in `pyproject.toml` and `src/shelf/__init__.py`, and
`uv run python scripts/release_check.py` ends with `release check passed` at the tag.

### 2. The hidden tests: `evals/kit/sandbox-judge/<slug>/test_judge_<slug with _>.py`

One folder per feature CR (11), each with one test file (a few at most), for example
`evals/kit/sandbox-judge/delete-item/test_judge_delete_item.py`. They are never under
`evals/kit/sandbox/` (they would enter the initial commit) nor under `sandbox-crs/` (setup copies
those into the workspace), and never pushed to the sandbox. Chantier's own `just test` does not
collect them (it runs in `skills/chantier/scripts/cli`).

Rules for every hidden file:

- It runs inside a clone of the sandbox, copied into its `tests/` folder: it uses the
  `client` fixture and the autouse `SHELF_DATA` fixture of `tests/conftest.py`, the standard
  library and pytest only, and builds its data through the HTTP routes (never the data file).
- It checks only what the CR's specification states: status codes, the headers named, the exact
  texts and attributes named, the presence or absence of a test's own unique titles (escaped), and
  order by the position of those titles in the page. It never compares a whole page. HTML is read
  with `html.parser` (a small parser class in the file) where an attribute or a tag's text is
  checked.
- It does not depend on another CR's feature, so every hidden file passes on the final `main` of
  a `full` run where all CRs merged.
- It fails on the base (at least one test fails) and passes on a correct solution.

What each checks:

| Slug | The hidden tests check |
| --- | --- |
| `delete-item` | delete answers 303 to `/` (`urlsplit(location).path == "/"`), the title is gone from `/`, the item page is 404, the other item stays; unknown id 404; `GET` on the delete path 405; two items, delete #2, add one: `/items/3` shows it and `/items/2` is 404; the item page holds a form with method `post` (any case) and action `/items/1/delete` |
| `edit-item` | the edit page's `title` input holds `Tom &amp; Jerry &lt;3&gt;` for the title `Tom & Jerry <3>`, and both inputs exist; a valid edit answers 303 to `/items/1` and the item page shows the new title, not the old; an empty title, a 201-character title and `ftp://x` each give 400 and leave the old title on the item page; unknown id 404 on `GET` and `POST`; the item page has a link `href="/items/1/edit"` |
| `status-filter` | `/?status=reading` shows the reading item's title and not the others; `/?status=` shows all; `/?status=lost` is 400 with `Unknown status: lost`; `/?status=<b>` shows `&lt;b&gt;`; the four links with their hrefs; `aria-current="page"` on `All` for `/` and on `Done` for `/?status=done`, and on no other filter link; `No items with this status.` when nothing matches |
| `json-api` | `[]` on an empty shelf; two items in id order with `id`, `title`, `url`, `status`, `added` (`\d{4}-\d{2}-\d{2}`); `url` is `null` with no URL; a status change shows; a title `<b>&` comes back raw; `/api/items/9` is 404 with `{"error": "not found"}`; `POST /api/items` 405; the content type starts with `application/json`; the list page has `href="/api/items"` |
| `stats-page` | the rows of `table.stats` read `To read 0, Reading 0, Done 0, Total 0` on an empty shelf, then `1, 1, 1, 3` after three items set to-read, reading, done; `/` and `/items/1` link to `/stats`; `POST /stats` 405; the page holds `shelf.__version__` |
| `csv-export` | an empty shelf gives exactly `id,title,url,status,added\r\n`; a title `Hello, "world"` reads back the same through `csv.reader`; rows in id order; `url` empty with no URL; the two headers; the list page has `href="/export.csv"`; `POST` 405 |
| `item-notes` | notes `line one\nline <two>` show as `line one\nline &lt;two&gt;` and saving answers 303 to `/items/1`; 2000 characters save; 2001 give 400 with `Notes are limited to 2000 characters.` and keep the old notes; unknown id 404; `/static/style.css` holds `pre-wrap`; a `textarea` named `notes` exists |
| `title-search` | `/?q=DUNE` finds `Dune Messiah` and not `Foundation`; a blank `q` shows all; `/?q=<i>` gives `value="&lt;i&gt;"` in the `q` input; no match shows `No items match "&lt;i&gt;".`; the form has method `get`, action `/` and an input `q` |
| `item-rating` | `Rating: none` by default; rating `4` gives `Rating: 4/5` on the item page, `4/5` on the list, option `4` selected; `""` clears it; `0`, `6`, `x`, `2.5` give 400 with the message and leave it unchanged; unknown id 404 |
| `sort-list` | with `banana`, `Apple`, `cherry` added in that order: `/` and `/?sort=oldest` give banana, Apple, cherry; `newest` gives cherry, Apple, banana; `title` gives Apple, banana, cherry; `/?sort=size` is 400 with `Unknown sort: size`; the three links; `aria-current="page"` on the current one only |
| `duplicate-url` | adding the same URL again gives 400, `Already on the shelf:` and a link `href="/items/1"`, and `/` does not show the second title; `HTTPS://Example.com/a/` clashes with `https://example.com/a`; `https://example.com/A` does not clash with `https://example.com/a`; two items with no URL are both added; a different URL is added (only the add route is judged) |

### 3. The judge: `evals/kit/judge.py`

Standard library only, POSIX and Windows. Called alone or by the audit:

```text
uv run --no-project python evals/kit/judge.py <repository> <ref> <slug> [<slug> ...]
uv run --no-project python evals/kit/judge.py --release <version> <repository> [<slug> ...]
```

`<repository>` is a git URL or a local path; `<ref>` a SHA-1 or a ref name. Exit codes: 0 pass,
1 fail, 4 not run (the clone, the fetch, the ref or `uv` failed; the tool's text is printed).

**A feature judge** (the first form):

1. Clone `<repository>` into a new temporary folder with `--no-checkout`, fetch
   `+refs/pull/*/head:refs/remotes/origin/pull/*` too (a GitHub PR's head stays reachable after
   its branch is deleted; on a repository with no such refs it fetches nothing), then
   `git checkout --detach <ref>`. A ref that is not there: not run, `head <ref> not found on the
   origin`.
2. Copy every `test_*.py` of `evals/kit/sandbox-judge/<slug>/` for each slug given into the
   clone's `tests/`. A slug with no folder: not run, `no hidden test for <slug>`.
3. Run `uv run --locked pytest -q -p no:cacheprovider tests/<the hidden files>` (the hidden
   tests), then `uv run --locked pytest -q -p no:cacheprovider` (the project's long gate, hidden
   files included), each with a 10-minute timeout and with `VIRTUAL_ENV` and `SHELF_DATA` taken
   out of the environment.
4. Print one line per run, `hidden: <pytest's summary line>` and `suite: <pytest's summary
   line>`, then `judge <slugs> at <sha7>: pass` (both runs exit 0) or `fail`. Remove the
   temporary folder (read-only git objects on Windows included).

**A release judge** (`--release`), at the tag `v<version>` of `<repository>`:

- the tag exists (`git ls-remote --tags`) and its commit is on `main`;
- at the tag: `pyproject.toml`'s version, `shelf.__version__` and the first `## ` heading of
  `CHANGELOG.md` are `<version>`; `uv run python scripts/release_check.py` ends with
  `release check passed`;
- the hidden tests of the slugs given pass at the tag (as above);
- when `<repository>` is the sandbox: `gh release view v<version> --repo
  gsemet/chantier-eval-sandbox --json tagName,name,body` succeeds, its name is `v<version>`, and its
  body holds each bullet of that version's `CHANGELOG.md` section. For any other repository this
  part prints `not run: not the sandbox` and does not fail the judge.

It prints one line per item and `judge release v<version>: pass|fail`.

### 4. The workspace: `evals/kit/setup.py`

`CAMPAIGNS` keeps `claude-planted` as it is and gets four sandbox campaigns: `full`,
`real-foreman`, `real-direct` and `copilot` (which replaces the staged `copilot`, its
`done-unknown-id` on the local forge). Each sandbox campaign lists its batches: the CRs in `open`
order, the release's item number, the CR added during the batch, the slots, the budget and, for
`real-direct`, `--direct`:

| Campaign | Batch | `open` items, in order | Release | Added during it | Slots | Budget |
| --- | --- | --- | --- | --- | --- | --- |
| `full` | 1 | A B C D E F G H L | `--release 9` | I | 4 | 40 |
| `full` | 2 | J K M | `--release 3` | - | 4 | 15 |
| `real-foreman` | 1 | A B C D E | - | - | 3 | 20 |
| `real-direct` | 1 | A B C D E, `--direct` | - | - | 3 | 20 |
| `copilot` | 1 | A | - | - | 1 | 3 |

`uv run --no-project python evals/kit/setup.py <campaign> <workspace>`, for a sandbox campaign:

1. **Preconditions** (exit with the reason, nothing created): `<workspace>` does not exist and is
   not inside this repository; `gh auth status` passes; the sandbox is at its base, by the same
   survey `sandbox.py reset` makes (`main` at `sandbox.json`'s `base`, no other branch, no tag, no
   open PR, no release). If it is not: `the sandbox is not at its base: run sandbox.py reset, then
   reset --yes`. Setup never resets and never pushes.
2. **The run's number:** 1 plus the highest `<n>` among the sandbox's PR titles that start with
   `[eval <n> ` (`gh pr list --repo gsemet/chantier-eval-sandbox --state all --limit 1000 --json
   title`), 1 when there is none. The date is the local date at setup, `YYYY-MM-DD`. The **prefix**
   is `[eval <run> <date> <campaign>]`, for example `[eval 4 2026-11-14 full]`.
3. **The clone:** `git clone https://github.com/gsemet/chantier-eval-sandbox.git <workspace>`; its
   `HEAD` must be the base (else exit 2). Then, in the workspace, `$CHANTIER init` (this checkout's
   CLI: `uv run --script <checkout>/skills/chantier/scripts/cli/chantier.py init`) and
   `uv sync --locked`.
4. **The frozen CRs:** each CR of the campaign (all its batches, and the added one) is copied from
   `evals/kit/sandbox-crs/<slug>/` to `<workspace>/.agents/changes/3-ready/<slug>/`. In each copy,
   setup appends to `03-change-spec.md`:

   ```markdown
   ## Eval run

   This CR runs in chantier's eval campaign `<campaign>`, run <run>, set up on <date>.

   - Every pull request this CR opens has a title that starts with `<prefix> `, followed by the
     title it would have anyway, for example `<prefix> feat: delete an item`.
   ```

   and, in a release CR's copy, one more bullet: `- A fix this release needs carries this section
   into its fix-<n>.md, so its pull request's title starts the same way.`
   This is where a run puts its PR-title convention: in the planning folder of the workspace,
   which the sandbox's git does not track, so the frozen commit never changes. The hidden tests
   are never copied.
5. **The run record:** `<workspace>.run.json`, next to the workspace (as the staged campaigns
   keep `<workspace>.origin.git` and `<workspace>.forge/`), UTF-8 without a byte-order mark:

   ```json
   {"campaign": "full", "run": 4, "date": "2026-11-14", "prefix": "[eval 4 2026-11-14 full]",
    "repository": "gsemet/chantier-eval-sandbox", "base": "<40-hex>",
    "chantier": {"version": "0.8.0", "commit": "<40-hex>", "dirty": false},
    "host": "claude", "crs": ["delete-item", "..."]}
   ```

   `chantier` is this checkout's (`__version__` of the CLI, `git rev-parse HEAD`, and whether
   `git status --porcelain` is empty): the checkout the plugin is installed from.
6. **It prints** the campaign, the run, the prefix, the workspace, the base, the CRs placed, and
   each batch's `open` line, ready to paste, with `--mode <mode>` left for the quick campaigns.

Setup writes no `.claude/settings.local.json` and no fake `gh` for a sandbox campaign: the agents
use the real `gh`. `claude-planted` keeps its staging exactly as today.

### 5. The audit: `evals/kit/audit.py --sandbox`

`--sandbox` replaces `--real`, which goes (with `EVAL_LINE` and the `porcelain-at-open.txt`
snapshot): no campaign runs on this repository any more.

```text
uv run --no-project python evals/kit/audit.py <workspace> --sandbox [--batch <id>] [--projects <dir>]
```

It reads `<workspace>.run.json` (absent: exit 2, `not a sandbox workspace`), runs on every host
(Copilot: the shared checks, the run and the judge, no scorecard), before `close --yes` as today.
Its output, in this order:

1. **`## The run`**, a table ready to paste in the report: the campaign, run and date; the PR
   prefix; chantier's version and commit at setup, and whether this checkout's commit now differs
   (a difference is printed, not a failed check); the sandbox's base, and whether the workspace's
   root commit (`git rev-list --max-parents=0 HEAD`) is that base; the batch, its `mode` and its
   steering (Foreman or direct) from `batch.json`, the host; **the models**: for the steering
   session and for each role, the models its transcripts used (`message.model` of the assistant
   records), with the agent count, for example `cr-driver: claude-sonnet-5-5 (9)`; on Copilot `not
   read`.
2. The facts and the agent tree, as today.
3. **The checks**: everything the staged mode checks today except the local forge's call log (the
   batch paused, each CR merged or cancelled, `3-done` and `6-trash`, STATUS.md, the main checkout
   with nothing outside `.agents/changes/`, the transcript checks with `real` false), and, from the
   real forge, read-only:
   - **J5:** each CR's PR (`gh pr view`): its title starts with the prefix; no auto-merge; checks
     green at its head; a merged one was merged into the default branch.
   - **C12:** every PR whose title starts with the prefix and that was merged after the batch's
     `created` is a PR of this batch; with a release, each merge of the release or a fix is
     recorded by an `order merged` of the Foreman (as `release_checks` does today).
   - **C11, J23** for a release, as `release_checks` does today, but the tag is read from the
     sandbox (`git ls-remote --tags`); **C20** is `not seen` when the release had no fix.
   - **J24** (rewritten, every mode): each `blocked` hand-back's reason starts with a hand-back
     word.
4. **`## The judge`**: one row per CR of the batch: the CR (number and slug), its PR, the head
   judged, the hidden tests' and the suite's summary lines, and `pass`, `fail` or `not run (<why>)`.
   A feature CR is judged at its recorded `head` in `batch.json` against the workspace's `origin`
   (`git -C <workspace> remote get-url origin`); when the forge's PR head differs, the row says
   so. A CR with no PR or no head, a cancelled CR and a CR with no hidden test are `not run`. Then
   one row for `main` on the origin at the audit's time with the hidden tests of every CR merged by
   this run (both batches for `full`'s second). A release CR is judged by the release judge with
   the hidden tests of every CR merged by this run before it. It ends with
   `Judge: <n> pass, <n> fail, <n> not run`.
5. The scorecard and the cost (`real_cost`, unchanged: the cost lines and the steering share),
   and below the table the judge's line.

The audit exits 1 on a failed check, an unknown rail, or a judge `fail`; `not run` is not a
failure. The judge marks no rail.

### 6. The runbooks

**Common to the sandbox campaigns**, written once in `evals/README.md` and referred to by each
runbook:

- **Preparation, before the run**, from this checkout, by the user in a terminal (these commands
  prepare the run; they are not steps of it): `uv run --no-project python evals/kit/sandbox.py reset`, read the plan,
  then `… reset --yes`; then `uv run --no-project python evals/kit/setup.py <campaign>
  <workspace>`, with `<workspace>` outside this repository, for example
  `../chantier-eval/<campaign>-<date>`. One run at a time on the sandbox: a reset ends any other.
- **The operator** is a new Code session of the Claude Desktop app opened on the workspace (not
  under Remote Control: it starts the Foreman's sessions), started with the runbook's prompt,
  which names the runbook by its absolute path in this checkout. It is the Chief of Staff and
  plays the user in full: the go after the plan, every merge, every answer, every approval, the
  release's confirmation, the injected CR, `pause` coming and the "close the batch". Nothing waits
  on the real user. `$CHANTIER` is `uv run --script "<this checkout>/skills/chantier/scripts/cli/chantier.py"`,
  run from the workspace.
- **A merge** is the user's: `gh pr merge <n> --repo gsemet/chantier-eval-sandbox --rebase`, alone,
  never chained; a refused merge (a conflict, a red check) merges nothing, and the steering session
  sees it as usual. Then `$CHANTIER order merged CR-<n>` and its line to the steering session. In
  parallel mode the operator merges in the order the CRs become ready; in series, in the series'
  order; in a stack, from the bottom up, as `chief-of-staff.md` says for the mode.
- **A question** (`blocked question:`): the frozen CRs leave none open, so a question is a
  finding; the operator answers `Follow the specification as written; where it is silent, choose
  the simplest behaviour and say so in the PR.`, records it in the CR's `02-answers.md`, and sends
  `$CHANTIER order note CR-<n> --note "answer: …"`.
- **A CR stuck** (the round limit, or blocked twice): the operator drops it (`order drop`), so the
  batch can pause; the report says why.
- **The audit** runs when the steering session reports `final` (the batch paused), before
  `close --yes`: `uv run --no-project python evals/kit/audit.py <workspace> --sandbox`, then
  `$CHANTIER cost --explain` and `$CHANTIER cost --by cr` from the workspace. Then the operator runs
  the `close` flow and `close --yes`.
- **The report** goes in `results/<campaign>-<date>-run<n>.md`, written in a worktree of this
  repository on its own branch, with its PR (the main checkout does not change during an eval).
  The sandbox is left as the run ends: its PRs and releases stay for inspection until the next
  reset.
- **The 10-message limit:** see `full` below; a quick campaign stays under it (the Foreman's
  start and at most one send per merge wave).

**`evals/full/RUNBOOK.md`** (new):

- What it proves: two batches end to end on a real forge, with merges and the rebases they cause
  (four slots, CRs that touch the same files), a CR injected into a running Foreman batch that
  the release then waits for, two releases by the project's own procedure (the operator confirms,
  approves the notes and each irreversible step, and the Foreman merges the release PR), and the
  judge on every CR and on both releases.
- Start: in the operator session, `/chantier:chief-of-staff Run the chantier eval campaign full:
  follow <this checkout>/evals/full/RUNBOOK.md.`
- Batch 1: `$CHANTIER open .agents/changes/3-ready/delete-item … .agents/changes/3-ready/title-search
  .agents/changes/3-ready/release-v0-2-0 --release 9 --mode parallel --slots 4 --budget 40
  --default-branch main` (the nine folders in the order of section 4); a new Foreman session.
- The user's turns, batch 1:
  1. The go once the plan is shown.
  2. At the first `ask ready` (the first CR handed back ready), before or with its merge:
     `$CHANTIER order add --note ".agents/changes/3-ready/item-rating"`, and its line.
  3. Each `ask ready`: the merge, `order merged`, its line.
  4. Once every other CR has ended, the release waits for the user's confirmation (`status`):
     `$CHANTIER order confirm CR-<L> --note "v0.2.0, nothing else"`, its line.
  5. A `draft` on the release's line in `status` (the notes): the operator reads it, checks it
     has one bullet per merged feature, leaves it as written; each `ask blocked CR-<L> approval:
     <action>` (the notes, the merge of the release PR, the tag, the GitHub release, as the
     procedure asks): `$CHANTIER order approve CR-<L> --note "<action>"`, its line. The Foreman
     merges the release PR itself.
  6. If the release needs a fix (`ask blocked CR-<L> fix: …`): `$CHANTIER order grant CR-<L>
     --note "fixes=on budget=40"`, then `$CHANTIER order add --note "<fix file>" --fix-for CR-<L>`,
     their lines (as `claude-planted`'s turn 9).
  7. `final`: the audit, the cost, `close --yes`.
- Batch 2: `$CHANTIER open .agents/changes/3-ready/sort-list .agents/changes/3-ready/duplicate-url
  .agents/changes/3-ready/release-v0-3-0 --release 3 --mode parallel --slots 4 --budget 15
  --default-branch main`; a new Foreman session; the same turns with `v0.3.0` and no added CR.
- Expected: every CR `merged` (or `cancelled` with its reason), the tags `v0.2.0` and `v0.3.0`
  and their GitHub releases on the sandbox, the injected CR merged before the release of batch 1
  started (C2), the release taken only on the confirmation (C18), no irreversible action without
  a `go` (C11), the judge `pass` on every merged CR, on `main` and on both releases.
- **Living with the 10-message limit.** This campaign goes past it, and its report says so.
  The Foreman's messages past its tenth are lost: the operator follows the host's notes of each
  of the Foreman's turns and `$CHANTIER status` / `$CHANTIER asks`, and acts from there. The
  operator records every order with `$CHANTIER` before sending, and sends at most one message per
  wave, holding every line recorded since its last send (merges that come together go in one
  message). Expected sends: about 9 to 12 in batch 1 (the Foreman's start, the added CR, the merge
  waves, the confirmation, the approvals) and 6 to 8 in batch 2. Past the limit, a refused send is
  reported (J15) and never sent another way; the order is already recorded, and the Foreman
  reads it at its next heartbeat wake. If the Foreman's heartbeat has already ended (`status`
  says `heartbeat stopped`) while an order waits, the user types one line, `ping`, in the
  Foreman's session (Q8); the report counts it as the run's one human step. It is the only
  possible human step during a `full` run.
- Cost and time: the budgets cap them ($40 and $15); the first run measures them, and this
  runbook's figures are written from its report.

**`evals/real-foreman/RUNBOOK.md`** (rebuilt): the 5 CRs of the quick set on the sandbox, in the
mode chosen at launch, steered by a Foreman. Start: `/chantier:chief-of-staff Run the chantier eval
campaign real-foreman in <stack|parallel|series> mode: follow <this checkout>/evals/real-foreman/RUNBOOK.md.`
Open: `$CHANTIER open .agents/changes/3-ready/delete-item .agents/changes/3-ready/edit-item
.agents/changes/3-ready/status-filter .agents/changes/3-ready/json-api
.agents/changes/3-ready/stats-page --mode <mode> --slots 3 --budget 20 --default-branch main`.
The operator plays the user in full, merges included, as in "Common" (Q7). It loses: the inbox picks, the grill, the
"Nothing merges" section, the eval first line of the PR body, the `porcelain-at-open.txt` step,
the two prepared CRs, and "Each PR is merged or closed within the day". The mode is written in the
report, so runs of one mode compare with each other and the modes with each other.

**`evals/real-direct/RUNBOOK.md`** (rebuilt): `real-foreman` with `--direct` on `open`, and the
start `/chantier:chief-of-staff direct Run the chantier eval campaign real-direct in <mode> mode,
in direct mode: follow <this checkout>/evals/real-direct/RUNBOOK.md.` It keeps its section "What
it proves on top of real-foreman" and the note that the 10-message limit does not apply (no
Foreman session). Its first run follows this CR.

**`evals/copilot/RUNBOOK.md`** (updated): setup `setup.py copilot <workspace>`; the CR `delete-item`;
open `$CHANTIER open .agents/changes/3-ready/delete-item --slots 1 --budget 3 --default-branch
main`; the merge with `gh pr merge` on the sandbox as in "Common"; the audit with `--sandbox`. The
first bullet of "Still to fill in" (the local forge's environment for Copilot sessions) goes: the
agents use the real `gh`.

### 7. Docs

**`evals/README.md`**:

- The intro: the staged campaign (`claude-planted`) runs on `tasks-cli` with a local forge; the
  real campaigns (`full`, `real-foreman`, `real-direct`, `copilot`) run on the sandbox (shelf),
  reset to its recorded base before each run, with frozen CRs and the judge.
- The campaigns table: a `full` row (two batches, 9+1 then 2 feature CRs with a release each,
  Foreman, the operator plays the user; cost: the budgets, measured by the first run; "not run
  yet"); `real-foreman` and `real-direct` rewritten (5 frozen CRs on the sandbox, mode at launch);
  their "Last run" says the campaign moved to the sandbox and keeps the 2026-11-12 link as "on
  this repository, before the sandbox"; `copilot`: one frozen CR on the sandbox, real `gh`.
- "Which campaign, after a change": the quick campaigns are now 5 CRs ("one real campaign with
  one small CR" becomes "one quick campaign"); before each release, `full` runs with both quick
  campaigns (Q9); the rest unchanged (Q3).
- "Run a campaign": the staged steps stay for `claude-planted`; a new subsection "A sandbox
  campaign" holds the "Common" text of section 6; the run's number and prefix are explained
  (a run that opened no PR leaves its number free for the next).
- "The host's limits": one line pointing to `full`'s way of living past the limit.
- "The report": a section `## The run` after the verdict (paste the audit's table: campaign, run,
  date, prefix, chantier version and commit, base SHA-1, mode and steering, host, models) and the
  judge's line in "Numbers"; for `full`, one report for both batches, with one scorecard where a
  row is `seen, wrong` if it was wrong in either batch, and the cost per batch and in total.
- "The kit" table: rows for `kit/sandbox-crs/` (the frozen CRs), `kit/sandbox-judge/` (the hidden
  tests, never in the workspace or on the sandbox), `kit/judge.py`; `kit/setup.py` and
  `kit/audit.py` rows updated (`--sandbox` instead of `--real`).

**`evals/SCORECARD.md`**:

- The intro names the Claude campaigns `full`, `real-foreman`, `real-direct`, `claude-planted`.
- "where seen": `full` is added to every row that names `claude-planted`, `real-foreman` or
  `real-direct`, except C13 (direct mode only).
- J5: `a CR's PR opens as a draft and turns ready only on the default branch, with no auto-merge
  and CI green at its head (a release PR opens ready); in a sandbox campaign its title starts with
  the run's prefix`; how marked: `audit (sandbox): gh pr view of each PR: title prefix, base, auto-merge, checks at the head`.
- J24: `a blocked hand-back's reason starts with one of the hand-back words (…)`, where seen: every
  Claude campaign; how marked: `audit: every blocked hand-back of the log`.
- C11, C12, C14, C16: their "how marked" says the audit marks them in the staged and the sandbox
  modes.
- Below the table, a third line: `**Judge:** the audit's judge line (pass, fail, not run), for the
  sandbox campaigns`.

**Outside `evals/`**: `CONTRIBUTING.md`'s eval bullet says "one quick campaign (`real-foreman` or
`real-direct`, five frozen CRs on the sandbox)" instead of "one real campaign with one small CR";
the root `README.md`'s line listing the campaigns adds `full`.

### 8. One structure test

In `skills/chantier/scripts/cli/tests/test_structure.py`, one fast test: load `evals/kit/setup.py`
by its path and, for each sandbox campaign of `CAMPAIGNS`, every CR it names (batches and added
CR) has `evals/kit/sandbox-crs/<slug>/` with `intake/request.md`, `01-intent.md`, `02-answers.md`
and `03-change-spec.md`; every feature CR has `evals/kit/sandbox-judge/<slug>/` with at least one
`test_judge_*.py`; no `test_*.py` is under `evals/kit/sandbox-crs/`; `full` names 13 CRs, the
quick campaigns the same 5, all among `full`'s. No network, no git.

## Out of scope

- Running any campaign: the real runs (`real-direct` first, then the others) come after this CR,
  and the first `reset --yes` after a campaign proves the reset's clean-up (`eval-sandbox-app`'s
  evidence item 7), recorded in that run's report.
- The release v0.9.0 (`release-v0-9-0`, in the inbox).
- `claude-planted`, `kit/fixture/`, `kit/crs/`, `kit/forge.py`, `kit/merge.py`: unchanged.
- The sandbox project itself, `sandbox.py`, `sandbox.json` (`eval-sandbox-app`'s).
- The plugin, the cards, the CLI, `hooks/`, `types/`, the scenario.
- Reference solutions of the frozen CRs: written for the evidence only, in scratch folders, never
  committed.
- A Copilot transcript audit and a Copilot scorecard.

## Evidence

The CR changes the eval kit and the docs, plus one structure test, which is neither the CLI, a
card nor the scenario: AGENTS.md asks for no `just scenario`, and `just mod` is not concerned (no
`hooks/` or `types/`). The long gate is `just check`. No paid campaign runs in this CR. Every
scratch folder is outside this repository; the main checkout does not change.

1. **`just check` passes** at the pushed head (the new structure test included).
2. **The hidden tests are right.** In a scratch repository made by `sandbox.py build <tmp>/ref`:
   - for each of the 11 feature CRs, `judge.py <tmp>/ref <base> <slug>` prints `fail` (exit 1):
     every hidden file fails on the base;
   - the Driver writes a reference solution of each feature CR on its own branch (a coder of
     this CR's round may write them, from the frozen specification only), and `judge.py <tmp>/ref
     <branch> <slug>` prints `pass` for each, with the project's suite green;
   - the 9 references of batch 1 combined on one branch in `open` order (A to H, then I), then J
     and K on top: `judge.py` with all their slugs passes at each of the two heads.
   Each command is quoted with its summary lines.
3. **The release judge.** `judge.py --release 0.2.0 https://github.com/gsemet/chantier-eval-sandbox.git`
   against today's sandbox prints `fail` (no tag `v0.2.0`). On the scratch repository, a release
   commit made by `RELEASING.md` steps 1 and 3 on top of the batch-1 branch, tagged `v0.2.0`
   locally: `judge.py --release 0.2.0 <tmp>/ref <A … I>` passes, its GitHub part `not run: not the
   sandbox`.
4. **The workspace.** With the sandbox at its base (`sandbox.py reset` prints `nothing to do`):
   - `setup.py full <scratch>/full` prints run 1 (or the next number), the prefix, the 13 CRs and
     the two `open` lines; `<scratch>/full.run.json` holds the fields of section 4; each copied
     `03-change-spec.md` ends with its "Eval run" section; no `test_judge_` file is anywhere in
     the workspace; `git -C <scratch>/full status --porcelain -uall` shows only paths under
     `.agents/changes/`; `HEAD` is the base;
   - in that workspace, `$CHANTIER open` with batch 1's line, then `$CHANTIER status` shows nine
     CRs queued, the release waiting for the others; `$CHANTIER order add --note
     ".agents/changes/3-ready/item-rating"` then `status` shows the release waiting for it too. No
     `take`, no agent;
   - `setup.py real-foreman <scratch>/rf` and `setup.py copilot <scratch>/cp` place 5 and 1 CRs;
     `setup.py full <a folder inside this repository>` is refused.
   Nothing is pushed to the sandbox: the workspaces are deleted afterwards.
5. **The audit's judge on made-up heads.** A scratch workspace cloned from `<tmp>/ref`, with a
   `<workspace>.run.json` and a `4-batch/batch.json` written by hand there (never in a real
   batch) naming three CRs: one whose `head` is a reference solution, one whose `head` is the base,
   one with no head. `audit.py <workspace> --sandbox` prints `## The run` and `## The judge` with
   `pass`, `fail` and `not run`, and exits 1. The forge checks that cannot reach a PR print `not
   seen`; that is expected here. The judge section and the run table are quoted.
6. **The runbooks' free commands** (`reset` plan, `setup.py`, `open`, `status`, `order add`,
   `judge.py`, `audit.py --sandbox`) were each run once in items 2 to 5; the paid steps (the
   Foreman, the Drivers, the merges and releases on the sandbox) are not, and the PR says so.

The PR body's Deliverables quote items 2 (a summary table of the 11 fail/pass pairs and the two
combined runs), 3, 4 and 5.
