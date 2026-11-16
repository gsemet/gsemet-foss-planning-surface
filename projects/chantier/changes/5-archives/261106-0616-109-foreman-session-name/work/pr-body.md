The Chief of Staff now titles the Foreman's session after its own, with the batch's number, so a
user with several sessions sees which one started it and which batch it runs.

In `skills/chantier/references/chief-of-staff.md`, "Starting a batch", step 4:

- Claude Desktop: `<your title> - Foreman [batch <NN>]`, the title read from
  `get_session("self")`, which that step already calls for the session id.
- Copilot SDK host: `Foreman [batch <NN>]`, as it gives no such title here.
- `<NN>` is the two-digit number of the batch's folder, as `open` prints it.

From a session titled `[Battlestation] Chantier`, the batch of folder `04-cr-board` gives
`[Battlestation] Chantier - Foreman [batch 04]`.

The Foreman's prompt, `--batch` and the CLI do not change.

`just check` and `just scenario` pass; `grep -n "Foreman <batch>" skills` finds nothing.
