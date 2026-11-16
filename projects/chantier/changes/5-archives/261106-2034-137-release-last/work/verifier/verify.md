# Verify CR-137 at 6b5b7c3: VERIFIED

Each Done-when bullet was observed with the worktree's real CLI in a throwaway repo; see evidence/before-after.md and the transcripts beside it.

- Release waits for each CR, a later one included, `status` says so: observed.
- `ready` keeps waiting; merged and dropped do not: observed.
- Others ended: take refused until `order confirm`; a CR added voids it: observed.
- `order add` refused once started and again after PR merged/queued; `--fix-for` works: observed.
- `order after <release>` and a second `--release` refused: observed.
- `open --release` alone: no confirmation: observed.
- Inspector points: (a) take passes with no new confirm after merged PR back to queued and fixes ended; (b) depends.json naming the release is refused as a cycle naming it, by open and by order add.
- Not rerun: `just scenario`, `just check`.
