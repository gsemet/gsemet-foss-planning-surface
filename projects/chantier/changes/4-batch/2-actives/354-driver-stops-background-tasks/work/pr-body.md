## Summary

A background task that outlives its purpose wakes its owner each time it reports, and on Windows a process whose current folder is inside a folder keeps that folder from being moved or removed. A CR Driver used to start inside its CR folder in the planning surface, and the Foreman's own wait loops ran there too, which blocked the CR's move between stages. This change starts a CR Driver in its worktree (or the project's root before the worktree exists) and makes each Driver stop its background tasks before it hands back.

## Deliverables

On Claude Code, the plugin's mod now picks the folder a spawned agent starts in:

| Prompt | Start folder |
| --- | --- |
| `writes:` only (a worker's) | first `writes:` folder, as before |
| `worktree:` line, folder exists | that worktree |
| `worktree:` line, folder absent yet | the project's root named by the prompt's first line |
| neither usable | the parent's folder, still guarded, with a board note |

Rules and cards: no shell changes its folder into a CR folder; a Driver stops each background task by its id and, before any hand-back, every one still running except the shell that runs the long gate; the steering session starts no waiting task and stops an ended Driver that wakes again. The four Claude Code Driver agents gain the `TaskStop` tool.

## Blast radius

Grade: **2**. The mod's start folder is shared by every guarded spawn, and the cards change Driver behaviour; revert restores the old behaviour.

## Autonomous decisions

None

## Known gaps

- No run in a real batch yet: the new host rows stay unproved (the start folder of a CR Driver on Claude Code and on Copilot, `TaskStop` by a Driver, and whether stopping an ended Driver also ends its leftover tasks). Each row names its trial.
- The long gate (`just scenario`) is not yet shown green at the head in this description.

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: `worktreeOf` and `rootOf` helpers; the `agent.spawn` hook chooses the start folder; the recorded worker's `cwd` is that folder.
- `hooks/register.test.tsx`: four tests.
- `skills/chantier/references/` (`concepts.md`, `driver.md`, `foreman.md`, `hosts/claude-code.md`, `hosts/copilot.md`), `CONTRIBUTING.md`, `docs/boards.md`: the rules and wording.
- `agents/{cr,stack,qa,release}-driver.md`: `TaskStop` on `tools:`.

## Human decisions

- A CR Driver starts in its worktree, or in the project's root while the worktree does not exist yet, never in its CR folder.
- A long gate still running at a Driver's hand-back is left to finish, and the CLI records its result; every other background task is stopped first.

## Impacts

No visual change. A CR Driver on Claude Code starts in its worktree.

## Test plan

- [x] New or changed tests (four hook tests in `hooks/register.test.tsx`)
- [ ] Local gates at `<sha7>`: `just check`, `just mod`
- [ ] Evidence: none (no visible change)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-354 driver-stops-background-tasks.

</details>
