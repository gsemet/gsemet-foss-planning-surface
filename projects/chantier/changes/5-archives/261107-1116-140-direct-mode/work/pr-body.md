## Summary
Direct mode: a batch can be steered by the Chief of Staff itself instead of a Foreman session.

- `open --direct` records `steering`, shown in `brief.md`, `status` and `STATUS.md`; `preflight --direct` drops the Foreman-start check.
- `order add` / `order qa` are refused on a direct batch; a later epoch from another transcript switches the batch to Foreman mode.
- Cost is priced per claim window; the steering row reads "Chief of Staff (steering)" and the "Chief of Staff" line excludes the window. `close` is not blocked by the Chief's own transcript.
- Cards, host references, driver descriptions (both hosts), README and docs updated.

## Checks
`just check` and `just scenario` (github and gitlab) pass on Windows at this head.

## Evidence (Verifier, at f83b3ab: VERIFIED)
Before (origin/main): `preflight --direct` and `open --direct` are unrecognised arguments (exit 2).
After: `open --direct` records and shows the steering; cost shows one "Chief of Staff (steering)" row ($2.00), a Driver row ($1.00), total $3.00 with nothing counted twice, and a "Chief of Staff" line holding only the pre-claim call; `order add`/`order qa` exit 2 on a direct batch; a later epoch from another transcript flips steering to foreman, the old epoch exits 3, `order add` then passes; `close` is not blocked by the Chief's own fresh transcript. Text outputs stay in the CR's `work/verifier/evidence/` (before-after.md). A Copilot direct run is unproved.
