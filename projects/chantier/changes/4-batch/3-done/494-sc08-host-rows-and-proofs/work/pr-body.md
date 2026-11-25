## Summary

When a role uses a host function that was never tried for real here, nothing says so, and the host cards carry the trial history inline. This PR turns each host card's capabilities into data (one row per capability, with a one-word mark), adds `chantier host [<capability>]` to print a row (with one sentence when the row is not proved), and copies every trial story of both host cards into two proof files that no role loads. The host cards are not edited.

## Deliverables

- Two data files, `skills/chantier/references/hosts/claude-code.json` and `copilot.json`: 50 rows each, same ids in the same order; `mark` is `proved` or `untested`. 13 Claude Code rows are `proved`, none on Copilot (its card marks every line unproved).
- `chantier host` prints the first line `host: <host> (<batch or "this session">)`, then the rows. Output with no capability, no batch: `work/host-claude.txt` (37 of 50 rows end with the sentence) and `work/host-copilot.txt` (50 of 50), at the head.

```text
$ CHANTIER_HOST=claude chantier host own-session-id
host: claude (this session)
own-session-id: Own session id and title (proved)
  `get_session("self")` gives the session's id and title.
  The transcript's id is `$CLAUDE_CODE_SESSION_ID`.
```

- Two proof files, `docs/proofs/claude-code.md` and `docs/proofs/copilot.md`: a `## <capability>` per row, then `## Other: <section>` for card sections that give no row. A test checks every date and batch name of each card is found in its proof file.
- The 13 `proved` Claude Code rows and the card words each rests on:
  `own-session-id` "proved, same"; `start-driver` "the agent: proved, same"; `message-driver` "proved, same"; `message-chief` "proved, same"; `driver-hand-back` "Foreman mode: the final report as the hand-back's route is proved"; `stop-driver` "proved, same"; `agent-ids` "proved, same"; `preflight-p2` "proved, same"; `move-session` "proved 2026-11-20 (the move and the denial)"; `heartbeat` section ends "Proved: same."; `end-turn-background` "proved, batch-16"; `subagent-stops` "proved, batch-18"; `resume-subagent` "proved, batch-15", refusal "proved, batch-22".
- Tests: `just test` before 116.88 s, after 111.69 s on the same machine (within noise; the new tests add under 2 s).

## Blast radius

Grade: 1. New files and a new read-only command; nothing existing changes behaviour. A `git revert` restores the previous state.

## Autonomous decisions

- Unknown capability exits 2 (`EXIT_PRECONDITION`, which is 2 in this CLI), as the specification intends. The refusal when no host can be told keeps the exit code `detect_host` raises (1), which the test asserts.
- The proof files and rows follow the specification's row table; any correction is named in the notes.

## Known gaps

- `references/concepts.md` lists commands and does not name `host`: cards are out of scope for this change.
- Two tests are weaker than the specification words: the "untested row prints the sentence" test calls the row printer in process instead of the CLI for each row (the CLI path is covered by the batch-record test and the scenario), and the batch-record test rewrites the record's host instead of opening a Copilot batch.
- No Windows run of the long gate: this PR is not on top of its stack, so the local run is owed by the top PR; the pipeline's `scenario` passed at ac03671.

<details>
<summary>Details</summary>

## Changes

- `src/host_rows.py` (rows, `UNTESTED`, `load_rows`, `row_lines`), `src/commands/host.py`, `src/declare/host.py`, `src/cli.py` (registration, `FULL_OUTPUT`).
- `docs/hosts.md` pointer, AGENTS.md paragraph for `host`, scenario step and coverage bullet.
- `tests/test_host_rows.py`: nine tests.

## Impacts

No visual change. No role reads `host` yet.

## Test plan

- [x] New tests in `tests/test_host_rows.py` (they fail on the previous code: no `host` command)
- [x] Local gates at `ac03671`: `just check` pass, `just eval-dry-run` pass; CI at `ac03671`: all five checks pass, `scenario` included
- [x] Review: inspector approved at `ac03671` (carried from `64ff139`, a clean rebase); Verifier VERIFIED at `ac03671`
- [x] Evidence at `ac03671`: `host` outputs on each host, no batch (above)

## Internal references

- CR-494 (sc08-host-rows-and-proofs), batch-31.

</details>
