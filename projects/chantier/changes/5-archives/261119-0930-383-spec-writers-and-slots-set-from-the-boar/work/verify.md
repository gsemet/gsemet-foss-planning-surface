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

---
## Re-judgment after the move bb2eb0f..70e5e8a..9c3fb6d

Head: 9c3fb6dd6fdf37385766461637c19b8a759e6323

Base moved to CR-375 (fe2c215). Judged again at 9c3fb6d:
- Behaviour (slots/specifying limit from config, open default slots, label, 0 refusal, playbook limits line,
  journal lines, watcher `events`): `pytest tests/test_limits.py tests/test_limits_cells.py tests/test_forge_hub.py
  tests/test_playbook_config.py tests/test_playbook_layers.py -q` at 9c3fb6d -> `85 passed in 24.71s`.
- Conflict-resolved files keep both intents (`git diff fe2c215 HEAD` of the files): chief-of-staff.md has the new
  `specifying.parallel`/`batch.slots` config keys, the limits paragraph, the slots wording and the `config changed on the board`
  watcher lines, with CR-375's watcher text intact around them; hosts/claude-code.md and copilot.md "Run the watcher" rows keep
  the `watch: not running`/`still running` wording and add the config-line wake note; opening.py has `read_limits`, `_slots_from`
  and the `where` label added on top of the base, with the base's other code unchanged.
- Move 70e5e8a..9c3fb6d: `git diff 70e5e8a HEAD` touches scenario/run_scenario.py only (the expected watch last line,
  `cursor(n)` helper, two check expectations); no product code.
- CI at 9c3fb6d (`gh pr view 348`): check ubuntu/macos/windows, scenario ubuntu, eval-dry-run all SUCCESS.
- Carried from bb2eb0f: PR description claims (pr-body.md; no change of the CR's patch beyond conflict resolution and
  the scenario expectation), Review box/log, declared Known gaps; the scratch CLI probe is covered by the in-process
  open/playbook tests above, rerun at this head.

VERIFIED

## Description pass (posted body of PR 348) at 9c3fb6dd6fdf37385766461637c19b8a759e6323

Head: 9c3fb6dd6fdf37385766461637c19b8a759e6323

- Posted body equals work/pr-body.md: `gh pr view 348 --json body -q .body` vs pr-body.md, `diff` (CR-stripped) -> identical
  (only a trailing blank line differs).
- Template: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details fold with Changes,
  Human decisions, Impacts, Test plan, Internal references; CR-383 named only in Internal references; role names (Chief of Staff,
  spec-writers) are product terms of the cards this PR changes.
- SHA marks: 70e5e8a is an ancestor of 9c3fb6d (`git merge-base --is-ancestor 70e5e8a 9c3fb6d` -> true); 9c3fb6d is the head.
- Boxes vs `chantier log CR-383`: "Review: approved at 70e5e8a, committed as 9c3fb6d" matches notes `r4 approved at 70e5e8a, committed as 9c3fb6d`;
  "Local gates at 70e5e8a: just check 731" matches restack note; "Verified at 9c3fb6d" matches verdict VERIFIED at 9c3fb6d;
  "CI green at 9c3fb6d" matches `gh pr checks 348`: 5 of 5 pass (check x3, eval-dry-run, scenario ubuntu).
- Known gaps present and lists the unproved wake and the missing screenshot; no images attached.

VERIFIED
