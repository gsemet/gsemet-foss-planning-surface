# Verify CR-299

Head: 6f132fe6058d510fd210cedad40be0ce1c6de290

All claims judged at 6f132fe (git rev-parse HEAD in the worktree, tree clean). CLI run from the worktree:
`uv run --no-sync --project <worktree> chantier --project <scratch>/surface/projects/demo playbook --host <h>`.
Scratch: `<scratchpad>/v299/surface` (git init'd surface, project `demo`, code repository `projects/demo/.repo`, git init'd). Gates (scenario, pipeline) not rerun, as asked.

## 1. No user file, both hosts (6f132fe)

`playbook --host claude` and `--host copilot`: "playbook: no chantier.yaml, the plugin's agents and models", then all 14 roles `agent=chantier:<role> model=(its file's)` (claude) and `agent=chantier-<role> model=(its file's)` (copilot). Escalate line: claude `opus (claude-opus-5-5 ...)`, copilot `(none on this host)`. PASS.

## 1b. Three user files (6f132fe)

Coder models set under hosts.claude.roles (surface root claude-haiku-5-5, project claude-haiku-5-5, repository claude-opus-5-5; the Coder's shipped default is claude-sonnet-5-5):

- three files, claude: `playbook: chantier.yaml, projects/demo/chantier.yaml, projects/demo/.repo/chantier.yaml, valid, host claude` / `coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude Opus 5.5) [repository]`. PASS.
- repository `model: default`, claude: `coder: agent=chantier:coder model=(its file's) [reset in repository]`. PASS.
- repository file removed, claude: `coder: agent=chantier:coder model=haiku (claude-haiku-5-5, Claude Haiku 5.5) [surface project]`. PASS.
- Copilot, same three files with models: refused, `projects/demo/.repo/chantier.yaml:9: Copilot cannot set a model when it starts an agent (hosts/copilot.md, "Models")` (also with `agent: my-coder` set: line 10). This is Copilot's existing rule for a model, which the PR body names as kept; so a Copilot layered model cannot be printed. Copilot with the repository reset: `coder: agent=chantier-coder model=(its file's) [reset in repository]` (with `agent: my-coder` in the layers: `coder: agent=my-coder [repository] model=(its file's) [reset in repository]`). PASS for what Copilot allows; the strongest-model-with-label case is shown on claude only.

## 2. Refusals and acceptance (6f132fe)

- top-level `roles`: exit=2 `projects/demo/.repo/chantier.yaml:1: "roles" goes under a host: hosts: claude: roles: or hosts: copilot: roles: (every role setting is per host)`. PASS.
- both files: exit=2 `projects/demo/.repo/chantier.yaml and projects/demo/.repo/chantier.yml are both present: keep one`. PASS.
- `chantier.yml` alone: exit=0 `playbook: projects/demo/.repo/chantier.yml, valid, host claude` / `coder: ... model=opus (claude-opus-5-5, ...) [repository]`. PASS.
- model equal to the default (gpt-6.1-sol) on `--host copilot`: exit=0 `coder: agent=chantier-coder model=(its file's)`. PASS.
- bad model under hosts.copilot, `--host claude`: exit=2 `projects/demo/.repo/chantier.yml:5: role "coder": model "not-a-model" is unknown on Copilot; known: ...`. PASS.

## 3. Agent files, hooks, types

`git diff origin/main --stat -- agents com.github.copilot/agents hooks types` -> no output (0 lines). PASS.

## 4. Defaults equal the agent files

`uv run --no-sync --project . pytest "skills/chantier/scripts/cli/tests/test_playbook_layers.py::test_the_shipped_defaults_give_each_role_the_model_its_agent_file_declares" -q` -> `2 passed in 0.39s` (two parametrized cases). PASS.

## 5. pr-body.md against the diff (description pass, 6f132fe)

Summary, Deliverables (layers, labels, `[reset in surface project]` form, refusal of top-level roles), Changes (layers.py new, config.py, yaml_subset.py, lines.py, models.py, plugin_files.py, rules/preflight/opening/gate/board address+command, defaults file, cards/docs/scenario/AGENTS.md) match the 35-file diff stat. Minor unmentioned: `.gitattributes` line for the defaults file (eol=lf). Known gaps present (no release notes, scenario checks first run, just test 63 s, AGENTS.md rule change). The scenario-not-run gap is stale: the local scenario and pipeline passed at this head, per the Driver; the Driver may update it. Test plan boxes are unchecked (Driver's to tick).

## Verdict

VERIFIED

## Description pass (PR 253 body, 6f132fe)

Head: 6f132fe6058d510fd210cedad40be0ce1c6de290

Body read against `git diff origin/main...HEAD` (35 files) and the proofs above. Summary, Deliverables (layers table, labels, reset line, refusal of top-level roles), Changes, Impacts, Autonomous decisions (prices/ci labels in lines.py, shipped-defaults test in test_playbook_layers.py, startup card reflow, AGENTS.md sentence) and Known gaps match the diff. Test plan boxes are ticked and match the proofs (tests named exist; defaults test passes). `.gitattributes` is listed. Scenario sections 11 and 20, CI and review boxes rest on the Driver's record, not rerun here.
Failed: one internal reference outside Internal references: Autonomous decisions says "as the specification's section 4 reads". Reword or drop.

Verdict: NOT VERIFIED (that one line only)

## Description pass 2 (PR 253 body, 6f132fe)

Head: 6f132fe6058d510fd210cedad40be0ce1c6de290

Posted body re-read against the 35-file diff and the proofs above. The first Autonomous decisions bullet no longer cites the specification; no internal reference outside Internal references (the Chief of Staff card bullet names a card this PR changes: product term). Changes list matches the diff. Known gaps present and consistent. Review box: log shows 'r2 approved at d37ae50, committed as the head', carried over a clean rebase as 6f132fe. Verified/CI boxes rest on the Driver's record.

Verdict: VERIFIED
