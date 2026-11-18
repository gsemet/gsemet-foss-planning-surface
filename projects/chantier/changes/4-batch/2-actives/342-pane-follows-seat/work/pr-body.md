## Summary

In a session whose main checkout is a planning surface, the CR board pane listed every project of the surface, so a session steering one project saw an error for another project's missing status and then someone else's batch before its own. The pane now shows the project or projects this session steers: those whose seat file or current batch record names this session's id (as seat, Foreman or Chief of Staff). With no match it still shows every project, under one dim line saying so.

## Deliverables

The pane's choice, made at opening, at every 15 s check and at Refresh:

| Session state on a surface | Pane shows |
| --- | --- |
| id found in a project's `seat.json` (`session`, `transcript`) or `4-batch/batch.json` (`foreman`, `foreman_transcript`, `foreman_transcripts`, `chief_transcript`, `chief_transcripts`) | only the matching projects, in name order, no line |
| no match | every project, plus `No seat names this session: showing every project.` |
| the session id cannot be read | every project, plus `This session's id cannot be read (<error>): showing every project.` |
| project with `.agents/changes` (not a surface) | unchanged, no seat read, no line |

- Screenshot of the pane from a real session: not yet attached (see Known gaps).
- Choices: two projects that match are both shown; the files are re-read only when their modification time changes; the session id is read at opening and at Refresh only; the line also shows on the single-view "No chantier status here" screen.

## Blast radius

The change is local to the board pane (one hook, its types, its tests and one docs page); a plain `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

- The session id is stored in the site atom (shape tag `site-4`, one step past the specified `site-3`), because a plugin reload resets module variables while the atoms persist, which would have made a seated pane flip to every project.

## Known gaps

- No screenshot of the pane from a real session: the pane needs a real Claude Code session running this head, seated on a surface project; it is to be added in Deliverables when the user provides it.

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: reads `$.session.id()`, matches it against the seat and current batch records of each project of a surface, keeps the matched projects (all when none), re-chooses at opening, each periodic check and Refresh; the site atom gains `unseated` and the session id `sid` (shape tag `site-4`), so a plugin reload keeps the id; header comment updated.
- `types/index.d.ts`: `PluginState.chantier.site` gains `unseated: string | null` and `sid`, the session id read (or its error).
- `hooks/register.test.tsx`: parametrized tests for each matching field, two projects matched, no match, an unreadable id, the single-view screen, a seat written after opening, no re-read without an mtime change, and the unchanged in-project case.
- `docs/boards.md`: "What it is" and "How to read it".

## Impacts

The pane of a seated session shows only its own project. No change for a session with no seat or batch record naming it.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `8ae64cb`: `just check` pass (506 tests), `just mod` pass (plugin validate accepts `$.session.id`; 78 plugin tests pass)
- [ ] Evidence: no screenshot yet (see Known gaps)
- [x] Review: approved at `8ae64cb` (reviewed before the rebase onto the updated base; same patch)
- [x] Verified at `8ae64cb`
- [x] CI green at `8ae64cb` (gh pr checks 304: all five jobs pass)

## Internal references

- CR-342 pane-follows-seat
- Stacked on CR-341's branch.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
