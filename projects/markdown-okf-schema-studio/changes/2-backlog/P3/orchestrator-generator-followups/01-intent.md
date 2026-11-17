# ORCHESTRATOR.md generator: follow-ups

Tooling · P3 · Filed 2026-10-31 after the first dry run of `just orchestrator` (#238)

:::{note}
The generator works on a copy of the live tree. These gaps showed up in that dry run; none blocks the
first live run.
:::

| # | Gap | Effect today | Direction |
| --- | --- | --- | --- |
| 1 | A `report.md` under `04-archives/` that is not valid UTF-8 | The script crashes | Read with `errors="replace"` and report the path, like an unparsable header |
| 2 | Older `report.md` files write the PR and date in other formats | 65 Landed rows have no date, 73 no PR | Learn the older formats, or backfill a `Landed:` line in those reports |
| 3 | A backlog item without an H1 in its first file | Title shown as "—" | Fall back to the folder name and report the item |
| 4 | No status for an owner-paced CR (first live run, 2026-10-31) | CR 170 (brainstorming) had to be written `blocked`, shown 🔴 | Add a status such as `paused` (owner-paced), with its own icon |

## Done when

- [ ] A non-UTF-8 `report.md` is reported, not fatal.
- [ ] Landed rows without a date or PR drop well below today's 65 / 73.
- [ ] An item without an H1 shows a usable title and is listed in the warnings.
- [ ] An owner-paced CR has its own status and icon.
