# CR-137 before / after (real CLI, throwaway git repo, fake gh)

Before = detached worktree of c4aac8e. After = the CR worktree at 6b5b7c3. Same driver script
(`drive.py` in the Verifier's scratchpad, built on `scenario/run_scenario.py`'s World). Transcripts:
`before.md` (section A), `before-B.md` (section B, before), `after.md` (A, B, C), `after-D.md`, `after-E.md`.

| # | Step | Before (c4aac8e) | After (6b5b7c3) |
|---|------|------------------|-----------------|
| 1 | `order add --release --note <folder>` on a running batch | exit 2, argparse usage error (unknown flag) | exit 0: "added CR-104 (release), queued, after CR-103; ... starts on `order confirm`"; `batch.release` filled, default grant |
| 2 | `status`, batch made by `open --release 3` | `CR-103 queued r0/3 - release \| -` (no wait) | `CR-103 ... release \| waits for CR-101 queued, CR-102 queued`; with CR-101 ready: `waits for CR-101 ready, CR-102 queued` |
| 2b | `take` release while a CR is `ready` | refused, "releases what is merged..." (others_merged) | refused, "waits for CR-101 ready, CR-102 queued: it starts once each is merged or cancelled" |
| 3 | `take` release, others merged/cancelled | exit 0, release starts | exit 2 "needs the user's confirmation (`order confirm`)"; status shows `waits for the user's confirmation`; after `order confirm CR-103 --note v1.5.0` take exit 0 |
| 4 | `order add` after release started | exit 0 (CR-104 added) | exit 2 "CR-103 has started (working, attempts 0) ... Add a fix with `order add --fix-for CR-103`, or put the new work in the next batch"; `--fix-for` exit 0 |
| 4b | same after release PR merged, back to `queued`, attempts 1 | (the plain add was already consumed by step 4, exit 1 "prepared CR not found": artefact, not a refusal) `--fix-for` exit 0 | exit 2 "has started (queued, attempts 1)"; `--fix-for` exit 0 |

## The after alone (all observed in `after.md`, `after-D.md`, `after-E.md`)

- A CR added after `order confirm` voids it: `confirmed` gone, note "confirmation voided: CR-106 was added", take refused ("waits for CR-106 queued"); after drop + new confirm, take passes.
- Merged (CR-103) and dropped (CR-105) are met; `ready` keeps waiting.
- Later-added CR is appended to the release's `after` (`['CR-103','CR-105']`), shown by `status`.
- `order after CR-104 --note CR-103` refused ("the CLI keeps what it waits for"); `order after CR-105 --note CR-104` refused as a cycle naming CR-104; second `order add --release` refused (one per batch, next batch named).
- `order confirm` refused while after unmet ("still waits for ..."), after start ("has started or ended"), and alone in its batch ("alone in its batch, it needs no confirmation").
- `open --release 1` alone: status shows no wait, take exit 0 with no confirmation.

## The two points the scenario does not show

(a) Confirmed release taken again without a new `order confirm` (`after-D.md`, 2 slots): release confirmed 'v1.5.0', fix merged (release stays confirmed), release PR merged -> `queued`, attempts 1, `confirmed='v1.5.0'` kept. A new fix then blocks the take ("a fix of the release must be merged or cancelled first", correct, pending_fixes); once that fix is dropped, `take` of the release exits 0 with no new confirm. (Ids shift between runs; in D the CR taken is the release.)
(b) `depends.json` naming the release: by `open` exit 2 "CR-107: depends.json names 'release-v2-0-0', the batch's release CR CR-108, which waits for every other CR: a cycle. Remove it from depends.json" (`after.md` section C); by `order add` (release not started) exit 2 with the same message, CR not added (`after-E.md`). The release is named in both.

## Not shown, and why

- A fix merged putting the release back to `queued` (as opposed to a merged release PR): that route is the Foreman/Release driver's procedure, outside the CLI frame; the confirmation is kept on the CR in every state change seen.
- The long gate: not rerun; the Driver's log at work/gates (6b5b7c3) was not rerun by me.
- Two script artefacts in `after.md` section B (a scripted driver tried a round on a CR with no free slot) and `before-B.md` (a `fix.py` write into an uncreated worktree): the transcripts stop there; they are harness limits, not CLI faults. D replaced B8-B10 for the after.
