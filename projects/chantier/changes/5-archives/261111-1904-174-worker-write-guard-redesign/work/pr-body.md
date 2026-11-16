## Summary

The plugin's guard on a worker's writes refused every Write and Edit of every worker in a recent automated run, inside its own worktree too, with an empty path in the message: it read the path from a field the engine does not set on a `tool.call` event, and its tests mirrored that mistake and were never run. This PR redesigns the guard: one `writes:` line in an agent's prompt names the folders it may write in, the agent starts in the first one, and a guard that cannot judge lets the call pass and says so on the board. A recipe, `just mod`, runs the mod's checks so the tests can be run.

## Deliverables

The contract between the cards and the hook is one line in a worker's prompt (the hook knows no role and parses no other wording):

```text
writes: <worktree>; <CR folder>
```

The hook, in outline:

```text
agent.spawn:  read the first "writes:" line; every entry absolute -> next({...e, cwd: <first folder>})
              (not on a resume); record { folders, cwd } under the agent id
tool.call:    Write/Edit -> e.file_path, NotebookEdit -> e.notebook_path   (flat, nothing else)
              inside a folder -> next(e)
              outside         -> refused: <path> is outside the folders this agent may write in (<folder>; <folder>); write there
              cannot judge    -> next(e) and a board note ("... the call passed.")
```

Before and after:

| | Before (base 24cc7eb) | After |
| --- | --- | --- |
| Which agents | a list of worker roles, found by parsing two CLI lines | any agent whose prompt holds a `writes:` line |
| Path read | `input.file_path` (always empty on `tool.call`) | `file_path` or `notebook_path`, flat |
| Guard at fault | every worker refused | the call passes, one board note |
| Proof | tests never run | `just mod`: `claude plugin validate` and 41 plugin tests (the 11 guard tests use the engine's real shapes) |

Choices made: a worker starts in its worktree (a shell write cannot reach the main checkout by a relative path); shell writes are not guarded, the agent that coordinates the work reports what changed in the main checkout with `git status`; the eval's audit checks each worker's prompt holds the line.

**UNVERIFIED:** the start-in-the-worktree behaviour and a refusal seen in a real session (a trial of both runs before merge; the refusal is required).

## Blast radius

Grade: 1. The guard is one hook and its tests, plus card and doc text; the guard fails open. A plain `git revert` restores the previous state.

## Autonomous decisions

- `types/index.d.ts` declares the new `workers` state: `claude plugin validate` refuses the plugin without it.
- The review step's `just mod` rule is in the review section of `worker.md`: there is no separate review card.
- The guard text removed from the README, CONTRIBUTING and the Claude Code host reference by the previous commit is written again, rewritten for the new design.
- `just mod` finds `claude` on the PATH, else through the session's `CLAUDE_PID`.

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: the guard (spawn rewrite and record, flat-field check, pass with a note); no role list, no CLI-line parsing.
- `hooks/register.test.tsx`: guard tests with the real event shapes, including the old wrong shape passing with the note.
- `scripts/mod.py`, `justfile`: the `mod` recipe.
- `evals/kit/audit.py`: a check for the `writes:` line.
- Cards: `concepts.md` (the prompt line), `driver.md`, `worker.md`, `chief-of-staff.md` and `status-layout.md` (the `git status` look before each report), `hosts/claude-code.md`.
- `AGENTS.md`, `CONTRIBUTING.md`, `README.md`: the rule and the description of the guard.

## Human decisions

- A worker starts in its worktree, tried first; if the trial fails, the PR ships without the rewrite.
- A guard that cannot judge lets the call pass and says so on the board; no second refusal message.
- No role list: the prompt's `writes:` line is the only contract.
- `just mod` is run by the agent that changes `hooks/` or `types/`; if it cannot run, the agent stops.
- The main checkout is watched by the coordinating agent's `git status` before each report, not by the hook.
- `just mod` stays outside CI (CI has no `claude` binary).
- A refusal must be seen once in a real session before this ships; if the start-folder rewrite cannot be tried or fails, it ships without the rewrite, and the refusal is still required.
- The release waits for this change.

## Impacts

No visual change. Contributors run `just mod` for a change to `hooks/` or `types/`; the coordinating agent's status reports may carry a line about stray files in the main checkout.

## Test plan

- [ ] New or changed tests (they fail on the previous code): 11 guard tests in `hooks/register.test.tsx`, passing at 24cc7eb plus the working tree (`just mod`: 41 pass, 0 fail; the SHA moves with the commit)
- [ ] Local gates: `just check` (44 pass) and `just mod` green, **UNVERIFIED** at the final head: judged on the working tree over 24cc7eb
- [ ] Evidence: **UNVERIFIED** until independent verification runs
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] `just scenario` at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-174 "the worker write guard, redesigned" (batch-11), the guard it replaces is CR-171's.
- Specification: `.agents/changes/4-batch/2-actives/174-worker-write-guard-redesign/03-change-spec.md`

</details>

