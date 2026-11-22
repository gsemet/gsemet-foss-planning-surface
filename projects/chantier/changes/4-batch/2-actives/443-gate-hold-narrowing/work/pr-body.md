## Summary

`chantier gate` ran any text through a shell and `chantier lease <unit> hold -- <command>` ran any program. Both are chantier commands, so chantier's allow rules let them through with no prompt: an agent with shell access could run anything through them. This PR closes both doors. `gate` now runs only the long gates a project names in its code repository's root `chantier.yaml` (`long_gate.commands`), asked for by name; `lease hold` runs nothing and only keeps a lease alive for a bounded time.

## Deliverables

Before and after, for the two commands:

| | Before | After |
| --- | --- | --- |
| Long gate | `chantier gate <cr> "just scenario"` runs the text | `chantier gate <cr> scenario` runs the command `long_gate.commands.scenario` names; a free command is refused (exit 1) |
| No entry | any command runs | refused (exit 2), the refusal prints the three lines to add |
| Lease wait | `lease <unit> hold --lease <n> -- <command>` runs the command | `lease <unit> hold --lease <n> [--minutes N]`: 45 minutes by default, 90 at most; `--` is refused |

```yaml
# chantier.yaml, in the code repository's root (the only file that may name a command)
long_gate:
  parallel: 1
  commands:
    scenario: just scenario
```

Choices made:
- Only the code repository's root `chantier.yaml` names a gate's command; `long_gate.commands` in a planning surface's file is ignored for running, and `playbook` and `validate` say so (a `validate` gap). `long_gate.parallel` still merges across layers.
- No transition period: a free command is refused from this version on.
- A hold keeps the lease live up to 90 minutes with no process behind it; past it the lease shows "not confirmed", the designed safe state, and the holder's next command is accepted as late. `agents set <unit> -` ends a held lease once the host shows the holder ended.
- The `.lease-hold.*.run` records, the `holds` facts of a lease and the `held` state of the terminal client are removed. Published API change: `holds` is gone from the lease object of `project.state` (`docs/server-api.md`).
- Known limit: `just scenario` runs the worktree's justfile, which a Coder edits. This guards the read-only roles against running anything through chantier, not a Coder.

**Before you update:** add the entry to the code repository's root `chantier.yaml` before updating the plugin, since from this version `gate` refuses a free command and every gate of a running batch is refused until the entry is there:

```yaml
long_gate:
  commands:
    scenario: <your long gate's command>
```

After this PR merges, the maintainer runs `sandbox.py reset --yes` once: the eval kit's sandbox base changed (a new `chantier.yaml`), and `evals/kit/sandbox.json` is re-recorded here.

## Blast radius

Grade: 3. Every long gate of a running batch is refused until its project holds the `long_gate.commands` entry, and the published lease object loses a field. Rollback is a revert, plus removing the entry if added.

## Autonomous decisions

- The long gate code moved into a new `playbook/long_gate.py` and the lease-hold tests into `tests/test_lease_hold.py`, to keep files under the 400-line limit.
- `lease hold` tests and the chantier root file are checked by shipped-state tests (the root `chantier.yaml`, `AGENTS.md` and the eval kit's two `chantier.yaml` files).

## Known gaps

- Until this PR merges, the CLI that runs is the old one, so this PR's own local gate uses the free form.

<details>
<summary>Details</summary>

## Changes

- `playbook/config.py`, `playbook/long_gate.py`, `playbook/lines.py`, `commands/validate.py`: the `long_gate.commands` key, read from the code repository's root only, the `long gate:` lines of `playbook`, the `validate` gap for an ignored surface file.
- `commands/gate.py`, `declare/gate.py`, `commands/facts.py`, `commands/driver_checks.py`: `gate <cr> <name>...` with its refusals; log lines and events carry the name.
- `commands/leases.py`, `core/leases.py`, `declare/driver.py`, `commands/driver.py`, `commands/orders.py`, `commands/take_checks.py`: `lease hold [--minutes N]`, no command, no record files, `CHANTIER_LEASE_TEST_MINUTE` test seam.
- `board/crs.py`, `board/fingerprint.py`, `clients/tui/model.py`, `docs/server-api.md`: the `holds` lease facts go.
- Root `chantier.yaml`, `AGENTS.md`, the cards (driver, foreman, verifier, concepts, chief-of-staff, init, Claude Code host), the docs, `README.md`, `scenario/README.md`.
- Eval kit: `chantier.yaml` in the sandbox and the fixture, `dry_run.py` gate by name, re-recorded `sandbox.json`.
- Tests and `scenario/run_scenario.py`: gates by name, a free-command refusal check, section 3a on a hold with no process, a stack lease-late check.

## Human decisions

- `gate` runs only commands named in `chantier.yaml`, by name; no free command, no transition.
- `lease hold` runs nothing: 45 minutes by default, 90 at most.
- chantier's own gate ships committed in the repository's root `chantier.yaml`; the eval kit's sandbox and fixture ship their entry too.
- A project with no gate written is offered the entry once, written on the user's yes.

## Impacts

No visual change. Projects must add `long_gate.commands` to run a long gate; waits are kept alive by `lease hold` with no child process.

## Test plan

- [x] New or changed tests at `11f98d9` (config key, gate refusals and named run, ignored layer, hold limits, shipped files)
- [x] Local gates at `11f98d9`: `just check` pass, `just eval-dry-run` pass; `just scenario` passed at `1353bbd` and is re-run by the pipeline job
- [x] Evidence: none beyond tests (no visual change)
- [x] Review: approved at `11f98d9` (restack with a conflict resolved)
- [x] Verified at `11f98d9`
- [ ] CI green at `11f98d9` (pending the push of the restack)

## Internal references

- CR-443 gate-hold-narrowing (batch-30), step 2 of the permissions-bypass split; after CR-432.

</details>
