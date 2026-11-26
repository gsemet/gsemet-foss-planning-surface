# Verify CR-491

Head: 537465754469a0859833198e22e5adc35c27d9cc

All claims judged at 5374657. PR description not yet posted: not judged here.

1. Dry-run case alone (`python -I evals/kit/dry_run.py --case behaviour`), exit ok:
   `ok behaviour: the fixture's figures, regressions (one detector, one S-list line) and --since as expected; each detector matches its positive and not its negative example; the guard refuses a leak (exit 1, no file); --prune lists its two candidates and writes nothing (took 0 s)` / `dry run: 1 of 1 cases as expected`.
2. `behaviour.py --projects evals/kit/behaviour-fixture/projects --out <scratch> --since 2020-01-01`: exit 0, "8 files read, 0 skipped, 7 runs of 6 roles, 1 of no chantier role". JSON top keys hold every section-2 key (cards_commit, cards_date, commit, detectors, driver_runs_per_cr, files_read, files_skipped, first_event, host=claude-code, last_event, not_chantier_runs, previous, regressions, roles, s_list, schema, since, version, wake_shares, written). Each role holds runs, tool_calls, model_calls, card_bytes, files_read, cli, help, host_denials, write_guard_refusals, waits, tool_not_in_list, pushes. wake_shares for foreman and chief-of-staff; driver_runs_per_cr {crs 1, runs 2, mean 2.0}.
3. Detectors: independent regex run over evals/kit/detectors.json: all 9 ids match positive and not negative (True True each); floors 1,2,2,5,5,10,null,null,null as spec.
4. Committed baseline (json 87027 chars, md 52206): counts of home path 0, login name 0, `C:\Users`/`/Users/`/`/home/` 0, URLs 0, uuids 0, agent ids 0, "gsemet" 0.
5. ci.yml not in `git diff --name-only <base> HEAD`; `grep behaviour justfile .github/workflows/ci.yml` shows only the recipe (justfile:40-41); `check` does not reference it.
6. No --since, empty out: "no earlier measure in <out>: pass `--since <date>`", exit 2. `--prune` with zero and with one file: "needs two measures", exit 0.

Not checked: the posted PR description (not yet posted); the long gate (CI green per the brief).

VERIFIED
