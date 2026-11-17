---
type: cr-answers
description: The user's answers to the grill of the Copilot role model defaults.
---

# Answers

## copilot-role-models-Q1: now, or with the configuration system

2026-11-16, the user chose the recommended answer: ship now, as a small independent CR. The
models change in the current Copilot agent files (`com.github.copilot/agents/`) and in the
documentation. The future configuration system
([model-defaults-board-config](../261116-2138-299-model-defaults-board-config/01-intent.md)) takes these values
as its Copilot defaults.

## copilot-role-models-Q2: a model the host enforces

2026-11-16, the user's words (French, translated): "You are in Claude Code, so you cannot test.
Just prepare the evaluation as well as you can, and I will run a CR on Copilot to validate the
behaviour. Look up the Copilot CLI documentation on the internet to understand what is possible.
Careful: chantier will not work in what is called VS Code's local harness (Copilot in VS Code did
not use the Copilot CLI or the Copilot SDK, and that is now arriving in the 'Copilot harness in VS
Code'). The Copilot App is the equivalent of Claude Desktop and already uses the Copilot SDK, so
chantier should work there."

So:

- This CR changes the files and prepares the proof; it does not run it. The Chief of Staff
  (Claude Code) cannot run a Copilot session.
- It prepares an evaluation the user runs in a later CR on Copilot: for each role, check in a
  real Copilot session that the role runs on its model, from the host's own record of the model
  used, and say what to do when the host enforces another one.
- The documentation of what Copilot allows (a custom agent's model, an override at the start, an
  enforced model) is read from Copilot CLI's and the Copilot SDK's own documentation, with links.
- Hosts: the Copilot App (on the Copilot SDK, like Claude Desktop) and the Copilot CLI are
  supported. VS Code's local harness is not (it did not use the Copilot CLI or SDK); the "Copilot
  harness in VS Code", which is arriving, uses them.

## What the Copilot documentation says (read by the Chief of Staff, 2026-11-16)

- A custom agent's `model` is an optional frontmatter string; unset, the agent inherits the
  default model ([custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)).
- In the Copilot SDK, a custom agent's `model` overrides the parent session's model while it
  runs; `subagent.started`, `subagent.completed` and `subagent.failed` carry an optional `model`
  field, the record of the model used. The documentation describes no enforcement and no
  precedence between the agent's model and a model the parent passes
  ([SDK custom agents](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents)).
