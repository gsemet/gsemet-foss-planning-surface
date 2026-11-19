Head: bb2eb0febbd44420ea578e6c5735a40582727286

All claims judged at bb2eb0f.

1. Spec behaviours (config checks, shipped defaults, read_limits, open label/0 refusal/no plugin root,
   playbook limits line, board PUT journal lines, event_text, watcher `events`, status slots line):
   `uv run --no-sync --project . pytest tests/test_limits.py tests/test_limits_cells.py tests/test_forge_hub.py
   tests/test_playbook_config.py tests/test_playbook_layers.py -q` -> `85 passed in 22.24s`.
2. Real CLI probe in a scratch git repo (work/scratch/p, removed): repository chantier.yaml with
   specifying.parallel 2, batch.slots 0, two work/specifying markers.
   `chantier playbook` -> `limits: specifying 2 [repository], markers 2 (cr-a, cr-b); batch slots 0 [repository]; specifying at the limit`
   `chantier open --mode stack` (no --slots) -> `error: open: batch.slots is 0 in chantier.yaml: a new batch needs 1 slot or more to start a Driver; give --slots <n>, or set batch.slots on the board's Configuration page`
   (refusal matches spec text; names file and key).
3. PR description (pr-body.md as posted on PR 348): renders, Summary/Changes match the diff (42 files; the
   `limits` helper `specifying_markers` in stages.py, rules.py wiring and init.md wording are covered by the
   `limits:` line and cards bullets). Known gaps hold the four stated gaps; no UNVERIFIED/STALE; no images.
   Review box `approved at bb2eb0f` matches `log`: "r3 approved at 020fd864, committed as bb2eb0fe".
   Unchecked boxes (Verified, CI green) are the expected pending ones.
4. CI at this head: just check (ubuntu) and eval-dry-run green; macOS, Windows, scenario pending at read
   time. Long gate not run by me (the pipeline's job); not claimed.
5. Not proved here: the wake of an idle session (Known gap, declared); the board's Limits tab visually (no
   screenshot, declared; Configuration page is outside the pane rule); the board PUT paths covered only by
   the in-process tests of item 1, not a hand-run server.

Evidence: none captured (before-after), see PR Known gaps; no UI capture taken.

VERIFIED
