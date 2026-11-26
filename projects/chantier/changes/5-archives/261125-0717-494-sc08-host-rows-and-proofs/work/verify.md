# Verify CR-494

Head: ac0367164ca5827c7e47353fcbc186116b330fd6

All claims judged at ac03671 (worktree HEAD = PR 480 head, `gh pr view 480`).

1. `chantier host`, empty temp folder, no --project, CHANTIER_HOST=claude: first line `host: claude (this session)`; 50 rows, 13 `(proved)`, 37 `(untested)`, 37 sentences "This path was never tried for real here."; no proved row is followed by it. CHANTIER_HOST=copilot: first line `host: copilot (this session)`, 50 rows, 0 proved, 50 sentences. PASS.
2. With --batch batch-31: `host start-driver` prints `host: claude (batch-31)`, row marked (proved), no sentence, exit 0. `host nope` exit 2, `error: unknown capability `nope` on claude: one of start-foreman, ..., start-driver, ...`. PASS.
3. `pytest tests/test_host_rows.py`: 14 passed (9 test functions, parametrized). PASS.
4. For every date and batch-N of the cards (claude 26, copilot 3 distinct), grep finds it in docs/proofs/<host>.md: no MISSING. `git diff --stat origin/main -- skills/chantier/references` lists only hosts/claude-code.json and copilot.json (new); no .md card changed. PASS.
5. PR body (as posted, same head): 13 proved rows, 50 rows each, 37/50 and 50/50 sentence counts match; AGENTS.md paragraph, docs/hosts.md pointer, scenario README bullet and four run_scenario `host` checks present in the diff; `just test` here: 2719 passed, 20 skipped, 112.42 s (claimed 111.69 s, same order, within noise). Known gaps "UNVERIFIED scenario pending" is conservative (CI scenario is green at this head per the brief); not a failure. PASS.

VERIFIED

## Description pass

Judged at ac0367164ca5827c7e47353fcbc186116b330fd6 (`gh pr view 480` headRefOid equals worktree HEAD).

- Renders: sections, fold, no images. PASS.
- Matches diff: `git diff --stat origin/main...HEAD` lists the two hosts JSON (50 rows each, 13 proved / 0 proved by python count), two proof files, host_rows.py, commands/host.py, declare/host.py, cli.py, AGENTS.md, docs/hosts.md, scenario files, test_host_rows.py (9 test functions). Nothing unmentioned, nothing missing. PASS.
- Exit codes: commands/host.py raises EXIT_PRECONDITION for unknown capability. PASS.
- Review box: `chantier log` shows "r1 inspector approved at 64ff139" and "r1 approved at 64ff139f, committed as ac036716". PASS.
- Proofs name ac03671; Known gaps complete (no screenshot owed, no UNVERIFIED claim, Windows run owed by the top PR); internal references only in the last section. PASS.

VERIFIED
