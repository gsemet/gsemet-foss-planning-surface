The CLI starts as fast as it did before CR-221: each `chantier` command pays no more than before the refactor.

The user (2026-11-14), on why a long gate took 70 minutes: "70 minutes ? Pourquoi est-il aussi long ?"

Measured (2026-11-14, Windows, the user's machine):
- `just scenario`, same 695 checks per forge: about 700 s (GitHub) and 690 s (GitLab) in every gate of 2026-11-13; about 1075 s and 1065 s in every gate from 2026-11-14 00:43 (CR-221's first gate on the new CLI) on. About +55 %, +12 minutes per long gate, on every CR.
- `uv run --script chantier.py --help`: 264-444 ms at 2d9a2aa (before CR-221), 489-562 ms on main at ff701a9 (after). About +200 ms per call; the scenario runs over a thousand CLI calls per forge, and every agent's `chantier` command pays it too.
- CR-221's PR #170 named it in its Known gaps: "start-up timings … were not measured".

Likely causes, not proven: the imports of pydantic, ruamel.yaml and psutil at start, whatever the command; uv's PEP 723 lock check on each `uv run --script`.

Wanted:
- measure where the start-up time goes (imports, uv), per command;
- bring the start-up back to the level before CR-221 (within ~10 %), keeping the PEP 723 dependencies (AGENTS.md's rule) and the pydantic records;
- a structure test or a `just check` step that fails when the start-up regresses past a threshold, so the next refactor cannot slow it silently.
Justification (AGENTS.md: measured token- or time-costly behaviour): +12 minutes per long gate under one lock, about +2.5 hours for batch-17's 13 gates.