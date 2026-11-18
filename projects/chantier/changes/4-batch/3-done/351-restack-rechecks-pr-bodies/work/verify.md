# Verify CR-351

Head: 5e73a369151e20182830b381a96fb84561e05642

Scratch repo (own git repo under work/scratch): base commit, an "old" commit 871f773 then reset away
(object still local, not in history), head a16fd49. Probe calls `delivery._stale_body_shas(None, None, <scratch repo>, <head>)`
with `work()` pointed at a temp body file, via `uv run --no-sync --project <worktree> python -I probe.py` (and probe2.py).
All judged at 5e73a369151e20182830b381a96fb84561e05642. Outputs in work/scratch/probe.log, probe2.log (removed at end; reproduced below).

| Body | Output | Expected |
|---|---|---|
| `Screenshots carried from `old`` + `Test plan 12 and 2026-11-17` | nothing (probe2) | not named: OK |
| `after carried from   old` (spaces, no backtick) | nothing (probe2) | not named: OK |
| `Verified at `old` (carried from `old`)` | `pr-body.md line 1 names 871f773, not in a16fd49's history: ...` | named: OK |
| `at `old` carried from `old`` | `line 1 names 871f773 ...` (same SHA elsewhere checked) | named: OK |
| `![after at old](https://github.com/acme/demo/blob/<old>/a.png?raw=true) carried from old` | `line 1 shows an image from 871f773, not in a16fd49's history: attach it with the forge's CLI: ...` (one line only) | image line: OK |
| `STALE <img src="https://raw.githubusercontent.com/acme/demo/<old>/b.png">` | `line 1 shows an image from 871f773 ... attach it with the forge's CLI: ...` | image line on STALE: OK |
| `STALE (judged at old, head now head)` | nothing | not named: OK |
| fixed body (`Verified at head (carried from old)` + non-commit image URL) | nothing | nothing: OK |

Card edits: `git diff HEAD~1 HEAD -- skills/chantier/references` at 5e73a369 read against 03-change-spec.md Cards:
pr-template.md (proof bullet, before/after bullet, Verified-at box comment) and driver.md (evidence bullet, SHA-marks sentence,
Review box sentence, clean-rebase paragraph, stack moved-PR paragraph, restack paragraph) all present and worded as specified; no agents/ change
(`git diff --stat HEAD~1 HEAD` lists 5 files: README, run_scenario.py, driver.md, pr-template.md, delivery.py). Off-line wording in cards matches delivery.py's two forms.

Not run by me: just check, eval-dry-run, scenario (gate/CI claims out of this task's scope). PR description not checked (not asked).

VERIFIED
