# Diagnosis: 3 test_forge_hub failures in the full `just test`

## Reproduction (serial, deterministic; same at base 9ff16d56 and at HEAD 682e37d4)
cd skills/chantier/scripts/cli
uv run --no-sync --project <checkout> python -m pytest -p no:xdist -q tests/test_open_no_clone.py tests/test_forge_hub.py -k "open_no_clone or config_line"
-> 7 failed (test_open_no_clone's own + the 3-4 test_a_config_line_ends_the_watcher... cases), also at the base worktree.
Same with tests/test_limits.py in place of test_open_no_clone.py. test_event_audience, test_plugin_files, test_validate do not leak.

## Cause
Not the CR's code. A pre-existing test-isolation leak: `chantier.cli.main` sets the module global
`repo.PROJECT = args.project` (cli.py:126) and never restores it. Tests that call `chantier("--project"...)`
(test_open_no_clone, test_limits) leave `repo.PROJECT = "demo"` set in the worker process. The next test on
that worker that calls `Repo.find()` directly, without `main` (test_forge_hub's
test_a_config_line_ends_the_watcher_and_is_told_in_its_form, line ~225 `found = Repo.find()`), reads
`project = project or PROJECT` (core/repo.py:107), takes the external path and raises
`no project folder <tmp>/proj/projects/demo in a planning surface` (repo.py:140), since its `repo` fixture is a
plain repository. Other test_forge_hub tests go through the `chantier` fixture or main, which reset PROJECT,
so only this direct-call test fails.

## Why only the CR's branch fails under xdist
`-n auto` distributes tests by load; the CR adds 2 test files and ~265 test lines (test_order_drop_to.py,
test_forge_moved.py), which shifts which tests land after a PROJECT-leaking test on one worker. At base the
distribution happened to avoid it. The CR's diff touches no PROJECT, Repo.find or hub code (checked: no
PROJECT/environ/chdir in orders_drop.py, moveout.py, records.py, history.py).

## Place to fix
Either (a) tests/conftest.py: an autouse fixture doing `monkeypatch.setattr(repo_module, "PROJECT", None)`
(or the value main's default is), or (b) in the test: `Repo.find(project=None)` is not enough (it falls back to
the global), so reset via the fixture; or (c) cli.main: restore PROJECT in a finally. (a) is smallest and
is the right fix; the leak is also a latent flake at base.
