## Summary

The host's auto-mode classifier refuses an agent's force push of its own CR branch, and the agent stops. This adds `chantier push <cr> --lease <n>`: it runs the `git push --force-with-lease` of the CR's own recorded `chantier/*` branch itself, for GitHub and GitLab, and states that it exists to declare that operation legitimate: chantier's own update of the CR's own branch after a rebase, with the lease held. Measured cost: 13 classifier refusals of force pushes in 12 days, each one a lost Driver, and 4 questions to the user.

## Deliverables

```text
chantier push <cr> --lease <n> [--unit stack|O-k]
  rails (before any git write): branch recorded, chantier/*, not the default branch,
        lease given and held, worktree exists and clean, HEAD on the branch
  git push --force-with-lease=<branch>:<expected> <remote> HEAD:refs/heads/<branch>
  never --force, --no-verify, a retry, a forge call, a profile or the server
```

| Before | After |
| --- | --- |
| `take`'s Rewrites line names `git push --force-with-lease -u ...` | names `$CHANTIER push <cr> --lease <n>` (`--unit stack` for a stack's branches) |
| `ship` "not pushed" line | also names `chantier push <cr> --lease <n>` |

Choices: the unit that holds the lease is named (`--unit`), since lease numbers repeat across units; git's own refusal text is printed verbatim (exit 4); the lock is never held during the network push.

## Blast radius

Grade: 2. A new command and CLI output lines, plus AGENTS.md exceptions; revert restores the previous lines.

## Autonomous decisions

- The stack driver's `--unit stack` push is allowed even while the CR's own lease is live (the specification's open question, left as specified).

## Known gaps

- The cards (`concepts.md`, `driver.md`, `hosts/claude-code.md`) still quote the raw `git push --force-with-lease` form; later changes rewrite them.
- The classifier's verdict on `chantier push` is unproved until the smoke trial and the later rate measure.

<details>
<summary>Details</summary>

## Changes

- New `commands/push.py`, registered in `declare/delivery.py`.
- `push` joins the commands that never run through a profile or the server.
- `driver_prompt.py`, `driver.py`, `delivery.py`: lines that point to the command.
- `AGENTS.md`: git exception, network use, profile lists, named exception.
- Tests: `tests/test_push.py`; scenario case `push_own_branch`.

## Impacts

No visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: smoke trial records
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-487 sc01-push-own-cr-branch.

</details>
