# Fable's advice (2026-11-14), taken whole by the user

Read-only advice; it timed only bare process starts on the user's machine (Ryzen 7 7800X3D,
8 cores / 16 threads).

## Measured

- `python -m chantier --help`: about 130 ms; `uv run --no-project python -c pass` warm: 70-90 ms;
  bare `python -c pass`: about 35 ms; `git status`: 70-100 ms.
- The 2026-11-04 transcript: about 263 commands in 106 s, about 0.4 s each (crude count). Today's
  1,200 s per forge is then about 2,500-3,000 commands plus about 60-80 s of sleeps (guess).
- The lever is the number of commands, then the sleeps; process start is not the bottleneck.
  Removing uv from `GATE` saves seconds, not minutes.

## Plan

1. `baseline-and-legacy`: long gate on main and its fixes, the one-off migration, the legacy
   readers and their three scenario cases removed. A green baseline must exist before the
   restructure, to show no coverage is lost.
2. `fast-scenario`: units, parallel runner, moves to pytest, cut sleeps, README contract,
   GitLab reduced. No change under `src/`.
3. `gate-rules`: the four rules; it adds scenario cases, so it comes after the split; it carries
   `just mod` and the pane screenshot.

## Target shape (budgets are guesses until step 0 measures)

Wall time is about max(longest unit, total / 4): the total work must drop to about 800 s.

| Unit | Content | Budget |
|---|---|---|
| parallel (GitHub) | main batch: preflight, open, rounds, ship, order add, drop, Foreman restart, lost Driver, merges and fast-forward, one cost line, close, retro | 150 s |
| stack | stack of 3 with a joiner, ready words, the forge's native stack | 120 s |
| release | release, granted fixes, a release added later, a slim release on a stack | 150 s |
| gates | rails' live queue, two gates at once, cancel and stop, hand-back proofs, gate proof, event-driven waits | 120 s |
| series-deps | series, live dependencies, folders following status | 70 s |
| direct | direct batch, seat handover, Foreman in a worktree | 80 s |
| surface-board | external surface, autosync, the board server | 100 s |
| qa-driver | QA on head, Driver restart, lost messages | 40 s |
| gitlab | a slim ship and merge path plus the GitLab forge stack | 70 s |

To pytest (in-process, parametrized): the `chantier.yaml` refusals and the rest of
`playbook_config`; the rails, close, triage and `depends.json` refusals; cost arithmetic and
Copilot cost; STATUS rendering of a prepared record; restore; next number; `cr_summary`; the card
text checks. Dropped: the legacy cases, the `confirmed` check, the duplicates (analysis section
B), and the pause/close/price tail on cases not about closing. Writing backlog folders directly
instead of `file` plus `triage`: pytest only, never in the units.

## Risks

Guessed budgets; upper-bound timing checks flaking under load (event-driven gates remove most);
Defender and locked temp folders during parallel cleanup on Windows; Linux CI runner size (4 vCPU
public, 2 private: check); regrowth without a standing rule. `AGENTS.md`'s tests rule changes in
this CR; pytest gets a time budget too (guess: under 30 s added to `just check`).
