# Before and after, CR-481

Before: c155c8977ab84a9c44b208b3a7e6180598558e72 (origin/main, detached worktree, removed).
After: 007aa019c42db53b8261b854e35578769a491db6.

- STATUS.json fields (merged, created, counts, services, no key): `skills/chantier/scripts/cli/tests/test_status_index_services.py`
  run through `write_dashboard` in a test repo. Before (test file copied onto the base): 3 failed
  (`KeyError: 'services'` and missing fields). After: 3 passed. Reproduce:
  `uv run --locked --group dev pytest -q skills/chantier/scripts/cli/tests/test_status_index_services.py`.
  The live planning folder was not written (rule: no probe on it).
- Pane: `just mod` at the head, 94 pass, 0 fail.
- Screenshot of the pane from a real session: not captured (needs the user's own Claude Code session); a Known gap in the PR.
