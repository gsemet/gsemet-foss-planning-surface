# Lessons from the Markdown OKF-Schema Studio run

Field report from a production run of chantier's predecessor (Markdown OKF-Schema Studio,
2026-11-03: 16 CRs, 3 release attempts). The owner agrees with the points below, to be taken up
after the claude-full eval. Anything touching a forge works on GitHub and GitLab alike.

1. `order merged` checks the forge before acting: the PR is merged, on GitHub and GitLab, through
   `forge.py`, with both fakes and a check in `just scenario`. Otherwise an error and no partial
   action: no archive, no branch deletion. Today it trusts the user's word.
2. `chantier cost` reports the Foreman's average context per wake and its number of wakes, not
   only the peak, so points 3 and 4 can be decided on numbers.
3. Bound the Foreman's context without killing its Drivers. Drivers are background agents of the
   Foreman's session: a new session cannot reach them, and their hand-backs go to their parent.
   So keep the same session and compact at a lower threshold (find how to set it for the Foreman
   alone: 400k is global today), or allow a fresh Foreman only when no Driver is live. Never in
   the middle of live Drivers. Verify what happens to them when the session ends.
4. Heartbeat without the model: only if the numbers show that heartbeats cost. It wakes every 55
   minutes, so the events and orders probably cost more.
5. Orders: the Foreman reads the pending orders in the state at every wake, so a message is only
   a signal and a late one changes nothing. The orders already live in `batch.json`, with ids; no
   new file.
6. Release: chantier imposes no gate. The Chief of Staff asks the project to plan a long check on
   the exact head of the default branch before the version commit, if its procedure has none:
   per-CR gates miss interactions between CRs and any check skipped on a PR.
