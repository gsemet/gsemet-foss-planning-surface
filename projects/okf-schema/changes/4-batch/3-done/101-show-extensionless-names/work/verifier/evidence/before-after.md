# Before and after

- Before: base `2f09cef3e786d1696e42b5cb305d4a55111e7725`
- After: head `41fcd6dbebaddff719c2a3f54f610298034d0ad6`
- Host: Windows 11, Python 3.12.10, symbolic links permitted
- Local folders are written `<disposable>`, `<base>`, `<worktree>`, `<probe>`, `<others>` and
  `<scratch>`. Every pair of the evidence plan was captured.

The base ran from a detached worktree (`git worktree add --no-checkout --detach <base>
2f09cef3e786d1696e42b5cb305d4a55111e7725`, then `git checkout <same sha> -- src tests
pyproject.toml` in it, a partial checkout that keeps paths short on Windows). The same virtual
environment ran both sides, with `PYTHONPATH=<base>/src` for the before; each output names the
package it imported. The worktree and the disposable folders were removed afterwards.

## Pair 1: the `show` command

Files: `before-show.txt`, `after-show.txt`.

| Step | Before (base) | After (head) |
|------|---------------|--------------|
| `api/health-check`, `/api/health-check` | not found, exit 2 | concept shown, exit 0 |
| `/etc/passwd` | not found at the drive root, exit 2 | not found inside the bundle, exit 2 |
| `api` (a directory), `.` | traceback `PermissionError`, exit 1 | `Concept not found`, exit 2 |
| `../../secret.md`, absolute outside path, `leak.md` (link leaving) | outside file printed, exit 0 | `Concept path is outside the bundle`, exit 2 |
| `../../secret`, `../../missing`, `leak` | not found, exit 2 | outside the bundle, exit 2 |
| `\api\health-check` | not found at the drive root, exit 2 | outside the bundle, exit 2 |
| name with `.md`, absolute inside path, `api/../api/health-check.md` | shown | shown (unchanged) |

In this pair no file `bundle.md` sat beside the bundle, so `.` is "not found". The PowerShell
scenario below adds that file, and `.` is then "outside the bundle".

Reproduce, in an empty folder:

1. `git init`, `okf-schema init my-knowledge-base`,
   `okf-schema new --path my-knowledge-base/bundle --name api/health-check`.
2. Append the line `The service answers.` to the new concept; write `secret.md` holding
   `SECRET-MARKER` in the folder; make `my-knowledge-base/bundle/leak.md` a symbolic link to it.
3. Run each command listed in the files, once per side.

## Pair 2: the new tests on the previous code

Files: `before-tests.txt` (22 failed, 15 passed), `after-tests.txt` (37 passed).

Reproduce: the command is the second line of each file. For the before, the three test files are
taken from the head into the base worktree (`git checkout 41fcd6d -- tests/test_api.py
tests/test_cli_remaining.py tests/test_edge_cases.py`) and run against the base sources.

## After only (no before: these show the head's documented behaviour)

- `after-scenario-powershell.txt`: the specification's scenario steps and `show --help`, from
  PowerShell.
- `after-scenario-git-bash.txt`: Git Bash rewrites a leading `/`; with `MSYS_NO_PATHCONV=1` the
  concept is shown.
- `after-probe-names.txt`: unusual names (empty, directory, link loop, junction, UNC, device
  names, very long names), with the exit code and the count of files read outside the bundle.
  Setup: a bundle with `concept-a.md` and `sub/`, an outside folder with `secret.md`, and in the
  bundle the links `away` (folder), `rel-leak.md`, `chain.md`, `dangling.md`, `loop` (to itself)
  and a junction `junction`; call `show_bundle` and the `show` command with each listed name while
  recording `Path.read_text` calls.
- `after-other-commands.txt`: `validate`, `list`, `backlinks`, `lint --check` and `index` on a
  bundle holding a link that leaves it (the known gap).
