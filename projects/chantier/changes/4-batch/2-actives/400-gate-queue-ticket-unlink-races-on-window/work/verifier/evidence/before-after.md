Before: base 995a6b073183c5c5376aa3b50576781113a2b323. After: head 830b74dbb876117a7ab0e69cce8108190a5a2d62.

Pair 1: the new test, base: 1 failed (PermissionError at gate_queue.py:76); head: 9 passed.
Reproduce: detached worktree of the base, copy the head's tests/test_gate_queue_order.py in, run pytest from the CLI folder with PYTHONPATH on the base src.
Pair 2: LongGateLock.__enter__ with unlink always refused: base raises PermissionError; head enters.
Logs are in the verify.md. No screenshot.
