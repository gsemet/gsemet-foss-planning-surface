## Summary

`chantier close` used to refuse for five minutes after any agent's transcript was written, even when that agent had already handed back, and it missed a silent tool call that ran longer than five minutes. `close` now reads the end of each Claude Code transcript: an agent that handed back (or ended its turn with no tool call) is finished, and one with a tool call that has no result yet is running, whatever the file's age.

## Deliverables

An agent that stopped without handing back (an app restart, the user's stop) reads as running. For it, `close` takes the user's word:

```text
close --batch <batch> --stopped agent-<id> [--stopped <name> ...] [--yes]
```

| Transcript's last `user`/`assistant` record | Reading |
| --- | --- |
| the result of the host's hand-back tool call | ended |
| an `assistant` record with no tool call and `end_turn` / `stop_sequence` | ended |
| a tool call with no result yet | still runs |
| a tool result or a prompt with no answer after it | still runs |
| an `assistant` record stopped on `tool_use`, null or another value | still runs |
| missing file, unreadable, cut last line, no record | cannot be read (refuses; `--stopped` does not pass it) |

With `--yes`, the declaration is recorded in the batch's archived record (`stopped_agents` in the JSON, a line under `## Cost` in the Markdown). Copilot sessions keep the five-minute file-time rule.

## Blast radius

Grade: **2**. `close` deletes the batch's files, so a wrong "ended" reading would allow a close while an agent still runs; the rule is conservative (anything not clearly ended refuses) and is covered by the reader test and the scenario's close steps. Revert restores the old rule.

## Autonomous decisions

- `close --stopped` reads the transcripts twice on a batch that is not paused (once per caller of the idle check); harmless, left as is.

## Known gaps

- Copilot sessions keep the five-minute rule; reading the end of Copilot's `events.jsonl` is a later change.

<details>
<summary>Details</summary>

## Changes

- `costs/sessions.py`: a reader of a transcript's end (label, agent name, path, state: ended, still running with its cause, or cannot be read).
- `costs/sessions.py` also keeps one reader: `agent_handed_back` reads through it.
- `rails.py`: `running()` uses it for Claude transcripts; the Copilot branch keeps its own constant.
- `declare/closing.py`, `commands/closing.py`, `history.py`, `commands/close_archive.py`: the repeatable `--stopped` flag, its refusals and its record.
- Cards and docs: the closing and recovery sections, the batch definition, the planning-folder, tutorial and use-case pages, the scenario README.
- `scenario/run_scenario.py`: the close steps for the new rule and for `--stopped`; one parametrized reader test.

## Impacts

`close` no longer waits on finished agents; a refusal names the agent, its cause and its file.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_transcript_end.py` and the scenario's close steps
- [x] Local gates: `just check` pass (235 tests) on the working tree before the commit at `7f12cd2`; the scenario passed on Windows at the first round (`4212425`)
- [x] Evidence: none beyond the scenario
- [x] Review: approved at `7f12cd2` (reviewed before the final rebase onto main; the rebase was clean)
- [x] Verified at `7f12cd2`: reader and handed-back tests, scenario close steps (212 checks, Windows); the rest carried from `4212425`
- [x] CI green at `7f12cd2`: all five jobs pass

## Internal references

CR-294 close-finished (batch-18).

</details>
