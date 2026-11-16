## Summary

A Driver (the agent that carries one change request) sometimes called the host's hand-back without first recording `handback` in the CLI, leaving the change request `working` while its Driver was gone; the steering session found it only by chance. Separately, a Driver's turn that ended early was recorded as "out of context", and a Driver waiting on its own background work was read as ended. `status` now flags the first case, and the cards (Foreman, Driver, Claude Code host) say how to treat all three.

## Deliverables

`status` row for a working change request whose recorded Driver's transcript ends on the host's hand-back call:

```text
... working ... | Driver agent-one ended, no hand-back recorded
```

The reader, in `costs/sessions.py`:

```python
def agent_handed_back(root, sessions, agent) -> bool | None:
    # True: last tool call is SubagentHandback; False: another tool;
    # None: not measured (no file, unreadable, no tool call)
```

Choices: the flag only states the fact (the card says what to do: resume the Driver once to record its hand-back, restart only if that fails); `status` writes nothing; Copilot is not flagged (no per-agent record); the 130,000-token context threshold is unchanged, since no Driver compacted in the measured runs (peaks 80k to 124k, first compaction at about 162k).

## Blast radius

Grade: 1. A read-only flag on `status` rows and card wording; a revert restores the previous behaviour. A host that renames the hand-back tool makes the flag silent, never wrong.

## Autonomous decisions

- The reader `agent_handed_back` is new in this PR: no transcript-end reader existed on the base, so a later change that needs the same read reuses it.
- The Foreman card names the host's resume means generically ("the host's means to resume a stopped agent"), because the structure tests forbid host tool names in cards.

## Known gaps

- Two behaviours are not seen in a real batch yet: the Foreman leaving a Driver alone on "waiting on its own background work", and resuming a Driver flagged `ended, no hand-back recorded`. A later batch's Foreman transcript proves them.
- The flag reads Claude Code's transcript format (`SubagentHandback` as a `tool_use` name); a host update that renames the tool makes the flag silent.

<details>
<summary>Details</summary>

## Changes

- `costs/sessions.py`: `agent_handed_back`, reading an agent transcript from its end.
- `commands/batch_status.py`: the flag on a working row with a recorded agent (not on Copilot).
- `foreman.md`: the new `status` flag, read the row before `agents set <cr> -`, a Driver "waiting on its own background work" has not ended, resume once a Driver that ended with no hand-back, and a `context:` ask from the host named "a turn ended early".
- `driver.md`: the order of the end (`handback` first, then the host's hand-back), the early-ask wording, the description pass by a new short Verifier start, ending a turn on its own background work is allowed.
- `hosts/claude-code.md`: the resume row, the new "A background subagent stops" row, the measured peaks.

## Impacts

No visual change. A Foreman running `status` sees one new flag on affected rows.

## Test plan

- [x] New or changed tests (they fail on the previous code): parametrized reader test, scenario steps in `driver_liveness`
- [x] Local gates before the rebase onto the moved main (re-run by CI at `c1149ee`): `just check` pass (196 tests); `just scenario --unit qa-driver` pass 57/57. The full long gate is the pipeline job below.
- [x] Evidence: none (no visible change)
- [x] Review: approved at `842b800`, committed and rebased as `c1149ee`
- [x] Verified at `c1149ee`
- [x] CI green at `c1149ee`: `just check` (3 systems), `eval-dry-run`, `just scenario (ubuntu-latest)` all pass

## Internal references

- CR-289 "Change Specification: a Driver always hands back, within its context", batch-18.

</details>
