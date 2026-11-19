# Investigation CR-385: addressed events (first take)

Read at worktree head `4ca2f825` (branch `chantier/batch-28/cr-385-...`). `S` = `skills/chantier/scripts/cli/src/chantier`.

## Base state versus the spec

CR-375, CR-383 and CR-384 are all already in this worktree's history. Confirmed present:
- CR-375: `hub/autostart.py` (`session_key`, `watch_command`, `pull_command`, `board_clause`), `WatcherLock`, `not_running_line`.
- CR-384: `journal.py` has `config` and `board` kinds, `board_event`, `waking`, `config_text`, `board_text`, `_slots_line`; `hub/watch.py` has `once()` and the board clause; `board/write_api.py` and `board/config_api.py` write through `journal.append(..., "board")`.
- CR-383: `playbook/limits.py`, `limits_check.py`, `plugin_files.read_limits`, `limits_line`, `batch.slots` and `specifying` in the defaults.

Mismatches or points to settle:
1. The command that prints the `limits:` line is `chantier playbook`, declared in `declare/rules.py` and implemented in `commands/rules.py::playbook`. The spec is right on the name. The new `events:` line goes after the `limits_line` append (~line 90). The `--batch` branch also prints `limits:` live, so `events:` follows the same rule (live, "not readable" when problems).
2. `plugin_files.read_limits` returns `(found, problems)` through `limits.load_limits`, which returns `None` on ANY problem in any layer. `read_wake_rules` must split the problems into "events block" and "first other", so it cannot reuse `load_limits` as is.
3. The spec's "a problem tagged with its block": problems are plain strings `"<file>:<line>: <msg>"` (`layers._sink`). There is no tag. The smallest way is for the `events` checker to emit messages that start `events:` and to classify by the part after `file:line: `. The spec's messages already do (`events: unknown key ...`, `events: "wake_every" is ...`). A `events` key that is not a map is a third message to write (as `_limit`'s `"events" holds its key: ...`).
4. `timing_check.parse_duration` returns None below 60 s, so the `wake_every` check and reader cannot reuse it. The check needs its own (`_DURATION` regex reused, minimum 20 s).
5. `limits.held()` and `_one()` only read ints. `wake_every` is a duration, so a new reader (`playbook/events.py`, or a generalised `limits._one` with a parse function) is needed. Smallest: generalise `_one` and `held` with a `parse` argument.
6. `layers.read_defaults` calls `limits_check.missing_limits` (layers.py:102). `events.wake_every` in the shipped defaults should be added to that check (same pattern), otherwise "the shipped defaults hold it" is not enforced beyond the test.
7. `read()` currently returns `(entries, bad_line_numbers)`; 10 call sites use `[0]`, and `batch_status._seen_lines` unpacks both. A newer-version line must be named by line number in `status`, so the return needs a third item (the `(n, v)` of newer lines) or a flag. Smallest: a third list `newer: list[tuple[int, int]]`, and fix the `[0]` call sites to still work (they index `[0]`, so a 3-tuple is compatible; only `batch_status.py:241` unpacks and must change).
8. Start line: the spec puts `for <values>` right after the cursor, then `, the hub`. So the hub line becomes `watch: demo from cursor 0 for project, session:none, the hub`; the commas inside the list and before `, the hub` read ambiguously, and the scenario asserts `.endswith(", the hub")` (run_scenario.py:1825) and `startswith("watch: demo from cursor 0")` (1825, 1830, 1881). `test_forge_hub.py:255/259/266` compare whole start lines. These all need updating; decide a separator for the values (the spec says "values", I propose a space-less comma list is what it implies; confirm) before coding.
9. Session key `none` (no session id): the subscription then omits `session:`. Existing tests set a session id (`4ca2f825`). Scenario watchers run with the sandbox's key; their start line will be `for project` or `for project, session:<key>` depending on the environment, so the scenario must compute it, not hard-code.
10. `waking()` now also needs "for it": the filter is a new function in `journal.py` (next to `waking`) taking the subscription, so `hub/watch.py` stays thin. The spec says the rate limit lives only in the watcher; `hub/times.py` gets one function for the cap (`min(configured, test quiet)` under `TEST_ENV`).

## Files and entry points

- `S/hub/journal.py`: `append(repo, events, by)` becomes `(repo, events, source)`; line = `v, seq, t, kind, source, audience, payload`; `by` no longer written. Add `VERSION`, `KINDS`, `SOURCES`, audience form check (`^(project|user|role:[A-Za-z0-9-]+|cr:...|session:...)$`), `read()` normalising v0 (`source` from `by`, audience project), newer-version handling, `for_subscription(entry, subs)`. `_key` unchanged; docstring becomes the short reference. Writers need no code change (they pass `"hub"`/`"board"` positionally): `hub/cycle.py:126`, `board/prs.py:297`, `board/write_api.py:83`, `board/config_api.py:147`.
- `S/hub/watch.py`: `Watch.__init__` gains `audiences` (the `--for` values) and `wake_every`; subscription = `project`, own `session:<key>` (not `none`), `--for` deduped. `poll`: skip lines not for it (cursor moves, never in `events`, never sets `last_new`); end condition `now - last_new >= quiet_s and now - start >= wake_every`. `start_line` adds `for ...` and the `; configuration: ...` clause. `once()` filters. `watch()` validates `--for`, reads `read_wake_rules`, refuses before any lock (the lock is taken in `start_line()` through `elect()`, after the refusals: good).
- `S/declare/watch.py`: `--for` (append, repeatable), help text names audience, `--for`, end rule.
- `S/hub/times.py`: a `wake_every_s(configured)` capped by the test quiet.
- `S/playbook/config.py`: `events` into `_KEYED`, the unknown-key list text (line 84 has the list) and a `_events` checker (like `_long_gate`).
- `S/playbook/limits.py` / new reader + `S/plugin_files.py`: `read_wake_rules(repo)` beside `read_limits` (line 313), same `defaults` path (`plugin_root()/config/chantier.defaults.yml`).
- `S/playbook/lines.py` and `S/commands/rules.py::playbook`: the `events:` line.
- `config/chantier.defaults.yml`: `events: wake_every: 20s` (no `events`/`wake_every` in the file now).
- `S/commands/batch_status.py:241` (`_seen_lines`): unpack three, name newer lines.
- Docs: `docs/planning-folder.md` (new section; line 49 unchanged), `skills/chantier/references/chief-of-staff.md:1298-1301` (the watcher bullet; confirmed outside Startup core, which is a short section at the top), `AGENTS.md:75`, `CONTRIBUTING.md:125`, `scenario/README.md` (bullets ~295 and ~300ff), `hub/__init__.py` docstring (mentions the 20 s).
- Not touched: `core/files.py:149` IGNORED and `board/fingerprint.py:20` SINGLE (name unchanged).

## Smallest change

1. Journal line format and one `read` that normalises (everything else keeps calling `read`).
2. `Watch` filter plus `--for`, start line, `--once` filter.
3. `events.wake_every`: defaults line, check, reader, cap, `playbook` line.
4. `status` newer-line message.
5. Docs/card/AGENTS/CONTRIBUTING.
No new module except possibly a reader file; no hook, no type, no `board/web`.

## Risks

- Readers of `by` (search for the old field done): tests `test_board_config.py:154`, `test_board_journal.py:68`, `test_forge_hub.py:118,244`, `test_limits_cells.py:37`; scenario `run_scenario.py:1506, 1862, 1921, 1931, 8553`. Prepared old lines with `"by"` (`test_board_prs.py:245`, `test_limits.py:238`) are legitimate v0 fixtures. All must move to `source` (except the deliberate v0 cases).
- Every start-line assertion (item 8): `test_forge_hub.py:255,259,266,270`, scenario `1825,1830,1881`, plus scenario README text.
- Role-free test: a code line like the refusal text `role:<name>` is followed by `<`, so the structure test must match `role:[A-Za-z]`. The help text must not give a real role in an example (use `role:<name>`). The scenario's `--for role:griller` is outside `chantier/` and the defaults.
- `read()` adding keys to entries changes the dict shapes the tests compare (`shape(...)` in `test_forge_hub.py:118`); new fields `source` and `audience` appear in `read` output for every line.
- `_key` for `config`/`board` is `(kind, seq)`: unaffected.
- Dedup under a mixed v0/v1 file: v0 `merged` and a v1 `merged` for the same CR dedupe (key ignores audience/by): intended.
- Rate limit with `CHANTIER_HUB_TEST_TIMES` (`cycle:quiet`): cap needed, or scenario watchers (quiet 4 s) with the shipped 20 s would wait 20 s. The cap is mandatory in the scenario.
- A watcher with `wake_every` > quiet and an event arriving before `start + wake_every`: ends at `start + wake_every` if quiet has elapsed since the last event; events printed are all collected until then. Must be said in the help.
- Reading config at watcher start costs a few file reads (`read_user`, the defaults); `status` lines and the hub are unaffected.
- `plugin_root()` None (dev checkout vs plugin): matrix row "no plugin root" needs a test patching `plugin_root`.
- Windows: no new path or signal issue seen; the lock is already portable.

## Questions only the user can answer

None. Judgement calls for the Driver (spec-compatible): the start line's list separator (item 8), the third return item of `read` (item 7), and whether the shipped-defaults check also requires `events.wake_every` (item 6; suggested yes).

## Evidence plan

Kind: CLI behaviour and data-format change under `src/`, plus cards/docs text. No UI, no pane, no `hooks/`, `types/` or `board/web/` change: no screenshot, no `just mod`.

Before/after, each captured as text in `evidence/` (raw logs in `work/gates/*.log`):
1. The line format: a journal produced by the scenario's hub and board writes (copy of `forge-journal.jsonl`): before (main: `seq,t,by,kind`), after (`v,seq,t,kind,source,audience`). Technique: the scenario's `surface-board` and forge hub units (they already drive a fake `gh`), dumping the file. Unit tests prove each source, each refusal.
2. Version 0 and version 2 reading: unit tests on a prepared file (a case no writer produces: say so); the scenario unit with a v0 file then a board merge, watcher started with the printed `--after` prints it once.
3. The filter: parametrized unit tests on prepared audiences (`role:x`, `session:<key>`, `user`) for default and `--for` watchers, `--once`, start line, bad `--for` exit 2 with nothing written. Scenario: two watchers on demo (default and `--for role:griller`) both end on a forge merge.
4. The rate limit: unit test with injected monotonic clock: `wake_every` 60 s, event at 0 s, ends at 60 s not 20 s; shipped 20 s read from `config/chantier.defaults.yml`, the existing `test_a_watcher_ends_twenty_seconds_after_the_last_event` unchanged and green.
5. Configuration: `playbook` output for each row of the host and default matrix (shipped, surface project 2m, repository, no plugin root, `events` problem exit 3, `hosts` problem runs with the problem in the start line); captured as command output through the scenario's `surface-board` unit under the test times, and in-process tests for check texts.
6. The one-writer and role-free structure tests (grep-style, in `tests/`), the card/AGENTS/CONTRIBUTING text tests.
7. Gates: `just check` and `just eval-dry-run` in the worktree before the first push; the pipeline's `just scenario (ubuntu-latest)` green; the local `just scenario` on Windows if this CR is the batch top (the stack: 383, 384 below, and the surface server CR above is not yet in the batch).

Cannot be shown: the routing itself (no writer of a non-`project` audience exists; the proof is by prepared lines, stated as such), a cross-version upgrade with a real older chantier running (shown by a prepared v0 line only), the real forge (fake `gh`/`glab`), and the Windows run before the user's machine runs the local gate.
