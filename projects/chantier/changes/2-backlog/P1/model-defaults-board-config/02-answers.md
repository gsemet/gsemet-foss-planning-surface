---
type: cr-answers
description: The user's answers to the grill of the cross-harness agent configuration and its board editor.
---

# Answers

## Scope note from copilot-role-models (2026-11-16)

The P1 copilot-role-models now replaces chantier's hand-written Copilot model list (the model
list only: after its Q9 the prices stay with copilot-session-usage) with a copy of GitHub's own
tables (`github/docs`, `data/tables/copilot/`), each model's identifier
taken from its name and checked against the Copilot CLI reference. So this CR does not own the
model catalog: it owns each role's choices (model, tools) and where they are configured. If
copilot-role-models ships first, this CR builds on its catalog.

## model-defaults-board-config-Q1: the file's name

2026-11-16, the user chose: accept both `chantier.yaml` and `chantier.yml`. Both present in the
same place is refused, with the two paths named.

## model-defaults-board-config-Q2: where a project's configuration lives

2026-11-16, the user chose the recommended answer: the surface first. With an external planning
surface, `projects/<name>/chantier.yaml` (or `.yml`) in the surface is read first; the file at
the code repository's root is the base and the surface's file overrides it key by key. With no
surface, nothing changes.

## model-defaults-board-config-Q3: generated agent files

2026-11-16, the user chose: no generated file. chantier writes no agent file anywhere (not in
the plugin, not in a managed folder). What a host cannot apply at an agent's start is refused on
that host, with the reason. Today: Claude Code takes a model at the start, not tools; Copilot's
agent files set `model-policy: required`, so their model wins over a model given at the start.

## model-defaults-board-config-Q5 and Q6: a model per role on each host

2026-11-16, the user's words (French, translated), on Copilot's `model-policy: required`: "I
don't understand. You have a tool that starts a subagent or a nested session. You can choose the
model for that subagent, can't you? At worst, the tools are the same as the caller's, no?" And:
"Of course I want to find the way to change the model per role. It is for you to give me the
solution for Claude Code and, according to the documentation, how to do it in Copilot."

So a model per role, configurable, on both hosts, is in scope; no generated agent file (Q3).
The Chief of Staff's solution:

- **Claude Code (proved, used in every batch):** the Agent tool's `model` parameter takes
  precedence over the agent file's `model` frontmatter. chantier already passes the playbook's
  model at each start (`SETS_MODEL_AT_START["claude"]`). The plugin's named agent keeps its own
  tools; only the model changes.
- **Copilot (documented, unproved):** the Copilot CLI reference says an explicit model takes
  precedence over a custom agent's `model` "unless the agent sets `model-policy: required`", and
  in the Copilot SDK a custom agent's model overrides the parent session's. Every chantier
  Copilot agent sets `model-policy: required`, which is why CR-296's requested Sol was replaced
  by the Coder file's Luna. The way: remove `model-policy: required` from the agent files (their
  `model:` stays the default) and pass the role's model at each start (the `task` tool's model
  parameter), as on Claude Code; then read the model used in `subagent.started` /
  `subagent.completed` (`model`), and stop with the reason if it differs. To be proved by the
  user's Copilot run.
- **A generic agent instead of the named one** (CR-296 round 6 proved on Copilot that a generic
  agent started with `model: gpt-6.1-sol` ran on Sol): it has the caller's tools, not the role's
  restricted ones; kept only as the user's explicit choice, not as a fallback (AGENTS.md: no
  fallback).
- **Tools:** neither host changes a named agent's tools at its start; the named agent keeps the
  tools its file gives (the role's restriction).

## model-defaults-board-config-Q8: the role's agent, its own model

2026-11-16, the user's words (French, translated): "With no special configuration, we take the
agent the skill ships. The user can give their own agent for any role (they must be able to give
its name in the YAML), and if they want a different model, the agent files are not used, and the
call to task (or its equivalent) rebuilds the prompt and the model."

So, per role, in the configuration:

- nothing set: the plugin's agent for the role, with its file's model;
- an agent name: the user's own agent runs the role (its file, its tools, its model);
- a model different from the agent file's: no agent file is used; the start (`task` on
  Copilot, the Agent tool on Claude Code, or their equivalent) is a generic agent whose prompt
  carries the role's whole contract, rebuilt by chantier, with the model given. This is the
  user's configuration, said in the board and the playbook, never a fallback.

## model-defaults-board-config-Q9: a model change alone, per host

2026-11-16, the question: on Claude Code the Agent tool already takes another model for a named
agent, which keeps its restricted tools; when the user changes only a role's model, what starts?
The user's words (French, translated): "Named agent and model, and make sure to prepare the
ground for when Copilot allows it. And if I add another coding agent later, it may be in one
case or the other."

So Q8's "generic agent" is narrowed to the hosts that cannot set a named agent's model at its
start:

