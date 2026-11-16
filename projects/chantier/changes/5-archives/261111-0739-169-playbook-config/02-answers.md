# Answers (grill of 2026-11-07): left aside for now

- **Models per role:** the `chantier` section of `AGENTS.md` names a model for a role (e.g.
  "Coder: opus"); the parent passes it when it starts the agent; nothing set means the agent
  file's model. A host that cannot take a model at start refuses clearly, no workaround.
- **Where the fine configuration lives** (agents per role, models, required skills and tools):
  the user does not know yet; left aside, the CR stays in the inbox.
- 2026-11-07, the user: not in batch-08; later.
- **What chantier does with a required skill or tool** (e.g. a Jira skill): the user does not
  know yet.

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **Where the fine configuration lives.**
   - The recommendation was the `chantier` section of `AGENTS.md`.
   - The user chose "Un fichier playbook à part": a dedicated file in the project.
   - **This changes a rule:** this repository's `AGENTS.md` says the user's `AGENTS.md` is the only configuration. The CR amends that rule. The Chief of Staff said so to the user.
2. **The playbook's place and form.**
   - The recommendation was `.agents/chantier.md`, in Markdown.
   - The user chose "chantier.yaml à la racine".
   - It is YAML, structured, and validated by the CLI.
   - It is optional: with no `chantier.yaml`, chantier works as today.
3. **A required skill or tool that is missing** (for example a Jira skill).
   - The recommendation was to refuse at preflight.
   - The user chose "Prévenir et continuer".
   - The Chief of Staff warns the user, naming what is missing, and the role works without it.
   - The spec must keep this apart from the "no fallback" rule: the role works without the missing skill, and never with a look-alike or a workaround.

## Grilled enough (2026-11-10)

- **The full restatement:**
  - An optional `chantier.yaml` at the project root, validated by the CLI, gives per role: the agent (the user's own Drivers included), the model, and the required skills or tools.
  - With no `chantier.yaml`, chantier works as today.
  - A host that cannot set a model at start refuses clearly.
  - For a missing required skill, the Chief of Staff warns the user and the role works without it.
  - The rule "AGENTS.md is the only configuration" is amended to match.
- The user chose "Oui, grillé (Recommandé)".

## A warning from the user, after "grilled enough" (2026-11-10)

- The user: "Attention pour les modèles et parsing de config il faut passer par le CLI. Les modèles peuvent confondre des modèles (Opus 5.6 and 5.6). Il faut que ce soit un sc". The message ends there; "un sc" is read as "un script".
- The CLI parses and validates `chantier.yaml`, never an agent.
- The CLI resolves each role's model to its exact identifier, and refuses a name that is unknown or ambiguous.
- The parent that starts an agent passes the model exactly as the CLI printed it. It never reads or interprets the model name itself: an agent can mix up close model names.
- The Chief of Staff restated this. The user confirmed: "Oui, un script (Recommandé)".

## The specification's open questions (2026-11-10)

The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's recommendation on each question. The user may change them while reviewing the PR.

1. **Where the file sits.** With an external planning surface, `chantier.yaml` sits at the code repository's root.
2. **A model alias** (such as `opus`). Accepted if the trial shows it runs the right model, and both the alias and the full name are printed.
3. **A model the CLI's table does not know.** Refused until a chantier release adds it.
4. **A configured agent that is not found.** No warning from the CLI: the host's refusal is enough.
5. **The `chantier` section of `AGENTS.md`.** The agents per role move to `chantier.yaml` only. The review steps, the release pointer and the `planning:` line stay in `AGENTS.md`. The Chief of Staff offers to move any leftover agent line.
6. **A plugin agent that needs a skill or MCP tool.** The spec had no recommendation. The Chief of Staff chose the smaller and safer scope: the plugin agents' tools do not change, and a need such as Jira is met only through the user's own agent for that role.
7. **The Foreman's model.** Not in this CR.