- Known host issues: the Copilot CLI once refused a `model` given as an array ("Expected string,
  received array", [copilot-cli#2133](https://github.com/github/copilot-cli/issues/2133)); the
  SDK dropped an SDK-provided agent's model at `session.create`
  ([copilot-sdk#1609](https://github.com/github/copilot-sdk/issues/1609)); sub-agents could run
  another model than the session's, with no sign of it, fixed in CLI v1.0.62 with an "Inherit
  session model" option and the timeline showing `AgentType(model)`
  ([copilot-cli#3824](https://github.com/github/copilot-cli/issues/3824)).
- Likely cause of CR-296's "Required model enforcement replaced requested model `gpt-6.1-sol`
  with `gpt-5.6-luna`": `com.github.copilot/agents/chantier-coder.agent.md` itself declares
  `model: [GPT-5.6 Luna, gpt-5.6-luna]`; the agent file's model won over the override. Changing
  the file to Sol is this CR's change. To be confirmed by the user's Copilot run.
- Today's files (`model:` is an array of display name and identifier): CR Driver Sonnet 5.5,
  Investigator Luna, Inspector Sol already match. To change: Coder Luna → Sol, Verifier Sol →
  Terra, Debugger Luna → Terra, Conflict resolver Luna → Terra. GPT-6.1 Terra is in no chantier
  file yet: its exact identifier must be confirmed.

## copilot-role-models-Q3 and Q4: model names and identifiers

2026-11-16, the user's words (French, translated), in order: "There is a way to load the
available models by loading a YAML, models-and-pricing.yaml." Then: "Look at the other YAMLs,
https://github.com/github/docs/blob/main/data/tables/copilot/model-release-status.yml." Then:
"Make sure you understand the ids and the names well. The Copilot SDK's tool calls ask for the
name gpt-6.1-terra. Find the way to get the right name."

So the value a Copilot SDK call takes is the identifier (`gpt-6.1-terra`), not the display name
(`GPT-6.1 Terra`); the CR must get it from a source, not by guessing.

What the Chief of Staff found:

- GitHub's own tables in `github/docs`, `data/tables/copilot/`, key every model by its display
  name only, with no identifier: `models-and-pricing.yml` (`model`, `provider`,
  `release_status`, `category`, `threshold`, `tier`, prices per million tokens `input`,
  `cached_input`, `output`, `cache_write`), `model-release-status.yml` (`name`, `provider`,
  `release_status`), `model-supported-clients.yml` (`name` and one availability flag per client,
  `cli` among them), `model-supported-plans.yml`, `model-deprecation-history.yml`,
  `model-comparison.yml`, `auto-model-selection.yml`. GPT-6.1 Terra is there: GA, "Versatile",
  $1.00 in, $0.05 cached, $5.00 out, $1.25 cache write (up to 272K).
- The identifiers come from the runtime, for the signed-in account: the Copilot SDK's
  `client.listModels()` (`client.rpc.models.list()`), whose entries carry an `id`
  ([@github/copilot-sdk](https://www.npmjs.com/package/@github/copilot-sdk)); in the Copilot CLI,
  `copilot /model --list --json` once signed in, reported in
  [copilot-cli#700](https://github.com/github/copilot-cli/issues/700) (still open: no documented
  list command; `copilot --silent -p "/model --list --json"` works only sometimes).
- An unknown identifier can fall back silently to another model with no error
  ([copilot-sdk#2856](https://github.com/github/copilot-sdk/issues/2856)): the identifier must be
  checked against the list, and the model used read from the `subagent.*` events.
- chantier today keeps a hand-written catalog (`playbook/models.py`, `MODELS`: identifier,
  display name; Copilot has Opus 5.5, Sonnet 5.5, Luna and Sol) and its own prices.

## copilot-role-models-Q5: where the identifier comes from

2026-11-16, the user: "Find it in the Copilot CLI's code!" The local Copilot CLI (1.0.107,
`%LOCALAPPDATA%\GitHubCopilotCLI\copilot.exe`) is a packed binary with no readable model
strings, and its npm package `@github/copilot` is only a loader. GitHub's own sources give the
answer:

- The Copilot CLI command reference
  ([`content/copilot/reference/copilot-cli-reference/cli-command-reference.md`](https://github.com/github/docs/blob/main/content/copilot/reference/copilot-cli-reference/cli-command-reference.md)),
  section "Supported models", lists the identifiers `--model` and `COPILOT_MODEL` take:
  `claude-sonnet-5.5` (the default), `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-astra`, `gpt-6-luna`,
  `claude-opus-5.5`, `claude-haiku-5.5`, `claude-haiku-4.5`, `gpt-5.3-codex`,
  `gemini-3.8-flash`. Terra's identifier is `gpt-6.1-terra`.
- The same reference: "An explicit `--model` takes precedence over a custom agent's `model`
  unless the agent sets `model-policy: required`." Every chantier Copilot agent file sets
  `model-policy: required` (a test checks it), so the agent file's model always wins: this is
  the "Required model enforcement" CR-296 met, the Coder's file saying Luna. The fix is the
  file's model, not an override.
- GitHub's `gh-aw-firewall` keeps a Copilot model catalog with `rawId` (`gpt-5.6-terra`) and
  `lookupId` (`gpt-5-6-terra`) per model
  (`shared/model-information/sources/copilot-main.json`): another sign that the identifier is the
  lower-case name, spaces as `-`, dots kept.
- The name-to-identifier rule holds for every model both lists name: lower case, each space
  becomes `-`, the dots stay (`GPT-6.1 Terra` → `gpt-6.1-terra`, `Claude Sonnet 5.5` →
  `claude-sonnet-5.5`). The Copilot run confirms it with `listModels()`.

## copilot-role-models-Q6: GitHub's tables in this CR

2026-11-16, the user chose: in this CR. chantier's Copilot model list and prices come from
GitHub's own tables (`data/tables/copilot/`: `models-and-pricing.yml` for the prices,
`model-release-status.yml` for the status, `model-supported-clients.yml` for the availability in
the CLI) instead of being written by hand, with each model's identifier from the rule above,
checked against the CLI reference's "Supported models".

The project's rule holds: the CLI needs no network once uv's cache holds its packages (AGENTS.md).
So the tables are a copy kept in the repository, refreshed by a command, not read from GitHub at
run time; how is the specification's.

## Grilled enough

2026-11-16, the user: grilled enough; the spec-writer writes the specification.

- Spec critic: yes (the user's choice: the CR now touches the CLI and the cost computation).

## The specification's open questions (first run), 2026-11-16

### copilot-role-models-Q7: GPT-6.1 Sol missing from `model-supported-clients.yml`

The user (French, translated): "What are you talking about? Find it, it exists! Search the
documentation, the internet, find the solution for Copilot."

What the Chief of Staff found in `github/docs`: `model-supported-clients.yml` indeed has no
`GPT-6.1 Sol` entry (it has GPT-6.1 Terra, and GPT-5.6 and GPT-6 Sol): a gap in that one table.
GPT-6.1 Sol is in `data/tables/copilot/auto-model-selection.yml` with `cli: true` and
`app: true` (also `chat`, `cloud_agent`), in `model-release-status.yml` (GA),
`models-and-pricing.yml`, `model-supported-plans.yml` (not on the Pro plan: `pro: false`,
`pro_plus`, `max`, `business` true), `model-comparison.yml`, `data/variables/copilot.yml`
(`gpt_61_sol: 'GPT-6.1 Sol'`), and in the CLI reference's "Supported models" (`gpt-6.1-sol`).

So a model is in the Copilot catalog when any of GitHub's sources says the CLI or the App has it:
`model-supported-clients.yml` `cli: true`, `auto-model-selection.yml` `cli` or `app` true, or the
CLI reference's "Supported models". Sol stays. A model's plans (`model-supported-plans.yml`) are
shown, refusing nothing.

### copilot-role-models-Q8: GPT-5.6 Luna

The user: "gpt-5.6-luna". The Investigator stays on `gpt-5.6-luna`. The comparison with the CLI
reference's list (which names `gpt-6-luna` and no GPT-5.6 model) reports the difference and
refuses nothing.

### copilot-role-models-Q10 and Q11: the spec critic's questions (second run)

2026-11-16. The spec critic noted that after Q9 the copied catalog has no visible reader on
Copilot today (every model resolves, then is refused: Copilot cannot set a model at an agent's
start).

- Q10, the user chose: a separate CR. This CR ships the role models (the four `model:` lines,
  GPT-6.1 Terra added by hand to `MODELS["copilot"]`), the docs and the eval preparation. The
  copy of GitHub's tables, `just copilot-models`, `copilot-models.json` and `MODELS["copilot"]`
  built from it become their own CR (`copilot-model-catalog`), with Q5 to Q8's decisions; this
  supersedes Q6 here. model-defaults-board-config builds on that CR.
- Q11, the user chose: the model check goes in the current `evals/copilot/RUNBOOK.md`, as
  specified; the inbox CR evals-rework moves it when it replaces that runbook.

### copilot-role-models-Q9: the Copilot prices

The user (translated): "But why do you want to replace copilot-session-usage? If it has bugs,
open a ticket." So the cost computation does not change: on Copilot, `chantier cost` keeps its
prices from copilot-session-usage. The copy of GitHub's tables carries no role in pricing: the
prices table is not copied (or, if copied whole, is not read). A bug found in
copilot-session-usage is reported as an issue on that project, never worked around in chantier.
