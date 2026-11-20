# Change Specification: the web client moves out of the server's package; `board --ui <folder>|none`

Origin: verbal (2026-11-20, planning-server's grill, answer planning-server-Q29; split off the CR
`server-api` by its answer 1, settled by the Chief of Staff). No tracker issue.

This CR is the second half of a cut in two. The first half, `server-api`, publishes the surface
server's API (protocol 1, over a WebSocket and over HTTP) and ports the web client to it, in its
old folder. This half only moves the web client out of the server's code and lets the server serve
another client's files, or none. Everything this CR needs from the first half's decisions is
copied below: the first half's folder goes to the archives at its merge, so nothing here depends
on reading it.

Decisions carried, from the first half's answers (2026-11-20, settled by the Chief of Staff, the
user asking no questions), marked "(A*n*)" in the body:

- A1. Two CRs: `server-api`, then this one (the folder move and `--ui`).
- A9. The UI goes to `chantier/clients/web/`, in the one wheel; `chantier board --ui
  <folder>|none`.
- A10. No build step, no framework.
- A11. Clients shipped: the web client and the CLI's own probe and seat call; no SDK.
- A13. The command stays `chantier board`.
- A16. The `AGENTS.md` edits are approved as written, this CR's part being the `DESIGN.md` path
  sentence; they stand on the user's merge of the PR, as every project rule's change does.
- The spec critic's point 13: the first half's Part 2 text is this CR's, copied here and made its
  own.

This CR's own answers (`02-answers.md`, settled by the Chief of Staff on 2026-11-20, the user
asking no questions, each the first draft's recommendation), marked "(B*n*)" in the body:

- B1. `--ui` when a board already runs: no refusal; the usual "already running" line, plus
  `--ui not applied: a board already serves this surface; stop it to change what it serves`.
- B2. No `board.ui` key in `chantier.yaml` in this CR; a later CR only if the user asks.
- B3. `AGENTS.md`'s server sentence gains "(another folder's with `--ui <folder>`, none with
  `--ui none`)", standing on the merge.
- B4. The file types served stay today's list (html, js, css, svg, json, ico, png, woff2),
  documented; others only when a real UI needs them.
- B5. `--ui <folder>` requires a folder holding an `index.html`; refused at the start otherwise,
  before anything is written.

## 1. Goal, in the user's terms

The surface server is the one writer of the surface: it keeps the state and exposes the server,
chantier's equivalent of Vercel Board (the user, 2026-11-20). The user wants the UI out of
`chantier board`, so that "everything goes through a WebSocket, or HTTP as the degraded case
(behind a proxy, for instance)", and so that several UIs, or native Android or iOS apps, can be
built on it (planning-server-Q29).

After `server-api`, the web client already talks to the server only through the published API.
This CR gives:

- **The web client in a folder of its own**, `skills/chantier/scripts/cli/src/chantier/clients/web/`,
  outside the server's package `chantier/board/`, still shipped in the one wheel (A9).
- **A server that serves a folder, not its own page**: `chantier board` serves the shipped web
  client by default, another client's static files with `--ui <folder>` (the user's own UI), or
  none with `--ui none` (the API only) (A9).
- **A rule that keeps them apart**: the server's code names nothing of `clients/`, checked by a
  test.

## 2. Dependencies and neighbours

- **After `server-api`** (`depends.json`: `after: server-api`). That CR leaves, in
  `chantier/board/`: the package `board/api/` (`protocol.py`, `protocol.json`, `ops.py`,
  `topics.py`, `push.py`, `auth.py`, `ws.py`, `http.py`, `times.py`), the web client ported to it
  (`js/core/transport.js` new, `js/core/api.js` over `call`), the test
  `tests/test_server_protocol.py` that reads the shipped `js/` from `board/web/`, and
  `docs/server-api.md`. This CR moves the folder and changes the paths those name; it changes no
  op, topic, frame, key rule or view.
- If the user has this CR started before `server-api` lands (their word only), the Driver moves
  the folder as `main` holds it then (no `board/api/`, no `docs/server-api.md`): the `--ui none`
  answer then names `docs/web-board.md` instead of `docs/server-api.md`, and `server-api` carries
  its own paths to `clients/web/` when it lands second. The rule is "the web client lives in
  `clients/web/` and the server names nothing of it once both are merged", whichever lands second.
