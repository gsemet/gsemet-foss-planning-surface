# CR-296 handoff (paused by the user, 2026-11-16)

User order: stop, push the PR as a draft, record findings for a later takeover. Stop-and-package only;
no new coder, Inspector, Verifier, gate or model experiment ran.

## State
- Draft PR: https://github.com/gsemet/chantier/pull/247 (verified OPEN and draft).
- Snapshot head: `97490a33ee23d394e02d2f9b72120be4a01c69dd`.
- Branch chantier/batch-20/cr-296-proposal-improve-skill-boot, base origin/main 5eb0c1e. Rounds 6 of 6 spent;
  a seventh needs a new user authorisation.
- One snapshot commit holds all r1-r6 edits (draft PR, WIP). Not ready to merge.
- No worker is running: the round-6 generic Coder completed before the stop.
- Orchestration is stopped and CR-296 is blocked. The CLI refused
  `pause --batch 20 --epoch 1` because CR-296 is not merged, despite no live
  or queued worker and no pending order. Batch metadata therefore still says
  running; do not infer an active worker or restart from that label. No
  cancellation, merge or manual state edit was used to bypass this limitation.
- uv.lock identical to base; changed and new files scanned for secrets, tokens, internal URLs: no match.

## Model evidence
- r5: named Coder, override gpt-6.1-sol replaced by the host with gpt-5.6-luna
  ("Required model enforcement replaced requested model ...").
- r6: generic agent, task with model gpt-6.1-sol. Host event log of the steering session
  (subagent.started / subagent.completed): model gpt-6.1-sol, firstDispatchedModel gpt-6.1-sol,
  modelSelectionSource explicit_override. Read after the run: not a pre-execution validation.

## Findings still open
1. r5 (Luna) and r6 (Sol) edits have had NO Inspector review. Last Inspector verdict: r4 FIX-REQUIRED.
   The r6 Coder claims the four r4 blockers and the minor one fixed (work/coder/r6.md): safe liveness,
   router reload max 12,258 <= 12,288 (30 bytes margin), deterministic join-watch test, Foreman host
   Startup core counted, truthful body. All unreviewed claims.
2. No long gate, no CI, no Verifier at the pushed head.
3. Local macOS `just scenario`: parallel 211/212 and surface-board 153/154 fail, identical on origin/main
   (r4 baseline). The project long gate is CI job `just scenario (ubuntu-latest)`; not run yet.
4. `just validate chantier` from the surface skips Chantier (no index.md): not content validation.
5. Real Claude Code / Copilot sessions untested; Windows only simulated.
6. Reload margin is 30 bytes: rerun test_startup_manifest.py after any mandatory prose change.

## Tests the Coder reported (the Driver re-ran none)
- env UV_NO_CONFIG=1 just check: 258 passed.
- startup_manifest + board tests: 30 passed.
- watcher pair, 100 runs: 200/200 (command in work/coder/r6.md).

## Restart
Work is stopped at the user's request (see the CLI pause limitation above). Obtain an explicit resume
instruction before starting any review, gate or worker; any seventh coding
round also requires a new round grant.

1. Read work/r4.md, work/coder/r6.md, this file, 03-change-spec.md, last two sections of 02-answers.md.
2. Fresh named inspector on the diff against origin/main, with the r4 blockers.
3. If approved: rebase, env UV_NO_CONFIG=1 just check, CI `just scenario (ubuntu-latest)` green, named
   verifier at the pushed head, update PR body boxes. hooks/types untouched: no `just mod`.
4. Never change global uv config; keep uv.lock at base. Do not use the named Coder with a model override
   on this host (enforced to Luna).
