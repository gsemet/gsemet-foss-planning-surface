Stacked on #214.

## Summary

Four rough edges of the CLI cost round trips and failed commands in a recent night run. A Driver that handed back `blocked` could not hand back `ready` once the block was gone without going through the steering session. On Windows, in chantier's own checkout, `uv run` raced the board or a gate for `.venv\Scripts\chantier.exe` (os error 32) and sometimes ran on a stale environment. `uvx --from <checkout>` served an old cached build of the board. And `take`, `handoff` and `ship` printed `base origin/main` for a stacked CR whose PR targets another branch.

## Deliverables

| Before | After |
| --- | --- |
| `handback <cr> ready` on a blocked CR: refused, `take --note` round trip | accepted when the blocking Driver is still recorded; notes `ready after blocked: <reason>`, prints `it was blocked: <reason>` |
| Dev run line `uv run --locked --project <root> chantier` | `uv run --no-sync --project <root> chantier`, with `uv sync --locked --project <root>` run only at named moments by the steering session |
| `take`/`handoff`/`ship` of a stacked CR print the start base | they print the PR's base as the forge reports it (GitHub `base.ref`, GitLab `target_branch`); a failed read prints `base ? (not read from <link>: <text>)` |

```text
steering session: uv sync --locked  (session start, batch start, after a merge changing uv.lock)
everyone else:    uv run --no-sync --project <root> chantier <command>
```

`forge-stack create` already builds from the ready CRs and lists the others as `to come` (merged earlier); this PR adds no code for it and quotes the existing scenario checks as proof.

## Blast radius

Grade: 2. Every `$CHANTIER` line in chantier's own checkout changes form, so the old allow rule `uv run --locked --project * chantier *` no longer matches until the new rules from the permission check are added; `take`, `handoff` and `ship` make one forge read for a stacked CR with a PR. Rolling back is a revert, plus restoring the old allow rule.

## Autonomous decisions

- The five open points of the specification took the specification's own recommended reading, since no answers file exists: Part B stays proof only; a blocked release keeps the `take --note` route; the sync after a merge that changes `uv.lock` waits for no gate to run; `AGENTS.md` carries the new run line; a failed forge read prints `base ?` and the command goes on.

## Known gaps

- The Windows os error 32 evidence (board running, second session's `--no-sync` command, sync with the board running) is not captured yet: **UNVERIFIED**.
- The refusal of a blocked release's hand-back as ready is **UNVERIFIED** by a command; it is shown in the code only.
- The GitLab `target_branch` read has no scenario check; it was exercised once with a mocked `glab`.
- The scenario's `stack (github)` unit ran over its time budget at this head (345 s against 320 s); the gate still passed.
- The base read catches the forge's expected error shapes only; an answer of an unexpected shape could still fail the command, where the specification says a failed read never does.
- `evals/README.md` still shows the old dev run line; the eval kit is out of scope.
- The old allow rule `uv run --locked --project * chantier *` no longer matches; the new rules must be added to the user's settings (the permission check names them).

<details>
<summary>Details</summary>

## Changes

- `handback` and `live_cr` (`commands/driver.py`, `commands/driver_checks.py`): a blocked CR with a recorded agent may hand back `ready`; every other refusal is unchanged; blocked releases and a second `blocked` stay refused.
- `plugin_files.py`: `cli_command` in the dev mode uses `--no-sync`; new `sync_command()`.
- `commands/preflight.py`: on Windows in the dev mode the tools line carries the sync sentence. `commands/permissions.py`: new dev rows, including the sync rule.
- `commands/forge_base.py` (new), `commands/facts.py`, `commands/delivery.py`: the PR's base read for stacked CRs.
- Cards, skills and docs updated to agree: `driver.md`, `foreman.md`, `chief-of-staff.md`, `concepts.md`, `status-layout.md`, `hosts/claude-code.md`, the four `SKILL.md` files, `AGENTS.md`, `CONTRIBUTING.md`, `docs/web-board.md`.
- Tests: `test_plugin_files.py`; scenario checks and the fake forges (`scenario/`).

## Impacts

No visual change. Developers on Windows no longer meet os error 32 from `uv run`; the steering session syncs at named moments.

## Test plan

- [x] New or changed tests: `test_plugin_files.py` and the scenario checks
- [x] Local gates at `680c9a7`: `just check` pass, `just eval-dry-run` pass (8 of 8), `just scenario` pass
- [ ] Evidence: Windows os error 32 not captured (see Known gaps)
- [x] Review: approved at `680c9a7` (round approved at `9a63cf2`, carried over a rebase with one conflict resolved, re-reviewed)
- [x] Verified at `680c9a7`, with the two UNVERIFIED claims of Known gaps
- [x] CI green at `680c9a7`: `just check` on three systems, `just eval-dry-run`, `just scenario`

## Internal references

- CR-264 b17-cli-fixes
</details>

