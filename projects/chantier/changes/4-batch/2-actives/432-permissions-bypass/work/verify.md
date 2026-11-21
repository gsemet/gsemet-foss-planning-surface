# Verify CR-432

Head: 1559e15b583fc2332015b6142e5e179716b851d1

All claims judged at 1559e15 (worktree clean, `git rev-parse HEAD` = the full SHA above). Rules read first (`$CHANTIER rules`): AGENTS.md, CONTRIBUTING.md, chief-of-staff.md and others; nothing there changes this check. CI is green at this head per the brief; no long suite re-run.

## 1. Trial (evidence/trial.md)
- Read `evidence/trial.md` (Claude Code 2.1.326, Windows, `dontAsk`, `--setting-sources local`): a, c, e ran; b, d, f, g, h, i refused; quoted form ships. Controls h and i refused, so the setup is sound.
- Spot-check at 1559e15, `python matrix.py quoted ab` (scratchpad `trial/matrix.py`): case a Bash and PowerShell ran the command (`uvx --from "C:/Users/gaeta/Projets/chantier" chantier --skill ".../skills/chantier" status` -> the CLI answered `Exit code 2 error: not inside a git repository`, so the rule let it through); case b Bash and PowerShell refused (`Permission to use Bash has been denied because Claude Code is running in don't ask mode`; same for PowerShell) for `uvx --from "/elsewhere" chantier status`. Consistent with trial.md.

## 2. P10 run for real (preflight at 1559e15, scratch HOME and scratch git project, `USERPROFILE`/`HOME` pointed at it; throwaway removed)
Plugin mode = copy of the skill folder without `.git` (`--skill <copy>` and `CHANTIER_SKILL_DIR`); dev mode = this worktree.
- Plugin, no chantier rule: P10 warn names `add Bash(uvx --from "<copy>/..plug" chantier *)` and PowerShell form, with the real path; no dev rule named.
- Dev, no chantier rule: names `add Bash(uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-432" chantier *)` (the Bash form allowed by nothing; both tools shown) and `add Bash(uv sync --locked --project "C:/.../batch-30-CR-432")`.
- Filled recommended rules alone (`filled_allow()`), both modes: `P10 ok   every batch: the commands its agents run are allowed by your settings; not checked here: a stack, ...`.
- Broad rules only (`Bash(uvx --from * chantier *)`, `Bash(uv run --no-sync --project * chantier *)`, `Bash(uv run --script * *)`) in the scratch HOME settings:
  - plugin: `P10 warn ... broad rules let any command through, remove them by hand: Bash(uvx --from * chantier *) (<home>/.claude/settings.json), replaced by Bash(uvx --from "<plugin copy>" chantier *); Bash(uv run --no-sync --project * chantier *) (...), no chantier command needs it; Bash(uv run --script * *) (...), no chantier command needs it`
  - dev: `... Bash(uvx --from * chantier *) (...), no chantier command needs it; Bash(uv run --no-sync --project * chantier *) (...), replaced by Bash(uv run --no-sync --project "C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-432" chantier *); Bash(uv run --script * *) (...), no chantier command needs it`
- Filled rules plus the three broad ones: P10 stays warn (not ok) even though all commands are allowed; plugin: `Bash(uvx --from * chantier *) ... replaced by Bash(uvx --from "<plugin copy>" chantier *) present`; dev: `Bash(uv run --no-sync --project * chantier *) ... replaced by ... present`; the other two "no chantier command needs it".
- Stale (filled rules + `uvx --from "C:/old/plugin" chantier *` + `uv sync --locked --project "C:/gone/checkout"`): plugin mode names both under `stale chantier rules, remove them by hand: ... (<home>/.claude/settings.json)`; dev mode names only the gone sync rule and leaves the plugin-form rule alone (Q21, Q22). Missing-command count unchanged (line stays "allowed ... ; stale ...").
- Preflight exit code in the scratch project was 2 in every case including `P10 ok` (other checks of the bare scratch project), so P10 does not drive it; the one-line P10 fits the output cap.
- Tests at 1559e15: `pytest tests/test_allow_rules.py tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks -q` -> `3 passed in 15.09s`.

