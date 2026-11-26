# CR-510 matrix probe, round 2

Head: 7d2c4dc708572f0a48b6186e972cb77056e8441c

Result: NOT VERIFIED (cells 1, 3, 4 proved; cell 2 not proved).

`git rev-parse HEAD` in the worktree gave the SHA above, `git status --porcelain` was empty. Every command below ran at that SHA.
`<wt>` is the CR's worktree, `<tests>` is `<wt>/skills/chantier/scripts/cli/tests`, `<p>` is a scratch project.
Not run: the scenario, any real session or transcript, any Copilot session, any quiz, eval or paid model run.

Scratch runs (cells 2, 4, and the 18-role list of 3): a probe script under `<CR folder>/work/scratch/vm/` (removed at the end), run with `uv run --locked --group dev --project <wt> python probe.py <cases>`. Each case: `git init` of a new scratch repository with a local bare `origin`, `chantier.yaml` as stated (none for shipped), `CHANTIER_HOST` set to the host, a scratch home and config folder, then the worktree's `chantier` run with that repository as working folder, no `--project`, no `CHANTIER_ROOT`: `file`, `open ... --default-branch main --slots 4` with `--release 2` (parallel) or `--mode stack`, `foreman set`, `take`, `brief <role> ...`, and for the parallel batch `order drop` and `cancel` of the first CR (so the release CR starts) and `order qa`. In each output line, `contract=` counts the brief file's lines holding `contract (a generic agent`.

## Claim 1: Claude Code, shipped defaults: `brief` builds for the 18 roles; the hook's reload message names the floor

SHA 7d2c4dc708572f0a48b6186e972cb77056e8441c. PROVED.

Command: `uv run --locked --group dev --project <wt> pytest -v -p no:cacheprovider --rootdir <wt> -c <wt>/pyproject.toml <tests>/test_brief.py <tests>/test_brief_bytes.py`

Output: `45 passed in 13.92s`, among them `test_every_role_gets_a_stable_brief_in_the_git_folder_and_a_short_prompt[parallel-claude]` and `[stack-claude]` PASSED (parallel: all roles but stack-driver; stack: stack-driver and foreman; fixture with no `chantier.yaml`), the role-only briefs of the 18 roles, and the 18 `test_brief_bytes.py` cases (Claude Code).

Command: `uv run --no-project python <wt>/scripts/mod.py` (what `just mod` runs; Claude Code 2.1.330)

Output: `Validation passed with warnings` (marketplace description, TypeScript warnings in `register.tsx` about `views` and `common`, icon), then `119 pass 0 fail`, among them `(pass) the reload message names the floor and no removed file`, `(pass) a compaction of a session that loaded a role skill ends with the reload line, manual or auto` and the three `a compaction after loading ... names the last role` cases.

The first of those tests checks only the test file's constants; the compaction tests assert the hook's output equals them. The message in `hooks/register.tsx` reads `... run your brief again (...) and read the file it names whole; the floor, in that brief, holds.`

## Claim 2: Claude Code, a configured generic agent for a worker: its brief carries the contract lines

SHA 7d2c4dc708572f0a48b6186e972cb77056e8441c. NOT PROVED.

The flow the matrix names does not exist. Command: `git -C <wt> grep -n -i -E "generic|contract" HEAD -- skills/chantier/scripts/cli/tests/test_brief.py`. Output: none, exit 1. `test_brief.py` has no configured-generic-agent or contract-lines case. The only generic-contract tests run (`test_a_copilot_batch_records_a_generic_start_whose_brief_holds_the_contract`, `test_a_generic_escalation_gives_the_contract_with_or_without_a_user_file[shipped|user]`; `3 passed in 1.50s`) are Copilot ones.

Real runs, host claude, `roles.coder` in `chantier.yaml`, cases a, b, c:

```
case a  coder: {agent: general-purpose}
[a] coder: exit 0 in_git=True floor=1 rows_host=claude proved=1 untested=0 writes_line=1 contract=0
[a]   playbook| coder: agent=general-purpose [repository] model=(its file's) escalation=opus (claude-opus-5-5, Claude Opus 5.5)
case b  coder: {agent: general-purpose, model: opus}
[b] coder: exit 0 in_git=True floor=1 rows_host=claude proved=1 untested=0 writes_line=1 contract=0
[b]   playbook| coder: agent=general-purpose [repository] model=opus (claude-opus-5-5, Claude Opus 5.5) [repository] escalation=opus (claude-opus-5-5, Claude Opus 5.5)
case c  coder: {model: opus}
[c] coder: exit 0 in_git=True floor=1 rows_host=claude proved=1 untested=0 writes_line=1 contract=0
[c]   playbook| coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude Opus 5.5) [repository] escalation=opus (claude-opus-5-5, Claude Opus 5.5)
```

