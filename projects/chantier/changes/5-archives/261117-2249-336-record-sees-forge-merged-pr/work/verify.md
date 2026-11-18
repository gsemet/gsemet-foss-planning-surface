# Verify CR-336

Head: 2a514cb102df88d32704b3e331393e8cc4f75bd9

All claims judged at 2a514cb1. Tests run from the worktree with `uv run --locked --group dev` (the
brief's `$CHANTIER` line imports the main checkout's code, so pytest through it fails 5 tests on the
old code: not used as proof).

1. Signal test (later, same instant, earlier, open-then-later with one second line and a third read
   writing nothing, chain with CR-0 recorded merged): `pytest -q skills/chantier/scripts/cli/tests/test_board_prs.py`
   -> `27 passed in 9.93s`. VERIFIED.
2. Status test, not landed then landed entry pair prints only the landed line, word for word
   (`board saw merged: <d> P into <a>'s branch at t, landed with <a> at u; for the Chief of Staff: order merged <d>`),
   not-landed line unchanged for CR without landed entry: same run, passes. VERIFIED.
3. Existing tests green; whole suite `pytest -q -n auto` -> `477 passed in 30.58s` (just test's time
   within limit). VERIFIED.
4. `wc -l skills/chantier/scripts/cli/src/chantier/commands/batch_status.py` -> 362 (<= 400). VERIFIED.
5. Code matches spec: `landed_with` pure, instants compared, chain/cycle/missing -> None; `signal`
   key (batch, cr, landed); `seen.lines` holds both old lines and the landed one; `batch_status` only
   reads and calls it (git diff read). VERIFIED.
6. Card/docs: chief-of-staff.md paragraph says `landed with` is recorded, only `not landed` is not,
   GitLab fold exception names the fold rule at line 1102 (`folded into <cr below>` -> `order merged <k>` at once):
   consistent. docs/web-board.md signal paragraph and the stacked-PR bullet updated. VERIFIED.
7. PR 296 description: sections render, Summary/Deliverables/Changes match the diff, Known gaps names
   the same-second gap, no images. Review box `approved at 2a514cb`: log note "r2 approved at a65a8d3d,
   committed as 2a514cb1" matches. VERIFIED. (Test plan boxes for Verified/CI stay for the Driver.)
8. Before/after of the status line: shown by the tests (not-landed line vs landed line); no screenshots owed.
   Long gate: none run by me; pipeline job and `chantier gate` remain the Driver's.

VERIFIED