## 3. Cards against spec section 3 (git diff base..1559e15)
- hosts/claude-code.md: three rows carry `"<checkout>"` / `"<plugin root>"`, Risk accepted "every chantier subcommand of the checkout/plugin at that path" with the `gate` and `lease hold` note; Mark "rule matching proved (main session, `dontAsk`; 2026-11-21, Claude Code 2.1.326, Windows 11)", auto mode and Driver unproved; pasteable block, "Capabilities and their commands" row, the two later mentions (auto-mode fate) use placeholders; the broad-rule paragraph (incl. `uv run --script` and `uv run --locked --project` forms) and the moved-path paragraph (plugin copy assumption marked unproved, dev folder-gone rule) added; "Allow rules to add" says real path, no placeholder, and the `'` quoting warning. Block-vs-RECOMMENDED_ALLOW test passes (above).
- chief-of-staff.md: question lists real paths; Broad rules and Stale rules bullets added as specified; "nothing else is written" left in place.
- The five `$CHANTIER` sentences (skills/chantier, chief-of-staff, griller, status SKILL.md and references/concepts.md): `grep -o` of the sentence from each file, sorted and counted -> one distinct line, count 5: "`<plugin root>` is written absolute, with forward slashes, quoted, the same path as P10's rule holds (...); `$CHANTIER` is carried verbatim into every brief and command, since another form of the path does not match the rule and meets the host's prompt." Word for word the spec's.
- Agent files untouched (diff stat lists none).

## 4. PR body (work/pr-body.md) against the diff
Summary, Deliverables (before/after table, trial claim, mermaid), Choices, Changes (launch.py, allow_samples.py, permissions.py, card, CoS, four skill files + concepts, tests, scenario check), Known gaps (auto mode and subagents unproved; scratch project stands in for the checkout; PowerShell forms not tested by a dedicated case; gate and lease hold) match the 15-file diff stat; nothing delivered is unmentioned. Review/Verified/CI boxes are the Driver's. Internal references names the CR and batch only in the Internal references section. The trial table is in evidence/trial.md; the body states its results (the host card Mark carries them too). No image attached.

VERIFIED

## Description pass

Head: 1559e15b583fc2332015b6142e5e179716b851d1

Judged at 1559e15 on the posted body (`gh pr view 402 --repo gsemet/chantier --json body`; headRefOid is the full SHA above; base is the CR-431 branch at db75bff).
- Diff base..head (`git diff --stat db75bff6 HEAD`): 15 files (scenario/run_scenario.py, 4 skill files, concepts.md, chief-of-staff.md, hosts/claude-code.md, allow_samples.py, permissions.py, preflight.py, launch.py, plugin_files.py, test_allow_rules.py, test_cli_runs.py). Summary, Deliverables, Choices and Changes match it; nothing delivered is unmentioned (the preflight.py and plugin_files.py edits fall under the launch/permissions changes and the preflight line limit).
- Before/after rule table matches the card rows and the code (`uvx --from "<plugin root>"`, dev, sync).
- Internal references: CR-432 and batch-30 appear only in the "Internal references" section; no role name outside it.
- Known gaps: the four unverified/untested items are present (auto mode and subagents, scratch stand-in, PowerShell test case, gate/lease hold); none is "None".
- Test plan SHAs: all `1559e15`, the review one carried from `c132602` with its reason; the branch head is 1559e15. No image attached, no STALE mark.
- Not re-run: suites (per brief).

VERIFIED

## Restack pass at 0641023

Head: 06410234fcdd3afb2b4452cdf0b503b816d69471

Move: clean restack onto CR-427 head 160e292. Own patch: `git diff --name-only 160e292 HEAD` lists the same 15 files as before. The base brought 40+ files (board, web client, hub, docs, `chief-of-staff.md`, `griller.md`, `scenario/run_scenario.py`), none of them the allow-rule code (`launch.py`, `permissions.py`, `allow_samples.py`, `preflight.py`).

- Re-run at 0641023: `just check` -> `1613 passed, 20 skipped in 138.17s`, `release-notes ... ok`, exit 0 (log: work/gates/verifier-check-0641023.log); worktree clean after.
- Re-run at 0641023: `pytest test_allow_rules.py test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks -q` -> `3 passed in 11.75s`.
- Carried from 1559e15: section 1 (rule-matching trial; Claude Code behaviour, independent of the move), section 2 (preflight P10 runs: the P10 code is not in the base's changed files), section 3 (card diffs: `chief-of-staff.md` changed in the base but in other parts; the CR's patch is the same 15 files), PR body vs diff (same 15 files).
- Description pass at 0641023: the posted body (headRefOid = the full SHA above) names `1559e15` in its Test plan for local gates, evidence, Verified and CI (lines 70-75), and its Review box carries from `c132602` without naming the restack. No `carried from 1559e15: clean restack` reason; the boxes are stale at this head.

NOT VERIFIED (description only: the Test plan SHAs are the old head; code and cards judged the same as at 1559e15)

## Description pass 2 at 0641023

Head: 06410234fcdd3afb2b4452cdf0b503b816d69471

Posted body re-read (`gh pr view 402`, headRefOid = the full SHA above). Test plan lines 71-76 name 0641023 or carry from 1559e15/c132602 with the clean-restack reason; no STALE mark; the Review box matches the Driver's note "move 1559e15..0641023 (restack) inspector approved at 0641023" (`chantier log CR-432`). Code, cards and tests judged above (just check re-run at 0641023, the rest carried).

VERIFIED
