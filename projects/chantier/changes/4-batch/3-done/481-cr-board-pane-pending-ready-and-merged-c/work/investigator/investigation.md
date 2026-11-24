# Investigation, CR-481 (before round 1; read only)

Paths are under the worktree; `S` = `skills/chantier/scripts/cli/src/chantier`.

## Files and entry points

CLI side
- `S/status/views.py`: `dashboard_view(repo, paths)` (l.321) builds the index. Per batch it holds
  `crs_total` and `crs` = active CRs only (`status not in ENDED`). `_done_rows` (l.297) builds
  `ChantierPast` rows, but only for CRs in `<batch>/3-done` and across ALL batches; `_past` reads
  `5-archives`/trash (cap `PAST_LIMIT` 50). Helpers: `when_of`, `_link`, `shown_title`.
  The batch's `merged` = the CRs of `d.crs` with `status == "merged"`, wherever their folder is
  (`repo.planning_path(c.path)`; `c.merged_at`, `c.shown_pr()`, `c.cost_usd`). Extract the row
  construction of `_done_rows` into one shared builder and use it for both (no second copy); sort
  by `merged_at` desc. `created` = the batch record's `created` (confirm the field in
  `core/records.py`); `counts` = `Counter(c.status for c in d.crs)` (any status by its own name).
- `S/status/write.py`: `write_dashboard(repo, paths)` is the only writer of the index (callers:
  `commands/closing.py:304`, `commands/intake.py:128,204`, `lifecycle/backlog.py:90,115,119,208`).
- `S/board/state.py:169` also calls `dashboard_view` and picks fields one by one (web API stays
  unchanged). `S/status/markdown.py` `dashboard_markdown` ignores unknown keys.
- `S/hub/state.py`: `live_entry(git_dir, SERVER|HUB|WRITER)` (l.108, process-alive check),
  `read(git_dir)` (top-level `key`, `read_key`), `other_version`, `other_build`, `build_source()`.
  Server entry: `pid, version, source, started, host, port`; hub: `pid, version, source, started,
  idle, projects`; writer: confirm the `state`/`text` names in the writer code when coding.
- `S/hub/lock.py:102` `watchers(git_dir, project)`: session keys holding a lock now, creates nothing.
  Project name as `hub/lines.py:75`: `(repo.project_dir or repo.root).name`.
- `S/board/address.py`: `url(host, port, key=None)` gives the bare link. `local_url(host, port,
  key: str)` has a required key and always appends `?k=` (and returns None when not applicable): make
  `key` optional there (a falsy key gives no `?k=`); `read_only_lines` (`board/command.py:68`) keeps working.
- `build_note`: `hub/lines.py:foreign_build_clause` is gated on the dev checkout, so do not reuse it
  as is; write one small helper from `other_version` / `other_build` against the writing CLI's
  `__version__` / `state.build_source()`, returning one string or None.
