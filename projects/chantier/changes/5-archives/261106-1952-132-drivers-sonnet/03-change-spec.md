# The CR Driver runs Sonnet

## Problem

The CR Driver runs Opus and is the largest Driver spend: $20.48 of batch-06's $64.28.

## Change

On both hosts together, the frontmatter only, the bodies unchanged:

- `agents/cr-driver.md`: the model becomes Sonnet 5.5, as in `agents/qa-driver.md`.
- `com.github.copilot/agents/chantier-cr-driver.agent.md`: `[Claude Sonnet 5.5, claude-sonnet-5.5]`.

Then what says otherwise:

- `skills/chantier/scripts/cli/tests/test_structure.py`: `cr-driver` leaves `OPUS_ROLES`.
- `skills/chantier/references/hosts/claude-code.md`, the Models row, and its Copilot twin if it names
  the models.
- `README.md`: the models table, split so that the CR driver has its own row, and the sentence under
  it that says the roles that judge run Opus.
- `CONTRIBUTING.md` line 51: "the Foreman and the Drivers (Opus 5.5) judge freely".

## Out of scope

The stack, release and QA drivers, the Foreman, and a project's choice of a role's model
(`playbook-config`).

## Done when

- A CR Driver's model is Sonnet 5.5 on both hosts; the stack and release drivers' are unchanged.
- No text in the repository says the CR Driver runs Opus.
- `just check` and `just scenario` pass.
