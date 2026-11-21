# Verify CR-430 (park-live-cr)

Head: 6fb2b356b48569532a05531d583e91ace39af274

All claims judged at 6fb2b356 (6fb2b35), the pushed head, with the worktree's code
(`uv run --no-sync --project <worktree> chantier`) on scratch projects under `work/scratch`
(removed at the end).

## Claims proved

1. `park` refusals (6fb2b35). Scratch stack batch, 4 CRs, 2 slots:
   - queued CR: `error: park: CR-101 is queued: only a working or blocked CR is parked` (exit 2).
   - working, no wait: `error: park: CR-102 has no outside wait recorded: --wait answer=<question>|approval|pipeline|merge` (exit 2).
   - bad type: `--wait: bogus is not a wait type: answer, approval, pipeline or merge` (exit 2).
   - already parked: `error: park: CR-102 is already parked (since 18:37)` (exit 2).
   - held, release, fix, ready, merged, cancelled: `pytest test_park.py::test_park_refuses_and_writes_nothing[...]`, 6 parametrized cases PASSED (held text checked before status; nothing written).
2. `park` of a working CR with `--wait "answer=does the trial pass?"` and an agent recorded (6fb2b35):
   `parked CR-102: waits for w1 answer ...; its slot is free and the batch goes on without it; it comes back on top once the wait is cleared`,
   `stop its Driver if it still runs, then \`agents set CR-102 - --epoch <n>\``, `stack: \`take stack --note "park: CR-102"\``.
   Record: CR-102 `blocked`, `blocked: parked: w1 answer ...`; `status` slots `live 1/2`; the old lease: `error: claim lost: CR-102's lease 1 ended at 18:37; stop now: nothing recorded` (exit 3); `take CR-103` accepted (2 of 2 slots held); `log`: `foreman park waits=['w1']`.
3. `handback CR-102 ready ...` of the parked CR: `error: handback: CR-102 is parked (since 18:37): take it back first (\`take CR-102 --note "wait cleared: <what>" --epoch <n>\`)` (exit 2).
4. `take` of a parked CR with an open wait, and `access`: `error: CR-102 is parked, waiting for w1 answer ...: \`wait CR-102 clear w1 --epoch <n>\` first` (exit 2); `access CR-102`: `claim: refused: CR-102 is parked, waiting for w1 ...`.
5. Wait cleared (6fb2b35): `wait CR-102 clear w1 --epoch 1`, then `status`: `parked: CR-102 wait cleared: take it back before any queued CR (\`take CR-102 --note "wait cleared: <what>" --epoch <n>\`)`, step `parked: wait cleared`. Take with the agent still recorded: refused (`agents set CR-102 - --epoch <n>` first); with no free slot: `error: no free slot for CR-102: 2 of 2 held`; with a free slot: `took CR-102 (2 of 2 slots held), lease 2 ...; back on top of the stack`; record: CR-102 `working`, order 5 above every CR including queued CR-104 (order 4), `parked` unset, round 0.
6. `close` with a parked CR (scratch 2, CR-101 merged, CR-102 parked on `answer=which colour?`): `error: cannot close batch-01: CR-102 is parked (w1 answer ...): its wait cleared (\`wait CR-102 clear w1 --epoch <n>\`), then \`take CR-102 ...\`; or send it out (\`order drop <cr> --note <trash|P1..P4|3-ready>\`). Nothing was deleted.` (exit 2). After `order drop CR-102 --note P2`: `CR-102 was parked: no stack driver needed`, then `paused batch-01: every CR is merged or cancelled`.
7. Tests at 6fb2b35: `pytest test_park.py test_park_back.py test_park_close.py test_park_pane.py test_park_shared.py test_park_stack.py test_came_back.py -v`: `49 passed in 18.77s`. They cover: dependents, `apart_owner` and the base rule (held and parked), series cases (queued third, started third a dependent), stack reads and `stack` / `--out-of-draft` refusals, forge-stack `waiting`, coming back in stack and series with chains kept, drop of a parked CR in stack, series and parallel, close and batch-end ways back (open, cleared, held, infra, release, dependents), release refusal in stack and parallel, pane words (`Parked`, phase, now/next), cards (`test_the_cards_name_the_park_and_its_way_back`).
8. Gate and CI (the Driver's `log`, at 6fb2b356): `gate result=pass head=6fb2b356b48569532a05531d583e91ace39af274 command=just scenario`; `gh pr checks 400`: macos, ubuntu and windows `just check`, `just eval-dry-run`, `just scenario (ubuntu-latest)` all `pass`; PR 400 is a draft, headRefOid 6fb2b356b48569532a05531d583e91ace39af274.
9. Description (6fb2b35): the posted body equals `work/pr-body.md` (one trailing newline apart); Summary, Deliverables and Changes match the 49-file diff; Known gaps names the missing pane screenshot and the test-file placement; no image attached.

## Pass 2 (description-only, head unchanged at 6fb2b356b48569532a05531d583e91ace39af274)

Claims 1 to 9 above: carried from 6fb2b35 (head unchanged, no move since).

10. Review box (6fb2b35): the posted body (`gh pr view 400 --json body`) reads `Review: approved at 18f2ac2 (round 2), then rebased onto 3b3eba0 as 6fb2b35; the conflicts in routing.md and the svg were resolved after the review`. `chantier log CR-430` holds `driver note r2 inspector approved at 18f2ac2b62f429b41e5327608f86eb21e24717b1`, the SHA the box cites; the rebase and the conflict resolution are named in the box and in the note `rebased onto origin/main 3b3eba06 (routing.md and svg conflicts resolved ...)`. Proved. The box is honest that the review did not cover the rebased head; the other claims are proved above at 6fb2b35.

VERIFIED

## Description-only pass (head 6fb2b356b48569532a05531d583e91ace39af274)

Judged at 6fb2b356 from `gh pr view 400 --json body`, `chantier log 430`, `gh pr view 400 --json statusCheckRollup`
(5 checks SUCCESS at the head), gate log first line (`gate CR-430 ... head 6fb2b356...`).

11. Boxes and SHAs: gate pass, CI, Review (18f2ac2 has an approval note), Verified: true.
12. Known gaps: complete (pane screenshot, test file placement); no `**UNVERIFIED:**` claim without a bullet.
13. Internal references: FAILED. The Test plan's Review line (outside Internal references) reads
    `Review: approved at 18f2ac2 (round 2), ...`: "round" is an internal reference that the pr-template
    rule (no round outside Internal references) forbids. Role names (Foreman, Chief of Staff, stack driver,
    Driver) are product terms of cards the diff changes: allowed.

NOT VERIFIED

## Description-only pass at 6fb2b356b48569532a05531d583e91ace39af274

Head: 6fb2b356b48569532a05531d583e91ace39af274

- PR 400 body (`gh pr view 400 --json body`), judged at 6fb2b35 against the pr-template audit: sections in order, fold with blank lines and nothing after it, no internal reference outside Internal references (the word "round" is gone; role names are product terms of the changed cards), Deliverables has a flowchart, Changes and Impacts match `git diff --name-only 3b3eba06 HEAD` (park.py, declare/park.py, stack_apart.py, status/now_next.py, test_park*.py, test_came_back.py, cards, docs, scenario), Known gaps present. Review box: `$CHANTIER log 430` holds "r2 approved at 18f2ac2b... committed as 3b3eba06" and the box cites 18f2ac2 with the rebase to 6fb2b35.
- Verdict: VERIFIED