- Git dir: `repo.git_dir` (`core/repo.py:99`; the surface's for an external surface).

Pane side
- `hooks/register.tsx` (1209 lines). Header comment l.1-4 ("no process but `git rev-parse`").
  `findRoot` l.252 runs it: `root = parentOf(common dir)`; only `root` is kept in the `site` atom
  (shape `site-4`). `readSessionId` l.179 (`site.sid.id`). Folds: `turned` atom, `isOpen`, `Section(key,
  byDefault, label, body)` l.1014. `Batch(b)` l.1024-1068 draws "Waiting for you", "Why", "In progress".
  `Board(v)` l.1155 draws header, batches, Backlog, Merged, Trashed (folded). Reuse `Crs`, `Pasts`,
  `Table`, `money`, `minutesSince`, `prCell`, `isWaiting`, and the `Link` component (used for the PR
  on the sheet page, l.1097) for the board links. `readJson($, path)` l.272 reads a file.
- `types/index.d.ts` (no imports): optional `merged?`, `created?`, `counts?` on `ChantierBatch`;
  `services?` on `ChantierIndex`; new `ChantierServices` type.
- Test: `hooks/register.test.tsx` (1430 lines): factories `row`, `index(over)` (older shape, good
  for "older file draws as today"), `batch(over)` l.690, `world(on)`, `w.put(path, data)`, `surface(w)`.
  Run by `claude plugin test .` through `just mod` (`scripts/mod.py`; no `claude` binary = exit 1,
  a stop per AGENTS.md).

Python tests (`skills/chantier/scripts/cli/tests/`): none reads the written dashboard `STATUS.json`
fields (`test_board_dashboard.py` is the web Dashboard page, unrelated). Build on `batch_helpers.open_batch`,
`conftest` (`SEEDED_COMMON_DIRS`, `_key`), `state.write_server(git, host, port, key, read_key)`
(`test_board_running.py:160`), `test_watch_events.py` / `test_watcher_autostart.py` for a held
`WatcherLock`, `dashboard_world.py` for record builders. Add one file (e.g. `test_status_index_services.py`),
2-3 parametrized tests: merged/created/counts; services with a live server (own PID) and a held
watcher lock, and neither key text in the file; no server gives `services.server` null.

Docs
- `CONTRIBUTING.md` l.174-186 "A mod": "no process but `git rev-parse`", "reads `STATUS.json`".
- `docs/boards.md` l.5-28 "The CR board (Claude Code)": "What it is" repeats the no-process claim;
  "How to read it" describes Waiting/In progress/Backlog/Merged/Trashed. Also grep README.md for the pane.
- Release notes: there is no unreleased-notes file; `docs/release-notes/<date>-vX.Y.Z/` is written
  by the release Driver at release time (`docs/release-process.md`; `just release-notes` only checks
  existing folders). See question 3.

## The smallest change

1. views.py: per-batch `merged` (shared row builder), `created`, `counts`. Compute `services` in
   `write_dashboard` (add to the view dict there) or behind an argument of `dashboard_view` that
   defaults off: `board/state.py` calls `dashboard_view` on every board read and `services` probes
   processes and lock files.
2. address.py: optional key on `local_url`.
3. types: the optional fields.
4. register.tsx: batch section = "Waiting for you" (kept) + one default-open group per non-empty
   state (queued, working incl. blocked, ready, merged via `Pasts` from `b.merged`) with distinct
   fold keys, and one figures line (counts out of `crs_total`, age from `created`, spend per merged
   CR). Backlog label `Backlog (N, K ready)`. New folded `Services` section from `index.services`
   (server/hub/writer state, this session's watcher via `site.sid.id` in `services.watchers`,
   "as of N min ago" from `services.at`, links with `?k=` from `server.json`, one line when unreadable
   or keyless, no read-only link without `read_key`). Update the header comment.
5. Docs as above.

## Risks

- Staleness: the index is rewritten only by `closing`, `intake` and `backlog` commands, not at each
  `take`/`ship`; "as of N min ago" may be hours. The spec accepts it (age shown).
- Where `server.json` is: for an external surface it is in the SURFACE's git dir. The pane's `root`
  comes from the session cwd's git; deriving `root + '/.git'` is wrong for a separate git dir or when
  the session's repo is not the surface's. Prefer keeping the common dir `findRoot` already gets in
  the `site` atom (shape bump `site-5`) over assuming `/.git`. Check, before coding, how a session
  in the chantier code repo reaches the surface's `projects/chantier/changes` in the pane; if it
  reads the code repo's git dir, `server.json` is not there (then: links without key plus the line).
  Re-read `server.json` at each check, not once (`--new-key` replaces keys).
- Publication: `STATUS.json` is committed and pushed by the surface writer (published paths), so
  `services` (PIDs, ports, the LAN address, `source` path) would reach the planning remote. No key,
  per the spec, but flag it (question 1).
- `local_url` signature change touches only `read_only_lines`.
- The keys sit in `server.json` beside; the test must search the written file for both key texts.
- Global `merged` list semantics unchanged (3-done first, capped at 50); the per-batch list is
  separate and uncapped. Values others measure from: no size or constant changes; `crs_total` appears
  only in views.py, types, register.tsx and its test.
- Fold keys are `scope + key`: new state groups need distinct keys or toggles collide.
- `just mod` needs a `claude` binary; none is a stop, no workaround.

## Questions only the user can answer

1. `services` published to the planning remote (LAN address, PIDs, build path): accept as the spec
   says, or keep it out of the published index? Not blocking; the spec chose it.
2. Release note: no unreleased file exists; add nothing in this PR (the release Driver writes them),
   unless the user wants a line now.
(Spend per merged CR: Driver's call; use the mean of the merged rows' `cost_usd`, say so in the PR.)

## Evidence plan

Kind: CLI file change plus a UI (pane) change.
- STATUS.json before/after: run a command that calls `write_dashboard` on the real surface or the
  scenario sandbox at the base commit and at the head; diff batch-31's entry and the new `services`
  (excerpt in `evidence/`, raw log in `work/gates/*.log`). Shows `merged`, `created`, `counts`, `services`.
- Python: `uv run --locked --group dev pytest -q <new file>`, red at base, green at head.
- Pane: `hooks/register.test.tsx` through `just mod`, output kept.
- Screenshot (AGENTS.md, required): real session `claude --plugin-dir <worktree>`, pane at batch-31
  showing CRs by state with merged CRs, captioned with the head's 7-character SHA, private link
  hidden (Services fold closed or key masked). Needs the user's terminal; until then the PR's Known
  gaps says "no screenshot of the pane from a real session".
- Gates: `just check`, `just mod`, `just eval-dry-run` in the worktree; long gate `scenario` in CI
  and the local Windows run per the batch's shape.
Cannot be shown: the pane without a real Claude Code session; process liveness (a snapshot only);
macOS/Windows pane rendering beyond the local Windows run.
