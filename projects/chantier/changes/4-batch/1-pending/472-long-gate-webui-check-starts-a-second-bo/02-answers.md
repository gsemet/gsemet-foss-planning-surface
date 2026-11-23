Short name: `dynamic-port`

1. dynamic-port-Q1: **Port choice.** A. A dynamic port: the default port 8765 is tried, then +1 until a free one is found (the user's word 2026-11-23, own-gate-Q6); the board, `webui` and the scenario's webui check never depend on 8765 being free.
2. dynamic-port-Q2: **Grilled enough.** A. Specify, for the running batch batch-31 (it runs before own-gate).

Destination: running batch batch-31.

3. dynamic-port-Q3: **Windows exclusive bind.** A. Out of scope (SO_EXCLUSIVEADDRUSE is not set here); a follow-up if wanted.
4. dynamic-port-Q4: **AGENTS.md.** A. This CR may reword its sentence on the default port.

5. dynamic-port-Q5: **Unknown cause of the restarted scenario server.** A. The Driver first reproduces on Windows with the first server's stderr captured, names the cause in the PR, and fixes it if it is not the port.
6. dynamic-port-Q6: **A board of this surface on a walked port with no record.** A. Accept the risk; the claim reads 'found by its record, or at 8765'.
