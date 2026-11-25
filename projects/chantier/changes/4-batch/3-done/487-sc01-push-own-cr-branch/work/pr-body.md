## Summary

The host's auto-mode classifier refuses an agent's force push of its own change-request (CR) branch, and the agent stops. This adds `chantier push <cr> --lease <n>`: it runs the `git push --force-with-lease` of the CR's own recorded `chantier/*` branch itself, for GitHub and GitLab, and states that it exists to declare that operation legitimate: chantier's own update of the CR's own branch after a rebase, with the lease held. Measured cost (the owner's count from past session logs, not reproduced in this PR): 13 classifier refusals of force pushes in 12 days, each one a stopped agent, and 4 questions to the user.

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

Owner's word for this subcommand: "a CLI subcommand ... that runs the `--force-with-lease` itself, for GitHub and for GitLab. ... say plainly that the command exists to declare that the operation is legitimate in what the Driver is doing".

Test time added to `just test`: `test_push.py` (13 tests) took 10.49 s wall under `pytest -n auto --dist worksteal` (8 workers, run at `096f073` on this Windows machine: `13 passed in 10.49s`); an earlier run of the file alone in one process took about 57 s. A full before/after of `just test` was not taken, so the 30 s budget is **UNVERIFIED** for the whole suite.

Smoke trial (the host did not show its permission mode), five pushes of this branch at 096f073, all in the compound form `uv run --no-sync --project <worktree> chantier --project <planning> push <cr> --lease 1 --batch <batch>`; none was refused by the classifier:

| Try | Outcome |
| --- | --- |
| 1 | ran; a real rebase push, the pre-rebase head to `096f073` |
| 2 to 5 | ran; no-op, "was 096f073" |

Choices: the unit that holds the lease is named (`--unit`), since lease numbers repeat across units; git's own refusal text is printed verbatim (exit 4); the lock is never held during the network push.

## Blast radius

Grade: 2. A new command and CLI output lines, plus AGENTS.md exceptions; revert restores the previous lines.

## Autonomous decisions

- A stack's `--unit stack` push is allowed even while the CR's own lease is live: the question was open and is left permissive.

## Known gaps

- The smoke trial did not show its permission mode (the host does not print it to the agent), so "auto mode" is not confirmed by the trial itself.
- The local Windows scenario gate (`chantier gate <cr> scenario`) passed at `096f073` (carried from `b9e02b6`); it is owed again only by the change that ends up the stack's top, at its own head.
- The whole-suite seconds added to `just test` are not measured (see Deliverables).
- The cards (`concepts.md`, `driver.md`, `hosts/claude-code.md`) still quote the raw `git push --force-with-lease` form; later changes rewrite them.
- The classifier's verdict on `chantier push` is unproved: five pushes passed unrefused, and the later rate measure decides.

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

- [x] New or changed tests (they fail on the previous code): `tests/test_push.py`, scenario case `push_own_branch`
- [x] Local gates at `096f073` (carried from `b9e02b6`, clean rebase): `just check` 2645 passed, `just eval-dry-run` 19 of 19, local scenario gate passed
- [x] Evidence: smoke trial records (Deliverables), at `096f073`
- [x] Review: approved at `096f073` (carried from `9f33092`)
- [x] Verified at `096f073`
- [x] CI green at `096f073`: `just check` on ubuntu, macos and windows, `just eval-dry-run`, `just scenario` (ubuntu)

## Internal references

CR-487 sc01-push-own-cr-branch.

</details>
