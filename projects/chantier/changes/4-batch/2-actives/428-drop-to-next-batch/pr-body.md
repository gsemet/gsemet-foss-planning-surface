## Summary

Taking a change request out of a batch could only send it to the trash, the inbox or a backlog row, and a change that was already planned had no way to wait for the next batch. This PR adds `ready` (the folder `3-ready/`, the next batch) as a destination of `order drop`, and removes the inbox from it: a change that was planned has no reason to go back to the inbox, whether or not a Driver took it.

## Deliverables

Destinations of `order drop <cr> --note ...`:

| Destination | Before | After |
| --- | --- | --- |
| `trash` | yes (PR closed) | yes (PR closed) |
| `P1`..`P4` | yes | yes (PR turned to a draft) |
| `ready` | no | yes: `3-ready/<number>-<slug>/`, next batch (PR turned to a draft) |
| `inbox` | yes | refused: `order drop never sends a CR to the inbox: P1..P4, ready (the next batch) or trash` |

- The folder moves whole with its work, `formerly.json` and open waits, and keeps its number; `open` or `order add --note 3-ready/<number>-<slug>` brings it back.
- Outside a stack, a PR that is out of draft gets an order line ending `; turn its PR to draft <link>` (also on `cancel`'s line for a live change); `formerly.json` then records `"pr_draft": null` so a returning change does not hold a stale state.

## Blast radius

Grade: 2. The order command, its move helper, the cards and the docs change together; a revert restores the earlier destinations, and dropped folders already in `3-ready/` stay valid.

## Autonomous decisions

- No investigation: the specification names every file and edit.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `commands/orders.py`, `declare/orders.py`: destination table and help with `ready`, inbox refusal before anything is written.
- `lifecycle/moveout.py`: `ready` target; `close_pr_clause` becomes `pr_clause` (close for trash, draft for other destinations); `pr_draft` reset in `formerly.json`.
- `commands/orders_drop.py`, `commands/release.py`: use `pr_clause`; `cancel`'s refusal names `ready`.
- Cards (`chief-of-staff.md`, `foreman.md`, `driver.md`, `concepts.md`), docstrings, docs and their SVGs, scorecard row C16, scenario and its README.
- Tests: `test_order_drop_to.py`, `test_came_back.py`, card-content check.

## Impacts

No visual change. Users who drop a change choose among trash, `ready` and `P1`..`P4`.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_order_drop_to.py`, `test_came_back.py`, card-content check
- [x] Local gates at `d91edcf`: `just check` (1557 passed), `just scenario` pass; `just eval-dry-run` pass in CI at `d91edcf`
- [x] Evidence: no visual change; the tests run the real commands on prepared states, after at `d91edcf`
- [x] Review: approved at `d91edcf`
- [x] Verified at `d91edcf`
- [x] CI green at `d91edcf`

## Internal references

- CR-428 drop-to-next-batch

</details>
