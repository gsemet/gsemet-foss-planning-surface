## Summary

CR-502 carries three parts of the `simplify-cards-and-prompts` program in one PR (children 16, 17, 18), one commit per part:

1. SC16: `chantier retro draft` drafts the retro points from the batch's events (prints; `--write` appends once to `retro.md`).
2. SC17: one launcher (`skills/chantier/scripts/chantier.py`) that picks the mode and runs the CLI.
3. SC18: role data in `skills/chantier/roles.yaml` and a `just roles` check of the wrappers.

Spec: `03-change-spec.md` of the CR folder.

## Review

- [ ] Part 1 inspector approved (pending)

## Deliverables

Part 1: `retro draft` command, tests (`tests/test_retro_draft.py`, 23 cases, 1.74 s), scenario step, AGENTS.md line.

## Known gaps

- Parts 2 and 3 not yet done in this body.
