The project says how many long gates may run at once; chantier's lock honours it.

Generic form (the user, 2026-11-14): the gate lock is chantier's, the long gate is the project's. Today the lock lets one long gate run in the whole batch, whatever the project; a project whose long gate is isolated (its own ports and folders per worktree) loses hours for nothing.

What happened (batch-17): every `just scenario` of the batch ran one at a time (about 35 minutes each); with four CRs ready together the last waited about two hours.

Wanted:
- `chantier.yaml` gets a key for the number of long gates that may run at once (default 1, today's behaviour); the lock admits that many;
- the Chief of Staff's init or grill asks the project once whether its long gate is isolated per worktree;
- for chantier's own repository (a project item): make `just scenario` isolable per worktree (ports, temporary folders, the fake forge), measure the CPU load of several at once on the user's machine, then set the key.
Related: gate-lock-priority (orders the queue meanwhile), CR-235 gate-liveness (the lock tells the truth).
## After the critic's review (Fable, 2026-11-14)

- Merged here: gate-lock-priority (removed). The queue is tickets named by arrival time (`commands/gate_lock.py:63-72, 83`); a manual "move up" for the steering session is enough; automatic ordering by dependents is ceremony once two gates may run. Also: a docs-only gate (`just check`) waited behind the lock on 2026-11-14 with all four Drivers queued: the specification says which gates take the lock.
- Keep only the generic part: the `chantier.yaml` key and the lock honouring it. Making chantier's own `just scenario` isolable is a project item, filed apart when this lands.
- After CR-235 (gate-liveness), which rewrites `gate_lock.py`.