- each host says whether it can start a named agent with a model given at the start (today
  Claude Code: yes, proved; Copilot: no, until the user's Copilot run proves it);
- a host that can: the role's agent (the plugin's or the user's) starts with the configured
  model, keeping its file's tools;
- a host that cannot: no agent file is used; a generic agent starts with the role's whole
  contract in its prompt and the configured model (Q8);
- Copilot switches to the first case by changing its one capability, once proved, with nothing
  else to rewrite; a host added later declares its own capability and falls in one case or the
  other.

## model-defaults-board-config-Q10: a role's tools

2026-11-16, the user chose the recommended answer: a role's tools change only by naming the
user's own agent for the role (its file gives its tools). No host restricts a named agent's
tools at its start, and a generic agent has its caller's tools: in that case the board and the
playbook say "the caller's tools, not restricted", hiding nothing. No `tools` field in the YAML.

## model-defaults-board-config-Q11: a shipped defaults file

2026-11-16, the user chose: a shipped defaults file. `config/chantier.defaults.yml` in the
plugin is the lowest layer, read like the user's file (then the code repository's
`chantier.yaml`, then the surface's). The models the shipped agent files declare must stay
equal to it; a test checks it. The model catalog itself (identifiers, names, availability)
stays copilot-role-models' copy of GitHub's tables.

## The specification's open questions (first run), 2026-11-16

Catalog: copilot-role-models' Q10 moved the Copilot model catalog to its own P1 CR,
copilot-model-catalog; this CR builds on that one.

- Q13, the user chose the recommended answer: on Copilot, a user's own agent named for a role
  together with another model is refused with the reason (at the batch's open; the board says it
  as it is entered). Nothing hidden, no generic agent in its place.
- Q14, the user chose the recommended answer: the board's Configuration page edits only each
  role's agent and model; the rest of `chantier.yaml` (prices, board, CI, long gate, needs) is
  shown read-only.
- Q15, the user chose the recommended answer: the existing `roles.<role>.tools` stays what it is,
  a list of what the role needs, checked at preflight, restricting nothing; the docs say so.
- AGENTS.md wording (the configuration sentence, the board writing the surface's
  `chantier.yaml`): the Chief of Staff's decision, the user reads and approves it in the PR's
  diff at the merge.
- The grill cost line: the Chief of Staff's decision, accepted: a spec-writer or spec critic
  started as a generic agent, or replaced by the user's own agent, leaves the grill line;
  `cost --explain` says so.
- Q12 (`model-policy: required` on the Copilot agent files): the user asked what it is. The
  Chief of Staff explained: per the Copilot CLI reference, a model given at the start (`--model`,
  `task`'s `model`) takes precedence over the agent file's `model:` unless the file sets
  `model-policy: required`, which enforces the file's model whatever the caller asks; chantier
  set it on every Copilot agent (a test checks it) so a role never runs on a substituted model;
  it is why CR-296's Coder asked for Sol ran on Luna. The user then chose the recommended answer:
  remove it in this CR, to be proved. Copilot's capability stays "no" (the generic agent) until
  the user's Copilot run; this CR's eval preparation adds the probe: a named agent started with a
  requested model, the model it ran on read from `subagent.*`; if it matches, a one-line change
  switches Copilot's capability on (a later CR). The test asserting `model-policy: required`
  changes accordingly.

## The spec critic's questions, 2026-11-16

- Q16, a model only one host knows in a section for all hosts. The user (French, translated):
  "There is no model for all hosts. There is a configuration for all the projects of an agentic
  surface, but there is always a configuration per host." So no layer has role settings shared
  by all hosts: every layer sets roles per host only.
- Q19, the layers' order (the user's words, translated): "the shipped chantier.yaml, then the
  surface at its root, then in the surface's subfolder, then the target project. Merge per node,
  to put only the node that changes." So, weakest to strongest: the shipped
  `config/chantier.defaults.yml`; the surface root's `chantier.yaml` (all its projects);
  `projects/<name>/chantier.yaml` in the surface; the target project's (code repository's)
  `chantier.yaml`. Each layer is merged node by node: a layer carries only the nodes it changes.
  This supersedes Q2's order (there the surface's project file overrode the code repository's).
- Q17, the user chose: remove `model-policy: required` from `chantier-coder` only (the probe's
  agent), not from the other thirteen files, until the proof covers them (supersedes Q12's
  "every file").
- Q18, the user chose the recommended answer: three CRs in a stack. (A) this CR,
  model-defaults-board-config: the configuration in layers and the shipped defaults. (B)
  `role-model-per-host`: a model per role on each host (the host capability, the generic agent
  with its contract, the Coder's `model-policy` removal, the probe, `cost --explain`). (C)
  `board-config-page`: the board's Configuration page. B builds on A, C on A and B.
- The critic's text fixes (the "writes only plain JSON and Markdown" clause and the other places
  the old configuration sentence stands, the Copilot start rows, the probe step as the
  operator's explicit eval order, the surface file's read/check/write as CLI code the board only
  routes to) are the spec-writer's.

## Grilled enough

2026-11-16, the user: grilled enough; the spec-writer writes the specification.

- Spec critic: yes.
- Depends on copilot-role-models for the Copilot model catalog.

## model-defaults-board-config-Q4: a change while a batch runs

2026-11-16, the user chose the recommended answer: it applies at the next batch. A batch keeps
the team frozen at its `open`, as today; the board says "applies at the next batch".

## model-defaults-board-config-Q7: where the board's Configuration page writes

2026-11-16, the user chose the recommended answer: the surface only. With a surface, the page
edits `projects/<name>/chantier.yaml`, committed by the autosync, and shows the value inherited
from the code repository's file and the effective value. With no surface it is read-only and says
to edit `chantier.yaml` by hand.
