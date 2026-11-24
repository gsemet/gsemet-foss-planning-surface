## Summary

The CR board pane (the Claude Code mod that draws the running batch) showed a batch's active CRs only, in two groups, so a batch whose CRs had all merged looked empty, and it said nothing of the web board or the watcher. The pane now shows the running batch's CRs by state (pending, working, ready to merge, merged) with a short figures line, and a folded Services section with the web board's links.

## Deliverables

The batch section, open by default, now groups its CRs by state; the rest stays folded.

| Section | Default | Shows |
| --- | --- | --- |
| Batch | open | Waiting for you (kept), a figures line, then Pending, Working, Ready to merge, Merged (empty groups left out) |
| Backlog | folded | unchanged rows; label `Backlog (N, K ready)` |
| Merged (all batches), Trashed | folded | unchanged |
| Services | folded | server, hub, writer, this session's watcher, "as of N min ago", the board's links |

The index file (`STATUS.json`, schema still 3, additions only) gains, per batch, `merged` (all merged CRs, newest first), `created` and `counts`, and at the top a `services` snapshot:

```text
services: { at, server: {pid, version, source, started, host, port, url, local_url, build_note} | null,
            hub, writer, watchers: [session keys] }
```

Choices: the figures are the CRs per state out of the total, the time since the batch started and the mean spend per merged CR; `services` is taken when the index is written, never by the pane, which still runs no process but `git rev-parse`; no key is ever written to the index: the pane reads the two keys from the git folder's `chantier/server.json` and draws a private and a read-only link.

Evidence (text; no image, see Known gaps), before at `c155c89`, after at `bf5fdbd`:

- The new `test_status_index_services.py`: `3 failed` (`KeyError: 'services'`) at `c155c89`, `3 passed` at `bf5fdbd`. It asserts `merged` (newest first, with cost), `created`, `counts`, `services` (server pid, url, build note; hub and writer null; watchers), `server` null with no server, and no key text nor `?k=` in the written `STATUS.json`.
- `just mod` at `bf5fdbd`: 94 pass, 0 fail, among them the pane tests (a batch of merged CRs shown, each state shown, the figures line, Backlog, Merged and Services folded, links with keys from `server.json`, no `server.json` gives keyless links and one line, an index of the older shape draws as before).
- The long gate `scenario` passed at `bf5fdbd`; CI at `bf5fdbd`: `just check` on ubuntu, macos and windows, `just scenario` and `just eval-dry-run` all green.

**UNVERIFIED:** the pane as drawn in a real Claude Code session (see Known gaps).

## Blast radius

Grade: 1. Additions to an index file that older readers ignore, and a pane redraw; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- `services` is computed when the index is written, not on each board read, because the web board reads the same view on every request and the probe touches processes and lock files.
- Spend per merged CR is the mean of the merged CRs' costs.
- A CR that waits for the user appears in "Waiting for you" and in its state group.
- One unused import was removed from `commands/orders_apply.py` because lint failed on it.

## Known gaps

- No screenshot of the pane from a real session.
- `services` (LAN address, PIDs, build path, no key) is published with `STATUS.json` by the surface writer, as the specification chose.
- The snapshot's age can be hours: the index is rewritten only by some commands; the pane shows its age.

<details>
<summary>Details</summary>

## Changes

- `status/views.py`: shared merged-row builder, per-batch `merged`, `created`, `counts`.
- `status/write.py`: `services` in `write_dashboard`; `board/links.py` (new, holds the link helpers; `board/address.py` re-exports them): `local_url` key optional.
- `types/index.d.ts`: the new optional fields.
- `hooks/register.tsx`: state groups, figures line, Backlog label, Services section, links; `hooks/register.test.tsx` and `tests/test_status_index_services.py`.
- `CONTRIBUTING.md` ("A mod") and `docs/boards.md`.

## Human decisions

- One change for the batch's states, the links, the services and the figures.
- Running batch open, everything else folded.
- Both links shown, the read-only one and the private one; the private one is hidden in the screenshot.
- Figures: CRs per state out of the total, time since start, spend per merged CR.

## Impacts

The pane shows merged CRs of the running batch and a Services fold; no change to the web board, `chantier live` or `STATUS.md`.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `bf5fdbd`: `just check`, `just mod`, `just eval-dry-run`
- [x] Evidence: before at `c155c89`, after at `bf5fdbd`
- [x] Review: approved at `bf5fdbd` (rebase conflict reviewed)
- [x] Verified at `bf5fdbd`
- [x] CI green at `bf5fdbd`

## Internal references

CR-481 cr-board-pane (batch-31).

</details>
