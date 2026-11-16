## Summary

The agents that drive a change sometimes did work that belongs to their helpers, lost context without warning, discarded work in their worktree or spent a round on nothing. This change makes the CLI refuse a round on which nothing happened, show the context size of the agent driving each change, and extends the plugin's write guard to that agent and to the shell writes it can see. The cards say how large outputs stay in files, when to hand back before the context runs out, and that work in a worktree is never discarded by the driving agent.

## Deliverables

Behaviour after the change:

| Area | Before | After |
| --- | --- | --- |
| `round` called twice with nothing between | counted | refused, exit 2, count unchanged |
| `note` / `round` output | `ok` | adds `context: <n> tokens (agent <id>)` or `context: not measured (<why>)` |
| `cost --by cr` | calls only | adds peak context and compactions of the driving agent |
| Shell write (`Set-Content`, `>`, `sed -i`...) outside the folders of a guarded agent | allowed | refused by the guard |

```text
round event -> { wt_head, wt_state }   (read-only git fingerprint)
next round: refused when no other event since AND same fingerprint
```

Choices: the guard applies to any agent whose prompt carries a `writes:` line; the agents that run a stack, a release or QA stay unguarded; the context threshold of 150,000 tokens is three quarters of the 200,000-token compaction window of the plugin's agents.

## Blast radius

Grade: 2. The guard now judges shell calls of every agent with a `writes:` line, and `round` can refuse. Revert restores the previous behaviour.

## Autonomous decisions

- The round fingerprint is a hash of read-only git output (head, status, untracked files), so the CLI changes nothing in git.
- A previous round without a recorded fingerprint is judged on the events alone, since nothing else can be compared.

<details>
<summary>Details</summary>

## Changes

- `rails.py`, `commands.py`: stray-round check, fingerprint, `context:` line.
- `costs.py`: `agent_context` reads the end of the agent transcript; `cost --by cr` figures.
- `hooks/register.tsx`: shell write guard for Bash and PowerShell, with tests.
- Cards and docs: `driver.md`, `foreman.md`, `concepts.md`, `hosts/claude-code.md`, `docs/boards.md`, `CONTRIBUTING.md`, `scenario/README.md`.

## Impacts

No visual change. Developers see a `context:` line on `note` and `round`, and a refused stray `round`.

## Test plan

- [ ] New or changed tests: `tests/test_structure.py`, `hooks/register.test.tsx`, scenario steps
- [x] Local gates at `1db06ea`: just check, just mod, just scenario pass
- [ ] Evidence: none (CLI and hook change)
- [x] Review: approved, round 1 committed as ae3355a (carried to 8eef57c by a clean rebase), round 2 at 1db06ea
- [x] Verified at `1db06ea`
- [x] CI green at `1db06ea` (gh pr checks 163: 5 checks pass)
- **UNVERIFIED:** that drivers hand back `context:` before running out, and that the shell guard refuses a real driver's shell edit in a live session.

## Internal references

CR-216 driver-stays-a-driver.

</details>


