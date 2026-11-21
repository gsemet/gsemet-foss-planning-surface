# Intent: measure `just test` at rest before deciding its ceiling

AGENTS.md caps `just test` at 30 s above its 18.5 s of 2026-11-14 (48.5 s) on the user's Windows
machine. CR-417 (batch-29, PR #393) sped the suite up and kept all 1419 test ids, but every
measure it took ran on a loaded machine (another batch sharing the CPU, load 16-68 %): 63.0 to
106.8 s at its head, 73.1 to 93.5 s on main. What remains slow is said to be the tests that run
real git: the writer, carry-ship and release-tag tests.

The user chose (test-ceiling-Q1) to measure first, on an idle machine: a CR runs `just test`
several times at main's head with nothing else working, names the slowest tests and the share of
the real-git tests, and brings back the numbers. The user then decides between raising the
ceiling in AGENTS.md and moving or cutting the real-git tests. Until then the ceiling stays.

This CR measures and reports. It changes no ceiling, no test and no CLI code.
