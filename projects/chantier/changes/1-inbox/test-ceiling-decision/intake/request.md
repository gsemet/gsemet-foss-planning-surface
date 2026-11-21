# just test ceiling: raise it or cut the real-git tests

# just test ceiling: raise it, or keep it and cut the real-git tests

Priority P2. From CR-417 (test-time-over-budget, batch-29, PR #393), 2026-11-21, a decision for the user.

CR-417 sped up `just test` while keeping all 1419 test ids, but it did not meet AGENTS.md's ceiling of 48.5 s (18.5 s on 2026-11-14 plus 30 s). Its measures, all on a loaded machine (batch-07 sharing the CPU, load 16-68 %):
- `just test` at the head: 63.0, 106.8 and 80.1 s;
- `just test` on main: 77.6, 93.5 and 73.1 s.

What remains is the real-git tests: the writer, carry-ship and release-tag tests. No idle measure was possible.

The user decides between:
- raising the ceiling in AGENTS.md;
- keeping it, and moving or cutting the real-git tests in a further CR, which may cost coverage;
- first measuring on an idle machine.
