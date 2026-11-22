# Verify CR-458

Head: bfdf5a2b9b4984de70ee71f2f86494984a00d0a7

Verdict: VERIFIED

Claims, each judged at bfdf5a2b9b4984de70ee71f2f86494984a00d0a7.

1. Unit tests for the new paths pass. Command, from `skills/chantier/scripts/cli`:
   `uv run --no-sync --project <worktree> python -m pytest tests/test_remote_cli.py tests/test_server_api_calls.py -q`
   Output: `50 passed in 48.92s`.
2. End to end (login, profile, forwarded commands, refusals, logout) on a real served surface.
   Command, from the worktree: `uv run --locked python work/verifier/run_remote_cli.py <out>`, which runs scenario case `remote_cli`.
   Output (log: `work/verifier/remote-cli.log`, keys and home path redacted): `surface-board on github: 13/13 checks passed`. Checks:
   - `login <private link>` stores the default profile and prints no key.
   - A remote `file` and a remote `note` land in the server's planning folder.
   - A remote `status` equals `status --profile local`, less the `watch:` line.
   - `gate` is refused through a profile (exit 1).
   - A read profile (`--no-default`) keeps the default, and a forwarded `note` under it is refused before any request.
   - `login` with no link lists the profiles without keys.
   - `logout` ends the profiles, and `status` runs locally again.
   - With the server stopped, a remote `status` exits 4 with `error: remote:`. A command for another project still runs locally (exit 2).
   - Nothing was written outside the planning folder.
3. The PR description on the forge equals `work/pr-body.md`, apart from a trailing newline.
   - Its Summary and Deliverables match the diff: `cli.run`, `profiles.py`, `remote.py`, `login.py`, `origin.py`, `idle.py`, the `live` and `webui` changes, and the docs, AGENTS.md and eval kit changes.
   - The small `autostart.py` change, no `watch:` line under a forwarded command, is in the Summary's behaviour.
   - Known gaps (no remote watcher, no real eval) are stated.
   - No image is attached.
4. CI at this head: check x3, scenario ubuntu and eval-dry-run, all green, per the brief. Not re-run here.
5. Review box: the PR body says `Review: pending` (a draft), so there is no claim to prove.

Not proved: Windows or macOS runs of the long gate, which the Driver owes.

## Description pass at bfdf5a2b9b4984de70ee71f2f86494984a00d0a7

Command: `gh pr view 434 --json body,headRefOid` (headRefOid bfdf5a2b9b4984de70ee71f2f86494984a00d0a7); `git diff --name-only bb8765a4 HEAD`; `gh pr checks 434`; `$CHANTIER log CR-458`.
- Template order, fold (blank lines after summary and before details, nothing after) and audit items 1-3, 6, 7, 10: in place. No internal reference outside Internal references; no role name; no image attached.
- Summary, Deliverables and Changes match the diff (cli_run.py, profiles.py, remote.py, login.py, declare/remote.py, origin.py, remote_wire.py, idle.py, live/webui, docs/server-api.md, AGENTS.md, chief-of-staff.md, evals/kit, scenario, tests).
- Test plan: Local gates at 6f91973 matches the note 16:39:43; Review matches the note 16:52:20 (inspector APPROVE at bfdf5a2); Verified at bfdf5a2 matches the verdict event 17:01:27; CI checks all pass per `gh pr checks 434`.
- Known gaps (no remote watcher, no real eval) accurate; no UNVERIFIED claim in the body.
Verdict: VERIFIED
