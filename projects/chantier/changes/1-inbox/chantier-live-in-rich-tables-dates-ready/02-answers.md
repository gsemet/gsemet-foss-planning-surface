Short name: `live-rich`

1. live-rich-Q1: **What Agents lists.** A. The project's active sessions: Chief of Staff, Foreman, Drivers and workers, each with its role and its CR. The grill's check: the spec confirms whether `none` with a batch running was a bug.
2. live-rich-Q2: **The time zone.** A. Date and time in the user's local zone, the zone written in the header. The spec checks the observed gap (header 11:26 UTC, Flow lines 16:20) and says which it was.
3. live-rich-Q3: **Where Ready comes from.** A. The server's published API gives the PRs or MRs with their state (the board's colours); the client calls neither `gh` nor `glab`.
4. live-rich-Q4: **The time hotkey.** A. The key `t`; it starts on date and time and switches to the time since the event ("46 s", "2 min", "1 h", "3 days", rounded) and back.
5. (from the request, no question) Rich rendering with real tables and boxes; `--once` keeps printing a plain-text screen; layout: Projects top left, Agents below it in its own box, Flow centre, Ready above Tasks on the right, a clickable link where the terminal allows (OSC 8). Rich is a new dependency: the spec checks the `uv`/`uvx` launch and the dependency rules.
6. live-rich-Q5: **Grilled enough.** A. Specify, for the running batch batch-31.

Destination: running batch batch-31.
Spec critic: yes, default model (it changes what the user sees and adds a dependency).
7. live-rich-Q6: **Tasks' `to review` section.** A. It goes: the hand-back age moves to an `Age` column in Ready; Tasks keeps the working and blocked CRs.
8. live-rich-Q7: **QA drivers in Agents.** A. Left out for now (the server's `project` topic does not carry them; no server or API change in this CR).
Spec-writer's findings from the code, kept: Rich is already a dependency (no change to `pyproject.toml`, `uv.lock` or the launch); the `none` in Agents was right for the old narrow list (Drivers of working CRs), and the new list is the one of Q1; the time gap was events of an earlier day (header and Flow both in UTC), so the date is shown on every Flow line and times are local with the UTC offset in the header; Ready reads the server's existing `prs` topic.
9. live-rich-Q8: **The Chief of Staff in Agents.** A. The seat holder, labelled "Chief of Staff (seat)", with no claim that it is running.
10. live-rich-Q9: **Ready's colours.** A. The spec's one-word table is kept and its claim of matching the web PRs page is dropped; an open PR to review shows in grey, as on the board.
11. live-rich-Q10: **`live --once` with a slow or offline forge.** A. It prints the screen at the deadline, Ready saying "not read".
12. live-rich-Q11: **The Flow's width.** B. A shorter date form (for example `11-23 12:26:25`), so the Flow keeps its room (the user chose B over the recommended A).
Critic's other findings, applied without a question: the equality test with `tokens.css` parses only the 8 state names, not the `-tint` variables; the spec says whether Ready lists a paused batch's CRs and makes the empty line's words match; `docs/boards.md` and the `docs/server-api.md` paragraph say that the server's `prs` read can also append the "merged, not recorded" journal line while `live` watches.
