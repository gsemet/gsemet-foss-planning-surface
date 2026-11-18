## Summary

A Driver's lease-protected force push of its own `chantier/` branch was refused by Claude Code's auto-mode classifier even though the user's allow rule matched the command. This PR records that proof in the host's reference, states that a Driver pushes only its own CR's branch, and says that a legitimate refused push is never a question for the user. Behaviour and the CLI do not change.

## Deliverables

The refusal on record, and the matcher check showing the allow rule covers that exact command:

```text
refused: git -C C:\Users\gaeta\Projets\chantier.worktrees\batch-23-CR-318 push
--force-with-lease -u origin chantier/batch-23/cr-318-cr -> Permission for this action was
denied by the Claude Code auto mode classifier. Reason: [Destructive or Unwanted Actions].
```

The refusal above is quoted verbatim, path included. The check, run on that command against both forms of the rule `git -C * push --force-with-lease -u origin chantier/*`:

```text
$ uv run --no-sync python -c "from chantier.commands.permissions import rule_matches as m; c=r'git -C C:\Users\gaeta\Projets\chantier.worktrees\batch-23-CR-318 push --force-with-lease -u origin chantier/batch-23/cr-318-cr'; r='git -C * push --force-with-lease -u origin chantier/*'; print(m('PowerShell('+r+')','PowerShell',c), m('Bash('+r+')','Bash',c))"
True True
```

| Card | Change |
| --- | --- |
| `hosts/claude-code.md` | allow-rule rows, "Every batch" mark and "Auto mode": the refusal with the rule set is recorded, "unproved, not documented" |
| `driver.md` | Push bullet: `<branch>` is the Driver's own CR's branch |
| `chief-of-staff.md` | a legitimate refused push is never a question for the user; the "On the yes" note |

Choices: the `git -C` push stays (an in-worktree push would be a chain, forbidden and matching no rule); the refusal route stays as it is; no rule is added or widened.

## Blast radius

Grade: 1. Cards only; a `git revert` restores the previous text.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/hosts/claude-code.md`: own-branch sentence in the "Risk accepted" cells of the two `git push --force-with-lease` rows; the refusal in the "Mark" of the `git -C` row and of "Every batch"; the "Auto mode" bullets (first, labels, batch-15, trial and alert lines).
- `skills/chantier/references/driver.md`: Push bullet, own CR's branch only.
- `skills/chantier/references/chief-of-staff.md`: "On the yes" and "A refused force push", step 3.
- No change to the CLI, the permission rules, the tests or the agent files.

## Human decisions

- A Driver force-pushes only its own CR's branch; the rule's wildcard does not enforce it, the card does.
- The Driver keeps the `git -C` push: no in-worktree push and no trial of it, since that would be a chained command, which the cards forbid and no allow rule matches.
- A refused force push keeps its route, with no question to the user when the push is legitimate.
- The refusal with the rule set is recorded in the host's reference as unproved, not documented.

## Impacts

No visual change. A reader of the cards now knows the classifier can refuse a matching force push and what to do.

## Test plan

- [x] No behaviour change (cards only)
- [x] Local gates: `just check` passed (443 passed) before the commit; CI runs it at `carried from c103c07`
- [x] Evidence: none, text change
- [x] Review: approved at `carried from c103c07`
- [x] Verified at `carried from c103c07`
- [x] CI green at `carried from c103c07` (all five jobs, including the Linux scenario)

## Internal references

- CR-329 driver-force-push-own-branch (batch-24)

</details>
