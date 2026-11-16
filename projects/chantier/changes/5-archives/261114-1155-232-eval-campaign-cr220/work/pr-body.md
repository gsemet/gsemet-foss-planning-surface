## Summary

The eval kit's setup script did not know the `ticket-summary` campaign (a ticket's summary, plan and demo posted on the user's yes), so its first real run would have been staged by hand. This teaches `evals/kit/setup.py` the campaign, so it is staged like the other sandbox campaigns and two runs start from the same frozen issue and request.

## Deliverables

`uv run --no-project python evals/kit/setup.py ticket-summary <workspace>` now does the usual preparation (base check, run number and prefix, clone, `init`, `uv sync --locked`, run record, Claude settings), places no frozen CR, and prints:

```text
issue     gh issue create --repo gsemet/chantier-eval-sandbox --title "<prefix> Dark theme for the reading list" --body-file <kit>/ticket-summary/issue.md   (run it, then note its number)
chat      <kit>/ticket-summary/chat-request.md   (the ticket-less request, typed in the chat)
```

- Setup creates nothing on the forge: the operator runs the printed line (it stays read-only, as the README says).
- The workspace allows only `gh issue comment *` and `gh issue artifact create *` (Bash and PowerShell forms), and no merge rule, since the campaign merges nothing.
- New frozen texts in `evals/kit/ticket-summary/`: a visible change (dark theme) for the ticket, a non-visible one (`--verbose`) for the ticket-less request.
- New dry-run case `ticket-summary-setup`.

## Blast radius

Grade: **1**. Eval kit, its docs and one structure test only; a plain `git revert` restores the previous behaviour. The other campaigns' rules and output are unchanged.

## Autonomous decisions

- The "CRs placed" line is left out when the list is empty, rather than printing `(0)`.

## Known gaps

- `evals/kit/dry_run.py` is about 909 lines (866 before), above the 400-line target; the new case adds 43 and the file was already over.
- The campaign has not been run for real yet; its first real run comes after the merge, by the operator.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/setup.py`: the `ticket-summary` entry of `CAMPAIGNS` (with `issue`, no batch), the run record's `issue` key, `issue_lines()`, `allow_rules` for a campaign with `issue`, the docstring.
- `evals/kit/dry_run.py`: case `ticket-summary-setup` (exit 0, no CR placed, run record, issue and chat lines, no merge or batch line, exactly four allow rules, no forge write).
- `skills/chantier/scripts/cli/tests/test_cli_units.py`: the sandbox campaigns are the previous four plus `ticket-summary`; it places no CR and its files exist.
- `evals/ticket-summary/RUNBOOK.md` setup steps; `evals/README.md` (five sandbox campaigns, kit table rows).

## Impacts

No visual change; eval kit and docs only.

## Test plan

- [x] New or changed tests (they fail on the previous code): the updated campaigns test and the new dry-run case
- [x] Local gates at the pre-restack head: `just check` (Windows), `just eval-dry-run` (8 of 8 cases), `mypy --strict` for linux, darwin and win32
- [x] Evidence: no before/after (no visible change); the `--keep` output, run record and settings are kept
- [x] Review: approved at the pre-restack head
- [ ] Verified at `acd7b40` (restack onto main; pending)
- [ ] CI green at `acd7b40` (restack onto main; pending)

## Internal references

CR-232 eval-campaign-cr220; follow-up named in CR-220's PR (Known gaps); no long gate (`just scenario`) was required since the CLI, cards and scenario do not change.

</details>
