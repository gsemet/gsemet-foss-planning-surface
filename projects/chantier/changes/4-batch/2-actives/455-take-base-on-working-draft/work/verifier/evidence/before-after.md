# before-after (CR-455)
Before: base 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9 (CR-442's branch). After: e5d656ee3f7fc487796817c7075ed5fbc11e0275.
Pair: head's `tests/test_stack_base.py` against the base's `src` (PYTHONPATH on a detached worktree of the base): 15 failed, 34 passed; against the head: all pass (68 with test_stack_hold.py). Reproduce: `git worktree add --detach <p> <base>`, copy the test file in, `PYTHONPATH=<p>/skills/chantier/scripts/cli/src uv run --no-sync --project <worktree> python -m pytest tests/test_stack_base.py` from `<p>/skills/chantier/scripts/cli`.
No screenshots (no UI change).
