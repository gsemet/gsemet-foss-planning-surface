# PowerShell quoting of `gh --jq`, and where `--epoch` goes

## The request

From the retro of batch-13 (2026-11-12), two slips of the steering session (the Chief of Staff
in direct mode, on Windows PowerShell 5.1):

- `gh ... --jq '<expression with spaces>'` broke several times: PowerShell 5.1 passes a native
  command's quoted argument with spaces so that `gh` received it split ("accepts 1 arg(s),
  received 3"). Printing `--json <fields>` plainly worked.
- `order add --epoch 1` was refused by the CLI: only `order merged` and `order add --fix-for`
  take `--epoch`. The card's list in "Steering a batch yourself", "Your epoch" (`take`, `agents
  set`, `order done`, `order merged`, `cancel`, `pause`) is right, but it reads as examples.

## What changes

- The Claude Code host reference (`skills/chantier/references/hosts/claude-code.md`), in its
  Configuration part (rule 9's host side), gets one line: on Windows PowerShell 5.1, a `gh` or
  `glab` argument with spaces (a `--jq` or `--template` expression) may reach the program split;
  print `--json <fields>` and read it, or use an expression with no space.
- `chief-of-staff.md`, "Your epoch", and `foreman.md`'s matching line say the list is complete:
  exactly those commands carry `--epoch` (with `order add --fix-for` and `status --refresh` on a
  wake), no other.

## Out of scope

- A CLI change to accept `--epoch` everywhere (no new behaviour from one slip).
- The Copilot reference (its host shell is not concerned; checked by the spec-writer).
