# CR-301 investigation: the web board's Configuration page

Worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-301`, base 9414455 (CR-300). Read only.
`CLI` below = `skills/chantier/scripts/cli/src/chantier/`. Rules read (`$CHANTIER rules`): AGENTS.md
(the board's exception and the "plugin must work with no setup" clause are the two sentences section 4
rewrites), CONTRIBUTING.md, scenario/README.md. Surface rules do not touch this CR.

## Map: what exists

- `CLI playbook/layers.py` (CR-300/A): `read_user(repo, roles_by_host)` returns the valid user
  `Layer`s (label `surface` / `surface project` / `repository`, `.path`, `.display`, `.tree` of
  `Node`s each stamped `.layer`/`.src`) plus every problem; `merge(layers)` returns `Merged`
  (tree, files, `resets` by path with layer/src/line); `default_model(defaults_tree, host, role)`;
  `_read(path, shown, label, roles_by_host)` is private and is the only way to get the defaults
  tree. `load()` returns `(None, [])` when no user file exists, so the view cannot be built on
  `load()`: use `read_user` + `merge` + `_read` of `config/chantier.defaults.yml` (plugin root).
  `_model_problems` (private) is where the `start` (`plugin`/`named`/`generic`) and Q13's refusal
  are decided; `load` only returns them as problems, never per row.
- `CLI playbook/config.py`: `FILES=("chantier.yaml","chantier.yml")`, `read_tree(path, display)`
  (reads a file: no in-memory variant), `check(tree, roles_by_host, bad)`, `typed(...)`,
  `start_refusal(host, role)` (Q13's line), `default_agent(host, role)`.
- `CLI playbook/yaml_subset.py`: `parse(text)` (ruamel `typ="safe", pure=True` events, so line
  numbers come for free), `Node`, `is_reset`. A quoted `"default"` is NOT a reset (`plain=False`).
- `CLI playbook/models.py`: `MODELS[host]` is a tuple built once at import (Copilot from
  `copilot_catalog()` at import), `NAMED_AGENT_MODEL_AT_START = {"claude": True, "copilot": False}`,
  `HOST_NAMES`, `resolve(host, name)`. `copilot_catalog()` reads `copilot-models.json` on each call;
  30 models, each `{id, name, release_status, cli, app, plans: {pro,pro_plus,max,business,enterprise}|null, ...}`.
- `CLI plugin_files.py`: `HOSTS=("claude","copilot")`, `plugin_roles(host)` (from the installed agent
  files), `read_playbook(repo, host)` (calls `layers.load`), `plugin_root()`.
- `CLI playbook/lines.py`: how `playbook` prints a row (`agent=(generic)`, `model=(its file's)`,
  tools `(the caller's, not restricted)`): the strings the view's `tools` and start wording must match.
- `CLI core/repo.py`: `repo.external`, `repo.surface_root`, `repo.project_folder` (= `projects/<name>`,
  holds `chantier.yaml`; the planning folder `repo.changes` is `project_folder/changes`), `repo.root`
  (the code clone: the `repository` layer), `repo.session_root`. `layers.display(repo, path)` prints paths.
- `CLI lifecycle/backlog.py`: the model for a hash-guarded write: `sha256_of(bytes)`,
  `edit_markdown(repo, item, relpath, text, base_sha256)` under `changes_lock(repo)`, 409 via
  `EXIT_CONFLICT`. `edit_surface_file` copies this shape (but the file is outside `changes/`).
- `CLI board/write_api.py`: `_write(ctx, req, project_id, op)` (404 unknown project, 415 non-JSON,
  400/409 from `ChantierError.code` via `STATUS`), `_attempt`/`_answer` (build `results`, add one
  journal line with `journal.record(repo, kind, slugs, words)`), `ROUTES` list with `P` prefix,
  spread in `board/routes.py` `ROUTES` (`*write_api.ROUTES`). `config_api.ROUTES` is added the same
  way (one import + one spread in `routes.py`). `write_api._writer`, `_text` are private; reuse by
  import or copy minimally. `_answer` returns `ok/lines/results/journal` and 200 even for a
  GET-style read: `GET` needs a plain `as_json` handler like `journal_of`.
