# Refusal proof (local run, not committed)

Copy of the CLI package (`skills/chantier/scripts/cli/src/chantier`) with
`LONG_GATE_WAIT_S = 3600` changed to `5` in the copy only. A small driver (`drive.py`) imports
`_LongGateLock` from the copy with a fake repo whose `changes` is an empty folder, and:

1. starts CR-A, which takes the lock and holds it 3 s;
2. 1 s later starts CR-B (queued behind A; holds the lock 20 s once it has it);
3. 1 s later starts CR-WAITER (queued behind A and B).

A releases, B takes the lock (the holder changes during the waiter's wait); the waiter is then
refused once B alone has held the lock for 5 s (the count restarted at B).

Command: `python -I drive.py <copy>/src <plan> CR-A 3` / `CR-B 20` / `CR-WAITER 0` (as above).

Output of the waiter:

```
LONG_GATE_WAIT_S = 5
refused: ChantierError exit 2 - the long gate of CR-B (pid 26064) has held the lock for over an hour: check it; this gate was queued behind it
log:
waiting for the long gate of CR-A pid 26668; queued ahead: CR-B
waiting for the long gate of CR-B pid 26064

queue left: (empty)
```

The refusal names CR-B, the holder alive at that moment, not CR-A seen when the wait began; exit
2; the waiter's ticket is removed. (The "hour" in the text is the real wording; only the number
was lowered in the copy.)