- Pending web-client items (`2-backlog/P3/board-griller`, `board-history`, `board-help-page`,
  `board-batch-view`, `board-triage-polish`) are not edited by it; each that lands after it works
  under `clients/web/`. One that lands before it rides the move (a rename keeps its history).

## 3. Decisions carried

| Decision (source) | Where it lands |
| --- | --- |
| The UI goes out of `chantier board`; several UIs and native apps must be possible (planning-server-Q29) | §1, §4, §5 |
| Two CRs, this one second: the folder move and `--ui` (A1) | §2, the whole CR |
| `chantier/clients/web/`, in the one wheel; `board --ui <folder>\|none` (A9) | §4, §5 |
| No build step, no framework (A10) | §4.4 |
| Clients shipped: the web client and the CLI's probe and seat call; no SDK (A11) | §10 (out of scope) |
| The command stays `chantier board` (A13) | §5 |
| The `DESIGN.md` path sentence of `AGENTS.md`, approved, standing on the merge (A16) | §7.1 |
| `uv` is the only tool to install; the plugin needs no setup; the CLI is one package, one wheel (AGENTS.md) | §4.1: package data of the same wheel; no new dependency, no new tool |
| A change under the web client's folder reads its `DESIGN.md` first and keeps it true (AGENTS.md) | §7.4 |
| The spec critic's point 13: Part 2's text copied here, made this CR's own | this document |
| `--ui` on a running board: not applied, said in one line, no refusal (B1) | §5, §8.1, §8.2 |
| No `board.ui` configuration key (B2) | §10 |
| `AGENTS.md`'s server sentence names `--ui` (B3) | §7.1 |
| Today's file types, documented (B4) | §4.3, §6 |
| A folder with no `index.html` refused at the start, nothing written (B5) | §5, §8.1, §8.2 |

## 4. The move

### 4.1 The folder

- Every file of `skills/chantier/scripts/cli/src/chantier/board/web/` moves, with `git mv`, to
  `skills/chantier/scripts/cli/src/chantier/clients/web/`, unchanged byte for byte: `index.html`,
  `DESIGN.md`, `css/`, `fonts/` (the `.woff2` files and `OFL.txt`), `js/` (152 files at the time
  of writing, more after `server-api`). No file is edited in the move commit but `DESIGN.md`'s
  path sentence (§7.4); every other file is a 100 % rename.
- `chantier/clients/` holds no Python file and no `__init__.py`: the web client is static files
  only. It stays package data of the one wheel: the root `pyproject.toml`'s
  `[tool.hatch.build.targets.wheel] packages = ["skills/chantier/scripts/cli/src/chantier"]`
  already ships every file under `chantier/`, so `uvx --from <plugin>` (the plugin) and `uv run
  --no-sync --project <checkout>` (chantier's own checkout, an editable install) both have it, with
  no change to `pyproject.toml`.
- `chantier/board/web/` no longer exists after the move.

### 4.2 The repository's own paths

- `.gitattributes`: its two lines `skills/chantier/scripts/cli/src/chantier/board/web/** text
  eol=lf` and `.../board/web/fonts/*.woff2 binary` name `clients/web/` instead, in the same commit
  as the move (so no checkout on Windows ever sees the files without their LF rule).
- `biome.json`: `files.includes` becomes
  `["skills/chantier/scripts/cli/src/chantier/clients/web/**"]`.
- `justfile`, recipe `lint`: the Biome line checks `skills/chantier/scripts/cli/src/chantier/clients/web`.
  Both Biome paths change together: a path that matches nothing would let Biome check no file and
  pass (§8.3 proves it does not).
- The tests that read the web client's files read them at `clients/web/` (§8.1).

### 4.3 The server's code

- `board/static.py` serves a folder it is given and knows nothing else of the client:
  - The module constant `WEB` goes. `serve(ui: Path | None, rel: str, if_none_match: str | None)`
    and `_file(ui, rel)` take the folder; the rest is today's code (`index.html` for `/`, the
    `resolve()` and `is_relative_to` check that keeps a request inside the folder, symlinks
    pointing out of it included, the `TYPES` table, the `ETag` and `no-cache`, `304`).
  - `ui` is `None`: every `GET` or `HEAD` outside `/api/` answers 404 with the one line
    `this server serves no UI: see docs/server-api.md` (a constant, `NO_UI`).
  - Its docstring says it serves the folder `chantier board` was given (`--ui`).
