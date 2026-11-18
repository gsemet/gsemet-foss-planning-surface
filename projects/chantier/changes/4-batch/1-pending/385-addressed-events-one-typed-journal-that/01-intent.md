# Intent

The user, 2026-11-18, during batch-28, looking at the shape the watchers, the forge hub and the
board are taking (drawing: `../surface-server-one-elected-process-for-t/intake/architecture.svg`):

- The Chief of Staff has a watcher that wakes it on messages. A server in front of the watchers
  should buffer, filter and limit their wakes, and route each event to the right watcher, by role
  and by project for example.
- That server watches the PRs and tells the Chief of Staff; it could as well wake a Driver
  directly, or the Foreman, to spare a costly Chief of Staff turn.
- It could notify the user of the events where they must act (a PR ready to review, the Chief of
  Staff wants to talk), and later take delegated actions (answer some questions, change a batch's
  slots or budget).
- "Don't do all of that, but let us lay solid bases to allow it later: one or two foundation CRs."

This CR is the first foundation: the events themselves. The second is the surface server
(`surface-server-one-elected-process-for-t`), which stacks on this one.

## What exists today

- `forge-journal.jsonl` per project: the forge hub appends one line per merge the record does not
  hold and per CI turning red on a PR ready to merge; the board's PRs page appends `merged` lines.
- CR-383 (config) and CR-384 (session events) add `board` and `config` lines for the Chief of
  Staff's and the Griller's watchers.
- `chantier watch --after n` reads its project's journal from a cursor and ends 20 s after the
  last new line, which wakes its session. Every line wakes every watcher of the project: a line
  says what happened, never whom it is for.

## The foundation asked

One typed, versioned event line, written to one journal per project, that says whom it is for,
and a watcher that wakes only on the events for it, with the wake rules (buffer, filter, rate
limit) in one place. Built now: the line, the audience, the watcher's filter, the migration of
today's lines. Not built: any new audience's watcher (Foreman, Driver), user notifications,
delegated actions.
