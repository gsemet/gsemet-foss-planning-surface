## Summary

A change request that cannot go on had only free text to say why. It now records what it waits for as a typed fact: a person's answer, a review request's approval, a green pipeline on a head, or a review request merged. Backlog items can wait too (the user's answer between two grills). When the forge shows an approval, a pipeline or a merge wait met, the forge hub tells the steering session, which clears the wait and takes the item back. The word is "wait"; "gate" stays for the fast and long gates.

## Deliverables

Commands and the data they keep:

```text
handback <cr> blocked --wait <type>[=<ref>] <reason>     # repeatable
wait <cr> add <type> [--ref <ref>] [--link <link>] --note "<text>"
wait <cr> clear <id> [--epoch <n>]
wait [<cr>]                                              # read-only
```

| Where | What |
| --- | --- |
| a batch's CR | `CrEntry.waits` in `batch.json` |
| a backlog CR | `waits.json` in its folder, moved with it, carried into the batch at `open` or `order add` |
| the journal | `wait-cleared@1`, written by the hub, wakes a watcher |

```mermaid
flowchart LR
  A[wait add / handback --wait] --> B[batch.json waits]
  B --> C[hub waits provider]
  C -->|same connectors.read| D[forge]
  C -->|met| E[wait-cleared@1 in the journal]
  E --> F[watcher wakes the steering session]
  F --> G[wait clear, then take]
```

Choices: the hub only signals, it never clears; a wait changes no rule of `take`, `close`, `open` or the slots; the waits add no forge query (same read per project and cycle); a wait the forge can no longer see met (no review decision, a head that moved, a closed PR) says "the forge cannot tell: cleared by hand"; a link in another repository is recorded and not read.

## Blast radius

Grade: 2. New record field with a default (older records read as no waits), a new file, a new journal type and a new hub provider; shared status, handoff and board code changed. Revert is possible; a `waits.json` left in a backlog CR is ignored by an older version.

## Autonomous decisions

- On a return to a held entry the record's list wins and the file adds only the ids it lacks, so numbering never restarts.
- With no recorded open PR, the hub compares wait links to the first wait link's repository.
- The wait line shows wherever the CR facts print (handoff, take, round), not only in handoff.
- AGENTS.md carries no count of its exceptions ("named exceptions", the list says which), per the Chief of Staff's decision of 2026-11-20, replacing the specification's recount of 8.1: CR-404, CR-409 and CR-410 no longer conflict on a number.

## Known gaps

- GitLab approval read not proved: no GitLab Free and Premium account. A GitLab approval wait stays "cleared by hand until proved"; GitLab pipeline and merge waits are read as on GitHub. A follow-up item for the proof and the read is needed.
- The GitLab fakes (`scenario/fake_glab.py`, `tests/forge_world.py`) have no approval answer, since that half is not shipped.
- `just test` at the head, measured: 58 to 68 s for 1199 tests (`pytest -n auto`, Windows), against AGENTS.md's ceiling of 48.5 s (18.5 s + 30 s) from 2026-11-14; main's own total today was not re-measured, so the growth is not isolated. This CR's 37 new tests (`test_waits.py`, `test_board_waits.py`, `test_forge_hub_waits.py`) take 13.3 s serial together (none above 0.6 s: the slowest are `test_waits.py`'s record round-trips and `test_forge_hub_waits.py`'s hub cycle), so about 3 s spread over the workers; the rest of the growth is not from this CR (slowest tests: `test_carry_ship.py`, `test_release_tag.py`, 2 to 5 s each). The Chief of Staff judges it at the ready; it is tracked in the inbox item `test-time-over-budget`.
- GitLab approval half: inbox item `gitlab-approval-proof` names CR-409.
- Scenario: the `gitlab` unit gained `typed_waits` (40/40, 60.3 s loaded, 61.5 s alone); its budget went from 95 s to 75 s in `UNITS` and the README table (measured + 25%); the README's measured columns (92.0, 67.5) still show the older runs. In the full run, `direct` (143.7 s > 135) and `qa-driver` (136.3 s > 115) warned over budget; not touched.
- No part of the CR board pane changed, so no screenshot is owed.

<details>
<summary>Details</summary>

## Changes

- `core/records.py`, `commands/waits.py`, `commands/wait_view.py`, `declare/driver.py`, `commands/driver.py`: the records, the `wait` command, `handback --wait`.
- `commands/joining.py`, `lifecycle/moveout.py`: waits carried in at join and written out at drop.
- `commands/batch_status.py`, `commands/facts.py`: `| waits:` and the wait line.
- `hub/waits.py`, `hub/interests.py`, `hub/cycle.py`, `hub/schemas.py`: the provider, `waits_unseen`, the journal type.
- `board/crs.py`, `board/backlog.py`, Kanban and backlog cards, English and French words, `validate`.
- AGENTS.md, the driver, foreman, chief-of-staff and concepts cards, and the docs the change makes false.

## Human decisions

- Four wait types, including `merge`; a backlog item may carry a wait.
- The hub reads no forge for a backlog item's waits: they are cleared by hand.
- The free-text blocked reasons stay; typed waits are added beside them.
- GitLab approval ships only when read on a real merge request.

## Impacts

Developers and the steering session see `| waits: ...` in `status` and the wait line in `handoff`; a blocked Kanban card shows its waits. No pane change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `tests/test_waits.py`, `test_validate`, `test_forge_hub`, `test_store_command_table`
- [ ] Local gates at `3246872`: `just check`, `just eval-dry-run`, scenario units surface-board and gitlab (before the rebase; the long gate runs at the head)
- [ ] Evidence: after at `3246872`: tests and scenario output (no visual change)
- [ ] Review: approved at `3246872` (whole branch, rebase resolutions in `work/conflicts.md`)
- [ ] Verified at `3246872`
- [ ] CI green at `3246872`

## Internal references

CR-409 typed-waits, batch-29. Based on main (CR-405 merged).

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
