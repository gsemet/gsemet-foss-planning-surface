## Summary

The write guard that limits a worker agent to its work folders refused two kinds of harmless write that the host itself recommends: the session's scratchpad, and a null device closing a command substitution (`$(git merge-base a b 2>/dev/null)`, where the closing `)` was read as part of the target). Each refusal cost the worker a turn and often a retry. This change makes the guard pass both; every other write is judged exactly as before.

## Deliverables

What the guard does now:

| Write | Before | After |
| --- | --- | --- |
| `$(cmd 2>/dev/null)`, `` `cmd 2>/dev/null` ``, `$(Get-Item x 2>$null)`, `$(dir 2>NUL)` | refused | passes, silently |
| Write, Edit, NotebookEdit, or a shell write inside the session's scratchpad (drive form or Git Bash form) | refused | passes |
| `$(echo x > <outside>/a)`, `/tmp/x.log`, a sibling or a parent of the scratchpad, a command with one target in and one outside | refused | refused (the refusal now lists the scratchpad among the allowed folders when the host gave one) |
| No scratchpad given by the host (disabled or hosted) | refused | refused, today's text |

```ts
// hooks/register.tsx, tool.call: the scratchpad is read lazily, once, only when the call would be refused
const info = await $.session.info();            // { scratchpadDir?: string, ... }
folders = [...known.folders, info.scratchpadDir] // judged again with it
```

Choice: the scratchpad comes from the host's own `$.session.info()`, not from a new prompt line; a failing call lets the call through with the board's usual "could not judge" note.

## Blast radius

The change only adds passes in one hook file; a refusal can appear only where one appeared before. A write into the scratchpad is no longer stopped, so a worker could leave results there instead of in its work folder. Roll back with `git revert`.

Grade: 1

## Autonomous decisions

None.

## Known gaps

- **UNVERIFIED:** the scratchpad pass in a real session: `$.session.info().scratchpadDir`, read from the host's 2.1.330 code, is only mocked in the tests; a later measured run counts it.
- The host and shared cards still describe the scratchpad as refused for a CR's work; a later card rewrite settles the wording.
- `/tmp` writes stay refused (outside this change's scope).
- No screenshot applies (no visible change).

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: `judgeShell` strips trailing `)` and backticks from a target before the null-device test; `tool.call` reads `$.session.info()` lazily and judges again with the scratchpad added; the refusal texts list it; the guard's comment block says so.
- `hooks/register.test.tsx`: `guardWorld` gains a scratchpad parameter; table-driven cases for each pass, each kept refusal, no scratchpad, a failing host call, the lazy read and the unguarded agent.

## Impacts

No visual change. Workers stop losing turns to scratchpad and `/dev/null)` refusals.

## Test plan

- [ ] New or changed tests (they fail on the previous code): the cases of `hooks/register.test.tsx`
- [ ] Local gates at `ff04241`: `just mod` (validate: "Validation passed with warnings", the one warning is the missing plugin icon; test: "117 pass, 0 fail, Ran 117 tests across 1 file. [4.35s]"); `just check` passed (2688 passed, 20 skipped); `just test` seconds added: 0 (no pytest file changes)
- [ ] Evidence: none (hook behaviour, covered by the mocked cases; real session unproved)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-490 sc04-hook-scratch-writes (child 4 of the program `simplify-cards-and-prompts`).

</details>
