Short name: `direct-switch`

# Answers

1. direct-switch-Q1: **The command.** The user: "fait quelque chose de simple et de proche de ce qui
   est fait. un chief of staff peut réorganiser son équipe comme il le veut". Settled by the Chief of
   Staff: mirror the existing switch to Foreman mode. Today a Foreman's `foreman transcript <id>` on
   a direct batch makes it a Foreman batch (`seat.py`, a `steering` event in the journal). Likewise,
   the Chief of Staff's own claim of the next epoch (`foreman set <its id> --epoch <n+1>`, then
   `foreman transcript <its session> --epoch <n+1>`) on a Foreman batch makes it direct, with a
   `steering` event `direct` in the journal. There is no extra command and no flag: the Chief of
   Staff reorganises its team as it sees fit, and the switch is said in the CLI's output line. How
   the CLI knows the claimer is the Chief of Staff (the seat's session, or the batch's recorded
   Chief of Staff transcript) is left to the spec-writer, from what the record already holds.
2. direct-switch-Q2: **When a Foreman is not answering.** A (recommended): its last heartbeat is
   older than the batch's heartbeat limit and one ping gets no answer within 5 minutes; the user's
   word is enough on its own, with no wait.
3. direct-switch-Q3: **Who stops a live Foreman's Drivers.** A (recommended): the Foreman itself.
   It notes each CR (`switch to direct mode: Driver stopped; the Chief of Staff restarts it`),
   stops each of its Drivers by the host's stop, answers that it is done, and stops. Stopping the
   Foreman's session from outside stays the path for a Foreman that is not answering.
4. direct-switch-Q4: **Back to Foreman mode.** A (recommended): yes, through the existing switch to
   Foreman mode, unchanged. The rule "a Foreman batch never becomes direct" goes away.

5. direct-switch-Q5: **Grilled enough?** A: specify (after the full restatement).

6. direct-switch-Q6: **A Foreman that ended its heartbeat on purpose.** A (recommended): if it
   then does not answer a ping, the time it ended its heartbeat counts as its last heartbeat.
7. direct-switch-Q7: **A Foreman that answers the ping but never confirms the hand-over.** A
   (recommended): the Chief of Staff waits; only the user's word moves it to the "not answering"
   path.
8. direct-switch-Q8: **The board's cost receipt after a switch** (`chief_outside` leaves out the
   Chief of Staff's steering outside its claim window). A (recommended): left as today in this CR;
   a separate small CR is filed for the receipt.
9. direct-switch-Q9: **The round-trip fix** (a new claim when the transcript differs from the last
   claim's, the last claim is the current session, pricing over each window). A (recommended): kept
   in this CR.

10. direct-switch-Q10: **Knowing an old Driver has ended** (after a Foreman stopped from outside).
    A (recommended): before restarting each CR, the Chief of Staff reads its old Driver's
    transcript ending with `close`'s check (no `--yes`, it lists each held agent's state); it
    restarts only those shown ended, and asks the user about any shown running.
11. direct-switch-Q11: **The batch records another Chief of Staff transcript.** A (recommended):
    before anything is stopped, the Chief of Staff compares its session's transcript with the
    batch record's `chief_transcript`; if they differ it runs `seat take <its id>` and checks
    again; if they still differ it stops and tells the user.
12. direct-switch-Q12: **Remote Control with a silent Foreman.** A (recommended): the Chief of
    Staff says the stop needs the machine (unproved from the phone), names the session and waits;
    the live-Foreman path stays available under Remote Control.

Settled by the Chief of Staff:

- On the Claude Desktop host, the Chief of Staff can stop another session (the session
  management's stop tool): a Foreman that is not answering is stopped by the user, or by the Chief
  of Staff on the user's yes. The spec's gap on stopping another session is answered so.

- The repository keeps no changelog: the release notes are written at release time
  (docs/release-process.md), so this CR edits none.
- The PR is a draft until CI is green; the user merges it by rebase.

