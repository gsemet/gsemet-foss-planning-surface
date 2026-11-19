# Diagnosis, CR-383 scenario red (surface-board)

Reproduce (worktree, ~250 s, unit over its 300 s budget locally too):
`uv run python scenario/run_scenario.py --unit surface-board --forge github`

Cause: hypothesis confirmed. After CR-375 (fe2c215e) a `chantier watch` that ends on an event prints a last line
`watch: <batch> still running: for the Chief of Staff, start again in the background now: <cli_form> watch --after N`
instead of `watch: cursor N; next: chantier watch --after N`. scenario/run_scenario.py lines 8488 and 8504-8505 still
expect the old cursor line. Actual got (local, same as CI):
['config changed on the board: ...', 'watch: batch-01 still running: for the Chief of Staff, start again in the background now: uv run --no-sync --project "<repo>" chantier --project "<surface>/projects/demo" watch --after 1']
(and `--after 2` for the second). Event lines are right; only the last line is stale.

Fix, in `surface_config_page` (scenario/run_scenario.py ~8437-8505): build the expected line the way the watch unit does
(lines 1764-1770): `cli_form = f'uv run --no-sync --project "{SKILL.parents[1].resolve().as_posix()}" chantier --project "{(w.surface / "projects" / "demo").resolve().as_posix()}"'`,
then `cursor = lambda n: f"watch: {w.name} still running: for the Chief of Staff, start again in the background now: {cli_form} watch --after {n}"`.
- line 8488: `got == [told, cursor(1)]`
- lines 8504-8505: `got == ["config changed on the board: specifying.parallel 4 -> 1", cursor(2)]`
Ideally lift `cli_form`/`cursor` into one shared helper used by both places. The two check names stay ("ends with ... and its cursor").

Separate note: the local run took 248 s (CI 149.9 s) against the 300 s budget; not a failure here.
