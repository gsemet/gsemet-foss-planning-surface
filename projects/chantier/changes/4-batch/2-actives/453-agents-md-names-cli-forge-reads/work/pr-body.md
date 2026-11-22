## Summary

The project's rules said the CLI needs no network beyond a few named parts and that "the agents do the work, git and the forge included". In fact the CLI calls the forge, with the user's own `gh` or `glab`, from `ship`, `take`, `round`, `handoff` and `forge-stack`. This change makes every text that states the rule name those calls, what they read or write, and their limits. No code behaviour changes: three docstrings and prose only.

## Deliverables

Where the rule changes, in one table:

| Text | Before | After |
| --- | --- | --- |
| `AGENTS.md`, no-setup bullet | network only for the server's PR read, the forge hub, the writer | adds the forge calls of `ship`, `take`, `round`, `handoff`, `forge-stack`, with the user's own `gh` or `glab` |
| `AGENTS.md`, scope bullet | "the agents do the work, git and the forge included" | "... but for the forge calls named below", plus one named exception: `ship` reads a PR's base and draft state, `take`/`round`/`handoff` read a stacked CR's base, `forge-stack` writes only stacks and bases |
| `CONTRIBUTING.md`, `README.md` | "no forge command" | the same calls named |
| `concepts.md`, `driver.md` (x2) | "The CLI reads no forge" | "The CLI reads no CI" |
| three docstrings | "no forge command at all" | the reads and `forge-stack` named |

Inventory check at the head: every hit of the spec's `rg` over the CLI's `src/` falls in a known call (`ship`'s `read_state`, the `forge_base` helpers used by `take`, `round`, `handoff`, `forge-stack`'s `gh`/`glab`, the hub's and the board's connectors) or in the non-forge list (`permissions.py`'s `gh extension list`). No new caller (the `rg` returned 10 files of the CLI, each in the inventory). Word check: no unqualified "no forge command" or "reads no forge" said of the CLI remains (`hub/watch.py`'s true docstring aside).

## Blast radius

Text only; no command's output changes. Other open changes touch neighbouring `AGENTS.md` text; conflicts, if any, are textual.

## Autonomous decisions

- `round` is named alongside `take` and `handoff`: it also prints a stacked CR's base.

## Known gaps

- No test guards the wording (decided).
- A flaky Windows test (`test_w2_a_shell_inside_the_folder_refuses_then_lets_go`) failed once in a `just check` run and passed on rerun.

<details><summary>Details</summary>

## Changes

`AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `skills/chantier/references/concepts.md`, `skills/chantier/references/driver.md`, and the docstrings of `commands/__init__.py`, `commands/forge_base.py`, `lifecycle/moveout.py`.

## Human decisions

- Name the CLI's forge calls in the rules; move or change no code.
- `forge-stack`'s forge writes are named, limited to stacks and bases.
- The exception cites why the calls exist, "named after the fact".
- Texts in scope: `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, the cards and three docstrings.
- No test guards the wording; a one-time inventory check stands in.

## Impacts

Readers of the rules and cards now see the CLI's forge calls named.

## Test plan

`just check` (passes), `just eval-dry-run`, and the pipeline's `just scenario (ubuntu-latest)` at the head.

## Internal references

CR-453 `agents-md-names-cli-forge-reads`, batch-30. CR-429, CR-443 and CR-449 touch neighbouring `AGENTS.md` text.

</details>
