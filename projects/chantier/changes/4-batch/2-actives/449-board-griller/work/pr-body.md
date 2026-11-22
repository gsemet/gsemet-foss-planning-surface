## Summary

The web board cannot yet start a Griller session on a backlog item. This PR adds the roles and
text that part needs: a `board-griller` agent for each host, its shipped defaults, and the
rules that tell the Chief of Staff and the Griller how a grill started from the board runs. It also adds the
server engine that runs the Griller (a headless host process per chat, its files, its turns), the
API ops and topic that drive it, and the write guard that refuses edits of a chat's CR. The web
client (a Grill button on a backlog item and a discussion panel) is in the last commit of the PR.

## Deliverables

- Two agent files with identical bodies: `agents/board-griller.md` (Claude Code) and
  `com.github.copilot/agents/chantier-board-griller.agent.md` (Copilot).
- `config/chantier.defaults.yml`: the role's agent, model and escalation defaults.
- `skills/chantier/references/griller.md`: a "Started from the board" section.
- `startup-manifest.json`, `concepts.md`, `docs/agents-and-models.md` and the host references
  (`hosts/claude-code.md`, `hosts/copilot.md`, rows marked unproved) name the role.
- `AGENTS.md`: the CLI-scope and server paragraphs name the board's Griller.
- The watcher's waking actions gain `grill`.
- `board/griller.py`, `griller_host.py`, `griller_files.py`: the engine; the API ops, the topic and
  the write_api refusals; `docs/server-api.md` and `docs/web-board.md` ("The board's Griller").
- The web client: `clients/web/js/panel/griller*.js`, `js/api/griller.js`, `css/griller.css`, en/fr strings, `DESIGN.md` section.

| Host | Agent file | Role |
| --- | --- | --- |
| Claude Code | `agents/board-griller.md` | the board's Griller |
| Copilot | `com.github.copilot/agents/chantier-board-griller.agent.md` | the board's Griller |

## Blast radius

Grade: 1. New files and text rows, one set entry and role-count tests updated; a `git revert`
restores the previous behaviour.

## Autonomous decisions

- The `AGENTS.md` edit on the no-setup bullet was adapted to the base's current wording, which
  already names the forge calls, instead of the quoted text of the specification.

- `startup-manifest.json` has no `actions.board-griller` key (the spec asked for one; the startup size limit forbade it and nothing reads it; `actions.grill` already lists griller.md).

## Known gaps

- No real Claude Code trial: `hosts/claude-code.md` stays marked unproved.
- Copilot is unproved, likewise.
- No screenshot of the pane from a real session.
- No check of the panel in a real browser yet (node smoke of the view only); the Verifier does it.
- CR-456 renames the server command `board` to `serve`: the `--new-key` hint strings say `board` until it lands; the command name is one constant (`BOARD_COMMAND` in `js/panel/griller-view.js`), to change when CR-456 merges.
- The `summary set <cr> --title *` allow rule also matches a trailing `--project <other>`; to narrow
  once the real trial proves the grammar.
- The Claude flags and `_claude_saved` are unproved (no real trial).
- `just test` time against its 30 s budget is not measured.
- No test checks that the refusal text in `hosts/copilot.md` matches the engine's reason.

<details>
<summary>Details</summary>

## Changes

- Role files, defaults, card section, manifest and concepts rows, docs, host rows, AGENTS.md.
- `hub/journal.py`: `WAKING_ACTIONS` includes `grill`.
- Tests that count roles follow the new role.

## Human decisions

- Only the plugin's `board-griller` agent runs a grill started from the board; its model is
  configurable like any role's.
- The agent exists as a file on both hosts, kept identical.
- Any holder of the server's key may start a grill from the board.
- The Griller's shell is limited to an allow-list of four command shapes.

## Impacts

The board shows a Grill button on backlog items and a discussion panel.

## Test plan

- [ ] New or changed tests (role-count and manifest tests)
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: none for a text-only part
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-449 board-griller. Docs changed by this CR, for CR-447: docs/agents-and-models.md (this part),
docs/web-board.md and docs/server-api.md.

</details>
