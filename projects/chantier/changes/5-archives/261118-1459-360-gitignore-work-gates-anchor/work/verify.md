Head: 34588bf8e9bfeeadf19b0554030fbf9918e6a705

# Verify CR-360 (round 1)

1. Base: `work/gates/` alone does not ignore a CR's log. Judged at origin/main (files.py line 153 `"work/gates/"`).
   Scratch git repo, `.agents/changes/.gitignore` = `work/gates/`, file `2-backlog/P1/x/work/gates/out.txt`:
   `git check-ignore -v <file>` -> no output, rc=1. (The base CLI could not be run from a detached worktree: `uv run --no-sync` -> "program not found", no venv there; the base entry is shown by `git show origin/main:.../files.py | grep -n work/gates` -> `153:    "work/gates/",`, and git's own matching on that line.)
2. Head 34588bf8: real CLI (`chantier file probe` in a fresh scratch repo) wrote `**/work/gates/` in `.gitignore`;
   `git check-ignore -v .agents/changes/2-backlog/P1/x/work/gates/out.txt` -> `.agents/changes/.gitignore:22:**/work/gates/`, rc=0.
3. Head: a `.gitignore` holding only `work/gates/`, then `chantier file probe2`: old line kept, `**/work/gates/` appended; a second call (`probe3`) left `grep -c 'work/gates'` = 2 (appended once).
4. Tests at head: `pytest skills/chantier/scripts/cli/tests/test_driver_prompt.py -q` -> `11 passed`. Scenario diff has the changed init check (`"**/work/gates/" in ignore.splitlines()`) and the new `git check-ignore` check; `gh pr checks 325`: just check (3 OS), eval-dry-run, `just scenario (ubuntu-latest)` all pass.
5. PR description: clean, sections render, Summary/Deliverables/Changes match the diff (files.py, run_scenario.py, test_driver_prompt.py); no images; Known gaps consistent. Test-plan boxes are placeholders for the Driver to fill.

Scratch folder and detached base worktree removed.

VERIFIED

## Description pass at 34588bf8e9bfeeadf19b0554030fbf9918e6a705

Head: 34588bf8e9bfeeadf19b0554030fbf9918e6a705

6. Posted description (`gh pr view 325 --json body`, headRefOid 34588bf8): renders, no images; Summary, Deliverables and Changes match `git diff origin/main...HEAD` (files.py, run_scenario.py, test_driver_prompt.py). Known gaps consistent. Judged at 34588bf8.
7. Review box: `$CHANTIER log CR-360` shows "r1 approved at 5717626d, committed as 34588bf8"; matches the box (34588bf).
8. CI box: `gh pr checks 325` shows all 5 jobs pass (check x3, eval-dry-run, scenario ubuntu).

VERIFIED
