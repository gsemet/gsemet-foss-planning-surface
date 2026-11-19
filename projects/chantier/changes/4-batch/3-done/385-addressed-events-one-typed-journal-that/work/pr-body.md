## Summary

Every event the project journal records (a PR merged, a CI check turned red, a configuration change, a board action) is now one typed, versioned line that says whom it is for. A watcher wakes its session only on the events addressed to it, and its wake rules (the 20 s quiet and a rate limit) live in one place. Today's behaviour does not change: every line written today is for the whole project, so the watcher a session starts wakes on exactly what woke it before. This lays the base for routing events to other sessions later.

## Deliverables

The new line (fields in this order), in `forge-journal.jsonl`:

```json
{"v": 1, "seq": 41, "t": "2026-11-18T10:02:03Z", "kind": "merged", "source": "hub",
 "audience": ["project"], "batch": "batch-29", "cr": "CR-12", "pr": "#88"}
```

| Before | After |
|---|---|
| `by` names the writer, no version, no audience | `v`, `source` (`hub`, `board`, `cli`), `audience` |
| `append(repo, events, by)` | `append(repo, events, source)`, the one writer path |
| `chantier watch` wakes on every line | `chantier watch [--for AUDIENCE ...]` wakes on lines for `project`, its own session and each `--for` |
| the end rule is a fixed 20 s quiet | 20 s after the last new event for it, and no sooner than `events.wake_every` (default `20s`) after its start |

Choices: the journal keeps its name and place (an old line reads as version 0, never rewritten); the CLI checks an audience value's form only (`project`, `role:<name>`, `cr:<id>`, `session:<key>`, `user`) and knows no role; a line of a newer version moves the cursor, wakes no one and is named by `chantier status`.

## Blast radius

Grade: **2**. The journal's line format and the watcher's end rule are shared by the hub, the board and the watcher; version 0 lines still read, so a revert leaves the file readable by the previous code except for version 1 lines it would treat as unknown.

## Autonomous decisions

- The start line joins the subscription values with ", ".
- `journal.read` returns a third item (lines of a newer version) so `status` can name them.
- The events-block refusal applies to the live watcher, not to `--once`.

## Known gaps

- A problem in the `events` configuration block refuses the live watcher but not `chantier watch --once`, which the specification says filters the same way; left as is, to be closed by a follow-up.
- A refused `events` block exits 2 (the precondition code), where the specification's matrix table says 3; the code follows the named constant.
- Routing to a non-`project` audience is unproved by design: no writer produces one yet, only prepared lines in tests.

<details>
<summary>Details</summary>

## Changes

- `hub/journal.py`: version 1 line, `append(..., source)` validation, `read` with effective source and audience.
- `hub/watch.py`, `declare/watch.py`: `--for`, subscription filter, start line, refusals, rate limit.
- `config/chantier.defaults.yml`, `playbook/`, `plugin_files.py`, `hub/times.py`: the `events.wake_every` key, its checks, its reader, a playbook `events:` line.
- `commands/batch_status.py`: names a line of a newer version.
- Docs, AGENTS.md, CONTRIBUTING.md, the steering card's watcher line and the scenario README state the end rule.

## Human decisions

- The journal keeps its single file and name (now historical); only the line's format changes, and old lines read as version 0.
- An audience is a form the CLI checks (`project`, `role:<name>`, `cr:<id>`, `session:<key>`, `user`); no role name is written in the code or the defaults.
- A watcher subscribes to `project` plus its own session; `--for` adds audiences; no `--for` is today's command.
- The rate limit is the one configurable key, `events.wake_every`, default 20 s; the 20 s quiet stays fixed.
- Foundation only: no routing to a role, a task or the user, no new watcher, no new forge read.

## Impacts

Developers: writers pass `source`; a new `--for` option on `chantier watch`. Users: no change.

## Test plan

- [x] New or changed tests (parametrized, in `test_event_audience.py`, `test_forge_hub.py`, `test_playbook_config.py`)
- [x] Local gates at `c7818ee` (carried from `f9fb169`): `just check` pass (868 passed), `just eval-dry-run` pass (18 of 18)
- [x] Evidence: no visual change; none
- [x] Review: approved at `c7818ee` (carried from `f9fb169`)
- [x] Verified at `c7818ee` (carried from `f9fb169`)
- [x] CI green at `c7818ee`

## Internal references

CR-385 addressed-events-one-typed-journal-that (batch-28); stacked on CR-383, CR-384; `work/investigation.md`, `work/r1.md`.

</details>
