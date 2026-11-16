## Why

A release CR existed only through `open --release`: a running batch could not take one. Its rule,
`others_merged`, sat apart from `after`, so `status` showed no wait on it. And nothing held a
release back for what only the end can settle, such as the version.

## What changes

- `order add --release --note <folder>` adds the batch's release CR to a running batch, with the
  default grant. A second one is refused unless the first was cancelled; `--fix-for` with it is
  refused.
- The release's `after` holds every other CR of the batch, fix CRs excepted. The CLI writes it, in
  `open --release` and `order add`. `order after <release>` is refused, and a CR that would wait
  for the release is refused as a cycle naming it (`order after`, `depends.json`).
- For a release an `after` entry is met only when `merged` or `cancelled`; `ready` does not meet
  it. `after` does not change for any other CR. `others_merged` is gone: `status`, `STATUS.md` and
  the board show the wait through `waits`.
- `order confirm <release> --note "<the version and what else was settled>"`: a release that
  shares its batch starts only on this word, given once the others have ended. `status` shows the
  wait for it, `take` refuses without it, and a CR added afterwards voids it, with a note and an
  event. A release alone in its batch needs none.
- `order add` is refused once the release has started, whichever state it is in now, and names the
  two ways out: `--fix-for`, or the next batch. Once the release has ended or been cancelled,
  `order add` works as before.
- Text: `handoff`'s `after` line, `order --help` and the usage messages, `chief-of-staff.md`,
  `foreman.md`, `concepts.md`, `scenario/README.md`.
- Scenario: section 14 confirms before its take; a new section 14c covers each case below.

## Decided within the specification

- A release is alone when no other non-fix CR has ever been in the batch, whatever its state; one
  that gets an `order add` is shared from then on.
- Only a non-fix `order add` voids a confirmation; `--fix-for` does not.
- `order confirm` is also refused on a release alone, started or ended; given again before the
  start, it replaces the earlier word.
- "Started" for `order add` is `attempts` above 0, or a state neither `queued` nor ended: a Driver
  holding the release before its first attempt counts.

## Out of scope

The Release driver's procedure, the grant's meaning, the meaning of `after` for any CR that is not
a release.

## Evidence

The real CLI in throwaway git repositories with the scenario's fake `gh`, the same transcript on
both sides: before is `c4aac8e`, the commit under this one; after is `6b5b7c3`.

| Case | Before (`c4aac8e`) | After (`6b5b7c3`) |
| --- | --- | --- |
| `order add --release` on a running batch | usage error, exit 2 | `added CR-104 (release), queued, after CR-103`, default grant |
| `status` of a release with other CRs open | no wait shown | `waits for CR-101 ready, CR-102 queued`; `take` refused, "it starts once each is merged or cancelled" |
| `take` of the release, the others merged or cancelled | it starts | refused, "needs the user's confirmation (`order confirm`)"; passes after `order confirm` |
| `order add` once the release has started | accepted | refused, naming `--fix-for` and the next batch; refused again at `queued`, attempts 1, after its PR merged; `--fix-for` accepted in both |

The after alone, observed by command:

- a CR added after `order confirm` voids it, and `take` is refused until a new one;
- a merged CR and a dropped CR are no longer waited for; a CR added later joins `after`;
- `order after <release>` and a second `--release` are refused;
- a CR that would wait for the release is refused as a cycle naming it, by `order after`, and by
  `depends.json` in `open` and in `order add`;
- `order confirm` is refused while `after` is unmet, once the release has started, and on a
  release alone;
- `open --release` alone starts with no confirmation;
- a confirmed release back at `queued` after its merged PR is taken with no new `order confirm`.

Checks at `6b5b7c3`:

- `just check`: 28 tests passed;
- `claude plugin test .`: 20 passed, 0 failed;
- long gate `just scenario`, local on Windows: 294/294 on `gh`, 294/294 on `glab`;
- CI: `just check` passes on Linux, macOS and Windows, `just scenario` on Linux, none skipped.

Not shown: a release put back to `queued` by a merged fix, as the Release driver's procedure does
it; the confirmation stayed on the CR through every state change seen. The transcripts stay in the
CR's folder, `work/verifier/evidence/` (`before-after.md` lists each pair).
