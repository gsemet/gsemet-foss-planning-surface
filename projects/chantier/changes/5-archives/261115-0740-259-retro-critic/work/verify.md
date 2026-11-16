# Verify CR-259

Head: eb14e28948e8ec8d1c49a6a85536e6cbd4e98675

Each claim judged at eb14e28 unless noted. Gate pass: the long gate passed at 9fd6d54 is carried (carried from 9fd6d54: clean rebase onto CR-264's head, no conflict; CI green at eb14e28, all 5 checks; Driver's local `just check` at eb14e28: 126 passed).

1. Agent files exist, same body, version 0.9.0, Opus 5.5 (eb14e28).
   Command: `git diff origin/chantier/batch-18/cr-264-...-cli-fixes..HEAD -- agents com.github.copilot`
   Output: `agents/retro-critic.md` (model claude-opus-5-5, `# chantier-agent: 0.9.0`) and `chantier-retro-critic.agent.md` (model [Claude Opus 5.5, claude-opus-5.5], required) added, identical bodies; description ends with the specified prompt line.
   Command: `pytest test_plugin_files.py test_playbook_config.py test_cost_reading.py -q` Output: `43 passed in 7.18s`.
2. `playbook --batch` and `playbook` print the retro critic's line (eb14e28).
   Command: `uv run --no-sync --project . chantier playbook --batch batch-18 | Select-String "retro|prompt"`
   Output: `retro-critic: agent=chantier:retro-critic ...` and `retro-critic prompt, first line: chantier retro-critic for the Chief of Staff, in the project C:/Users/gaeta/Projets/chantier.`; without `--batch` the same line plus spec-critic and spec-writer.
3. Cost: a retro-critic subagent counts on "Foreman's own subagents", not the grill line: `test_a_retro_critic_of_the_foreman_is_counted_on_the_foreman_own_subagents_line` in the 43 passed above. Deviation (Area 7 in pytest rather than the scenario) is named in the PR's Known gaps.
4. `close` deletes `retro-dropped.md`: scenario case added in `scenario/run_scenario.py`; carried from 9fd6d54 (long gate passed there; the rebase touched nothing in it).
5. Cards: `retro-critic.md` (new, 56 lines), `foreman.md` "The retro critic", `chief-of-staff.md` (lines 150, 170, 1171, 1190, 1395), `concepts.md` (421 row, 436, 440, 461), `status-layout.md` Retro bullet, both host references, CONTRIBUTING.md: read in the diff; each Area 2 to 6 item is present. Open questions 1 to 3 were settled by the Driver's choices (a, a, a), named in the PR description.
6. No `hooks/` or `types/` change (diff stat lists none), so no `just mod`; AGENTS.md unchanged.
7. PR description (https://github.com/gsemet/chantier/pull/207): renders, sections and fold are well formed; Summary, Deliverables, Changes match the diff; Known gaps names the two unproved items and the Area 7 deviation; no STALE mark. Test plan SHAs read 9fd6d54 and are the Driver's to update after this pass.

VERIFIED
