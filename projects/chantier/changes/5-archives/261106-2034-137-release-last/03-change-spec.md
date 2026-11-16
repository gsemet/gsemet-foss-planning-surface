# A release CR depends on every other CR of its batch

## Problem

A release CR exists only through `open --release`: a running batch cannot take one. Its rule,
`others_merged` in `rails.py`, is separate from `after`, so `status` shows no wait on it. And
nothing holds it back for what only the end can settle, such as the version.

## Change

### The release's `after`

The release CR's `after` holds every other CR of the batch that has not ended, fix CRs excepted:
`pending_fixes` keeps ruling those. The CLI writes it, in `open --release` and in `order add`:

- `order add --release --note <folder>` adds the batch's release CR, with the default grant (each
  irreversible action waits for the user), and fills `batch.data["release"]`. A second one is
  refused while the first has not been cancelled. `order grant` and `order approve` then apply.
- `order add` appends the new CR to the release's `after`.
- `order after <release>` is refused: the CLI keeps that list.
- A CR that would wait for the release is refused as a cycle, naming it.

### What is met

For a release, an `after` entry is met only when `merged` or `cancelled`: `waits_for` tells a
release by its `kind`. `ready` does not meet it; for any other CR `after` does not change. A dropped
or cancelled CR stays in the list as history and stops being waited for. `status`, `STATUS.md` and
the board show the wait through the existing `waits`, with no code of their own.

`others_merged` goes; `check_take` still refuses a release while `pending_fixes` has one, and its
message says "merged or cancelled", not "ready or merged".

### Settled at the end

A release that shares its batch with another CR starts only on the user's word, given once the
others have ended:

- `order confirm <release> --note "<the version and what else was settled>"` records it on the CR
  and in its notes; `check_take` refuses a release without it. It is refused while `after` is unmet.
- `status` shows the wait for that word once `after` is met.
- A CR added after the confirmation voids it, since what ships changed.
- A release alone in its batch has been grilled just before: no confirmation.

The specification of a release filed early says what is known; the Chief of Staff completes it at
the confirmation.

### Once the release has started

`order add` is refused once the release has started, whichever state it is in now: `attempts` says
so, since a merged release PR puts the CR back to `queued`. The message names the two ways out: a
fix (`--fix-for`), or the next batch. Once the release has ended or been cancelled, `order add`
works as it does today and touches no `after`.

### Text

- `handoff`: the `after` line says a release starts from the default branch, not from "the last one
  still open".
- `order --help` and the usage messages name `add --release` and `confirm`.
- `chief-of-staff.md`, Releases: a release may join a running batch; what is filed early and what
  is settled at the end; when the Foreman's question comes, grill the version from what was merged,
  complete the specification, then `order confirm`.
- `foreman.md`: once the others have ended, ask the Chief of Staff for the release's confirmation,
  then start the Release driver.
- `concepts.md` and the README follow if they describe a release's start.

## Out of scope

The Release driver's procedure, the grant's meaning, the meaning of `after` for any CR that is not
a release.

## Done when

The scenario shows, on a batch with a release added by `order add --release`:

- The release waits for each CR, one added later included, and `status` says so.
- A `ready` CR keeps the release waiting; a merged one and a dropped one do not.
- With every other CR ended, a take is refused until `order confirm`; a CR added then voids it.
- `order add` is refused once the release has started, and again after its PR merged and it went
  back to `queued`; `order add --fix-for` still works.
- `order after <release>` and a second `--release` are refused.
- `open --release` alone in its batch starts with no confirmation.

`claude plugin test .` and `just check` pass; the CLI changes, so `just scenario` passes too.
