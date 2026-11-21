Head: 830b74dbb876117a7ab0e69cce8108190a5a2d62

Claims, each judged at 830b74d.

1. New test passes at the head. `uv run --no-sync --project <worktree> pytest tests/test_gate_queue_order.py -q` (from the CLI folder): `9 passed in 0.15s`.
2. The new test fails on the base 995a6b0 (detached worktree, new test file copied in, `PYTHONPATH` on the base `src`, import path checked to be the base's): `FAILED test_a_sharing_violation_on_a_ticket_or_a_mark_stops_no_gate`, `1 failed, 8 passed`, raised at `gate_queue.py:76 (queue / m).unlink(missing_ok=True)`: `PermissionError: [Errno 32]` (reader case, which runs first).
3. Owner case on the base raises out of `__enter__`: probe (unlink always refused, `LongGateLock(...).__enter__()`): base prints `RAISED PermissionError from __enter__: [Errno 32] being used by another process`; head prints `ENTERED OK`.
4. `just test` at the head: `913 passed, 1 skipped in 41.15s`.
5. CI at the head (`gh pr checks 369`): check macos, ubuntu, windows pass; eval-dry-run ubuntu pass; scenario ubuntu pass.
6. Diff scope: `git diff HEAD~1 --stat` (HEAD~1 = 995a6b0 = the base) touches only gate_queue.py, commands/gate_lock.py, tests/test_gate_queue_order.py (98 insertions, 10 deletions). The diff reads: `ordered` sort/`is_next`, `QUEUE`, `MARK` and the slot locks (`_take`, `_acquire`, gate_slots) are not changed; only file operations are wrapped.
7. PR description (work/pr-body.md) matches the diff: Summary, Deliverables table (reader, orphan mark, move_first touch, os.replace publish, owner removal), Changes list and test list all correspond to the diff; no delivered change unmentioned; Known gaps "None" is consistent (no UNVERIFIED claim, no accepted failure); no image; no role name. Note: the Test plan boxes still hold `<sha7>` placeholders, the Driver fills them at its posting.
8. Screenshot and matrix: none owed (no pane change, no host/default matrix).

VERIFIED

Description pass at 830b74dbb876117a7ab0e69cce8108190a5a2d62 (PR 369 body as posted): VERIFIED.
- Sections and fold present; Summary, Deliverables and Changes match `git diff HEAD~1..HEAD` (gate_queue.py, gate_lock.py, tests/test_gate_queue_order.py); no unmentioned change.
- Internal reference (CR-400) only under Internal references; Known gaps "None", no UNVERIFIED claim.
- Test plan: `just check`/`just eval-dry-run` pass noted in `chantier log` ("before first push at 830b74d"); review approved at 995a6b0, "committed as 830b74d" (valid per card); CI: `gh pr view 369` shows 5 checks SUCCESS at 830b74d; verdict VERIFIED at 830b74d logged.
