## What

When a stack is ready, the Chief of Staff offers a demo of what it delivers. On a yes, a new agent, `demo-explorer`, studies the PRs, the CRs and, only if needed, the code, and writes `demo/demo.md` in the batch's folder. The Chief of Staff then guides the user through each change.

- `chief-of-staff.md`, `SKILL.md`: the Chief of Staff may start subagents for an exploration, a prototype or a study; none implements. The offer, the study, the demo and what a problem found becomes.
- `worker.md`: the "Demo explorer" section. `concepts.md`, `routing.md`: how such a subagent starts and answers.
- `agents/demo-explorer.md`, `com.github.copilot/agents/chantier-demo-explorer.agent.md`: identical bodies; models as the Investigator's.
- `tests/test_structure.py` and the README's model table know the new agent.

The CLI gets no new command.

## Checks

- `just check`: 27 passed.
- `just scenario`: 204/204 on GitHub and on GitLab, at 937264b.

## Stack

Stands on CR-120 once restacked; a `worker.md` conflict with CR-120 is expected there, keep both.
