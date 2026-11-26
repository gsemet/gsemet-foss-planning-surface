Head: f7b74e64be590ce2650b03f5209dbc7b00b040cd

# CR-502 verification (PR 484), judged at f7b74e64be590ce2650b03f5209dbc7b00b040cd

Base compared: d05934da (CR-500's head). Scratch project and base worktree removed at the end.

## Part 1, retro draft (all at f7b74e6, scratch project, own git repo, CLI from the worktree)
- Prints the draft: `chantier retro draft --epoch 0 --batch batch-01` on 8 prepared events (ask, two same `refused:` notes on two CRs, blocked handback, restart take, gate fail + stopped, pause) gave exit 0 and:
  `retro draft: batch-01, events 3..10, CRs CR-001, CR-002 (5 points)`, `cost: not read (no Foreman transcript recorded: ...)`, the begin/end markers, 5 points each followed by the three lines `home:`, `count:`, `why not code:`; refusal grouped `(2 times) (events 4, 5)`, the stopped gate not counted, last line `next: judge each point, ...`.
- Writes nothing without `--write`: sha256 of events.jsonl and batch.json equal before/after, retro.md absent before and after.
- No `--epoch`: exit 2 (`retro draft --epoch <n>: the steering session's command`). Stale `--epoch 5`: exit 3.
- `--write` on a file `## Author\n\n- my own line\n`: exit 0, `written: 4-batch/retro.md (5 points appended after 25 bytes of your text)`; file starts with the author bytes (od), one draft marker (grep -c = 1). Second `--write`: exit 2, `already has a draft section; retro draft --epoch 0 prints this one`, file `cmp` unchanged. events.jsonl stays 10 lines (no event logged).
- `--since 99` and `--since -1`: exit 1, text names `retro draft --since 0`; `--since 0` gives events 1..10.
- `uv run --no-sync --project . python -m pytest test_retro_draft.py test_launcher.py test_roles_data.py test_brief.py test_launch_modes.py`: 93 passed in 12.16 s.
- Scenario step and coverage bullet present (git diff d05934da..HEAD scenario/README.md); CI scenario green per Driver note (not rerun here).
- AGENTS.md exception line for `retro draft` present in the diff.

## Part 2, launcher (f7b74e6; launcher.py, launch.py and chantier.py are unchanged since d7db74a where the trial ran: `git diff --stat d7db74ae..HEAD -- <those files>` printed nothing)
- In a non-chantier project, `UV_OFFLINE=1 uv run --script .../chantier.py --print` printed `uvx --from "<root>" chantier --skill "<root>/skills/chantier"`, exit 0; `--sync` printed `plugin mode: no sync (only chantier's own checkout syncs)`, exit 0; `--version` printed `chantier 0.15.1`.
- From the checkout: `--print --project <surface>/projects/chantier` printed `uv run --no-sync --project "<root>" chantier --project "<surface>/projects/chantier"`; `--sync` printed `in sync`, exit 0; `--project <surface>/projects/chantier --version` printed `chantier 0.15.1`. `.venv/pyvenv.cfg` unchanged (13:31).
- Note: `--project X --print` (print not first) is passed to the CLI and errors, as the spec says `--print` is first-argument only; `--print --project X` works.
- Trial: judged from trial.md. Settings scratch, `claude -p --permission-mode dontAsk --setting-sources project`, Claude Code 2.1.326; launcher ran with Bash and PowerShell under its rule, dev form control ran, negative control refused the launcher in both tools, stop check found the CLI left running on Windows (recorded as Known gap, as the spec allows); consistent with the spec's pass/fail rules and with the PR text (overhead +128/+145 ms, same figures). Auto mode, subagent, Copilot, POSIX unproved, as the PR says.

## Part 3, roles.yaml
- `just roles` at f7b74e6: `roles: 18 roles, 15 wrappers on 2 hosts agree`, exit 0.
- On a scratch copy with coder's claude tools trimmed: `roles: coder (claude): tools [...] differ from roles.yaml's [...]`, exit 1 (the two other lines are from my copy leaving out the skills folders). `--write coder --host claude` printed `=== agents/coder.md` and the frontmatter; `--write foreman` printed `foreman has no wrapper`, exit 1; `git status` clean after (writes nothing).
- brief unchanged: in-process script, CLI at base d05934da vs head, 2 hosts x 18 roles x 5 units (none, CR-101, stack, O-1, folder) x with/without `--epoch` = 360 calls, each exit code, message and (for the 52 that wrote a brief) sha256 of the brief file with the root path normalised: the two outputs are byte-identical (sha256 of both listings b57c2d497af4cedf; files in verifier/evidence/briefs-base.txt and briefs-head.txt).
- help: for the 18 roles the output is identical at base and head. The only differences: `help --for nosuchrole`, `--for router`, `--for status` now refuse with the 18 role names (exit 1) where base printed `no topic for ...` (exit 0) or the 20-name manifest list. This is the exception the spec section 4 states (open question 3).

## PR description (pr-body.md)
- Summary, Deliverables, Changes match the diff (30 files; roles, launcher, retro, AGENTS.md, scenario). Known gaps lists the stop check finding, unproved cells, overhead, the unfilled draft archive. No image. Review/Verified/CI boxes are Driver-filled. Observation for the Driver: `log` holds `inspector approved` notes at 2ced739e and d7db74ae only; none cites f7b74e6 (part 3, roles), so the Review box must cite what the log proves or a new review note is needed.
- `just test` seconds are stated with the base and head figures (117.1 s to 130.6 s).

VERIFIED
