# CR-104: why `just preflight` was red at 1ae8870 on this host

## Verdict

Host cause, not the CR. The host refused symbolic link creation (`WinError 1314`). During this
diagnosis the Developer Mode value changed to on (registry key last written
2026-11-25T22:33:06+01:00; not by me, writing it needs elevation). Since then the same exports
pass: base 0 failures, head 0 failures. Nothing in the code needs a fix. The long gate itself was
not rerun in the worktree.

## Reproduction

In an exported copy with its own environment (`uv sync --all-groups --python 3.13 --frozen`):
`uv run --no-sync -- pytest -n 4 -rfs`. It fails only while Developer Mode is off and the shell
is not elevated. Host probe: `probe_symlink.py` (this folder).

## 1. Base 2f09cef fails the same way (proved)

Export: `git archive` of 2f09cef under `work/scratch/dbg/base`; `okf_schema.__file__` and pytest's
rootdir resolve inside that copy.

| Run | Developer Mode | Failed | Passed | Skipped | Log |
|---|---|---|---|---|---|
| gate, head 1ae8870 (worktree) | refused 1314 | 8 | 1118 | 14 | `../gates/20261125-222513.log` |
| base export | refused 1314 | 8 | 1094 | 14 | `base-test.log` (ended 22:33:08) |
| base export | on | 0 | 1104 | 12 | `base-test-devmode.log` |
| head export | on | 0 | 1128 | 12 | `head-test-devmode.log` |
| base, CI `windows-latest` (run 45609498484) | runner | 0 | 1104 | 12 | `ci-base-windows.log` |

`compare_failures.py` on the gate log and `base-test.log`: same 8 names, 8/8 identical signature
(raising test line and exception text, temp folder numbers removed). Head has 24 more tests (the
CR's).

## 2. Only the missing right causes them; the diff is not involved (proved)

- Same export, same environment: 8 failures before the host change, none after.
- Probe after the change: `CreateSymbolicLinkW` with flags 0 is still refused with 1314 (the
  account holds no `SeCreateSymbolicLinkPrivilege`; `whoami /priv` does not list it; not
  elevated); with flag 0x2 (unprivileged create, honoured in Developer Mode) it succeeds, as does
  `os.symlink`. Token: not restricted, not AppContainer, medium integrity.
- Seven tests raise 1314 on their own `symlink_to` setup line (`test_cli_core.py:140`,
  `test_file_links.py:811` and `:840`, `test_kb_install.py:73` and `:88`,
  `test_skill_installer.py:152` and `:245`). The eighth creates the link in a callback; the
  installer wraps the 1314 in `InstallationError`, so the expected message does not match
  (`test_skill_installer.py:263`).
- Two more tests skipped for the same cause (`test_file_links.py:104`, `:131`): 14 skips became
  12. They ran and passed.
- The diff touches none of the four failing test files, nor `skill_installer.py`,
  `file_links.py`, `cli.py` or `okfkb/install.py`. It does edit `validator.py` (imported by the
  CLI) and two packaged `SKILL.md` files. A coverage run of the ten symlink tests on the head
  export (10 passed) executes no line of the changed function bodies; of the changed lines only
  the module-level `_ACTOR_RE` definition runs, on import (`changed_lines_executed.py`).

## 3. Later preflight steps, on the head export

The export was given an empty `git init` so that project root detection stops at the copy.

| Step | Result | Log |
|---|---|---|
| `just test` equivalent (`pytest -n 4 -rfs`) | pass, coverage 95.58% | `head-test-devmode.log` |
| `just refresh-okf-schema-example` | pass | `step-refresh-okf-schema-example.log` |
| `just refresh-okfkb-example` | pass | `step-refresh-okfkb-example.log` |
| `just refresh-okfreq-examples` | pass | `step-refresh-okfreq-examples.log` |
| `just requirements-report` | pass | `step-requirements-report.log` |
| `just docs`: `sphinx-build -W` | pass, with the worktree's modified `CHANGELOG.md` | `step-docs-sphinx.log` |
| `just docs`: its `just changelog` | not run here (no history in the copy); the same recipe passed earlier in the gate | gate log |

`export_diff.py` after the steps: the refreshes changed no content; 14 files under
`examples/okfreq-examples/` differ by line ends only (`.gitattributes` sets `eol=lf`, so no Git
diff is expected; not checked with Git). Other differences: the copied `CHANGELOG.md` and the
ignored `dist/` reports. No unresolved LFS pointer.

## `CHANGELOG.md` modified in the worktree

The diff is what `cz changelog` generates after 1ae8870: this CR's entry under Unreleased and the
`v0.18.1` heading now that the tag exists. Left as it is.

- No rule requires a fix commit to carry it. Product maintenance guideline, step 9, says to
  preserve legitimate generated changes (it names the changelog); the commit message guideline
  and CONTRIBUTING say nothing about it. CI does not check for a clean tree.
- History is mixed: 18 of 40 `feat`/`fix` commits up to 2f09cef carry it; of the 13 since
  c6fe92f (2026-10-06), 3 do and 10 do not. The version commit 2f09cef carries it. 1ae8870 does
  not.
- Driver's choice. Leaving it out avoids conflicts with the stacked CR-102 and CR-103; carrying
  it follows the letter of step 9. `just preflight` regenerates it either way.

## Options for the gate on this host

1. Keep Developer Mode on (current state) and rerun `just preflight`. Recommended: every step
   after `just changelog` that failed or was hidden now passes on the export.
2. Without Developer Mode: run the gate from an elevated shell (the user's action; not tried).
3. Without any host change: judge by the PR's CI (preflight on Ubuntu, macOS and Windows) plus
   the local steps run one by one, and record the exception.
4. Separate CR: make these 8 tests skip when links are unavailable, as
   `test_file_links.py:101-104` does. It hides the symlink safety checks on such hosts.

No host setting was changed by this diagnosis. Disposable exports and environments remain in
`work/scratch/dbg/` (ignored by Git).
