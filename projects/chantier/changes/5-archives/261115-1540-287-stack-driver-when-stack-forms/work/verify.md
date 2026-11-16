# Verify CR-287

Head: 67b19d49316e06a169f1acd531a3541fe2f7c6a1

Later pass: move a246c37..67b19d4 (rebase onto main 242aa63, conflict resolved in e8158be, inspector approved e8158be per `chantier log`). Judged at 67b19d4, worktree clean.

1. Stack unit, scenario checks 1-5 of the spec's Evidence (touched: the base changed commands/driver.py, commands/facts.py, stacks.py).
   Command: `uv run --locked python scenario/run_scenario.py --unit stack` (log: work/verifier/stack-67b19d4.log)
   Output: `| stack | github | 137/137 | 672 | 239.2 | 640 | ok |`, exit 0 (all checks of the earlier pass still present, plus main's new ones).
2. Code matches spec sections 1-3: `git diff 242aa63 HEAD -- commands/driver.py commands/facts.py` shows the merged import (`draft_waited` and `start_on_for` kept), `_take_stack` extracted with unchanged behaviour, `start_on` recorded at first take of a queued CR, `_off_place_tail` in `stack_lines`. [x]
3. Cards/docs sections 4-5: `git diff 242aa63 HEAD --stat` shows the same 15 files as before (concepts.md, foreman.md, driver.md, README, docs, scenario); conflict file reports the carry wording intact. carried from a246c37: no agent file changed, doc content unchanged by the move beyond the auto-merge.
4. CI: `gh pr checks 242` at 67b19d4: all five pass incl. `just scenario (ubuntu-latest)`.
5. Description (posted): Summary, Changes, Known gaps "None" match the diff. FAIL to fix in the description pass: the Test plan boxes still name `a246c37` ("Local gates", "Review", "Verified", "CI green"), a SHA not in 67b19d4's history; the Driver's ship check says the same. This is a description item, not a code failure; re-run the description pass after the boxes are updated.
6. Evidence: none to capture (no UI, no pane field); not applicable.

VERIFIED (code at 67b19d4; description pass pending the box update)

## Description pass (PR 242 body as posted, judged at 67b19d4)

- Test plan boxes now cite 67b19d4; Review box e8158be matches the Driver's note "move a246c37..e8158be (conflict) inspector approved at e8158be" in `chantier log`; 842b800 note present. OK.
- Layout, fold, sections, Known gaps "None" (no UNVERIFIED claim, no uncaptured evidence): OK.
- FAIL: Autonomous decisions says the stack unit "runs in 303 s locally, under its 320 s budget". At 67b19d4 the unit's budget is 640 s and the measured run is 239.2 s (`| stack | github | 137/137 | 672 | 239.2 | 640 | ok |`, claim 1 above); 303 s / 320 s was measured at a246c37 and was not carried. The "24 commands" figure has no proof at this head either. Fix: state 239.2 s against its 640 s budget at 67b19d4 (or drop the figures).
- Minor: Test plan items "New or changed tests", "Local gates", "Evidence" are unchecked although proofs exist; Evidence names no SHA.

NOT VERIFIED (description only; code verdict above stands at 67b19d4)

## Description pass 2 (gh pr view 242 --json body, headRefOid = 67b19d49316e06a169f1acd531a3541fe2f7c6a1)

- Autonomous decisions now states 137/137 in 239 s under 640 s at 67b19d4: matches claim 1 above (`| stack | github | 137/137 | 672 | 239.2 | 640 | ok |`). The 303 s / 320 s / 24 commands figures are gone. OK.
- Review box `e8158be`: `chantier log 287` line "move a246c37..e8158be (conflict) inspector approved at e8158be9620c1e97b20bf30c87a2c8f7fe1f7132". OK.
- CI box: `gh pr checks 242` shows 5/5 pass at head 67b19d4. OK.
- Summary, Deliverables, Changes match the diff (checked in the earlier pass at this head); sections and details fold render; no images; no STALE mark; Known gaps "None" with no UNVERIFIED claim left. OK.

VERIFIED
