# Verify CR-398

Head: 995a6b073183c5c5376aa3b50576781113a2b323

All claims judged at 995a6b0 (`git rev-parse HEAD` in the worktree; `gh pr view 367 --json headRefOid` gives the same).

1. Card budget and manifest/prompt tests, 995a6b0: `pytest tests/test_startup_manifest.py tests/test_driver_prompt.py -q` -> `42 passed in 11.06s`.
2. Common-path bytes, 995a6b0: own sum of the opening plus each `driver.md#` section under `actions["cr-driver"]` -> `44758` (<= 45,000; PR body says 44,757, one byte of counting difference, immaterial).
3. `just check` at 995a6b0 -> exit 0, `912 passed, 1 skipped`, `release-notes ... ok`.
4. `just eval-dry-run` at 995a6b0 -> exit 0, `dry run: 18 of 18 cases as expected`.
5. Scenario strings, 995a6b0: `git diff` shows the new `driver_liveness` check (100,000 tokens, three `closing:` notes, foreman's second `context: closing:` ask); CI `just scenario (ubuntu-latest)` green at this head per the Driver (not rerun here).
6. Closing paragraph vs spec section 3, 995a6b0 (driver.md lines ~799-836): closing note kept as a checkpoint; below 100,000 the same Driver closes in order (evidence/boxes/audit/post, description pass, ready then ship, handback); 100,000 or more or `context: not measured` hands off with `blocked context: closing: ...`; one note per step (`closing: body posted at <sha7>`, `closing: description pass VERIFIED at <sha7>`, `closing: PR ready` / `PR kept draft on <base>`); the 130,000 rule applies during closing. `grep "whatever the context size\|never hands off for the closing again" -r skills` -> no match (both old sentences removed). Spec's steps 1-2 and 5-6 are grouped into 4 numbered steps with the same order: a matching presentation, not a rule change. Matches.
7. foreman.md, 995a6b0: diff shows the hand-off narrowed to 100,000+ or the context rule, restart path unchanged, and the second `context: closing:` hand-back with no new step note is `question <cr> driver out of context twice`. Matches spec.
8. Prompt line, 995a6b0: `driver_prompt.py` diff prints `  Card: {refs}/{card}: its Startup core now, each other section when its step comes, as the card's opening says;`; worker prompts untouched (not in the diff stat).
9. PR body (work/pr-body.md), 995a6b0: Summary, Deliverables (before 74,666 matches spec; after 44,757 ~ 44,758), Changes (driver.md, manifest, foreman/concepts/host refs, driver_prompt.py + dry_run.py, tests) match the diff stat (9 files). Known gaps holds the one UNVERIFIED (the aim, measured later). Role names (Driver, Verifier) are product terms of a change to those cards. Test plan SHAs are filled later by the Driver. Base is the CR-396 branch, consistent with the stack. Not yet posted text re-checked on the forge.

Evidence: none (cards and prompt text, no visible change); no before/after pairs.

VERIFIED

## Description pass (posted PR 367 body), head 995a6b0

NOT VERIFIED. Review box 8311949 matches the log note (`r1 inspector approved at 83119497`). Failures:
- Summary names "batch-28" and "the CR's specification, section ..." : internal references outside Internal references (pr-template, The rules).
- Deliverables table gives a before figure (74,666) with no base SHA; the after names 995a6b0 only in the caption text, the before has none.

NOT VERIFIED

## Description pass (short) at 995a6b073183c5c5376aa3b50576781113a2b323
Head: 995a6b073183c5c5376aa3b50576781113a2b323
Command: gh pr view 367 --json body; chantier log CR-398 (line "r1 inspector approved at 83119497...").
Claim: posted description follows pr-template; Review `8311949` matches the approved note; no internal refs outside Internal references; Known gaps holds the UNVERIFIED bullet. VERIFIED
