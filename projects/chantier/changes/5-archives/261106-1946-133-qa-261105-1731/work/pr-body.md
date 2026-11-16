CR-133. A QA run on 0.4.1 left nine findings on what misleads a new user of the CLI. Each was replayed on 0.6.0 in a throwaway repository, then fixed where it still held.

## Findings

| Finding | On 0.6.0 | Now |
| --- | --- | --- |
| `file` of an existing slug exits 3 | held | exit 2, the message names `--slug` |
| `triage` cannot move a backlog item, and its error misleads | held | it moves it; the same priority or a taken name exits 2; any other path says it expects `1-inbox/<item>` or `2-backlog/P<n>/<item>` |
| A second `order drop` reports a new drop; `order drop 101` is refused | held | exit 2 "already dropped", no order recorded; `order` takes `101` as `CR-101` (the CR, `--fix-for`, the ids of `order after --note`) |
| `order note` is accepted on a cancelled CR | held | exit 2 |
| `order rounds` and `order budget` errors are vague | held | full usage, and why the value is refused |
| Orders the CLI applied look like orders nothing touched | held | `status` lists them on their own line; `land`'s refusal says each ends with `order done <O-k>` |
| The refusal of a QA folder gives no hint | held | it says a QA report is an item to triage and split, not to open |
| `open`'s output is cryptic | held | each CR line shows its move, and a `next:` line comes before the list, so it survives the ten-line cut |
| `cost`, `close` and the path through them are undocumented; dropped CRs show as `cancelled` | held | `docs/use-cases.md` says what they answer, that a dropped CR shows as `cancelled`, and that `land` and `close` need a Foreman |
| `close` says `landed: none` with no pointer to `land` | no longer holds | `close` on a batch not landed exits 2 with `something still runs: ... order O-1 (drop) is open` |

`close` keeps refusing when it cannot price the batch (CR-130), and `rails.py` does not change.

## Decisions the specification left open

- An order counts as applied unless it is a `note`, a `qa` or a drop of a live CR: for those, the Foreman has everything left to do. Orders recorded before this change count as not applied. `orders_pending` in `STATUS.md` and `STATUS.json` still counts both, since `land` and `close` refuse on both.
- A `qa-` folder gets the new refusal only when it has no Change Specification; one with a specification opens as before.
- `order rounds` on a cancelled CR stays accepted: the specification names only `note`.
- `order qa` twice in the same minute also exits 2 now (it shares `file`'s code), and its message names no `--slug`, which it does not have.
- `open`'s `brief:` line is folded into `next:`.

## Checks

`just check` passes (28 tests) and `just scenario` passes on both forges at this head. The scenario gains checks for each CLI change above.

`order add` and `order drop` needing `--batch` with several open batches is not a finding any more: `resolve_batch` answers `several open batches (...): pass --batch`, and a repository has one open batch at a time.

## Evidence

Run at 3a69ea3 against the base 0cbdd58, the same steps in a throwaway repository with a bare origin, on Windows; Linux and macOS are CI's.

| Pair | Before (before.txt) | After (after.txt) |
| --- | --- | --- |
| file twice | exit 3, no `--slug` | exit 2, names `--slug <other>` |
| triage backlog -> P3 | exit 1 "not directly inside 1-inbox" | moved, exit 0; same priority: exit 2 "already P3" |
| triage README.md / dir | "not directly inside 1-inbox" | "triage expects a CR folder: 1-inbox/<item> or 2-backlog/P<n>/<item>", exit 1 |
| order drop twice | second: new order O-2, exit 0 | exit 2 "already dropped", orders unchanged (one O-1) |
| order drop 101 | exit 1 unknown CR | accepted (reaches "already dropped"); 101x still exit 1 |
| cancel then order drop | order O-3 recorded, exit 0 | exit 2 "already dropped" |
| order note on cancelled | recorded, exit 0 | exit 2 "cannot note CR-102: it is cancelled" |
| order rounds / budget | bare usage | usage plus why ('0' is not a whole number...; '-5' is not a positive amount...; "no value given") |
| status / land, applied + pending | one "orders pending" line of 8; land lists a Python list | two lines (pending: O-3 qa; applied: O-1, O-2); land says the Foreman ends each with `order done <O-k>` |
| open 2 CRs | titles then `brief:` | `next:` line, then `CR-n title: src -> dest` per CR |
| open QA folder | "missing Change Specification ... grill the CR first" | "is a QA report: an item to triage and split into CRs, not to open", exit 2 |
| open 8 CRs | 10 lines | 10 lines: opened, next, 8 CRs; none cut |
| unchanged | close/close --yes exit 2 nothing deleted; cost exit 2; order qa then status pending qa; order rounds on cancelled exit 0 | same |

The full transcripts are text, which `gh pr edit --attach` does not upload: they stay in the CR's `work/verifier/evidence/` (`before.txt`, `after.txt`, `docs-after.txt`, `replay.ps1`, `docs.ps1`).