- `board/context.py`: `Context` gains `ui: Path | None` (the resolved folder, or `None` for
  `--ui none`); `board/command.py`'s `_run` passes it; `board/routes.py`'s `_dispatch` calls
  `static.serve(ctx.ui, req.path, ...)`.
- Unchanged, and so applying to whatever folder is served: the key check before any file
  (`guard.authorised`: a static file with no key answers 401), the `?k=` exchange and its cookie
  (`guard.exchange`, with the relative `Location` `server-api` gives it), the answer's headers
  (`reply.SECURITY` on every answer, `reply.HTML_POLICY` on every `text/html` answer, through
  `Reply.all_headers`), the method rules (`guard.ALLOWED`: a `POST` outside `/api/` answers 405).
  With `--ui none` the `?k=` exchange still sets the cookie and redirects; the page it redirects
  to answers the 404 above.
- No module under `chantier/board/` (`board/api/` included) imports from `chantier.clients` or
  names its folder: no string literal equal to `clients` or holding `clients/` (§8.1 checks it;
  the word "clients" in a comment or a docstring, as "every client" in the push loop's, is free).
  The default folder is named once, in the command's declaration (§5), outside the server's
  package.

### 4.4 The web client

Hand-written HTML, CSS and native ES modules, no build step, no framework (A10), under the same
targets as today (CONTRIBUTING.md, "The board's page"): its files do not change. Its addresses
are all relative, so it works from the new folder as it did from the old one; its references stay
inside its own folder (`tests/test_code_targets.py`'s check, reading the new path).

## 5. `chantier board --ui <folder>|none`

Declared in `skills/chantier/scripts/cli/src/chantier/declare/board.py`:

- `--ui FOLDER`, help: "the folder of static files the board serves at `/` (default: the
  shipped web client); `none`: the API only, no page".
- Its default is the shipped web client's folder, named once there as a module constant,
  `SHIPPED_UI = Path(__file__).resolve().parents[1] / "clients" / "web"` (the declaration imports
  only `pathlib` for it: the CLI's start imports stay the standard library's and chantier's, as
  `tests/test_code_targets.py`'s start-import test checks).
- `HELP` (the command's one line) becomes: "serve the board's API and the web client (or another
  UI: --ui) on this machine and the local network, behind a key".

In `board/command.py`'s `board`, first thing after `--clock` (before the planning folder is
opened, the key read or anything written in the git folder):

- `--ui none` (the exact lower-case word): `ui = None`. A folder named `none` is given as
  `./none`.
- Otherwise the folder is resolved against the current directory (`Path(arg).resolve()`); it must
  be a directory holding an `index.html` file (B5), else the command stops with exit code
  `EXIT_USAGE` (as `--clock` does) and the one line
  `--ui <arg>: not a folder with an index.html: give a folder of static files, or none`.
  Nothing is written: no `server.json`, no key, no bind.
- The default and a valid folder go on as today; `ui` reaches `Context` through `_run`.
- A board already running for the surface (the `there` branch: `board already running at
  <link>`): it keeps serving what it was started with; this command's `--ui` does not apply to it
  and nothing is refused (B1). The command prints `board already running at <link>` (and
  `on this machine: ...` when it does today), then, only when `--ui` was given with a value other
  than the default (`args.ui != SHIPPED_UI`: `--ui none` or another folder), one more line:
  `--ui not applied: a board already serves this surface; stop it to change what it serves`. The
  exit code stays 0; a `--seat` given still registers the seat as today. A start with no `--ui`
  (the cards' `--seat` start) prints exactly what it prints today. The `--ui` folder check (B5)
  runs first even then: a bad folder is refused before the running board is looked for.
- The start lines do not change (`board on <link> over <folder>`, `on this machine: ...`, the
  `BEYOND` line), so `session-start.md`'s list of them holds. With `--ui none` the link still sets
  the cookie; its page answers the 404 line, which points to the API's doc.
- The cards start the board with no `--ui` (`$CHANTIER board --seat <id>`): they get the shipped
  web client, as today. No card changes.

## 6. What another UI gets (said in `docs/server-api.md`)

A section "Serving another UI" in `docs/server-api.md` (made by `server-api`), for a client's
author:

- `chantier board --ui <folder>` serves that folder's files at `/`, `index.html` for `/`, behind
  the same key: the link's `?k=` sets the cookie, and the page then calls the API from the same
  origin (the cookie counts there, as `docs/server-api.md`'s key section says).
- What the server sends: only files of the folder, by the types it knows (`.html`, `.js`, `.css`,
  `.svg`, `.json`, `.ico`, `.png`, `.woff2`; any other answers 404 (B4); a type is added, by addition, only when a real UI needs it), with `Cache-Control:
  no-cache` and an `ETag`; an HTML page carries the server's Content Security Policy
  (`default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src
  'self'; connect-src 'self'; ...`): no inline script or style, nothing loaded from another
  origin, the API on the same origin only.
- Its addresses must be relative to stay working behind a proxy with a path prefix (the key
  section's proxy rules hold for any served folder).
- `--ui none`: the API only; `/` answers 404 with a line naming this doc. A UI served elsewhere
  (another origin) or a native app uses the key in a header or in the WebSocket's first message,
  as the doc's key section says; it needs no `--ui`.
- The shipped web client's folder is the example of such a folder.

## 7. Project rules, docs and diagrams

### 7.1 `AGENTS.md` (chantier's; the user's merge of the PR is their approval) (A16)

- "A change under `skills/chantier/scripts/cli/src/chantier/board/web/` reads its `DESIGN.md`
  first and keeps it true." becomes "A change under
  `skills/chantier/scripts/cli/src/chantier/clients/web/` (the web client) reads its `DESIGN.md`
  first and keeps it true."
- The surface server's sentence, as `server-api` leaves it ("... and it serves the web client's
  files, one client among others; it edits ...") becomes "... and it serves the web client's
  files (another folder's with `--ui <folder>`, none with `--ui none`), one client among others;
  it edits ..." (B3), standing on the PR's merge.
- Nothing else in `AGENTS.md` names the folder.

### 7.2 `CONTRIBUTING.md`

As `main` holds it once `server-api` has landed:

- The board paragraph (item 2 of the parts list): "its page, in `board/web/`, is hand-written
  HTML, CSS and ES modules, with no build step" becomes "its web client, in `clients/web/`, is
  hand-written HTML, CSS and ES modules, with no build step, served as plain files (`--ui` serves
  another folder, or none); the server's code names nothing of it (a test checks it)".
- The tree drawing: "`scripts/cli/` ← the `chantier` CLI's source (its web board in
  `board/web/`)" becomes "(its web client in `clients/web/`)".
- "The board's page" section: its title line names `clients/web/` instead of `board/web/`; the
  **CSS** rule names `clients/web/DESIGN.md`; the **Page** rule's "the page loads its own font
  from `web/fonts/`" and "inside `web/`" name `clients/web/fonts/` and `clients/web/`.
- Nothing else changes (the dependency paragraph, the targets themselves).

### 7.3 Docs (chantier's `docs/` and `README.md`)

- `docs/server-api.md`: the section of §6; its list of what the server serves names `--ui`.
- `docs/web-board.md`, "Starting the board": one bullet after "By hand": **Another UI.**
  `chantier board --ui <folder>` serves your own UI's static files in place of the web board, and
  `--ui none` serves the API only; see [the server's API](server-api.md). The rest of the page is
  unchanged (it describes the shipped web client, which is still the default).
- `docs/boards.md`, `README.md`, `docs/demo/README.md`, `docs/agents-and-models.md`,
  `docs/costs.md`: they name "the web board" as a thing the user opens, not its folder: no sentence
  made false (searched for `board/web`, `web board`, `web page`). The Driver searches every
  `docs/*.md` and `README.md` again at the head for `board/web` and `--ui`.
- **SVGs: none changes.** No diagram names the web client's folder, the server's package or a UI
  served by the board: searched in every `docs/*.svg` (text and `<desc>`) and every
  `docs/*-texts.md` for `board/web`, `web board`, `browser`, `web page`, `chantier board` and
  `UI`; the only matches are the font stack's "Segoe UI" in every SVG and `cr-lifecycle`'s "a UI
  mockup" (a prototype, not the board), neither made false. The Driver repeats the search at the
  head; a diagram found false is changed with its `-texts.md` and its `<desc>` together.
- **Pictures:** `docs/web-board/*.png` and the `docs/board-mod-*.png` do not change: the page's
  files are byte-identical, so `just docs-screenshots` gives the same files (§8.3). The pane
  screenshots are not concerned (§10).
- Release notes: a line for the release that carries this CR (§9), in that release's new file;
  no old release note is edited.

### 7.4 `clients/web/DESIGN.md`

Read first, as `AGENTS.md` asks. Its rules and tokens do not change. Its path sentence (line 4,
"Any change under `skills/chantier/scripts/cli/src/chantier/board/web/` reads this file first")
names `clients/web/`. `tests/test_board_design.py` reads it at the new path. Its sentence "no
picture ships in the package" stays true.

### 7.5 Cards

None changes: no card names the folder or `--ui` (`session-start.md`, `chief-of-staff.md`,
`hosts/claude-code.md`, `hosts/copilot.md` start `$CHANTIER board --seat <id>` and name `GET
/api/board`; `coder.md`, `debugger.md`, `verifier.md` name the board's write paths). The Driver
searches `skills/chantier/references/` for `board/web` and `--ui` at the head. `agents/` and
`com.github.copilot/agents/`: unchanged.

## 8. Evidence

### 8.1 pytest (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- The tests that read the shipped web client read it from the repository at its new path, at the
  head under test: `test_board.py`'s `test_the_frame_is_shipped_with_the_package` (its file list
  under `clients/web/`, and `HTML_POLICY`'s checks kept), `test_board_design.py` (`WEB`,
  `DESIGN.md`), `test_code_targets.py` (the script-size and word-keys test, and `WEB` for the
  self-contained and style test), `test_open_empty_batch.py` (the i18n and views files), and
  `server-api`'s `test_server_protocol.py` (the JS read for op and topic names, and the
  `transport.js` rule). Their cases do not drop; a shared path constant or helper is the Driver's
  choice.
- `test_board_ui.py` (new):
  - **The split, on the shipped files** (read from the repository at the head): `chantier/board/web`
    does not exist; `chantier/clients/web/index.html` and `DESIGN.md` do; no `.py` file is under
    `chantier/clients/`; no `.py` file under `chantier/board/` (recursively, `board/api/`
    included) imports `chantier.clients` or has a string literal equal to `clients` or holding
    `clients/` (AST); `declare/board.py`'s
    `SHIPPED_UI` resolves to `chantier/clients/web/`.
  - **Serving a folder** (a prepared folder in `tmp_path`, through `routes.handle` with a
    `Context` whose `ui` is that folder, the key in the header): `/` answers its `index.html` with
    `text/html; charset=utf-8` and `HTML_POLICY`; `/app.js` answers it as `text/javascript`; a file
    with a type not in `TYPES` answers 404; `/../outside.txt` and a symlink out of the folder (when
    the OS lets the test make one; skipped otherwise, said in the skip) answer 404; with no key,
    `/` answers 401.
  - **No UI** (`ui` is `None`), parametrized over `/`, `/index.html`, `/js/main.js`: 404 with
    `NO_UI`; `/api/board` with the key answers the probe (200); `/?k=<key>` answers 303 with the
    cookie.
  - **The refusals of `--ui`**, parametrized (a path that does not exist, a file, a folder with no
    `index.html`), calling the CLI in-process (`cli.main(["board", "--ui", ...])`) on a prepared
    project: exit `EXIT_USAGE`, the one line of §5, and no `chantier/server.json` in the git folder
    afterwards (nothing written) (B5: the acceptance of the refusal).
  - **`--ui` on a running board** (B1), calling the CLI in-process with `board/command.py`'s
    look-up of a running board (`_recorded` or `_answering`) replaced by the test to answer an
    address, parametrized: `--ui none` and `--ui <a good tmp folder>` print `board already running
    at <link>` then `--ui not applied: a board already serves this surface; stop it to change what
    it serves`, exit 0; no `--ui` prints the first line only, as today; `--ui <a folder with no
    index.html>` is refused with the line of §5 before the look-up (the replaced look-up is not
    called).
- `test_board.py`'s `MODULES` keeps `static`; the lazy-import test is unchanged.
- `just test` stays within its budget (AGENTS.md: at most 30 s above its 18.5 s of 2026-11-14):
  the new tests add at most 1 s; the Driver reports `just test`'s time at the base and at the head
  on the same machine in the PR.

### 8.2 Scenario, unit `surface-board` (`scenario/run_scenario.py`)

Case `remote_board` keeps every step (they serve the default, the shipped web client: its "every
module and stylesheet the page loads answers 200" step proves the moved folder is served whole).
Added at its end, after the board it started is stopped, against a real `chantier board` process
(`BoardProc`, `--host 127.0.0.1 --port 0`):

- `--ui <folder>`: a folder made by the scenario with an `index.html` holding a marker and one
  `app.js`: `/` with the cookie (after `?k=`) answers that `index.html` with the CSP; `/app.js`
  answers JavaScript; `/js/main.js` (a shipped client's file) answers 404; `GET /api/board` with
  the key answers the probe.
- `--ui none`: `/` with the cookie answers 404 with `this server serves no UI: see
  docs/server-api.md`; `GET /api/board` with the key answers the probe; a call of the API
  (`board.get` over HTTP, `server-api`'s `POST /api/v1/call/board.get`) answers 200.
- `--ui` naming a folder with no `index.html`: the process exits with the usage code and the line
  of §5, before any start line, and no new `chantier/server.json` entry (B5).
- `--ui not applied` (B1): while the case's first board still runs (before it is stopped), a
  second `board --ui none --seat s-1` prints `board already running at` with the same link and the
  line `--ui not applied: a board already serves this surface; stop it to change what it serves`,
  exits 0, and the running board still serves the shipped client (`/js/main.js` answers 200).

`scenario/README.md`'s Coverage list names each new check with its test, as
`test_scenario_coverage.py` checks. The unit's budget (500 s) holds: the steps add at most 10 s
(two board starts, one refused start and one second start on the running board); the Driver reports the unit's time at the base and at the
head.

### 8.3 By hand, before the push (the Driver)

- `just check`; `just eval-dry-run` (a change under the CLI's `src/`); `just scenario` green on
  the pipeline's `just scenario (ubuntu-latest)` job, and, as the batch's top CR, locally on
  Windows (`chantier gate`), as AGENTS.md says. No CI job is added or changed.
- **The move is a move:** `git diff --find-renames=100% --name-status <base> <head> --
  skills/chantier/scripts/cli/src/chantier/` lists every file of the old folder as `R100` to
  `clients/web/`, but `DESIGN.md` (its one path sentence); quoted in the PR.
- **Line endings:** `git ls-files --eol skills/chantier/scripts/cli/src/chantier/clients/web` shows
  `attr/text eol=lf` for every text file and `-text` for the `.woff2` files, on the Windows
  machine; quoted in the PR (summarised).
- **Biome checks the files:** `just lint`'s Biome line reports the same number of files checked at
  the base and at the head (not 0); quoted in the PR.
- **The wheel ships the client:** `uv build --wheel --out-dir <a scratch folder>` at the head; the
  wheel's file list holds `chantier/clients/web/index.html`, `chantier/clients/web/js/main.js`,
  `chantier/clients/web/fonts/Inter-Regular.woff2`, and no `chantier/board/web/`; quoted in the PR.
- **The pictures:** `just docs-screenshots` at the base and at the head on the same machine: every
  picture of `docs/web-board/` comes out the same file; when one differs, the PR names it and why
  (none is expected: the page's files are the same bytes).
- **In a browser:** the board started from the worktree (`uv run --no-sync --project <worktree>
  chantier board --port 0`, after `uv sync --locked --project <worktree>`), its link opened in
  Chromium: the web client loads and updates as before; then started with `--ui none` (the 404
  line in the browser) and with `--ui` on a small folder of one page that calls `board.get` (the
  page shows the answer: a UI of the user's own works under the CSP).

### 8.4 The default and host matrix

What the server serves depends on a shipped default against a given value (`--ui`), and the
folder's path on the host. One line per cell, each with its proof:

| `--ui` | Host | Expected | Proof |
| --- | --- | --- | --- |
| absent (the shipped web client) | Linux | the web client, every module and sheet 200 | scenario `remote_board` (CI, ubuntu-latest) |
| absent (the shipped web client) | Windows | the same | scenario `remote_board` (local gate) |
| a folder with an `index.html` | Linux | its files, the CSP on its page, the shipped client's files 404 | scenario (CI); `test_board_ui.py` |
| a folder with an `index.html` | Windows | the same, a drive-letter path given | scenario (local gate, its temporary folder's native path); `test_board_ui.py` |
| `none` | Linux | 404 line outside `/api/`, the API answers | scenario (CI); `test_board_ui.py` |
| `none` | Windows | the same | scenario (local gate); `test_board_ui.py` |
| a bad folder | Linux | usage exit, the line of §5, nothing written | `test_board_ui.py` (CI's `just check`); scenario |
| a bad folder | Windows | the same | `test_board_ui.py` (`just check` on Windows); scenario (local gate) |
| given, a board already running | Linux | the running board kept, the "--ui not applied" line, exit 0 | scenario (CI); `test_board_ui.py` |
| given, a board already running | Windows | the same | scenario (local gate); `test_board_ui.py` |

## 9. Rollout

- Release notes (the release's new file): "The web board's files moved to
  `chantier/clients/web/`, out of the server's package; `chantier board --ui <folder>` serves your
  own UI's static files in its place, and `--ui none` the API only (see `docs/server-api.md`)."
- No data, configuration or record changes; no migration. The probe, the API and the start lines
  are unchanged, so mixed versions behave as `server-api` leaves them.
- A board running from chantier's main checkout (`uv run --no-sync`) across the merge's
  fast-forward keeps its old folder path in memory: its page answers 404 until the board is
  started again. The Chief of Staff of a session here restarts it after the merge (stop the
  running one by the host's means, then `$CHANTIER board --seat <id>`), as after any change to the
  board's code; a board run from the plugin's install is not concerned until the plugin updates,
  and then starts on the new folder.

## 10. Out of scope

- Any change to the API, the protocol, the key rules, a view or a word of the web client (that is
  `server-api` and the board CRs).
- A native Android or iOS app, another web UI, an SDK or a Python client (A11).
- A build step, a framework, a bundler (A10); a separate repository or package for the web client
  (against "no setup"); a top-level `clients/` folder outside the Python package.
- Renaming `chantier board` (A13).
- Serving several UIs at once, or a UI under a path other than `/`.
- A configuration key for the UI (`board.ui` in `chantier.yaml`) and a field naming the served UI
  in the probe or in `board.get` (B2: a later CR only if the user asks).
- The CR board pane in Claude Code (`hooks/`): it reads `STATUS.json`, not the server; untouched,
  so no pane screenshot is owed.

## 11. Settled questions

Open questions for the user: none. The first draft's five questions were settled by the Chief of
Staff on 2026-11-20 (`02-answers.md`), each on its recommended answer, and are written into the
body as B1 to B5 (listed under the title):

1. `--ui` on a board already running: no refusal; one "--ui not applied" line (B1; §5, §8).
2. A `board.ui` configuration key: not in this CR (B2; §10).
3. `AGENTS.md`'s server sentence names `--ui` (B3; §7.1).
4. The file types served: today's list, documented (B4; §4.3, §6).
5. `--ui <folder>` requires an `index.html`, refused at the start (B5; §5, §8).

## 12. Self-containment notes for the Driver

- Seams: `board/static.py` (`serve`, `_file`, `TYPES`), `board/routes.py` (`_dispatch`,
  `_judged`), `board/context.py` (`Context`), `board/command.py` (`board`, `_run`,
  `_not_started`, the `--clock` check as the model for the `--ui` refusal), `board/guard.py`
  (`exchange`, `authorised`), `board/reply.py` (`SECURITY`, `HTML_POLICY`, `Reply.all_headers`),
  `declare/board.py` (the parser, `HELP`), `core/errors.py` (`EXIT_USAGE`); the scenario's
  `remote_board` (its `BoardProc`, `Link`, `fetch` helpers) and `scenario/README.md`'s Coverage.
- The tests' `Context` builders pass `ui` (the shipped folder for the existing route tests).
- Portability: paths through `pathlib` only; the folder check and the containment check work on
  a drive-letter path; UTF-8 everywhere; no shell.
- `DESIGN.md` first (AGENTS.md); `clients/web/`'s rules are CONTRIBUTING.md's "The board's page"
  targets, enforced by Biome through `just lint` and by `tests/test_code_targets.py`.