- `CLI board/journal.py`: `record(repo, kind, items, words)` appends to
  `changes/board-journal.jsonl`; any `kind` string works; `items` are slugs (use `[]` or the file).
- `CLI board/web/js/views/registry.js`: `VIEWS` array (add `{id:'config', icon:'config', word:'nav.config', module: config}`,
  no `overview`, so "All projects" skips it); `ui/icons.js` holds one SVG path string per name;
  `nav.*` words are in `i18n/en.js`/`fr.js` (not `en-board.js`: that file only merges `kanban.*`
  words), so `nav.config` goes in `en.js`/`fr.js` and the `config.*` words in `en-board.js`/`fr-board.js`
  as the spec says (check `en.js` merges `en-board`); `index.html` lists CSS links one by one (add
  `css/views/config.css`); writes go through `js/api/backlog.js`'s `write()` pattern
  (`BoardWriteError`, `route(project, path)`, `send`), which only accepts `ok` bodies: the config
  page needs its own `api/config.js` (a dry run and a 409 carry the view/problem lines).
- `docs/web-board.md` + `docs/web-board/<view>-pc|phone.png`; `scripts/docs_screenshots.py`:
  `views()` calls `goto(page, url, "<view>", "shop-api")` + `shot(page, "<view>", size)`; surface is a
  copy of `docs/demo/` (git init'd) so `docs/demo/projects/shop-api/chantier.yaml` is the file to add.
- `ruamel.yaml==0.19.1` is a runtime dependency (`pyproject.toml`), banned at module level (ruff
  `banned-module-level-imports`): import it inside `edit_surface_file`. Round trip (`YAML()` default
  `typ="rt"`) is available in the lockfile; no existing code uses it yet.

## Smallest change that meets the spec

1. `CLI playbook/edit.py` (new): `config_view(repo)`, `edit_surface_file(repo, changes, base_sha256, dry_run)`.
   Refactor `layers.py` minimally so `edit.py` needs no private access: expose the defaults-tree read
   and a "judge these layers" function (the tail of `load`: merge, `typed`, `_model_problems`, per host)
   that `load` itself calls; a candidate text is parsed with `yaml_subset.parse` + `config.check`
   in memory (line numbers of the new text), then judged with the other layers' trees.
2. `CLI board/config_api.py` (new): two handlers + `ROUTES`; one line in `routes.py`.
3. `board/web/js/views/config.js` (+ `api/config.js`, css, icon, words, registry entry, `index.html` link).
4. Text changes of section 4, demo `chantier.yaml`, `docs/web-board.md`, two PNGs, release notes.
5. Tests and scenario §20 additions.

## Pitfalls and risks

- `MODELS["copilot"]` is frozen at import; patching `copilot_catalog()` in a test does not change it
  or `resolve()`. The spec reads `plans` from `copilot_catalog()` at call time, matched by id: a test
  catalog with ids absent from `MODELS` gives an entry with no `plans`. Either iterate `MODELS`
  and look up plans by id (and the test patches `copilot_catalog` with ids drawn from `MODELS`), or
  patch `MODELS["copilot"]` too. Decide in the first round.
- `load()` returns `(None, [])` with no user file; a view must still show shipped defaults and the
  start per row. Per-row `start` is only computed inside `_model_problems` (mutates `roles`):
  extract it, do not duplicate the rules.
- The view's `refused` start (Q13) is an error in `load` but must NOT block the write nor the view:
  validation for a write must filter that one line out (as Q13 says) yet refuse the others.
- No existing in-process route test: `tests/test_board.py` has structure tests only; board routes are
  exercised in `scenario/run_scenario.py` (`board_writes`, `BoardProc`, `Link`, `call`). The
  parametrized `PUT/GET /config` tests need a new harness: build `Projects` (needs a `Repo` in
  external mode, see `tests/conftest.py`/`batch_helpers.prepared`), a `Context(projects, KeyFile,
  Seats, version, stop)` and call `routes.handle(ctx, Request(...))` with a cookie/header key
  (`guard.authorised`), plus `Content-Type: application/json` and the `guard.refusal` rules for
  writes (check the Origin/Host rule before writing the harness). "Autosync not called": assert
  the module's spawn/join functions are not invoked (see `test_board_does_not_join_autosync_implicitly`).
- `test_board.py::MODULES` lists the board's modules: add `config_api` there. `playbook/edit.py` is
  CLI code; the repo's startup-manifest budget (`STARTUP_LIMIT` 12288 in `test_startup_manifest.py`) is
  tight for `SKILL.md`: use the shorter wording the spec allows if it fails.
- File change is outside `changes/`: the board's fingerprint (`board/fingerprint.py`) will not see it,
  so the page must re-GET `/config` after a save instead of waiting for the state poll. The journal
  line goes in the project's `changes/board-journal.jsonl` (needs `repo.changes`, which exists).
- ruamel round trip: set `preserve_quotes`, a width large enough not to re-wrap; dumping always
  emits LF: the spec says LF, but a CRLF file would change every line in the autosync diff (say so
  in the PR; do not use `_with_endings` as `edit_markdown` does, spec overrides). Write with
  `Path.write_bytes(text.encode("utf-8"))` to avoid Windows newline translation; keep a leading BOM
  if the file had one (`config.read_tree` reads `utf-8-sig`). `sha256` is of the raw bytes.
- Removing a key must also remove emptied `roles`/host/`hosts` maps and a held reset
  (`default`/`~`/`null`) for that key; when the file has no key left, keep the file (comments) rather
  than delete it. A new file starts as `hosts:` only. A key set to `default` is refused (Q23).
- `chantier.yml` vs `.yaml`: the page must write the existing file (either), create `.yaml` otherwise;
  both present is Q1's refusal, and `layers.read_user` already emits that line (reuse the text).
- Q22: `overridden_by` must be computed per (host, role, key) from the `repository` layer's tree only
  (set or reset); the effective value stays the merged one. In-project mode (no surface): `writable`
  false, 409 on PUT, still a full read-only view.
- In the demo surface the code clone may not exist (`checkout.yml` only): `repo.root`'s file is then
  absent, which must read as "no repository layer", not an error. Check with the real demo run.
- The journal text for an overridden row names the repo file: `, overridden by <path>`; `_answer`
  joins texts with `; ` and the toast shows it: keep it one line.
- Windows: `display()` returns posix paths; compare layer paths via `Path.resolve()`, not strings.
- Nothing in `hooks/` or `types/` changes: no `just mod`; no CR board pane change: no pane screenshot.
- Value derived from an element others measure: none (no size or constant changes).

## Questions only the user can answer

None found. (The spec's `en-board.js` for `nav.config` is a placement detail: `nav.*` live in
`en.js`/`fr.js`; the Driver decides.)

## Evidence plan

Kind: new CLI code + board route + web page + docs + project-rule text. Evidence:

- `just check` and `just test` output (log in `work/gates/`), on this Windows machine; the
  pipeline's Linux/macOS jobs at the PR head; `just scenario` locally (CR on top of the stack).
- Screenshots: `just docs-screenshots` (Playwright, real board on the demo copy) writes
  `docs/web-board/config-pc.png` and `config-phone.png`; the PC one must show the "Copilot models"
  list with plans. Add `goto(page, url, "config", "shop-api")` + `shot(...)` to `views()`. Copy both
  into the CR's `evidence/` for the PR. Needs Playwright (uv script) and Chromium; if the browser
  cannot run, say so, never draw a stand-in.
- Command output: on a copy of the demo surface, start `chantier board` (the screenshot script's
  `make_surface`/`start_board` can be reused), then `curl`/`Invoke-RestMethod` with the key:
  `GET /api/projects/shop-api/config` (a row `overridden_by` a repository file: write a
  `chantier.yaml` in the clone, show the Copilot entries with `plans` and one `null`), one
  `PUT .../config` and its answer, and `git diff` of the written `projects/shop-api/chantier.yaml`
  (comments kept). Save as `evidence/config-get.json`, `config-put.json`, `config-put.diff`.
- Scenario §20 extension output (the log lines of the new `check(...)` calls); tests by name.
- Cannot be shown: a real Claude Code or Copilot session reading the new value at the next batch
  (the scenario shows `playbook` output only); the autosync commit of the surface file in a real
  surface (the scenario's fake autosync stands in, as spec section 6 says).
