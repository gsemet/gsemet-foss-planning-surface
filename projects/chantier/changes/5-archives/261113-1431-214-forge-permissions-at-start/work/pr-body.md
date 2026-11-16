## Summary

An unattended batch used to stop in the middle of the night when the host refused a force push or a PR edit, and the preflight's allow-rules warning ("19 of 19 not found") was always on, so nobody heard it. The preflight now judges the allow rules by the commands they let through, not by their text, and the Chief of Staff checks at its first turn, and again when a batch starts, that the forge will accept what the batch needs (push rights, branch rules on `chantier/` branches, release publication). A missing right only warns; it never blocks.

## Deliverables

- P10 holds sample commands (the exact forms the cards make agents write) and asks whether an allow rule matches each one with Claude Code's documented matching. A user's narrower or differently written rule counts.

```text
before: P10 warn 19 of 19 recommended allow rules not found as written
after:  P10 warn <k> of <n> commands chantier's agents run are not allowed by your settings: <sample> (add <rule>); ...
```

- New "Forge permissions (P9)" check in the Chief of Staff card: GitHub (token scopes, viewer permission, branch rules for `chantier/` branches), GitLab (marked unproved), and what the user is told.
- New general rule for every host: a CR's branches must be force-pushable at all times, one command per branch, never a loop or script.
- Release publication: allowed by a named rule (the Release driver runs it) or announced at the start as the user's step.
- Recommended allow rules are narrowed to `chantier/` branches and extended with `gh pr edit/ready/view`, `gh stack`, `gh release create` and the GitLab equivalents.

## Blast radius

Grade: 2. The CLI preflight output changes and several shared cards are edited; the P10 check only warns. Revert restores the previous behaviour.

## Autonomous decisions

- The `gh stack` extension is detected by the presence of a `gh-stack` folder under gh's extensions directory, not by running `gh extension list`, because the CLI runs no forge command.
- Both forms of the rules endpoint (raw `/` and `%2F`) answered `[]` on this repository, which has no ruleset, so the trial cannot tell them apart; the card keeps the raw `/` form.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: sample table, `rule_matches()`, new P10 line; `RECOMMENDED_ALLOW` built from the samples.
- `test_structure.py` and the scenario: equivalence cases (user's own forms, `Bash(*)`, deny rule, full list, Copilot).
- Cards: chief-of-staff, concepts (rule 8), driver (stack push forms, release publication), session-start, init, hosts/claude-code, hosts/copilot; tutorial doc.

## Human decisions

- A missing forge right warns and never blocks a batch.
- On Claude Code the alert explains that auto mode's classifier refuses some force pushes, which come with every rebase.
- A CR's branches must be force-pushable at all times, on every host.
- The check names the release's publication: allowed by a named rule, or announced as the user's step.
- The allow-rules check judges equivalence by the commands a rule lets through, not by its text.

## Impacts

No visual change. Users see a more accurate P10 line and a forge-rights block in the first message.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_structure.py` P10 equivalence cases, at `ec84275`
- [x] Local gates at `ec84275`: `just check` pass (58 tests), `just scenario` pass (github 650/650, gitlab 638/638)
- [x] Evidence: P10 line with the real settings ("14 of 16", no longer "19 of 19") and the GitHub P9 outputs on this repository, at `ec84275`
- [x] Review: approved at `ec84275` (the round's pass recorded at `7705f00`, committed as `ec84275`)
- [x] Verified at `ec84275`
- [x] CI green at `ec84275`: `gh pr checks 159`, all five checks pass

## Internal references

CR-214 forge-permissions-at-start.

</details>

