## Summary

A session whose chantier CLI cannot run used to carry on "without it": a session was seen saying the CLI would not start and proceeding anyway. The stop rule covered only the dev mode's `uv sync`. This PR makes one rule in the startup core that every role reads at boot: if the CLI cannot run, in either mode and at any call, the session reports the exact error and stops.

## Deliverables

The rule, in `skills/chantier/references/startup-core.md`:

| Case | Handling |
| --- | --- |
| Launch fails (uv or uvx cannot set up or start the CLI, or it crashes on start), dev or plugin mode, at start or any later call | Report the exact error and stop: no work as the role, no seat, nothing written in the planning folder, never "without it" |
| Transient network error | One plain retry of the same command, then stop |
| CLI refusal, a command's own error exit, a host's permission denial | Existing handling, unchanged |
| Who tells whom | A steering session tells the user; a started agent ends its turn with the error as plain text |

Choices: the CLI is explicitly never a tool a role "works without" (a short clause added to every such line in the cards); no upgrade, reinstall, repair or substitute launch; the startup byte budget rose from 12288 to 12544 (the allowed maximum) because every role now reads a longer core. The chief-of-staff role on Copilot sits exactly at the new cap.

| Role (reload bytes) | Before | After |
| --- | --- | --- |
| chief-of-staff, claude / copilot | 12276 / 12282 | 12538 / 12544 |
| router, claude / copilot | 12243 / 12249 | 12496 / 12502 |
| griller, claude / copilot | 11733 / 11739 | 12219 / 12225 |
| status, claude / copilot | 11828 / 11834 | 12314 / 12320 |

## Blast radius

Grade: **1**. Cards, one manifest figure and tests only; no CLI code. A plain `git revert` restores the previous text.

## Autonomous decisions

- The new test is in its own file, `test_cli_stop.py`, because adding it to `test_plugin_files.py` would pass the 400-line cap that another test enforces.
- Wording trims in the four `SKILL.md` files (repeated or restated phrases only, no rule dropped) to make room. In all four: "the plugin's own folder" after `uvx --from`, "is the folder two levels above the common skill" before the plugin root's formula. Router: "the plugin ships the agents;", the line "Follow the manifest's action readings and session-start's deferred seat rules." (the manifest and the session-start card already hold both), ", typically after a compaction" and its parenthetical in the description, "by the host's means", "in one question". Chief of Staff: "With no argument your batches follow the surface (see the description).", "; a first word `foreman` or `direct` forces one" in the description (the body keeps the rule), "(or, in direct mode, steers the batch itself)", "Talks with the user,", "short-lived".

## Known gaps

- The sentence "The plugin root (`<plugin root>` = ...)" in the four `SKILL.md` files reads as a fragment after the trim; the chief-of-staff role on Copilot has no byte left under the cap to add a verb.
- The cards' text is proved by the new test; no model-driven run exercises a session that stops (the scenario runs the CLI with no model).

<details>
<summary>Details</summary>

## Changes

- `startup-core.md`: one paragraph replaces the old preparation paragraph.
- The four `SKILL.md` files: any failure of the sync or of the CLI, in either mode, at any call, follows the startup core.
- Clause "(never `$CHANTIER`: a CLI that cannot run is a stop, `startup-core.md`)" added to the "work without it" lines of `concepts.md`, `chief-of-staff.md`, `driver.md` and the eight worker cards.
- Startup limit 12288 to 12544 in `startup-manifest.json`, `test_startup_manifest.py`, `test_plugin_files.py`.
- New `test_cli_stop.py`: 16 parametrized cases reading the shipped files.

## Impacts

No visual change. Every role's boot reading grows by a few hundred bytes.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: none, text-only change
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-363 cli-unavailable-stops-session

</details>
