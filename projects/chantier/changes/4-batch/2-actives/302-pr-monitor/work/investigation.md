# Investigation: CR-302, the PRs page of the web board

Read only. Worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-302`. Paths below are
relative to `skills/chantier/scripts/cli/src/chantier/` (call it `SRC`) unless they start with a
repository folder. `$CHANTIER rules` listed: AGENTS.md, CONTRIBUTING.md, README.md,
`docs/use-cases-direct.md`, the Chief of Staff card, `scenario/README.md`, `evals/*`,
`docs/release-process.md`, and the surface's AGENTS.md and autosync guidelines. What touches this
work is AGENTS.md (board bullet, no network, tests budget, `just check`, scenario gate) and
CONTRIBUTING.md lines 93-99.

## 1. Files and entry points

### Server (`SRC/board/`)

- `routes.py`: `ROUTES: list[tuple[str, str, Handler]]` (verb, regex, handler). A handler is
  `handler(ctx: Context, req: Request, *groups) -> Reply`. It ends with `*write_api.ROUTES,
  *autosync_api.ROUTES`; add `*prs.ROUTES` there. `_judged` (key, method, write rule, then
  `_dispatch`) wraps every route, and turns `OSError/ValueError/KeyError/ChantierError` into a 500
  `"the record could not be read just now"`: the new handler must catch the forge's errors itself
  and answer 200 with `error`.
  Helpers to reuse: `_found(ctx, project_id) -> Project | None`, `_unknown() -> Reply` (404),
  `_state_of(ctx, project, ask) -> (state_dict, fingerprint)`.
  File is 190 lines; `routes.py` has no cost-style per-project cache, so the new module is right.
- `reply.py`: `as_json(data, status=200, headers=None) -> Reply`, `text(status, line)`. Every answer
  gets `X-Chantier-Now` in `handle`. `all_headers()` sets `Cache-Control: no-store`.
- `context.py`: `Context` dataclass (`projects, key, seats, version, stop, cache, last_push,
  _lives, _lock`), `Request(method, path, query, headers (lower-case names), body)`.
  `Context.live(project)` makes a per-project object under `_lock`: the model for a per-project
  forge cache. **Do not import a `board.prs` module from `context.py` if `prs.py` imports
  `Context`** (`test_code_targets.py` fails on an import cycle). Put the cache class in a module
  that does not import `context` (as `costs.Live` does) and add one field plus an accessor to
  `Context`.
- `costs.py`: `Live` is the pattern to copy: `threading.Lock`, `time.monotonic()` for the age.
  **Use `time.monotonic()` for the 10 s rule, not `clock.now()`** (`--clock` pins `clock.now()` for
  the docs demo; a fixed clock would freeze the cache).
- `state.py`: `project_state(project_id, repo, surface, live)`. It reads
  `folders = repo.batch_folders()`, `d = read_batch_json(folders[0] / "batch.json")`,
  `apply_batch_settings(repo, d)`, `events = read_events(folders[0])`, `_batch(...)`. The
  `_history(changes)` helper (module-private) lists the `batch-*.json` records newest first;
  `state["history"][0]["id"]` is the last batch. For the route, either call
  `routes._state_of(ctx, project, ask=False)[0]` (it is cached by fingerprint, gives
  `batch.crs`, `batch.merge_order`, `batch.state`, `history`, `now`) or read through
  `read_batch_json` + `crs.cr_rows`. **Smallest: call `_state_of(..., ask=False)`** (no live-cost
  side effect) and work from its dict; `routes._state_of` is private to `routes.py`, so either
  move the handler into `routes.py` (spec allows it if it stays short; it will not, with the
  GraphQL part) or import `project_state` and call it directly (cheap on 11 CRs; no cache).
  Note: `state["batch"]["state"]` is the batch status (`running`/`paused`); the batch dict
  has `id`, `mode`, `state`, `crs`, `merge_order`, `default_branch`.
- `crs.py`: `cr_rows(repo, d, events)`. A row has `cr, title, state (CR status), pr (link_of(c.pr),
  http(s) only, else None), kind ("fix"/"release"/None), to_review (bool), branch, merged_at,
  folder, order, ...`. `_on(d, repo, branch) -> str` is **private** and maps a branch to the CR
  whose branch it is (`{x.branch: x.id for x in d.crs if x.branch}.get(branch, branch)`): either
  import it as `crs._on` (a private name across modules; there is precedent only inside `crs.py`)
  or rename it `on_branch` in a one-line change. With the state dict alone (no `BatchRecord`),
  the same mapping is `{c["branch"]: c["cr"] for c in batch["crs"] if c["branch"]}.get(branch,
  branch)`: three lines, no import, matches the spec ("the same mapping").
  `merge_order(d, rows)` only lists CRs with `to_review`; the spec's "merge order first, then the
  other CRs in the batch's order" is `batch["merge_order"]` then the rest of `batch["crs"]` (already
  sorted by `order`).
- `projects.py`: `Project(id, repo)`, `Projects(home, surface, others)`, `.get(id)`, `.all()`.
- `guard.py` / `key.py`: the key travels as the `x-chantier-board-key` header or the
  `chantier_board` cookie (`key.HEADER`, `key.COOKIE`); without it `_judged` answers 401 with
  `guard.NEEDS_KEY`. A `GET` route needs nothing else.
- `write_api.py`: `ROUTES` is a list of `("POST"|"PUT", regex, handler)`; the model for the new
  module's `ROUTES = [("GET", r"/api/projects/([^/]+)/prs", prs)]`.
- `app.py`: Starlette; `handle` runs in `run_in_threadpool`, so **two requests run at once**: the
  forge cache needs a per-project lock held across the forge call (the second caller waits and
  then gets the same read: "two calls within 10 s, one forge call").
- `command.py` builds `Context(projects, KeyFile(key_path(projects.home)), seats, __version__,
  stop)` (line 92): adding a field with a default keeps this line unchanged.

### Forge helpers (`SRC/commands/`)

- `forge_stack_gh.py`: `PR_LINK` regex, `gh(args: list[str], host: str) -> Any` (finds `gh` with
  `shutil.which`, runs `gh api [--hostname host] *args`, returns `json.loads(stdout)`; raises
  `ChantierError(..., EXIT_EXTERNAL)` for "not found on PATH", a non-zero exit, non-JSON),
  `pr_parts(pr: str) -> tuple[str, ...]` -> `(host, owner, name, number)` for GitHub,
  `(host, project_path, "", iid)` for GitLab, refuses anything else with `NEITHER`
  (`EXIT_PRECONDITION`).
- `forge_stack_gitlab.py`: `GITLAB_LINK` regex, `glab(path, host, method="GET", fields=None)`.
- `forge_base.py`: `pr_state(link) -> (base, draft)`, `read_state(link)`, the model for "choose the
  forge from the link's shape": `if GITLAB_LINK.match(link): ... else: ...`.
- The "not all in one repository" refusal is a **literal inside** `forge_stack_gh.unstack_rows`
  (line 145: `"the batch's PRs are not all in one repository"`; `forge_stack.py:59` says "the stack's
  PRs..."). To answer "the same refusal text" without copying it, lift the literal to a
  module constant (e.g. `NOT_ONE_REPOSITORY` in `forge_stack_shared.py`) and use it in both places;
  a one-line edit that changes no behaviour of `forge-stack`.

Gaps in the existing runners (the page cannot just call them as they are):

1. `gh()` puts the whole argv in the error text (`gh api graphql -f query=<the query>: ...`), so
   the page's "forge's own message on one line" would hold the query. Catch `ChantierError` and
   keep `str(e).split(": ", n)`-style tail, or add a small `graphql(args, host)` sibling next to
   `gh()` that shows `gh api graphql: <stderr>`.
2. `glab()` adds `--method GET` as soon as `fields` is given and uses `-f k=v`; for GraphQL the
   call is `glab api graphql -f query=...` (a POST). With `method="GET"` and a field it gets
   `--method GET`, which GitLab's GraphQL endpoint refuses. A GitLab GraphQL call needs its own
   small runner, or `glab()` gets a `method="POST"` call (then argv has `--method POST`, which the
   spec's "no `-X POST`" test bans literally). See risk R3.
3. Neither runner has a timeout (`subprocess.run(... check=False)` with no `timeout`). A hung `gh`
   holds the per-project lock and one threadpool worker for every page. The new call should pass a
   timeout (a wrapper, not an edit of the shared runners).
4. Both read `shutil.which("gh"/"glab")` and the user's login: the board inherits the environment
   of whoever started it (the Chief of Staff's shell). No change needed; say so in the docs.

### Front end (`SRC/board/web/`)

- `js/views/registry.js`: `VIEWS` array of `{id, icon, word, module, count?(state), overview?}`;
  `entry`, `moduleFor`, `countOf` (only when `state.project !== ALL && state.data`). `main.js` calls
  `configure(ids(), overviewIds())`. Add after `batch`:
  `{ id: 'prs', icon: <new>, word: 'nav.prs', module: prs, count: (state) => crsOf(state.data?.batch).filter((c) => c.pr && c.state !== 'merged').length || null }`.
  Note: `count` returning 0 renders "0" (the sidebar shows `n == null ? '' : <span class="n">`),
  while the spec says "nothing when there is no batch": `crsOf(undefined)` gives `[]`, so write
  `batch ? n : null` to keep "no batch -> nothing".
- `js/ui/sidebar.js` (`navigation`, `item`) and `js/ui/bottombar.js` draw every `VIEWS` entry with
  `data-view`, `data-key="nav-<id>"` / `"bnav-<id>"`: no change. The phone bar gets a 6th button
  (check `css/shell.css` for the bottom bar's layout).
- `js/ui/icons.js`: `PATHS` has no PR icon; add one (`pr:`), or reuse `batch`.
- `js/ui/host.js` `show(root, state)`: mounts the module once per `project|view`, repaints with
  `view.render(state)` on every store update (markup-diffed by `core/paint.js`), calls
  `view.mount(root, state)` once (returns the cleanup) and `view.after(root, state)` on each paint.
  The 10 s forge loop belongs in `mount` (started on mount, stopped by the returned cleanup, so
  "only while it is the view shown" is free), with its result stored in the store.
- `js/core/store.js`: single `data` object, `snapshot()`, `update(patch)`, `subscribe`. Add a field
  (e.g. `prs: null`, `{rows, read_at, error, all_done, batch, ...}` plus the device time of the
  last good read). `js/core/router.js` `reset` object clears per-project fields when the project
  changes: add `prs: null` there.
- `js/core/api.js`: the only module that calls `fetch`; `get(path, etag)`, `route(id, path)`,
  `base(id)` private. Add `export const prs = (id) => get(\`${base(id)}/prs\`);`. `get` throws
  `AskError(status)` on a non-OK; the forge's failure is a 200 with `error`, not an HTTP error.
- `js/core/refresh.js`: the 5 s record loop: `start()`, `reload()`, `unreachable`; visibility rule
  `document.visibilityState === 'visible'` plus a `visibilitychange` listener that asks at once.
  Leave it unchanged; copy the visibility rule into the new feed. The new feed needs a second
  timer (10 s) and the restart rule (section 3): on each store update, if
  `state.data.batch.crs` holds a CR with a PR whose number is not in the last `prs.rows` and the
  loop is stopped, start it again.
- `js/core/format.js`: `age(iso, nowIso)` (server instant, empty when unknown), `span`, `hhmm`,
  `prNumber(url)`, `safeUrl(url)`, `usd`. Use `age(read_at, state.prs.now)` ("read 4 s ago") with
  the **forge answer's own `now`**, not `state.now` (which only moves on the 5 s record read).
- `js/model/semantics.js`: `crsOf(batch)`, `isFix`, `isRelease`, `mergedAt`, `vstate`, `baseOf`.
  `js/views/batch-pr-card.js` exports `prCard`, `mergedCard`, `bindGateLinks` and private
  `shell`, `kindTag`, `folder` (all non-exported): for the link rule and the kind tag reuse the
  pattern (`safeUrl(c.pr)`, `kindTag`); `kindTag` and `folder` would have to be exported to be
  reused (two `export` keywords) or rewritten in four lines. `js/ui/open.js`: `bindOpen(root)`,
  `opener(crKey(c), 'fold-')` (folder icon opens the CR's panel), `js/model/targets.js`
  `crKey`. `js/ui/parts.js`: `empty(text)`, `kpi`, `meter`, `dot`.
- `js/views/costs.js` + `costs-action.js`: the closest model: a view with its own server route, a
  `state.recomputing` flag, `mount` returning a cleanup that unbinds, and a polling loop
  (`untilDone`).
- i18n: `js/i18n/en.js` (254 lines) and `fr.js` (255) hold `nav.*`, `prs.*`; extra keys come from
  `en-board.js`/`en-write.js` spread into `en.js` (`import board from './en-board.js'`). New words:
  `nav.prs` in `en.js` and `fr.js` (a test checks the keys of `en.js` and `fr.js` themselves are
  equal, regex `^\s*'([\w.]+)':` over the two files only), and the page's words in a new
  `en-prs.js` / `fr-prs.js` merged in the same way. **The `prs.` prefix is taken** (the Batch
  view's columns: `prs.review`, `prs.none`, `prs.merged`, ...): use another prefix (`pv.`).
  `t(key, params)` fills `{name}` holes; `tn(key, n)` takes `<key>.one`.
- CSS: `css/views/prs.css` linked in `index.html` after `css/views/batch-prs.css` (the test
  `_reference_problems` checks each link exists). `batch-prs.css` uses `.batch .prs`/`.prcol`:
  use a distinct root class (`.prview`). Rules from `test_code_targets.py`: CSS <= 300 lines,
  nesting <= 3, **no colour outside `tokens.css`** (use `var(--green)`, `var(--blue)`, `--tint-*`,
  `--line`, `--radius`, `--space-3`), no id selector, no inline style/script in `index.html`.
  JS files <= 300 lines each; `registry.js` is 55 lines.
- Biome (`just lint`) checks `board/web`; the code style: two spaces, single quotes, `html\`...\``
  tagged templates (`core/dom.js`: `html`, `delegate`, `raw`, `setHtml`, `$`).

### Tests and scenario

- `tests/test_board.py`: **has no route test**; its docstring says "The behaviour (key, guard,
  state, files, costs, seats) belongs to `just scenario`". It checks the module list (`MODULES`,
  add `"prs"` if the module is new), lazy imports, shipped frame files, autosync/join
  subprocess cases. So the spec's in-process tests of `GET .../prs` need a **new fixture** and
  probably a new file (`tests/test_board_prs.py`) so `test_board.py` stays readable.
  Ingredients that exist: `conftest.repo` (a copy of a git repo with `.agents/changes`, chdir'd,
  env cleaned), `conftest.chantier` (in-process `main`), `batch_helpers.open_batch(repo,
  chantier, monkeypatch, *titles, args=(), seat=True) -> list[str]` (opens a batch, as the
  Foreman), `batch_helpers.record(repo)`, `write_record(repo, data)` (edit `batch.json` directly to
  set `pr`, `pr_draft`, `status`, `branch`, `mode`), `changes(repo)`. To call the route:
  `repo_obj = Repo.find(readonly=True)` (cwd is the repo), `projects = Projects(repo_obj, None,
  [])`, key = `key.load_or_create(repo_obj)` (writes `<git dir>/chantier/board.json`),
  `ctx = Context(projects, KeyFile(key_path(repo_obj)), Seats(projects), "t", lambda: None)`,
  `req = Request("GET", f"/api/projects/{projects.home_id}/prs", {}, {"x-chantier-board-key": key})`,
  `reply = routes.handle(ctx, req)`; `json.loads(reply.body)`. No existing test stubs `gh`.
  **Stub at one seam**: give `prs.py` one module-level function that runs the query (e.g.
  `read_forge(host, owner, name, numbers) -> dict` or `run_query(argv)`) and monkeypatch it with a
  counter; a second, small test of the argv (no `mutation`, no `-X`, no `PATCH/PUT/DELETE`) calls
  the argv builder directly. Parametrize with `pytest.mark.parametrize` (the project's habit).
  Budget: `just test` at most 30 s above 18.5 s; each case builds a repo copy (`open_batch` with
  four titles costs a few CLI calls); one batch fixture per module-scoped copy is cheaper than one per
  case: read the forge payload variations through the monkeypatch, keep the record fixed.
- `tests/test_code_targets.py`: py files <= 400 lines, functions <= 50 lines, no import cycle,
  JS <= 300, CSS <= 300, no colour outside tokens, `en.js`/`fr.js` key parity.
  `pyproject.toml` ruff: max-complexity 10, max-args 5, max-branches 12, max-returns 6, line 100;
  mypy strict-ish on `skills`. The row builder (Q6/Q9/Q10 judgement) must be split in small
  functions (state of one PR, ready, disagrees).
- `tests/test_startup_manifest.py`: measures startup bytes of cards (`chief-of-staff.md` is a
  reading of the manifest). The cards edit is two short lines (line 42 table row, line ~1185 Tips
  example); run `test_startup_manifest.py` after.
- `tests/test_scenario_coverage.py`: every bullet of `scenario/README.md` under `## Coverage`
  must end with `(unit: <key of UNITS>)` or `(test: file::name)`: the new surface-board bullet
  needs `(unit: surface-board)`; any new test must be named exactly.
- `scenario/fake_gh.py`: dispatches on `args[:2]`/regexes of `args` against a JSON state file
  (`FAKE_GH_STATE`), logs each argv to `<state>.calls`. State keys now: `next_pr`, `bases`
  (number -> base), `drafts` (list), `stacks`, `heads`, `extensions`, `merge_refused`,
  `pull_read_refused`, `patch_refused`... There is **no PR store**; `pr merge` only prints. A
  `["api", "graphql", "-f", "query=..."]` call hits the final `else` ("unsupported", exit 1).
  Add one branch (before the `else`) that answers the batch's query from a new `prs` map
  (`number -> {state, draft, mergeable, base, merged_at, closed_at, checks...}`), defaulting a PR
  with no entry to the `bases`/`drafts` data, so existing units keep their behaviour. The query's
  numbers must be parsed from argv (aliases `pr<N>`), so the fake needs the alias convention the
  real query uses. `gh()` calls `gh api graphql`, never `-X`.
- `scenario/fake_glab.py`: `glab api graphql` is rejected today (`path` must start with
  `projects/`); optional per the spec.
- `scenario/run_scenario.py`: unit `"surface-board": (250, ["github"], ["remote_board",
  "external_surface", "cr_summary"])`; budget 250 s against 196-236 s measured in README's
  table: **there is little slack**: keep the new steps in-process cheap (no extra `w.start`; no
  sleeps), or raise the budget in the same change and README's table. `remote_board(w)` (line
  1442) opens a direct batch with 4 CRs and a seat (`seat take s-1`, `foreman set uuid-chief
  --epoch 1`), starts a board with `board("board", "--host", "127.0.0.1", "--port", 0, "--seat",
  "s-1")`, `Link(line)`, `port`, `jget(port, link, path) -> (code, headers, json)`, `fetch(...)`,
  `folder_state(w.state)` and the `before` snapshot (step "7. nothing written" asserts the
  planning folder is unchanged since step 5). `driver_round(w, one, ...)` already opens a PR for
  `one` through `ship` (`open_pr` -> `https://github.com/acme/demo/pull/<n>`, numbers start at
  40, `OPENED[cr]`), so **one CR of that batch has a PR for free; the others (`two` is
  blocked, `three`/`four` queued) have none** and need `ship` (needs a started Driver and
  commits) or a direct `edit_cr`/record write to get a PR. Placing the new steps before step 7
  makes them part of the "nothing written" proof; the `order merged`/`order add` steps write the
  record, so they go after step 7 (or a new `# 6b` followed by their own before/after
  `folder_state`). The board child gets `w.env` whose PATH has the fake `gh` first, so the
  board's `gh api graphql` call reaches `fake_gh.py` with no change to `BoardProc`. Helpers to
  copy: `forge_draft(w, link, draft)`, `forge_base(w, link, base)` (they rewrite `w.gh_state`);
  add `forge_pr(w, link, **fields)` in the same style. `forge_calls(w)` reads `.calls`.
  The parallel unit's check at `run_scenario.py:1231` (only the agents called the forge) is
  unchanged (no board there).
- `scenario/README.md` lines 262-268 are the surface-board board bullets (the autosync one ends
  `(unit: surface-board);`): add the PRs-page bullet after it.

### Docs and rules text

- `AGENTS.md` lines 29-37: the board bullet (`One named exception: chantier board ... it never
  edits a batch and never messages an agent; it takes its dependencies like the rest of the
  CLI and knows no role.`). Line 14: `the CLI needs no network once uv's cache holds its packages`
  inside the "plugin must work with no setup" bullet: add ", except the board's PRs page
  (below)". Insert the spec's quoted sentence after "never messages an agent;".
  Also line 33-34: "The CLI's scope... The rest of the CLI keeps no git write" is not touched.
  One more sentence in AGENTS.md says the agents do the forge: "The agents do the work, git and
  the forge included": the exception reads as the board's own, as spec says.
- `CONTRIBUTING.md` lines 93-99: same paragraph ("never edits a batch and never messages an
  agent, takes its dependencies like the rest of the CLI ..."); insert the same words (the spec
  wants the same wording). Line 84 says the CLI has "no forge command: the agents have git, gh
  and glab": the exception sits beside it, so check this sentence is not contradicted ("no forge
  command" is about commands; `board` is a server): leave it, or add "(the board's PRs page reads
  the forge, read-only)".
- `docs/web-board.md`: line 4 intro ("It never touches a batch."), views `### Batch` (line 30) to
  `### Kanban` (line 41): insert `### PRs` between them? The spec says "after `### Batch`" under
  "## The views"; then "## Starting the board" (line 108) gets the `gh`/`glab` login + network
  sentence. No picture (spec). `docs/boards.md` line 3/70 and `README.md` 208-217 mention the
  web board's views in general terms: no change needed.
- `skills/chantier/references/chief-of-staff.md`: line 42 (the "board on my phone" row of the
  triggers table) and line 1185 (the Tips example under "After a status") are the two board
  mentions the spec names. Touch only those two lines.
  `skills/chantier/references/hosts/claude-code.md:611` has a table row for the remote board:
  not named by the spec; leave.

## 2. The smallest change that meets the specification

Server:

1. `board/prs.py` (new, <= 400 lines; likely split in two: `prs.py` = route + row judgement,
   `forge_read.py` = the GraphQL text, argv, runner and parse). Contents:
   - `ROUTES = [("GET", r"/api/projects/([^/]+)/prs", prs)]`; `prs(ctx, req, project_id) -> Reply`
     (404 for an unknown project via `_unknown()`/`text(404, "not found")`).
   - The body, from the record: `batch` id, `paused` (`batch["state"] == "paused"`), `last_batch`
     (`state["history"][0]["id"]` when no batch, else None; check the history element's key is
     `id`), the rows' CR set (`c["pr"]` truthy), the forge read (cached), the judgement.
   - One pure function per judgement so each is testable and under the complexity limit:
     `forge_state(pr) -> "open"|"draft"|"merged"|"closed"`, `checking(pr) -> bool` (Q9),
     `checks_word(pr) -> "running"|"green"|"failing"|"none"`, `ready_now(cr_row, forge_row) ->
     bool` (`cr_row["to_review"]` and open, not draft, not conflicting, not checking, checks
     green or none), `disagrees(cr_row, forge_row) -> str | None`, `all_done(rows) -> bool`.
   - The cache: `class ForgeReads` with `get(project_id, loader, now=time.monotonic) ->
     (payload, read_at_iso)`, a lock per project held across the loader call, a 10 s window, the
     last good read kept when the loader raises (so `{rows: last good, error: text, read_at: its
     time}`), kept in the module that `Context` imports without a cycle.
   - The runner: `argv` built from `pr_parts` of each CR's link; refuse mixed repositories with the
     shared constant; `gh api graphql -f query=<text> -F owner=.. -F name=..` (variables, not string
     interpolation of owner/name; numbers as integers in aliases), timeout, JSON parse, errors
     to one line (`" ".join(str(e).split())`, as `forge_base.read_state` does).
2. `board/routes.py`: `from chantier.board import ... prs` and `*prs.ROUTES` in `ROUTES` (2 lines).
3. `board/context.py`: one field for the cache (default factory) (2-3 lines).
4. `commands/forge_stack_gh.py` + `forge_stack_shared.py`: lift the "not all in one repository"
   literal to a constant (optional but it is the only way to share the text honestly).

Front end (all new files except 5 small edits): `js/views/prs.js` (render, mount, count helpers),
`js/views/prs-row.js` (one row), `js/views/prs-feed.js` (the 10 s loop, visibility, restart),
`js/i18n/en-prs.js` + `fr-prs.js` (+ `nav.prs` in `en.js`/`fr.js`, spread of the new files),
`css/views/prs.css` (+ link in `index.html`), an icon in `icons.js`, `prs()` in `core/api.js`,
`prs: null` in `core/store.js` and `core/router.js`'s `reset`, the registry entry.

Docs: AGENTS.md, CONTRIBUTING.md, `docs/web-board.md`, `chief-of-staff.md` (2 lines),
`scenario/README.md` (bullet + steps named), tests, `fake_gh.py`, `run_scenario.py`.

No change in `status.py`, `STATUS.json`, `hooks/`, `types/` (so no `just mod`), `agents/`,
`com.github.copilot/agents/`.

### Row judgement (what the code has to decide; proposed words for the Driver)

Per CR with `pr`: `forge` = the aliased result for its PR number.
`state`: `MERGED` -> merged; `CLOSED` -> closed; open + `isDraft` -> draft; else open.
`conflicting`: `mergeable == "CONFLICTING"`. `checking`: `mergeable == "UNKNOWN"`, or head
checks not started in a repo that has checks. `checks`: rollup `SUCCESS` -> green,
`PENDING`/`EXPECTED` -> running, `FAILURE`/`ERROR` -> failing, none only when the repository has
none. `merged_into`: `{"branch": baseRefName, "cr": <CR whose branch it is or None>}` for a merged
PR. `ready_now`: record `to_review` AND open AND not conflicting AND not checking AND checks in
(green, none). `disagrees`: record ready and (draft | conflicting | closed | failing ...) =
"ready in the record, <x> on the forge"; forge merged and CR state != merged = exactly
`merged on the forge, not recorded yet: tell the Chief of Staff`. `all_done`: rows non-empty and
every `state in (merged, closed)`.
Open edge: **zero rows**. `all(...)` of an empty list is true; with no PR yet, `all_done` should be
false (nothing is done) but the page must also not poll the forge (no PR to ask). Define
`all_done = bool(rows) and all(...)`, and the front end loops only when there is a PR to read.

## 3. Risks

R1. **No in-process route fixture exists**; the spec's test list is written as if there were. Cost:
   a new helper (about 25 lines) and a test file; the batch of four CRs with PRs needs
   `write_record` edits (set `pr`, `pr_draft`, `status: ready`, `branch`) because `ship` needs
   a Driver. `to_review` comes from `ready_word` (`stacks.READY_TO_MERGE = "ready to merge"`; the
   spec writes `ready-to-merge`: the field to read is `crs[].to_review`, which exists): it needs
   `status == "ready"`, `pr_draft` false and (for a stack) the base rules; in a parallel or
   direct batch a PR with `pr_base == default_branch` is enough. Set `pr_base: "main"` and
   `pr_draft: false` in the fixture.
R2. **`gh api graphql` is always an HTTP POST**: `-f/-F` imply POST; the argv carries no `-X`, so
   the spec's literal check ("no `-X` other than GET, no mutation") passes, but the true read-only
   guarantee is the query text. Test it too: the query string starts with `query` and holds no
   `mutation`/`subscription`. AGENTS.md's wording ("read-only") is about effect, fine.
R3. **GitLab GraphQL via `glab api graphql`** is also a POST and `glab()` adds `--method GET` when
   fields are present, so `glab()` cannot be reused for it; a new runner is needed, and GitLab's
   field names (`detailedMergeStatus`, `headPipeline`, `targetBranch`, `mergedAt`) and "this
   project has no CI" (no GraphQL field says it directly; `project.ciConfig` needs content;
   `project.pipelines` empty is ambiguous) are unproved (the spec already requires a real-GitLab
   trial). Rule when it cannot tell: "being checked", never "none": a GitLab project with no CI
   would then read "being checked by the forge" forever and never "ready": **flag to the user as a
   known gap** (not a question: the spec decided it).
R4. **GitHub "no checks" vs "not started"**: `statusCheckRollup` is null both for a repo with no
   checks and for a head whose checks have not registered yet. The spec's idea (no workflow folder
   on the default branch and no status context on the head) needs a second field in the same query:
   `repository { object(expression: "HEAD:.github/workflows") { ... on Tree { entries { name } } } }`
   (null when the folder is missing) plus `statusCheckRollup { state contexts(first: 1) {
   totalCount } }`. Workflows are not the only source (a third-party app posting statuses),
   hence the "no status context on the head" half. Unprovable by the fake; the spec has the trial.
   Branch protection "required checks" is another source: not read.
R5. **Query shape**: one query for N PRs = `repository(owner:$owner,name:$name){ p1: pullRequest(number:1){...} p2: ... }`.
   A PR number missing on the forge makes GraphQL return `errors` with partial `data`; treat any
   `errors` as the page's one-line error (no guess). Aliases are built from integers parsed by
   `pr_parts` (`\d+` regex), so no injection through the link; owner/name go through variables.
   With 11 PRs the query is small; GraphQL cost is one point.
R6. **The 10 s cache + lock**: keep the lock while the forge call runs; two requests wait for one
   call. A hung `gh` must not hang the threadpool: pass a timeout (for example 20 s: above 10 s
   keeps one call in flight at most; fix the value in the code, say it in the docs).
   The read is per project: key by `project.id`; in a surface with several projects each has its
   own repo link set.
R7. **`clock.now()` vs `time.monotonic()`**: `read_at` shown to the user comes from `clock.now()`
   (as the rest of the server's instants; fixed by `--clock`); the 10 s rule uses monotonic.
   The scenario's fake clock case (`--clock`) must not freeze the cache.
R8. **"Stops asking once all done / restarts on a new PR"** lives on the client: the server cannot
   tell if a page is open. Two points: (a) the first read when the view opens happens even when the
   last known state is all done (spec section 3); (b) the restart compares PR links of
   `state.data.batch.crs` (the 5 s record read) with the rows of the last forge read. A CR that gets
   a PR is detected within 5 s, then the next forge read happens at once (no waiting 10 s).
   A CR whose PR link changes (a new PR for the same CR after a close) is a different link: compare
   `pr` strings, not CR ids.
R9. **Cancelled / dropped CRs with a PR**: `cr_rows` returns every CR including `cancelled`; the
   spec says "one row per CR that has a PR recorded". A cancelled CR whose PR the user has not
   closed on the forge stays open forever and keeps `all_done` false and the refresh running.
   Following the spec literally is defensible (it is the truth on the forge); the alternative
   (skip CRs whose record status is cancelled) is a decision the spec did not take: keep the spec,
   state the behaviour in the docs. A CR the record shows merged with `pr` set is still a row (the
   forge confirms it).
R10. **Sidebar count and "0"**: the registry's `count` shows what it returns, including 0. The
    spec's formula gives 0 with a batch and no open PR; showing "0" next to PRs is acceptable but
    `null` for "no batch" must be explicit.
R11. **Sidebar/bottom-bar now has 6 views**: every committed docs picture (`docs/web-board/*.png`)
    shows the old sidebar and will drift from the real page once PRs is added (the spec says no new
    picture and `just docs-screenshots` unchanged; the old pictures are not retaken in this CR).
    Say it in the PR (not blocking). Check the phone bottom bar fits 6 buttons at 375 px.
R12. **Value others measure from**: the spec changes no size or value that other code measures
    from (no existing constant changes). New JS must stay <= 300 lines per file and CSS <= 300
    lines (searched: `MAX_SCRIPT_LINES = 300`, `MAX_STYLE_LINES = 300`, `MAX_FILE_LINES = 400`,
    `MAX_FUNCTION_LINES = 50` in `test_code_targets.py`). The `surface-board` unit budget (250 s)
    and its README table row (`| surface-board | 250 | 236.3 | 196.0 |`) are the one number the
    scenario steps push against.
R13. **i18n parity test blind spot**: `test_the_web_frame_...` compares only the keys written in
    `en.js` and `fr.js` themselves; keys in `en-prs.js` / `fr-prs.js` are not compared. Keep them
    equal by hand (or add the new files to the test's list, a 1-line change).
R14. **Card edit vs startup budget**: `chief-of-staff.md` is measured by
    `test_startup_manifest.py`; the two edited lines are not in a startup section as far as the
    headings go, but run the test after.
R15. **The Chief of Staff's own `gh` shell**: the board reads with whatever `gh` login the board
    process has; a board started by the Chief of Staff in a session without the forge login shows
    the forge's own error line (the spec's behaviour); no extra handling.
R16. **Network in tests**: no test may reach a real forge; `shutil.which("gh")` may find the
    developer's real `gh`, so tests must monkeypatch the seam, never rely on PATH being empty. In
    the scenario the fake is first on PATH (World.__init__).

## 4. Questions only the user can answer

None. Two spec/code mismatches the Driver can settle alone (decided above): the spec's
`ready_word` `ready-to-merge` is `to_review` in the code; the `prs.*` word prefix is taken.
One consequence worth telling the user at the ready line, not asking: R3 (GitLab project with no CI
reads "being checked by the forge" under the "never none when unsure" rule) and R11 (old docs
pictures lack the new sidebar entry).

## 5. Evidence plan

Kind of change: a new read route and a new web view (CLI/board code, cards text, scenario), no
change to the CR board pane (`hooks/register.tsx`, `STATUS.json`): so the project's screenshot rule
(AGENTS.md: only a change to what the CR board pane draws) does **not** apply, and `just mod` is not
required. The spec asks for a screenshot of the page "not required by the project's rules".

What shows it, before and after:

1. **Route, behaviour: the in-process tests** (`pytest -q tests/test_board_prs.py` output, captured
   to `evidence/` as a `.log`): a monkeypatched seam counting forge calls; cases from the spec
   (401, no batch, paused, four CRs with the fourth merged on the forge into another CR's branch,
   Q9 parametrized, Q6, two calls within 10 s -> one call, forge failure with the last good read
   kept, `all_done` parametrized, argv has no mutation / `-X`, planning folder byte-identical).
   Before: the route answers 404. After: the cases pass. Also `just test` time (<= 18.5 + 30 s).
2. **Route, end to end against the fake forge: the scenario unit `surface-board`**
   (`just scenario` on `--unit surface-board`; its `gate` log under `work/gates/`, the unit JSON,
   and the checks the new steps add: rows against the fake forge, a merge on the fake forge
   shows the Q10 line and writes nothing, `order merged` clears it, closed + merged -> `all_done`,
   a new CR with a PR -> new row and `all_done` false). Evidence: the checks' lines with the
   pass counts, and `.calls` lines showing one `api graphql` call per `/prs` read and none for
   `GET`-only reads of other routes. Capture: `uv run --no-sync --project <checkout> python
   scenario/run_scenario.py --unit surface-board` (or `chantier gate`), whichever the
   `scenario/README.md` names; log to a `*.log`. The Windows local run of `just scenario` at the
   head (AGENTS.md: the CR on top of the stack) is the long gate; `ubuntu-latest` is CI's.
3. **The page, drawn**: one real board started against a throwaway project (the scenario's `w`
   world kept by hand, or a temp repo with `open_batch`-like records) with the fake `gh` first on
   PATH, opened in Chromium via Playwright (as `scripts/docs_screenshots.py` does:
   `uv run --group docs ...`; look there for the invocation) at 1400x860: screenshots of the PRs
   view with (a) four rows mixed (ready, conflicting, being checked, merged-not-recorded), (b) the
   final table "all done" with the refresh stopped, (c) the forge-error line. Check the sidebar
   count against the record in the same shot. The shots go to `evidence/` and, one of them, in the
   PR's Deliverables (spec). The refresh behaviour (10 s tick, visibility stop, restart on a new
   PR) is shown by the fake forge's `.calls` log counted over a timed window while the page is
   open, then after "all done": `evidence/prs-refresh-calls.log` (count of `graphql` lines per
   10 s; zero after all done; one more after a new PR joins). A screenshot cannot show the timing;
   the log does.
4. **Docs/rules text**: `git diff` of AGENTS.md, CONTRIBUTING.md, `docs/web-board.md`,
   `chief-of-staff.md`, `scenario/README.md` (diff is the evidence; nothing to draw); `just check`
   output (lint, tests, release-notes) on this machine (Windows); Linux/macOS are CI's.
5. **Unproved reads, by hand on real forges** (spec's three trials: stacked PR merged into another
   PR's branch; a native GitHub stack; a real GitLab project): each needs a real repository, the
   user's `gh`/`glab` login and the network: the Driver cannot do them from the worktree. Each is
   recorded in the PR's Deliverables, or named in Known gaps (so the ready line quotes it).
   What cannot be shown from here: the real GraphQL field behaviour (R4, R3), "being checked
   by the forge" right after a push (needs a real push and the forge's timing), and GitHub's
   `UNKNOWN` mergeability; the fake can only return what it is told.
