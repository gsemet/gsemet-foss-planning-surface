## Summary

The web board cannot yet start a Griller session on a backlog item. This PR adds the roles and
text that part needs: a `board-griller` agent for each host, its shipped defaults, and the
rules that tell the Chief of Staff and the Griller how a grill started from the board runs. The
server, the API and the web client that use them come in later commits of the same PR.

## Deliverables

- Two agent files with identical bodies: `agents/board-griller.md` (Claude Code) and
  `com.github.copilot/agents/chantier-board-griller.agent.md` (Copilot).
- `config/chantier.defaults.yml`: the role's agent, model and escalation defaults.
- `skills/chantier/references/griller.md`: a "Started from the board" section.
- `startup-manifest.json`, `concepts.md`, `docs/agents-and-models.md` and the host references
  (`hosts/claude-code.md`, `hosts/copilot.md`, rows marked unproved) name the role.
- `AGENTS.md`: the CLI-scope and server paragraphs name the board's Griller.
- The watcher's waking actions gain `grill`.

## Blast radius

Grade: 1. New files and text rows, one set entry and role-count tests updated; a `git revert`
restores the previous behaviour.

## Autonomous decisions

- The `AGENTS.md` edit on the no-setup bullet was adapted to the base's current wording, which
  already names the forge calls, instead of the quoted text of the specification.

## Known gaps

- No real Claude Code trial: `hosts/claude-code.md` stays marked unproved.
- Copilot is unproved, likewise.
- No screenshot of the pane from a real session.
- The `AGENTS.md` text names server, API and client behaviour that ships in the next commits of
  this PR; until then it describes code that is not there yet.
- `docs/agents-and-models.md` links `web-board.md#the-boards-griller`, a section a later commit
  creates.
- No test yet checks that the refusal text in `hosts/copilot.md` matches the engine's reason;
  the engine comes later.

<details>
<summary>Details</summary>

## Changes

- Role files, defaults, card section, manifest and concepts rows, docs, host rows, AGENTS.md.
- `hub/journal.py`: `WAKING_ACTIONS` includes `grill`.
- Tests that count roles follow the new role.

## Impacts

No visible change yet; the new role is not started by anything until the later commits.

## Test plan

- [ ] New or changed tests (role-count and manifest tests)
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: none for a text-only part
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-449 board-griller. Docs changed by this CR, for CR-447: docs/agents-and-models.md (this part),
docs/web-board.md and docs/server-api.md (later parts).

</details>
