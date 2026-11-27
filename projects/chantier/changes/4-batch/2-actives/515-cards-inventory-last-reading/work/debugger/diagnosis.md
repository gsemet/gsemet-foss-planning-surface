# CR-515: `just check` fails 2 tests at 22ccbe0 on Windows

Cause: the environment. The Driver's run had `NO_COLOR=1`; the test depends on it being unset.
Not this CR's diff, not what fbdb53d2 changed, not flaky.

## Reproduce

From the worktree (Bash):

    NO_COLOR=1 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider \
      skills/chantier/scripts/cli/tests/test_live_ready.py -k colours_the_state_words

Result: 2 failed. With `env -u NO_COLOR` in front instead: 2 passed.

## Evidence

- Matrix (`../../evidence/debugger-no-color-matrix.txt`; script `probe.sh`): at 22ccbe0, at
  origin/main fbdb53d2 (exported tree) and at the old base 4d12a5be (exported tree), the test
  passes with `NO_COLOR` unset and fails at line 221 with `NO_COLOR=1`. At the head, 20 runs of
  each setting alone: 20 passes, 20 failures. So the failure predates fbdb53d2 and the CR.
- Neither `test_live_ready.py` nor `uv.lock` differs between 4d12a5be and 22ccbe0.
- This host's PowerShell tool has `NO_COLOR=1` at process scope only (User and Machine scopes
  empty); the Bash tool does not set it. In PowerShell, as is: 2 failed; after
  `Remove-Item Env:NO_COLOR` in that shell: 2 passed.
- The red log (`../scratch/driver-just-check-22ccbe0.log`) is a PowerShell run (`just check *>
  $log`, `NativeCommandError` header). The earlier green logs (`coder-just-check.log`,
  `coder2-just-check.log`, `inspector-just-check.log`) carry no such header: consistent with a
  Bash run. Their shell and environment were not recorded, so that part is inferred.
- Mechanism: `_interactive()` (`test_live_ready.py` lines 197-205) builds a rich `Console` with
  `force_terminal` and `color_system="truecolor"` but no `no_color`; rich then reads `NO_COLOR`
  (`rich/console.py` line 728) and strips colours (line 2139). Links stay, so line 220 passes and
  line 221 (the two RGB codes) fails. `rich_probe.py` shows both sides.
- Full gate at 22ccbe0 from Bash, `NO_COLOR` unset: `just check` exit 0, 2785 passed, 19 skipped
  (`../scratch/debugger-just-check-22ccbe0.log`).

## Place to fix

- This CR: nothing to change. The gate is green at 22ccbe0 in a shell without `NO_COLOR`.
- The test's fragility is on main, outside this CR's subject: pass `no_color=False` to the
  `Console` in `_interactive()` (`skills/chantier/scripts/cli/tests/test_live_ready.py`, line
  201). Probed on rich alone, not applied to the test. Whether to file it is the steering
  session's call. The product's own `Console()` (`clients/tui/screen.py` line 375) honouring
  `NO_COLOR` needs no change on this evidence.

## Not checked

- Linux and macOS; CI at this head (nothing pushed).
- Which program sets `NO_COLOR` in the PowerShell tool (only its scope was read).
