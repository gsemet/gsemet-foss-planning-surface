## Summary

Two slips of a session steering a batch on Windows PowerShell 5.1 are fixed in the role cards. A `gh ... --jq '<expression with spaces>'` reached `gh` split ("accepts 1 arg(s), received 3"), and `order add --epoch 1` was refused because the cards listed the commands that carry `--epoch` as examples. The Windows host reference now warns about the first, and the cards give the exact, complete list for the second.

## Deliverables

The commands that carry `--epoch`, now said as a complete list in two cards and checked against what the CLI accepts:

| Command | `--epoch` |
| --- | --- |
| `foreman set`, `foreman transcript` | required / checked |
| `status --refresh` (a wake), `status --stop-heartbeat` | checked / required |
| `take`, `agents set`, `cancel`, `pause` | checked |
| `order done`, `order merged`, `order add --fix-for` | checked |
| any other command or `order` kind | refused (exit 2) |

New host note (Claude Code reference, "Windows PowerShell 5.1"): print `--json <fields>` alone, or write a `gh`/`glab` expression with no space and no double quote.

## Blast radius

Grade: 1. Card text only, the CLI is unchanged; a plain `git revert` restores the previous text.

## Autonomous decisions

- The list includes `foreman set`, `foreman transcript` and `status --stop-heartbeat`, which the CLI accepts and the steering session runs; `foreman get` and plain `status` are left out because the CLI ignores `--epoch` there.
- The PowerShell note names spaces or double quotes, since the legacy argument passing mangles both.
- The Copilot reference is unchanged: the slip was seen on Claude Code's PowerShell tool only.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/hosts/claude-code.md`: new "Windows PowerShell 5.1" subsection in Configuration.
- `skills/chantier/references/chief-of-staff.md`: the "Your epoch" bullet lists the exact commands, says "no other", and says a refusal is exit 2.
- `skills/chantier/references/foreman.md`: the epoch line of the start section carries the same list.

## Human decisions

- The CLI stays as it is; only the cards change.

## Impacts

No visual change. A steering session reads a refused `--epoch` as its own slip (exit 2), not a stale epoch (exit 3).

## Test plan

- [x] New or changed tests: No behaviour change (card text).
- [x] Local gates at `76b0c87`: `just check` (48 passed), `just scenario` (github 586/586, gitlab 586/586)
- [x] Evidence: `--help` shows `--epoch` for `order`, `foreman`, `status`, `agents`, `take`, `cancel`, `pause` and for none of the other commands.
- [x] Review: approved at `76b0c87`
- [x] Verified at `76b0c87`
- [x] CI green at `76b0c87` (3 `just check` jobs and `just scenario`)

## Internal references

CR-194 powershell-gh-jq-and-epoch-flags
</details>
