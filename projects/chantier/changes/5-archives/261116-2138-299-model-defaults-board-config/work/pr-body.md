## Summary

Chantier's configuration could only live in one `chantier.yaml` at the code repository's root, and the default model of each plugin role lived in the agent files and in code. A user with several projects had to repeat the same settings everywhere, and there was no way to take back a value a weaker file had set.

This PR reads the configuration in four layers, merged node by node: the plugin's shipped `config/chantier.defaults.yml`, then the planning surface's root `chantier.yaml`, then the project's folder in the surface, then the code repository's own file (`.yaml` or `.yml`, never both). A stronger layer can take a value back with `default`. Every role setting is now per host, under `hosts.<host>.roles`. The default model of each role is one shipped file, kept equal to the agent files by a test.

## Deliverables

The four layers, weakest to strongest, and how a role's model is judged:

| Layer | File | Label printed |
| --- | --- | --- |
| defaults | `config/chantier.defaults.yml` (plugin) | `defaults` |
| surface | `<surface root>/chantier.yaml` | `[surface]` |
| surface project | `<surface>/projects/<name>/chantier.yaml` | `[surface project]` |
| repository | `<code repository>/chantier.yaml` | `[repository]` |

The configuration form, before and after (a top-level `roles` is now refused):

```yaml
# before (refused now)         # after
roles:                         hosts:
  coder:                         claude:
    model: opus                    roles:
                                     coder:
                                       model: opus
```

A reset: the surface root sets `hosts.claude.roles.coder.agent: my-coder`; one project writes `agent: default` and runs the plugin's Coder. `playbook` prints `coder: agent=chantier:coder [reset in surface project] model=(its file's)`.

Choices made: an empty value is never a reset (a forgotten value never unsets in silence); no model or agent can be named `default`; a configured model equal to the shipped default is the plugin's agent with no model passed, accepted on Copilot; a batch keeps the configuration frozen when it opens.

## Blast radius

Grade: **2**. Every reader of the configuration (`playbook`, `preflight`, `open`, `rules`, `gate`, the board's address, `cost` prices) now reads the merged layers, and a top-level `roles` stops being read. Rolling back is a revert, but a user file already moved under `hosts:` would need to be moved back.

## Autonomous decisions

- The `prices:`, `ci:` and `needs:` lines name the layer where they named `chantier.yaml`, since several files may now set them.
- An `agent` set together with the default model is passed on Claude Code and refused on Copilot (today's rule for a model on Copilot).
- A reset of a node no weaker layer sets is accepted silently.
- The shipped-defaults test lives in `test_playbook_layers.py`, because `test_plugin_files.py` is at the repository's 400-line limit; the board and gate surface-root case is one test there, since no board address test file exists.
- The Chief of Staff's startup card description was reflowed by a few bytes to stay inside the startup budget.

## Known gaps

- No release notes yet: the layers, `.yml`, `default` and the breaking change of a top-level `roles` are left to the release.
- `just test` takes about 63 s on the author's Windows machine, above the project's budget of 18.5 s plus 30 s; the suite was already slow there before this change and is not re-timed against the base.
- The PR changes a project rule: the `AGENTS.md` configuration sentence (section on the plugin working with no setup). The reviewer reads and approves its wording in the diff.

<details>
<summary>Details</summary>

## Changes

- `playbook/layers.py` (new): reads each layer, merges node by node, and records for each value the layer that set it and each reset (file, line).
- `playbook/config.py`, `yaml_subset.py`, `lines.py`, `models.py`, `plugin_files.py`: per-layer checks, `hosts.<host>.roles`, the `default`/`~`/`null` reset, `.yaml`/`.yml`, labels in the printed lines, a frozen record of the files read in a batch.
- `commands/rules.py`, `preflight.py`, `opening.py`, `gate.py`, `board/address.py`, `board/command.py`: read the merged configuration.
- `.gitattributes` keeps the defaults file on LF endings.
- `config/chantier.defaults.yml` (new): one model per plugin role on each host, equal to the agent files.
- Cards, host references, docs, README, `AGENTS.md` and the scenario describe and exercise the layers.

## Human decisions

- The order of layers: defaults, surface root, surface project, repository; each merges node by node.
- No role setting for all hosts: every layer sets roles per host.
- No backward compatibility: a top-level `roles` is refused.
- `default` (also `~` and `null`) takes a weaker layer's value back; an empty value stays refused.
- Both `chantier.yaml` and `chantier.yml` are accepted; both together are refused.
- A change applies at the next batch.

## Impacts

Users with a `roles:` block must move it under `hosts.<host>.roles`; otherwise no visible change with no user file.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_playbook_layers.py`, `test_playbook_config.py`, scenario sections 11 and 20, at `6f132fe`
- [x] Local gates at `6f132fe`: `just check` pass; `just scenario` pass (Windows)
- [x] Evidence at `6f132fe`: `chantier playbook` with no user file on both hosts, and in a surface with the three files, the reset and the file removed (Claude Code; on Copilot the reset and the default-equal model)
- [x] Review: approved, carried from d37ae50 over a clean rebase (head `6f132fe`)
- [x] Verified at `6f132fe`
- [x] CI green at `6f132fe`: all five checks pass

## Internal references

CR-299 model-defaults-board-config (A of three), on CR-298 (Copilot model catalog).

</details>
