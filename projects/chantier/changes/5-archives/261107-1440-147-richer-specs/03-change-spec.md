# Change Specification: a spec-writer agent writes the Change Specifications

## Goal

The Change Specifications the Chief of Staff writes are a bit light. A new role, the
**spec-writer**, writes them: started by the Chief of Staff in the background, only on the
user's word that a CR is grilled enough, on Opus 5.5, outside any batch.

## What changes

### 1. The card: `skills/chantier/references/spec-writer.md` (new)

The contract the Chief of Staff names in the spec-writer's prompt (a role's contract lives in a
card, never in the agent file). It says:

- **Input:** one CR folder (`intake/request.md`, `01-intent.md`, `02-answers.md`, any reference
  file there) and the project's rules (`$CHANTIER rules`). It reads the code the CR touches
  (read-only) to name real files, functions and commands.
- **Output:** `03-change-spec.md` in that folder, and nothing else written anywhere.
- **What a specification holds**, the criteria of a rich one: the goal in the user's terms; what
  changes, area by area, naming the files, commands, messages and cards; each decision of
  `02-answers.md` carried into it (none dropped, none invented); what is out of scope; the
  evidence that proves it (the checks and the scenario steps); self-contained, so a Driver needs
  nothing else. Any point the answers leave open is not decided by the writer: it ends with a
  list of questions instead, and the Chief of Staff takes them to the user.
- **End:** a short final answer: the spec's path, and the open questions if any.

### 2. The agent files, both hosts, identical bodies

`agents/spec-writer.md` (Claude Code, `model: opus`) and
`com.github.copilot/agents/chantier-spec-writer.agent.md` (Copilot, its Opus model), tools to
read the code and write a file (no Agent, no git that changes anything), a description in the
style of the others ("Writes one chantier CR's Change Specification from its grill. Started by
the Chief of Staff."). The structure test that checks both hosts' agents covers it.

### 3. The state: specifying, then specified (display only)

No new command. The state is read from the folder:

- **specifying:** `work/specifying` exists (the Chief of Staff writes it, one line with the time
  and the agent id, when it starts the spec-writer, and removes it when the writer ends, whatever
  the result);
- **specified:** `03-change-spec.md` exists and `work/specifying` does not.

`STATUS.json` and `STATUS.md` (`status.py`, the backlog view, and inbox items if the view shows
them) show this state per item, and the CR board mod (`hooks/register.tsx`) shows it on the
item's row. A specified CR stays where it is (inbox or backlog) until the user prioritises it
and picks it for a batch.

### 4. The Chief of Staff's card (`skills/chantier/references/chief-of-staff.md`)

- "Backlog and grill": the Chief of Staff no longer writes the Change Specification itself; on
  the user's word that a CR is grilled enough, it starts the spec-writer in the background with
  the CR folder (and the card's name in the prompt), at any time, a batch running or not. It
  reviews the result against `02-answers.md` before showing it to the user; open questions go to
  the user and the answers are recorded, then the writer runs again. A release CR's and a fix's
  specification stay the Chief of Staff's.
- The spec-writer takes no slot and no budget of any batch.
- The team table and "which agents and models?" name the new role.

### 5. Cost

A spec-writer's cost is on the Chief of Staff's line in `cost` and the reports, never in a
batch's spend or its budget check, including a direct batch, whose spend reads the Chief of
Staff's own subagents: those of type spec-writer are left out of it.

### 6. Docs and references

`concepts.md` (the roles), `routing.md` (who talks to whom), the host references (how the Chief
of Staff starts it, as for the demo-explorer), the README's role list, and `init.md`'s tour if it
lists the roles.

## Evidence

The structure tests pass with the new agent on both hosts; `just scenario` passes, and covers a
spec-writer state in `STATUS.json` (a folder with `work/specifying`, then with the spec); the
cost of a direct batch leaves a spec-writer transcript out. `just check` on the three systems.
