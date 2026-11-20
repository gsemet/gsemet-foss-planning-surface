Head: b629a67bdf747f3c51b2b53e9528df1c5527060a

Move e855fe9..b629a67 (rebase onto main dc80a81b, then commit b629a67). Verdict VERIFIED.

- Split changes no behaviour (b629a67): `git show b629a67 -- hub/` shows only a move of SyncConflict1/Blocked1/Late1/Resumed1 to hub/schemas_sync.py and of Payload/Sha/SHA to hub/schemas_base.py; field lists identical; `_Payload` renamed `Payload` (grep for `_Payload` elsewhere: no hit). `python -c "from chantier.hub import schemas as s; s.SyncLate1(since='a',paths=1,ahead=2)"` imports and validates (classes now in schemas_sync).
- Tests at b629a67: `pytest ... -k "schema or hub or writer or journal or code_targets or validate"`: 280 passed.
- AGENTS.md (b629a67): `grep -nE "First|Second|...|Sixth|two named"` finds no ordinal or count of exceptions (line 118 reads "has named git exceptions"). Matches the PR body's Autonomous decision.
- Specification still met: carried from e855fe9 (VERIFIED): the move touches only the model location, not the writer, its refusals or its lines; the tests above exercise them.
- PR body (b629a67): SHAs are b629a67 (in history); Review box proved by `log CR-404`: "inspector approved at b629a67bdf74..."; local gates claim proved by the Driver note "just check: pass; just eval-dry-run: pass" at b629a67 (cited as note only); Verified/CI boxes are unchecked and CI pending, stated truthfully; Known gaps list the UNVERIFIED bound. Not run by me: ruff (not installed in this env), just check, CI, scenario.
