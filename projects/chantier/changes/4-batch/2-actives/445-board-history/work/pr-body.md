## Summary

The web board has no place to see what was done over time: a reader had to open each batch and each archived change request (CR) to learn what shipped last week. This adds a read-only History page: pick a day, a week or a month, move with previous, next and Today, and read, grouped by local day, every CR merged or dropped, every PR opened and every release of that period, under five plain totals. It reads the records and the archived CRs' steps only (never the forge or git) and writes nothing. From now on a batch's close adds to its record the times and the release mark the page needs.

## Deliverables

The page is fed by one new server topic and draws nothing the board did not already have (existing chips, one-line titles, tokens only, no chart).

```mermaid
flowchart LR
  close[batch close] -->|kind, ended, shipped, version| record[(batch record)]
  record --> index[board/history_page.py index]
  index --> op[history.get / history topic]
  op --> feed[history-feed.js]
  feed --> view[history.js]
  view -->|h:CR or c:CR| panel[side panel]
```

| Choice | Result |
|---|---|
| Periods | day, week, month; `hp` and `hd` in the address, so Back walks them |
| Local day | computed on the server with `zoneinfo` and `tzdata`, from the browser's time zone |
| Rows | time, kind chip (merged, dropped, PR opened, release), number, one-line title, batch, rounds and cost |
| Older records | CRs with no recorded end are counted in a foot line, never guessed |

**UNVERIFIED:** the look of the page in a real browser (no screenshot yet).

## Blast radius

Grade: 2. The batch close now writes four more keys into each CR of the record, and the dependency set gains `tzdata`. Both are additive; a `git revert` restores the previous behaviour, and old records stay readable.

## Autonomous decisions

- The page's index is rebuilt when a record, an archive folder or `4-batch` changes, not when an archived `STATUS.json` is edited in place (archives do not change).
- A CR of a closed record is read as "new" when it carries the `ended` key; older ones are read from their archived steps.
- A CR that ended with no recorded time counts in the foot line's "no recorded end"; an unreadable archived file counts both as unreadable and, being a merged CR with no dated step, as "no recorded end".

## Known gaps

- A PR made ready (out of draft) is not shown: no record keeps that time once its batch is closed.
- Older CRs with no recorded end are in no period; the foot line counts them.
- A CR dropped back to the inbox or the backlog has no folder: its row opens nothing.
- No screenshot of the page from a real browser yet; the view has no Node-run test. Owed: day, week, month, an empty period, French and a narrow screen.
- A month's answer took 3.1 s, then 2.55 s, in process against the real surface (about 2.2 s of it in `state_of`), so "no visible wait" for a month is UNVERIFIED.
- This PR's base is CR-441's branch, so it stays a draft until that one lands. `pyproject.toml` and `uv.lock` add only `tzdata==2026.2`; a later lander of CR-446 or CR-448 re-runs `uv lock` and keeps both dependencies.

<details>
<summary>Details</summary>

## Changes

- Close: `commands/close_archive.py`, `history.py` and the shared `core/cr_times.py` write `kind`, `ended`, `shipped` and `version` for each CR of the record.
- Server: `board/history_page.py` (index and answer), `history.get` op and `history` topic, `HistoryArgs`, `protocol.json`, `docs/server-api.md`, `tzdata` in `pyproject.toml` and `uv.lock`.
- Client: `views/history.js`, `views/history-feed.js`, router keys `hp`/`hd`, registry entry after PRs, `history` icon, `en-history.js` and `fr-history.js`, `css/views/history.css`, the `h:<CR>` opener target, `DESIGN.md` and `docs/web-board.md`.

## Human decisions

- The page lists and totals only: no chart, curve, median, ranking or comparison with another period.
- Days are the browser's local day, computed on the server with `zoneinfo` and the `tzdata` wheel; weeks run Monday to Sunday.
- A release is told only from the record's own mark, never from a tag or a forge publication.
- A batch's close only adds keys to its record; records already written are not rewritten.
- The cost shown is the sum of the recorded costs of the CRs that ended in the period, labelled as such; steering and grill costs are not spread over days.
- A CR with no recorded time is in no period and is never dated from its archive folder's name.

## Impacts

A new "History" entry in the sidebar and the phone's bottom bar; Home, Costs and the Batch navigator are unchanged.

## Test plan

- [x] New or changed tests (`test_board_history.py`, `test_board_history_client.py`, one call added in `test_server_api_calls.py`)
- [x] Local gates at `12e6f7b`: `just check` and `just scenario` pass at `12e6f7b`; `just eval-dry-run` passes at `12e6f7b` (it ran at `86544ac`, and only `scenario/` changed since)
- [x] Evidence: after at `12e6f7b`, from the in-process month check below (no browser screenshot)
- [x] Review: approved at `12e6f7b` (rounds 1 and 2 approved at `819b848`, round 3 approved at `86544ac` and committed as `12e6f7b`)
- [x] Verified at `12e6f7b`
- [x] CI green at `12e6f7b`

## Internal references

CR-445 board-history.

</details>
