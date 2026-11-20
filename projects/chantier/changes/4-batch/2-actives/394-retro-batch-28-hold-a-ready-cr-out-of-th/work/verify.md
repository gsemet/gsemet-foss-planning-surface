# Verify CR-394 (hold a ready CR out of the stack), round 3 move

Head: ce7a7ef31aacda5a61ccd3ecd20d6efb58a5d7a8

Move judged: b2793ce1..ce7a7ef3 (rebase with conflict resolved in stacks.py onto CR-393 960cdb80, plus
round 3: `start_base` falls back for an ended `start_on` owner, a held owner goes to the default branch).
CLI runs used the worktree's code on a scratch git repository (bare origin, `open --mode stack` of three
CRs, record set ready with PRs 1-3, CR-103 started on CR-102's branch), removed at the end; the live
planning folder was never named.

## Claims, judged at ce7a7ef3

1. Hold/unhold through the CLI, re-proved. PROVED.
   - `order hold CR-102`: `CR-102 held out of the stack (order O-1): the Foreman takes the stack driver to take it out of the forge stack; \`order unhold CR-102\` puts it back`; record: `[('CR-101', None, True, None), ('CR-102', 'O-1', False, None), ('CR-103', None, True, None)]` (held, stacked, start_on; CR-103's start_on unset).
   - second `order hold CR-102`: `error: CR-102 is already held (order O-1)`.
   - `stack`: `the stack of batch batch-01: CR-101 -> CR-103`, CR-103 base `b/cr-1`; `status` prints `held: CR-102 (order O-1) out of the stack, PR https://github.com/o/r/pull/2 on main: \`order unhold CR-102\` puts it back`, and CR-102's label `PR in draft`.
   - `stack CR-102`: `error: CR-102 is held out of the stack (order O-1): \`order unhold CR-102\` first`; `stack --out-of-draft CR-102`: `... unhold it first (\`order unhold CR-102\`)`.
   - `order unhold CR-102`: `CR-102 back in the stack, on top: ...`; `order` 4 = max(1,2,3)+1; `stack`: `CR-101 -> CR-103 -> CR-102`; a second unhold: `error: order unhold: CR-102 is not held`.
2. Tests the move touched, at ce7a7ef3: `pytest tests/test_stack_hold.py tests/test_stack_base.py tests/test_mode_switch.py tests/test_carry_ship.py tests/test_gate_carry.py -q` -> `68 passed in 48.52s` (covers the held-owner `start_base`, the ended-owner fallback, the other held refusals, forge-stack rebuild with the fake forge). PROVED.
3. Cards (previously failing point), read at ce7a7ef3. PROVED.
   - `driver.md` "A CR held out of the stack" now holds six steps: PRs above to draft first; commits taken out of the CRs above (steps 2 and 3 of "Removing a dropped CR", which exists at line 1055; a working CR's Driver does it); held branch rebased on `origin/<default branch>`, pushed `--force-with-lease`, `ship`ped, top-of-stack case; its PR to draft, never out of draft; `stack <cr>...` then `forge-stack rebuild`; read-back (five checks), local gate at the mergeable top, mergeable part ready again; clean-rebase carry and conflict-resolver rule; `unhold` as "A draft that turns ready to merge"; final-order take orders only `chain`. Matches the specification.
   - `chief-of-staff.md`: hold/unhold words, the ask when out-of-stack vs out-of-batch is unclear, held CRs named in reports, the batch stays open at its end, release blocked: name it, offer `order unhold` or `order drop`, act on the user's answer only. Matches.
   - `foreman.md`, `concepts.md`: unchanged by the move; carried from b2793ce1 (match the specification).
4. Claims untouched by the move, carried from b2793ce1: section 1 refusals (nothing written), `order merged` of a held CR and of the release, mode switch unsetting `held`, forge-stack held PRs (tests above re-ran them at ce7a7ef3, all pass).
5. CI at ce7a7ef3 (`gh pr view 365`): `just check` ubuntu, macos, windows, `just scenario (ubuntu-latest)`, `just eval-dry-run (ubuntu-latest)`: all SUCCESS.
6. PR description (head ce7a7ef3, base CR-393's branch): Known gaps names the missing pane screenshot; no image; the Test plan still holds `<sha7>` placeholders and unticked Review/Verified/CI boxes, to be filled by the Driver after this verdict (carried note from the earlier judgment, not a content failure).

Pane screenshot: known gap, named in Known gaps (not judged). Before/after evidence: no UI; the CLI transcripts above are the proof.

VERIFIED

## Description-only pass, PR #365 as posted, judged at ce7a7ef31aacda5a61ccd3ecd20d6efb58a5d7a8

Head: ce7a7ef31aacda5a61ccd3ecd20d6efb58a5d7a8

- Posted body equals work/pr-body.md (diff: one trailing blank line only). Sections in template order; Known gaps names "No screenshot of the pane from a real session"; no image; no role name outside Internal references.
- Test plan: tests exist (tests/test_stack_hold.py, 373 lines in diff). Gate log 20261120-023856.log first line names CR-394 at ce7a7ef31aac..., "result: pass at ce7a7ef..." (just scenario). just check and eval-dry-run at a476dc3: log note "just check and just eval-dry-run pass at a476dc36", gates/evd.log "18 of 18 cases as expected", check4.log 907 passed. Review: `log` note "r3 approved at a476dc36, committed as ce7a7ef3". Verified at ce7a7ef: verdict VERIFIED event at ce7a7ef. CI: `gh pr checks 365`: check x3, scenario, eval-dry-run all pass at head ce7a7ef.
- Summary/Changes match the diff stat (22 files incl. orders_hold.py, orders_word.py, stacks.py, forge_stack*, cards, scenario).

VERIFIED
