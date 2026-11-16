# Intent: the Chief of Staff keeps its rules, through compaction

## The problem

The Chief of Staff's rules live in the cards. After a context compaction the session keeps only a
summary of them and acts against rules it no longer sees. On 2026-11-10, while it steered batch-09
in direct mode, it:

- grilled while its batch ran;
- offered the user, on Remote Control, options they could not take: Foreman mode, a terminal
  command, a local URL.

## What the CR changes (Claude Code only)

1. **What the steering session may do while its batch runs.**
   - It may do any work on the backlog's files: file, triage (directly or for a Griller),
     reorganise, merge, drop.
   - It may start the spec-writer on a CR that is already grilled.
   - It does not grill, and does not touch the running batch.
   - The cards say this, in place of today's stricter line that forbids triage and discussion.
2. **The reload.**
   - **Manual:** "chantier reload", in plain text or as `/chantier:chantier reload`. It reads the
     skill and its cards again, and `foreman.md` and the host's reference while steering a direct
     batch. It gives no introduction and touches nothing in the batch.
   - **Automatic:** the plugin's hooks module reloads the same cards at every compaction, manual or
     automatic, with no word from the user and without relying on the model noticing it.
   - After an automatic reload, the next answer starts with one line saying the rules were
     reloaded.
   - No new CLI gate: the CLI keeps refusing only what touches the batch.
3. **The options the Chief of Staff offers, by environment.**
   - A checklist in the cards gives each option, where it can be done from (phone on Remote
     Control, desktop app, terminal), and why.
   - When the host signals where the user is, the Chief of Staff offers only what the user can do
     from there.
   - When the host says nothing, it offers every option that fits, each with its condition.
   - A first draft of the table is in `intake/options-by-environment-request.md`.

## Where the information lives

- **The shared cards** hold what holds on every host:
  - the rules of point 1;
  - what a reload reads and does;
  - the general rule for offering options.
- **The host's reference** holds what is the host's:
  - how the automatic reload is triggered;
  - the surfaces and how the host signals where the user is;
  - each option's condition on that host.
- **`hosts/copilot.md`** gets the same sections, marked "not done yet" with the reason. The later
  Copilot CR fills them without reorganising anything.

## Out of scope

- Copilot's own behaviour: left to another CR, which only fills its sections.
- Adding several CRs to a paused batch: split out again as the P1 CR `add-several-while-paused`.
