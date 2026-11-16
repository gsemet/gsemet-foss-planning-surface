# Diagnosis: E4 "order merged stops its CR's gate only" failed at 233de2f

Verdict: a pre-existing race (flake under load), not caused by CR-266.

Failing output (scenario/results/scenario-20261115-043103-24544.md, lines 4927-4947): `order merged CR-103` moved the CR
to 3-done and stopped the gate, then the gate process died in `_finish_stopped` -> `g.note(...)`:
FileNotFoundError ... 2-actives\103-par-two\work\gates\20261115-043226.log (gate.py line 139 -> 89).
The scenario's check requires "Traceback" absent from the output (out starts with STOPPED), so it failed.

Cause: gate.py `_finish_stopped` does `if g.log.exists(): g.note(...)` (check then open). The log sits under the CR's
2-actives folder; `order merged` moves that folder to 3-done between the check and the open. Only when the stopped gate
wakes late (loaded machine, 9 units in parallel) does it lose the race.

Not this CR: gate.py differs from base b9f20b6 only by import moves (gate_queue/gate_slots paths). The race code is unchanged.
Base b9f20b6, units gates+stack+parallel+release run together on this machine: gates 78/78 (E4 ok), no Traceback. CI ubuntu
passed at the same head; gates alone passed 79/79 in round 3. Timing flake, not deterministic.

Over budget: stack 329.2 s > 320 s is a WARN from load; base measured stack 376.4 s in the same 4-unit run.

Suggested fix (separate CR or inbox item): in `_finish_stopped` wrap the note in try/except FileNotFoundError (the CR moved
is a legitimate stop reason), or write the gate log outside the CR folder. No change for CR-266; re-run `just scenario`.
