# Diagnosis: surface-board "a missing clone fails preflight and names the path and the remote"

Reproduction (worktree): `uv run --locked python scenario/run_scenario.py --unit surface-board --forge github --keep --verbose`
(log: work/scratch/sb.log). Reproduces locally: the check's `out` is `[]`, and the transcript shows
`$ chantier --project demo preflight -> exit 2`, `stderr: error: no folder <tmp>/external/code: git cannot run there`.

## Cause
Preflight does not print P8 at all: it dies with a ChantierError before printing anything.
`git()` (core/git.py:29) raises `no folder <cwd>: git cannot run there` when its `cwd` is not a directory.
CR-463 changed commands/permissions.py to run two git reads with `cwd=repo.root if repo else None`:
 - `_forges`, line 114: `git("remote", "get-url", remote, cwd=repo.root ...)`
 - `commands_not_allowed`, line 301: `git("remote", cwd=repo.root ...)`
In external (surface) mode `Repo.root` is the project's clone (repo.py:98), which is the folder the scenario
renames away. Preflight reaches them through `_check_allow` (host claude, preflight.py:306-307), after `_check_project`
had appended P8 to `r.lines`; the exception propagates out of `preflight()`, so no lines are returned and exit is 2 from the raise,
not from a failed P8. Before the CR these reads used the process folder (the surface), which always exists.
Main is green for that reason. Everything else the CR touched is fine: `session_checkout` runs in the process cwd, and
P8's `missing_clone()` check works (guards `clone.is_dir()`).

## Place to fix (product code, not the scenario)
core/commands: commands/permissions.py lines 114 and 301. The forge-remote read of the project's code must not
raise when the clone is absent (preflight must report P8 and carry on). Options, smallest first:
 1. Add a small helper in permissions.py, e.g. `_code_folder(repo)` returning `repo.root if repo and repo.root.is_dir() else None`
    (None = process folder, as before) and use it at both sites. Beware "no fallback": a cleaner variant is to
    skip the read when the clone is missing (remotes = [], url = "") since P8 already reports the missing clone and
    the forge is unknowable; but then `remote not in remotes and remotes` is already safe with an empty list.
 2. Or catch only in these two reads (`check=False` does not cover the missing-folder raise).
Keep the intent of the CR (read the project's own remote, not the surface's): with the clone present the behaviour is unchanged.
Add no scenario change; the existing check covers it. Also worth a glance: `_settings_rules` uses
`session_checkout().top or repo.session_root` (safe: a real, existing folder).
