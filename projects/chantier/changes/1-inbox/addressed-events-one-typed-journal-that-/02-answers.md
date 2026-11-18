# Answers

Settled by the Chief of Staff, 2026-11-18, under the user's standing word "plus de question"
(the Chief of Staff settles and informs).

1. **Scope.** A foundation only: the event line, its audience, the watcher's filter and wake
   rules, and the migration of today's lines. No Foreman or Driver watcher, no user
   notification, no delegated action, no new forge read: those are what the line makes room for,
   each a later CR from measured cost (AGENTS.md, CLI scope).
2. **One journal per project.** Today's `forge-journal.jsonl` and the `board`/`config` lines of
   CR-383 and CR-384 become one journal of typed events in the planning folder, never published.
   The spec names the file; a reader still takes an old line it meets (no rewrite of history).
3. **The line.** Versioned (`v`), with a sequence number the cursor counts, a time, a `kind`
   (`merged`, `ci-red`, `board`, `config`, ... the spec lists today's), its `source` (forge hub,
   board, CLI command) and an `audience`. Payload fields stay per kind.
4. **The audience.** Any of: the project (everyone, today's behaviour), a role (`chief-of-staff`,
   `griller`, `foreman`, `driver`), a CR (its Driver), a session id, and `user` (the user must
   act). A line with no audience is for the project. Naming a role here is data the CLI carries,
   not a role the CLI plays: the spec says how this stays within "the CLI knows no role", or
   names it as a new exception for AGENTS.md.
5. **Wake rules in one place.** A watcher subscribes to audiences (`watch --for ...`; the
   Chief of Staff's own default kept as today's command) and wakes only on its events. Today's
   20 s quiet window is the buffer; a filter by audience; a rate limit (at most one wake per
   watcher per window, configurable in `chantier.yaml`, default as today). The spec settles the
   keys.
6. **Writers.** Every writer of today (forge hub, board, CLI commands of CR-383/384) writes
   through one function; no second writer path. A single writer process is the surface server's
   job (next CR), not this one's.
7. **Order.** After CR-383 and CR-384 (it generalizes their lines). The surface server CR stacks
   on this one.
8. **Docs.** `docs/` gets the event line's reference; AGENTS.md's forge hub paragraph names the
   journal by its new name. The PR names any AGENTS.md change.
