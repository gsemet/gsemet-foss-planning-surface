## Summary

chantier can deliver a stack in several kinds of runs (a native stack, a release run on the user's grant, fixes merged on a grant), but its permission check looked at one fixed set of allow rules. A missing rule only showed up as a refused command at night, with nobody there to answer the host's prompt. Now each capability has its own known commands and rules, the preflight checks the capabilities the batch will use, and a missing rule is a strong warning that explains why the capability may stop.

## Deliverables

One table of capabilities (`hosts/claude-code.md`, "Capabilities and their commands") that the CLI's sample rows follow in order:

| Capability | Used when | Rules offered |
| --- | --- | --- |
| Every batch | always | the base set (unchanged, equals the recommended JSON block) |
| A stack | `--mode stack` | `gh stack*` when the extension is installed |
| A release on its own | `--autonomous-releases N` | merge, tag push, `gh release create*` (never in the base set) |
| Fixes on a grant | `--grant-fixes` | merge |

`preflight` takes `--mode`, `--autonomous-releases` and `--grant-fixes` and prints one `P10` line per checked capability, still warn-only (exit 0):

```text
P10 ok   every batch: the commands its agents run are allowed by your settings
P10 warn a release on its own: 3 of 3 commands ... are not allowed (gh pr merge*, git push origin v*, gh release create*): ... ; the host's auto-mode
         classifier judges each command at run time, and in a remote session (Remote Control) nobody
         may be there to answer its prompt: ...
```

Choices: the release and merge rules are offered only when the user grants them; trials are the Chief of Staff's own tool calls (a command run by the CLI is invisible to the host's check); forge probes (stacks API, default branch rules, merge methods) only warn; every refusal is recorded with its exact command and text for the next table.

Run at `2952a02` with HOME, USERPROFILE and CLAUDE_CONFIG_DIR on scratch folders: plain `preflight` prints one `P10 warn every batch: 14 of 14` line; `--mode stack` adds `P10 warn a stack: 1 of 1` (`gh stack view`); `--autonomous-releases 1 --grant-fixes` adds `P10 warn a release on its own: 3 of 3` and `P10 warn fixes on a grant: 1 of 1`. The force-push and tag-push dry-run trials and `gh pr view`, `gh stack view` went through the host; the stacks API answered 200, `rules/branches/main` returned `[]`, and the repository allows rebase merge only.

## Blast radius

Grade: **2**. The CLI change is confined to the P10 check (warn-only) but the cards of two hosts change. Roll back with a revert of the PR.

## Autonomous decisions

- The "not checked here" text is appended to the last P10 line instead of being a separate line, because the report is capped at 10 lines.
- The table's Rules column holds bare rules (`gh pr view*`), each written `Bash(<rule>)` or `PowerShell(<rule>)`, so a test can compare it with the CLI's samples.
- The SendMessage rule stays plain text in the table, and the test remote is switched to a GitHub URL for the release-warning assertions.
- The new subsection sits after "What not to add", because the JSON-block test reads the first JSON block after "Allow rules".

## Known gaps

- No local long gate ran on this PR: the user waived it for this batch (GitHub CI is the gate), so gaps a long gate would show are fixed in a later change.
- No run in a real session: the trials, the question for the release rules and the "Permission trials" record in `brief.md` are unproved until a Chief of Staff runs them at a go with a release grant.
- The GitLab probes and the Copilot trials are unproved.
- The project's own release commands (for chantier, `just tag`) are named, with no rule offered.

<details>
<summary>Details</summary>

## Changes

- `commands/permissions.py`: sample rows carry a capability; `GRANT_ALLOW` added; checks return gaps per capability.
- `commands/preflight.py`: the three options, one P10 line per capability, the strong warning text.
- `hosts/claude-code.md`, `hosts/copilot.md`, `chief-of-staff.md`, `foreman.md`, `session-start.md`, `init.md`, `driver.md`: the table, the question per capability, the trials, the probes, refusals noted and retro lines.
- `docs/tutorial-claude-code.md`, `scenario/README.md`, `scenario/run_scenario.py`, `tests/test_cli_runs.py`: wording and assertions.

## Human decisions

- A missing rule or a forge problem stays a warning, never a preflight failure.
- The release rules are offered only when the user grants a release to run on its own.
- Forge probes only warn.
- No local long gate for this batch: waived by the user.

## Impacts

Users see one P10 line per capability and a stronger warning; nothing else changes without a grant.

## Test plan

- [x] New or changed tests (assertions added to the JSON-block and P10 tests and to the scenario)
- [ ] Local gates: waived by the user for this batch (no local long gate)
- [x] Evidence: `preflight` outputs, trials and forge probes above, run at `2952a02`
- [x] Review: inspector approved at `3a96b35`, carried from `3a96b35` over a clean rebase onto main (`2952a02`)
- [x] Verified at `2952a02`: all spec sections hold; `just check` passes
- [x] CI green at `2952a02`: `gh pr checks 186` lists just check (macos, ubuntu, windows), just eval-dry-run and just scenario, all pass

## Internal references

CR-240 permissions-per-capability. Round report: work/r1.md in the CR folder.

</details>
