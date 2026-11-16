# Verify CR-277

Head: 96ab57c7ac856fe43fea3ac73d196aa0fe1d9be3

All claims judged at 96ab57c.

1. What changes 1 (CLI line). `git diff origin/main -- .../commands/driver.py .../stacks.py`: `_ready_lines()` no longer calls
   `pr_base_of`; prints `<cr> PR in draft: its PR|the release PR <pr> is <state>; it waits <what>` with state from `pr_draft`
   (True/False/None) and what from new `draft_waited()` (CR + PR or `no PR yet`, `on the branch <b> (no CR of this batch)`,
   `for its turn out of draft`). `draft_waits()` is built on it (same answer). Line 1, ready-to-merge and ready-locally lines untouched.
2. What changes 2/3 (cards, docs). Same diff: driver.md hand-back bullet, concepts.md PR in draft entry, scenario/README.md updated as specified.
3. No agent file changed, status/ untouched (notify/state_label unchanged): `git diff origin/main --stat -- agents com.github.copilot | wc -l` -> 0;
   `git diff origin/main -- skills/chantier/scripts/cli/src/chantier/status | wc -l` -> 0.
4. Evidence 1-8. `uv run --locked python scenario/run_scenario.py --unit parallel --forge github` -> `ok parallel (github): 185/185 checks`
   (work/verifier/parallel.log). `... --unit stack --forge github` -> 132/132 checks, exit 0, only "over budget" on time, 340.5 s vs 320 (machine speed; PR Known gaps names it)
   (work/verifier/stack.log, stack-checks.txt). Ready lines seen in the transcript:
   - base_from_pr: `CR-106 PR in draft: its PR .../pull/45 is out of draft on the forge; it waits on CR-105 (.../pull/44)`
   - step 3: `... is a draft on the forge; it waits on CR-105 (.../pull/44)`; step 4: `... is out of draft on the forge; it waits on CR-106 (.../pull/45)`
   - run-1 case (forge base main): same line, check "never on `main`" [x]
   - `it waits on CR-106 (no PR yet)` [x]; `is of unknown draft state (draft not read: ship CR-107 .../pull/46); it waits on CR-106 (...)` [x], word stays PR in draft
   - step 9: `the release PR .../pull/47 is a draft on the forge; it waits on CR-105 (.../pull/44)` [x]
   Existing ready-to-merge / ready-locally checks all pass in both units.
5. PR #231 description (gh pr view 231, headRefOid 96ab57c): clean; Summary/Deliverables/Changes match the diff; Known gaps names the stack budget and the GitLab unit not run. Test plan boxes are the Driver's to fill.
6. CI green at head (given by the caller; not re-run by me). `just check` not run by me.

VERIFIED

## Description pass (head 96ab57c7ac856fe43fea3ac73d196aa0fe1d9be3)
Head: 96ab57c7ac856fe43fea3ac73d196aa0fe1d9be3
- `gh pr view 231 --json body,headRefOid`: head matches; Summary, Deliverables, Changes match `git diff --stat main...HEAD` (6 files: stacks.py, driver.py, driver.md, concepts.md, scenario README and run_scenario.py); renders (sections, fold); Known gaps names the stack budget and the GitLab unit.
- Test plan boxes carry SHAs; Review box cites e856ee7, which `chantier log CR-277` shows as "approved at 9d4136c, committed as e856ee7"; verified/CI boxes at 96ab57c (log: CI note and ship at 96ab57c).
- No role name outside product terms.

VERIFIED
