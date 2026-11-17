## Summary

When the steering session built a Driver's prompt from memory, it once gave a release Driver a `writes:` line; the write guard then refused that Driver's own worktree writes and the CR had to be taken back. `take`, `take stack` and `order qa` now print the whole prompt skeleton of the Driver they start (first line, card, CLI line, facts, `Steering:`, `Team:`, `Needs:`, `Note:`), with a `writes:` line only for the roles that get one. The steering session copies it whole and fills in what is left.

## Deliverables

One table in `concepts.md`, "A Driver's prompt", says which template lines each Driver's prompt holds; the CLI reads it, and the cards point to it.

| Driver | Started after | `writes:` | `Team:` |
| --- | --- | --- | --- |
| `cr-driver` | `take <cr>` (change, fix) | CR folder, then the absolute archive path when `take` prints one | yes |
| `release-driver` | `take <cr>` (release) | none | none |
| `stack-driver` | `take stack` | none | yes |
| `qa-driver` | `order qa` | none | none |

```text
release-driver prompt (no writes: line: this Driver gets none; copy it whole, ...):
  chantier release-driver for CR-5 "<title>" of batch batch-23, in the project <root>.
  Read <skill>/references/startup-core.md, ...
  CLI ($CHANTIER): ...
  Steering: the Foreman <...>
  Note: <...>
```

Choices: a missing agent file or an unknown CR kind is a CLI error (exit 2) raised before anything is recorded; the archive path on `writes:` is absolute (worktree joined with the archive path); `order qa` joins the commands whose output is not cut at ten lines.

## Blast radius

Grade: 2

The Drivers' prompts now come from the CLI's output; a wrong skeleton would mis-start a Driver. Revert restores the hand-built prompts.

## Autonomous decisions

- A CR Driver's `Team:` is filled from the printed `team:` lines (prefix removed, joined with `; `), followed by a `<review steps>` placeholder, because the specification's two sections disagree.
- `default branch:` of the QA skeleton comes from the configuration, else git; with neither the command fails rather than assume `main`.

## Known gaps

- Worker opening lines appear twice in a CR Driver's block (the block copies all the facts lines).
- No real Driver was started from a printed skeleton on a real host.

<details>
<summary>Details</summary>

## Changes

- `concepts.md`: the "A Driver's prompt" table; `foreman.md`, `chief-of-staff.md`, `driver.md`, `hosts/claude-code.md` point to it.
- `driver_prompt.py` (new): reads the table, builds each block; `commands/driver.py` (`take`, `take stack`) and `commands/orders.py` (`order qa`) print it.
- Tests: `tests/test_driver_prompt.py`, `test_cli_runs.py`, `test_playbook_config.py`; scenario checks after each `take` and after `order qa`.

## Human decisions

- `take` prints the whole prompt skeleton for the CR's Driver: first line, card, and no `writes:` line for a release, stack or QA Driver.
- The archive on a CR Driver's `writes:` line is an absolute path (worktree joined with the archive path).
- The stack Driver's skeleton has its own shape: it carries the stack rows, and its `Team:` comes from the batch's playbook.
- `order qa` also prints the QA Driver's skeleton.

## Impacts

No visual change.

## Test plan

- [x] New or changed tests (structure test of the table on both hosts, CLI runs for the four skeletons, missing agent file refused with exit 2)
- [x] Local gates at `ffa427b`: `just check` pass (390 tests) (restacked; patch carried)
- [x] Evidence: the four printed blocks (change CR, release CR, `take stack`, `order qa`) read at `ffa427b`, kept as text in the CR's evidence folder (restacked; patch carried)
- [x] Review: approved at `42d9718`, carried from `42d9718` to `ffa427b` (rebase onto the new base, patch unchanged) (restacked; patch carried)
- [x] Verified at `ffa427b` (restacked; patch carried)
- [x] CI green at `ffa427b` (`gh pr checks 270`: five jobs pass, `just scenario (ubuntu-latest)` included) (restacked; patch carried)

## Internal references

CR-315 take-prompt-skeleton-per-role. Printed blocks: evidence/take-skeletons.txt.

</details>
