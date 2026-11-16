# Change Specification: a landed batch is paused, and takes new CRs in direct mode too

## Goal

A batch that ran `land` but not `close` is **paused**: the steering session has nothing running,
the Chief of Staff can grill the ideas stacked in the inbox, and `order add` of a grilled CR sets
the same batch running again. This already works in Foreman mode; this CR makes it work for a
direct batch, and says it plainly in the cards. There is no new state: "paused" is the landed
state, named.

## What changes

### 1. The CLI (`skills/chantier/scripts/cli/src/chantier/commands.py`, the `order` command)

Today `order add` and `order qa` exit 3 ("a direct batch is strict: switch to Foreman mode to add
work") on any direct batch, landed or not. New rule:

- On a **landed** direct batch, `order add` and `order qa` are accepted and reopen the batch
  exactly as on a Foreman batch (the existing `reopen` path: status `open`, landing and summary
  dropped, event `reopen`, the line "batch-<n> was landed: running again; `land` runs again at
  the end").
- On a **running** (not landed) direct batch they stay refused, with a message that says when it
  will be accepted, e.g. "a running direct batch is strict: add the CR once the batch has landed
  (`land`), or switch to Foreman mode".
- **The release exception:** `order add --release` (and `order add --fix-for <release-cr>`) are
  accepted on a running direct batch: a release CR needs no real grill.
- Foreman batches: unchanged.

### 2. The cards

- `skills/chantier/references/concepts.md` (Batch, the sentence "a direct batch is strict:
  `order add` and `order qa` are refused"): a running direct batch is strict, except a release
  CR; a landed batch, of either steering, is paused and takes new CRs, which set it running
  again.
- `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself" and "While it
  runs": ideas that arrive while a direct batch runs are filed in the inbox (`file`, no grill);
  once the batch has landed, it is paused: grill them with the user, and on the user's word add
  them to the same batch (`order add --note <folder>`), which runs again; `close` stays the
  user's word. A release CR may join a running direct batch.
- `skills/chantier/references/init.md` (the direct-mode sentence of the tour): add that a landed
  batch takes the next grilled CRs.
- The host references and the docs diagrams: only if they state the old rule (grep "strict").

### 3. The scenario

`just scenario` covers it: a direct batch that lands, then `order add` reopens it and a CR runs;
`order add` on a running direct batch is refused; `order add --release` on a running direct batch
is accepted.

## Out of scope

Pausing a batch while Drivers run (stop and resume them): not wanted; the pause is the landed
state only.

## Evidence

The scenario steps above pass; the refusal message on a running direct batch reads as written;
`just check` passes on the three systems (CI).
