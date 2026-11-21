# Verify CR-401

Head: d3ff96dc6b9deacede62add8509b3925b79a463e

All claims judged at d3ff96d (worktree clean, `git status --short` empty).

1. Gate pass: `work/gates/20261120-122042.log` first line: `gate CR-401 branch chantier/batch-29/cr-401-typed-journal-events-name-n-part-a-of-se head d3ff96dc6b9deacede62add8509b3925b79a463e`. CI green per brief (not rerun).
2. `just journal-schemas` at d3ff96d: output `uv run --locked python scripts/journal_schemas.py` (the recipe echo) and nothing else, rc=0; `git status --short` empty afterwards.
3. Spec §6 tests, at d3ff96d: `uv run --locked python -m pytest tests/test_event_types.py test_event_audience.py test_watch_events.py test_board_journal.py test_board_prs.py test_board_config.py test_forge_hub.py test_limits.py -q` -> `175 passed in 34.34s`. test_event_types.py holds the claims of §6: shipped schemas vs models in canonical form, normalized form, recipe merge, formats (parametrized), per-PUBLISHED-entry append/refusal/duplicate, CLI refusal, v1/v2 duplicate, read effective types, status lines skip.
4. Renames: grep of AGENTS.md, CONTRIBUTING.md, scenario/README.md, docs/web-board.md, skills/chantier/references/ and tests/ for `` `config` line``, `` `board` line``, `` role `config` ``, `` two-key `config` ``, `by: board`, `by: hub` -> no match.
5. Scenario checks: run_scenario.py lines 1521-1525, 1642, 1885-1886, 2002, 2024, 2029-2040, 2165 read `type`/`board@1`/`merged@1` and `v` 2. Remaining word "one `config@1` line" at 8907 uses the new name; known accepted gap (a check label/comment wording) is in PR Known gaps.
6. schemas.json tracked in git (`git ls-files --error-unmatch`), `.gitattributes` keeps LF.
7. PR description (work/pr-body.md): renders (sections, mermaid, fold); Summary/Deliverables/Changes match the diff stat (31 files: schemas.py/json, journal.py, cycle, prs, write_api, config_api, batch_status, tests, scenario, docs, cards, AGENTS/CONTRIBUTING); no image; Known gaps names the scenario wording gap and the no-screenshot note. Test plan boxes still hold `<sha7>` placeholders: the Driver fills them at ship.

Evidence before/after: not captured (no UI; behaviour proved by the tests above).

VERIFIED

## Description pass (PR 372), judged at d3ff96dc6b9deacede62add8509b3925b79a463e

Head: d3ff96dc6b9deacede62add8509b3925b79a463e

Command: `gh pr view 372 --json body` (same text as work/pr-body.md bar one trailing blank line), `git diff --name-only origin/main...HEAD`, `git diff origin/main...HEAD -- scenario/run_scenario.py`, `$CHANTIER log CR-401`, `gh pr view 372 --json statusCheckRollup`.

- Summary, Deliverables, Changes match the diff (31 files: hub/schemas.py and .json, journal.py, cycle.py, prs.py, write_api.py, config_api.py, batch_status.py, journal_schemas.py, justfile recipe, .gitattributes line for schemas.json, tests, docs, cards, run_scenario.py `type` reads): OK.
- Known gaps "None": run_scenario.py now reads `config@1`/`board@1` (diff shows it): OK.
- Test plan: gates d3ff96d (log: gate pass at d3ff96d), review notes (r1 committed as 7977684, r2 committed as d3ff96dc), CI 5 jobs SUCCESS, verified d3ff96d: OK.
- Rendering: sections, table, mermaid, json block, details fold well-formed; no images: OK.
- FAIL: Test plan Evidence line says "before at `d3ff96d`, after at `d3ff96d`". The before is the base 8bd198b (log: base=8bd198b18afe...); a before at the head is wrong. Fix to "before at `8bd198b`, after at `d3ff96d`" (or just "none captured").

NOT VERIFIED

## Description pass 2 (PR 372), judged at d3ff96dc6b9deacede62add8509b3925b79a463e

Head: d3ff96dc6b9deacede62add8509b3925b79a463e

Commands: `gh pr view 372 -R gsemet/chantier --json body`, `git diff --name-only 7977684 d3ff96d` (output: `scenario/run_scenario.py` only), `$CHANTIER log CR-401`, `gh pr checks 372`, `gh run view 44726824562 --json headSha` (d3ff96dc...).

- Summary, Deliverables, Changes match the diff (31 files; run_scenario.py line present): OK.
- Known gaps "None": remaining `kind` words in run_scenario.py are unrelated order/CR kinds; OK.
- Evidence line "none captured": OK (the false before at d3ff96d is gone).
- Review box: r1 "approved at 8bd198b, committed as 7977684", r2 "approved at 7977684, committed as d3ff96dc": OK.
- Verified, CI green at d3ff96d: CI 5 jobs pass on run at d3ff96dc; scenario gate log first line names d3ff96dc; check-r2.log passes: OK.
- Rendering: sections, table, mermaid, json block, details fold well-formed; no image: OK.
- FAIL: Test plan "Local gates at `d3ff96d`: ... `just eval-dry-run` (18 of 18)". The log shows the local eval-dry-run (18 of 18) ran at 7977684 only (note "before first push at 7977684"); none local at d3ff96d. The d3ff96d patch touches only scenario/run_scenario.py, so write "`just eval-dry-run` (18 of 18) carried from `7977684` (the later patch touches only scenario/run_scenario.py; CI's eval-dry-run job passes at `d3ff96d`)".

NOT VERIFIED

## Description pass 3 (PR 372), judged at d3ff96dc6b9deacede62add8509b3925b79a463e

Head: d3ff96dc6b9deacede62add8509b3925b79a463e

Commands: `gh pr view 372 --json body`, `git diff --stat main...HEAD`, `git show --stat d3ff96dc` (scenario/run_scenario.py only), `gh pr checks 372` (5 jobs pass, eval-dry-run included; headRefOid d3ff96dc), gate log head lines, `$CHANTIER log CR-401`, grep of run_scenario.py.

- Summary, Deliverables, Changes match the diff (31 files, .gitattributes, justfile recipe, schemas, writers): OK.
- Test plan: eval-dry-run now "at 7977684, carried to d3ff96d" with the reason and CI job: matches the log note and the d3ff96d patch: OK. Evidence line "none captured": OK. Gate at d3ff96d: scenario log "result: pass at d3ff96dc", check-r2.log passes: OK.
- Review box: notes "committed as 7977684" and "committed as d3ff96dc": OK.
- Known gaps "None": no UNVERIFIED claim; remaining `kind` words in run_scenario.py are unrelated: OK.
- Rendering: sections, table, mermaid, json, details fold well-formed; no image: OK.

VERIFIED
