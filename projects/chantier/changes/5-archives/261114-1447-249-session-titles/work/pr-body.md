## Summary

A phone shows about 25 characters of a session title. The old titles (`[env] Project [role]`) spent those characters on the role and hid whether the user talks to the session. The cards and docs now tell a session to name itself with the machine's short code first, an icon (💬 a session you talk to, ⚙️ the Foreman), the project, the batch number when there is one, and the role, so the first 25 characters tell who you talk to, then the project and the role.

## Deliverables

The forms, before and after (the machine code is the first six letters of the machine's name, `Remote` in a cloud session):

| Session | Before | After |
| --- | --- | --- |
| Chief of Staff | `[env] Project [Chief of Staff]` | `[Battle] 💬 Chantier · CoS` |
| Chief of Staff steering a direct batch | `[env] Project [Chief of Staff - Batch 17 - Direct]` | `[Battle] 💬 Chantier 17 · CoS` |
| Griller | `[env] Project [Griller]` | `[Battle] 💬 Chantier · Griller` |
| Griller, subject known | `[env] Project [Griller] <subject>` | `[Battle] 💬 Chantier · Griller · landing page` |
| Foreman | `[env] Project [Foreman - Batch 17]` | `[Battle] ⚙️ Chantier 17 · Foreman` |

Choices: the icon separates a session you talk to from one you do not; the batch number is on two digits and only for a session that steers a batch; every form shows the machine, the icon and the project within its first 25 characters. Only the text the cards and docs give changes: no renaming of running sessions, no CLI change.

## Blast radius

Grade: **1**. Cards, docs and two test fixtures change; a plain `git revert` restores the old titles.

## Autonomous decisions

None.

## Known gaps

- Sessions already running keep their old title until their next role change; nothing renames them earlier (by design, no migration).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/session-start.md`, section "Titles": the parts (icon, project, batch number, role, machine code, separator), the table of forms, the examples and the reason for the 25-character budget.
- `skills/chantier/references/chief-of-staff.md`: the Foreman's title in its prompt, and the direct-mode Chief of Staff's title at `open --direct` and after `close --yes`.
- `skills/chantier/references/concepts.md`, `docs/use-cases.md`, `evals/real-direct/RUNBOOK.md`: the new forms.
- Fixtures: the seat test in `skills/chantier/scripts/cli/tests/test_cli_runs.py` and `scenario/run_scenario.py` use a title with the icon and `·`, so the round trip of a non-ASCII title through `seat take --title` is checked on every platform.

## Human decisions

- The title starts with the machine's code in brackets, then the icon, the project and the role, so a phone shows the machine, who you talk to and the project first.
- The icon: 💬 for a session the user talks to (Chief of Staff, Griller), ⚙️ for one they do not (Foreman).
- The machine code is the machine's name when it has 6 letters or fewer, else its first 6 letters, first letter uppercase; `Remote` in a cloud session.
- The batch number is on two digits and appears only for a session that steers a batch.
- On a phone the role of the direct Chief of Staff and the Foreman is cut; the user kept the forms as they are rather than moving the role before the project.

## Impacts

Session titles take the new form at the next role change of a session. No visual change in the board or the pane (they show no session title).

## Test plan

- [x] New or changed tests: the seat test takes a title with the icon and `·` and reads it back unchanged
- [x] Local gates (at the pre-restack head, carried): `just check` passed on the round's files (and in CI at `03edf3a`, on Linux, macOS and Windows)
- [x] Evidence: a search outside the planning folder finds none of the old forms, at `03edf3a`
- [x] Review: approved at the pre-restack head, carried to 03edf3a (diff unchanged)
- [ ] Verified at `03edf3a` (pending)
- [ ] CI green at `03edf3a` (pending)

## Internal references

CR-249 session-titles.

</details>
