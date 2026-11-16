# Batch-17 retro: CLI fixes

Filed 2026-11-14 by the Chief of Staff, on the user's word (ID-Q1, A): the batch-17 retro's CLI
points, drafts 3, 5, 7 and 10 of `.agents/changes/batch-17-issue-drafts.md` (read it for each
point's evidence and fix).

3. `handback ready` from the recorded Driver of a blocked CR is accepted with a note, instead of
   needing a `take --note` round trip.
5. `forge-stack create` builds from the ready CRs and leaves the queued ones to a later `rebuild`.
7. chantier's own-checkout run line syncs once at batch start, before the board starts and after
   any merge that changes `uv.lock`, then runs with `--no-sync` (on Windows a running gate or the
   board holds `.venv\Scripts\chantier.exe`: os error 32); preflight says so on Windows.
10. `take`, `handoff` and `ship` take a stacked CR's base from its PR's base when a PR exists.

## Found 2026-11-14, evening

`uvx --refresh --from C:/Users/gaeta/Projets/chantier chantier board` served an old build of the board from uv's cache (`archive-v0/OULHeWrXMFCRg6VL`): its `js/views/registry.js` had no Triage view and `js/i18n/fr-write.js` did not exist, though both are on main at ce00ec3. The user toured a stale board. `uv run --no-sync --project <checkout> chantier board` served the live code. `--refresh` does not rebuild a local source whose version did not change. In chantier's own checkout, every start of the CLI (the board included) uses `uv run --project`, never `uvx --from <checkout>`; the cards and docs that say otherwise are fixed.

