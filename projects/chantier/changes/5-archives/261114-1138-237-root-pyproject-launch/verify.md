# Verification CR-237

Head: e54e29979ffcc3212ac4d0b4491a403a4e1d58c8

- E1: `just check` at head: exit 0 (ruff, mypy 77 files, uv lock --check, 63 tests, release-notes ok). Scenario 695/695 github, 676/676 gitlab and eval dry run 7/7 at e54e299 taken from work/gates/20261114-031608.log, not rerun.
- E2: `git diff <base> HEAD -- scenario/`: only the `cli: uv run --locked --project ` check and the `costs.session_usage_script()` line. OK.
- E4: `UV_OFFLINE=1 uv run --locked --project <worktree> chantier --version` -> `chantier 0.9.0`, uv.lock hash unchanged, tree clean.
- E5': git archive copy with no .git; `uvx --from <copy> chantier --project <p> --skill <skill> preflight`: P4/P5 ok (P6-P8 fail only because the session is a worktree, unrelated); without `--skill`: `error: cannot find the chantier skill folder: pass --skill <the skill's folder>`. cli_command() there prints `uvx --from "<copy>" chantier --skill "<copy>/skills/chantier"`. I did not run `take` itself (needs a batch); the line comes from cli_command, which take prints.
- E6.3/E7: branch SHA is on origin; `uvx --from git+https://github.com/gsemet/chantier@e54e299... chantier --project <scratch> board --port 8765` -> HTTP 200 on /, 1727 bytes.
- E8: `version.py set 9.9.9` in a scratch copy: 35 files, root pyproject.toml and uv.lock changed, plus the usual files, nothing else; `set notaversion` exit 1, wrote nothing.
- E9: medians of 10 warm runs of `--version`: dev form 492 ms, plugin form 403 ms.
- PR body vs diff: matches (root files, deleted nested files, allow rule, two scenario lines, version.py, Known gaps). Note: body says timings and board over HTTP are UNVERIFIED; they are now measured (above), so the body can drop those items. Remaining: cold cache not measured.


## Description pass (head e54e299, `gh pr view 171`; headRefOid e54e299 = HEAD, unmoved)

- D1: `git diff --stat <base>..HEAD` (31 files): body claims match (root pyproject/uv.lock, nested files deleted, 4 SKILL.md, allow rule `uvx --from * chantier *` at permissions.py:59, version.py, scenario lines). OK; claims carry E1-E9 above.
- D2: Test plan items all name e54e299 (CI unchecked, fine); cold cache UNVERIFIED has its Known gaps bullet. Fold layout, blank lines, order OK.
- D3: no internal reference outside Internal references (no CR/batch/role words in visible text). OK.
- D4 FAIL: `02-answers.md` records decisions that shape the change (one method; root pyproject.toml; dev mode runs local code live; plugin mode `uvx --from <plugin root>`), but the body has no `## Human decisions` section in Details (audit items 1 and 8). Add it, written with no internal reference.

Verdict: NOT VERIFIED (description only: Human decisions section missing)

## Description pass 2 (head e54e299 unmoved, \gh pr view 171\)

- D4 re-check: Human decisions section now in Details between Changes and Impacts; four bullets match 02-answers.md (one method, root pyproject, dev live, plugin uvx --from plugin folder); no internal reference. D1-D3 unchanged, OK.

Verdict: VERIFIED


## Description pass 3 (head e54e299, `gh pr view 171 --json headRefOid` = e54e299 unmoved)

- D5: Test plan CI box checked; `gh pr checks 171`: just check (ubuntu, macos, windows), eval-dry-run and scenario all pass. Claim matches. Rest of the body unchanged from pass 2.

Verdict: VERIFIED


## Move pass (e54e299 -> f108421, rebase)

- Patch-id of the CR commit identical before and after (7c54cd5f); diff e54e299..f108421 is only main's card files. Carried from e54e299: E2, E4 (re-run: chantier --version -> 0.9.0), E5', E6.3, E8, E9, D1-D5, because the patch is unchanged. Long gate passed at f108421 per the caller. CI on f108421 pending at check time (just check ubuntu pass).

Verdict: VERIFIED
