## Summary

A change request (CR) can reach a project's inbox or backlog without the Chief of Staff seeing it: another machine files it and its writer pushes it, or another project's session on the same PC writes it. The owner had to look to find it. The surface writer and the `file` and `triage` commands now append one `arrived@1` journal line per such CR, naming its folder and stage, which the session watcher carries to the Chief of Staff. The board page already updates from its file watch.

## Deliverables

- A new published journal type, `arrived@1`: `project`, `folder`, `stage`, `before`, `via` (`pull` or `session`), `upstream`. Its sentence: `surface pull brought <folder> (new in <stage> | moved from <before> | back from 3-ready); for the Chief of Staff: tell the user, act on nothing`.
- One pure arrivals function shared by the writer and the commands. Only CRs that end in `1-inbox` or `2-backlog/P<n>` are told; moves into `3-ready` or `4-batch`, and restores from `4-batch`, the archives or the trash, tell nobody.

```mermaid
flowchart LR
  remote[remote pull] --> writer[writer integrate]
  writer --> arr[arrivals function]
  cmd[file / triage by another session] --> arr
  arr --> journal[arrived@1 journal line]
  journal --> watcher[session watcher]
  journal --> list[seat and status listing]
  list --> mark[arrivals-told.json]
  watcher --> mark
```

- Pulled arrivals are computed from git trees (merge-base to upstream), only when an integration ran, and a conflict's end tells the CRs the upstream brought and the resolution kept.
- While no watcher runs, `seat` and `status` list the untold arrivals (at most 10, then an `and <k> more` line) and move a local told mark, `arrivals-told.json`, which is never published.

## Blast radius

Grade: 2

Shared writer, journal and session-start code change; no data format of existing lines changes. Revert is a plain `git revert`, the new local mark file is ignorable.

## Autonomous decisions

- The spec's `4-batch/<batch>/` is read as `4-batch/{1-pending,2-actives,3-done}` as the layout really is.
- `status` now writes the git-ignored told mark when it lists arrivals (its one write).

## Known gaps

- Scenario check for the writer step added but run only by the long gate.

<details>
<summary>Details</summary>

## Changes

- `hub/arrivals.py`, `hub/arrival_mark.py`, `writer/pulled.py`, `commands/arrival_line.py`: arrival computation, told mark, pulled reads, listing.
- `writer/cycle.py`, `writer/git_ops.py`: merge-base and tree reads, queued `arrived@1`, conflict-end arrivals.
- `commands/intake.py`, `commands/seat.py`, `commands/batch_status.py`, `hub/watch.py`: session lines and the told mark.
- `hub/schemas*.py`, `schemas.json`, `core/files.py`: the new type and the ignored file.
- Cards, AGENTS.md, docs and scenario README updated.

## Impacts

No visual change; the board page updates through its existing file watch.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`, `just journal-schemas`
- [ ] Evidence: none beyond tests
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-468 pull-arrival.

</details>
