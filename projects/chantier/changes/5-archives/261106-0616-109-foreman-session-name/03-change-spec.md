# The Foreman's session is named after the session that starts it

In `skills/chantier/references/chief-of-staff.md`, section "Starting a batch", step 4, both hosts
title the Foreman's session `Foreman <batch>`.

- On Claude Desktop the title becomes `<title> - Foreman [batch <NN>]`: `<title>` is the Chief of
  Staff's own session title, the `title` of `get_session("self")`, which that step already calls
  for the session id.
- On a Copilot SDK host, which gives no such title here, it becomes `Foreman [batch <NN>]`.

`<NN>` is the two-digit number of the batch's folder `3-requests/<NN>-<batch>/`, as `open` prints
it. From a session titled `[Battlestation] Chantier`, the batch of folder `04-cr-board` gives
`[Battlestation] Chantier - Foreman [batch 04]`.

The prompt of the Foreman, the `--batch` argument and the CLI do not change. Nothing else names
this title: no agent file, no test.

## Done when

- `just check` and `just scenario` pass, and `grep -n "Foreman <batch>" skills` finds nothing.
