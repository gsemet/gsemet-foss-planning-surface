# Verify CR-297

Head: 943fcb4868aafcb4d22c37cc96cb3dff0f25c2f6

All claims judged at 943fcb4 (`git rev-parse HEAD` in the worktree; tree clean). PR description not judged here (later pass).

1. Agent files: `git diff origin/main -- com.github.copilot/agents agents costs` shows exactly four `model:` lines: coder -> `[GPT-6.1 Sol, gpt-6.1-sol]`, conflict-resolver, debugger, verifier -> `[GPT-6.1 Terra, gpt-6.1-terra]`; `agents/` and `costs/` empty in the diff. `git diff origin/main --name-only` lists 11 files, none in agents/ or costs/. OK.
2. models.py: `git diff origin/main -- ...playbook/models.py` is one added row `Model("gpt-6.1-terra", "GPT-6.1 Terra", "")`. OK.
3. `chantier --project <scratch> playbook --host copilot`, no chantier.yaml: prints "playbook: no chantier.yaml, the plugin's agents and models", 14 agents each `model=(its file's)`, exit 0. OK.
4. Same with `roles: {coder: {model: gpt-6.1-terra}}` in a scratch project's chantier.yaml: exit 2, "chantier.yaml:3: Copilot cannot set a model when it starts an agent (hosts/copilot.md, "Models"): remove "model" for coder, ...". OK.
5. `COPILOT_HOME=<temp> uv run --no-project python evals/kit/copilot_models.py --session s1` on a fake session: all roles from the agent files -> every row `ok`, exit 0; coder recorded `gpt-5.6-luna` -> `coder: expected gpt-6.1-sol; recorded gpt-5.6-luna; MISMATCH (matched by order)`, exit 1; event lines end "no agent field in the event". `not recorded` and `unmatched (event count)` cases are covered by the new parametrized test, passing in item 6. OK.
6. `just check` at head: ruff, mypy, lock, biome clean; `262 passed in 47.20s`; release-notes ok; exit 0. OK.
7. Docs (agents-and-models, hosts, hosts/copilot.md, RUNBOOK "Models") read in `git diff origin/main`: match the specification's section 3 and 4 content. OK.
8. CI green at this head: stated by the Driver, not re-run here; `just scenario` not run locally by me (not the top-of-stack gate step asked).

Scratch folders in %TEMP% (v297a, v297b, v297c, v297h) only; planning folder untouched.

VERIFIED