All 17 briefs of each parallel batch printed `contract=0`.

Case a's brief file holds the Coder card (`# Coder`), `=== floor`, `=== facts` and `=== host rows: claude`, and no contract heading.

Why (read, not a run): `plugin_files.contract_lines` returns nothing unless the role's `start` or escalation `mode` is `generic`; `playbook/layers.py` and `playbook/escalation.py` give `generic` only where `NAMED_AGENT_MODEL_AT_START[host]` is false, and `playbook/models.py:57` has `{"claude": True, "copilot": False}`. So on Claude Code no configuration of this head produces them. `git diff main...HEAD` shows no change to `layers.py` or `escalation.py`, a comment only in `models.py`, and no change to the body of `contract_lines`: the branch did not introduce this.

Also seen on Copilot (case h, `coder: {agent: general-purpose}`): the coder brief printed `contract=0` too. Contract lines appeared only where chantier itself starts the role generic (cases d, f: coder, conflict-resolver, debugger).

## Claim 3: Copilot, shipped defaults: `brief` builds for the 18 roles; rows stay untested; no hook, so reload message and writes guard are inert

SHA 7d2c4dc708572f0a48b6186e972cb77056e8441c. PROVED, with the inertness inferred from files and unproved in a real Copilot session.

The run of claim 1's pytest command includes `[parallel-copilot]` and `[stack-copilot]` PASSED.

Real runs, no `chantier.yaml`: case d (parallel, 17 roles) and e (stack, stack-driver and foreman), 18 distinct roles, every `brief` `exit 0 in_git=True floor=1 rows_host=copilot proved=0`:

```
[d] roles briefed: 17: cr-driver coder conflict-resolver debugger inspector investigator verifier release-driver qa-driver spec-writer spec-critic board-griller retro-critic demo-explorer griller chief-of-staff foreman
[e] roles briefed: 2: stack-driver foreman
[d] foreman: exit 0 in_git=True floor=1 rows_host=copilot proved=0 untested=50 writes_line=0 contract=0
[d] coder: exit 0 in_git=True floor=1 rows_host=copilot proved=0 untested=1 writes_line=1 contract=1
```

Host rows: a count of the `mark`/`status` values of `<wt>/skills/chantier/references/hosts/*.json` printed `copilot.json {'untested': 50}` (`claude-code.json {'untested': 37, 'proved': 13}`).

Hook: `hooks/hooks.json` is `{"modules": ["./register.tsx"]}` (a Claude Code mod, no hook event), and the keys of `.github/plugin/plugin.json` are `$schema, agents, author, description, homepage, keywords, license, name, repository, skills, version` (no `hooks`). That Copilot therefore runs neither the reload message nor the writes guard was not tried in a real Copilot session.

## Claim 4: Copilot, configured: the same facts, unproved

SHA 7d2c4dc708572f0a48b6186e972cb77056e8441c. PROVED, same limit as claim 3.

Real runs with `roles.coder.model: gpt-6.1-terra` under `hosts.copilot`: case f (parallel, 17 roles) and g (stack, 2), 18 distinct roles, every `brief` `exit 0 ... rows_host=copilot proved=0`:

```
[f] roles briefed: 17: cr-driver coder conflict-resolver debugger inspector investigator verifier release-driver qa-driver spec-writer spec-critic board-griller retro-critic demo-explorer griller chief-of-staff foreman
[g] roles briefed: 2: stack-driver foreman
[f] coder: exit 0 in_git=True floor=1 rows_host=copilot proved=0 untested=1 writes_line=1 contract=1
[f]   playbook| coder: agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra) [repository] tools=(the caller's, not restricted) escalation=claude-opus-5.5 (claude-opus-5.5, Claude Opus 5.5) (generic)
```

Case h (`coder: {agent: general-purpose}`, parallel, 17 roles) also built every brief with `proved=0`. Rows and hook manifests: as claim 3.
