Head: e5d656ee3f7fc487796817c7075ed5fbc11e0275

# CR-455 verification (first pass, pushed head e5d656ee; PR head confirmed by `gh pr view 421 --json headRefOid`)

Claims, each judged at e5d656ee:

1. Gate pass at this head. `work/gates/20261122-044836.log` first line: `gate CR-455 branch ... head e5d656ee3f7fc487796817c7075ed5fbc11e0275`; last line: `result: pass at e5d656ee3f7fc487796817c7075ed5fbc11e0275` (`just scenario`). Worktree status clean.
2. Tests at head: `uv run ... python -m pytest tests/test_stack_base.py tests/test_stack_hold.py -q` in the worktree: `68 passed in 5.78s`.
3. The new tests fail on the previous code: detached worktree of the base (311ccf4d, CR-442 branch), head's `test_stack_base.py` copied in, `PYTHONPATH=<base>/src` (checked `chantier.stacks.__file__` is the base's): `15 failed, 34 passed` (cases A, B2, B3, D, working, blocked, Q3, Q2, Q4-merged, Q4-cancelled; the highest-open-dependency off_place test; Q4-landed; the `base:` line rows start-on-between, start-on-ended). Worktree removed.
4. Base rule of `take` (ready-only start candidate, default branch for working/blocked, walk stops at first PR, Q1/Q3): code `_start_candidate`, `start_on_for`, `stack_start` rule 3a read in the diff vs base; proved by the test rows ready/working/blocked/Q3 (claim 2) and scenario transcript `scenario/results/scenario-20261122-045630-33072.md` line 5703 (`[x] 4. ... working and a CR below it is ready ... default branch`), line 3743 (`[x] ... nearest earlier CR handed back ready with a PR ... handoff prints that branch`), line 4533 (`[x] 3.`), line 4673 (`[x] 9.`).
5. `after` dependencies (Q5, rule 3b): scenario line 3566 (`[x] order after ... base on the dependency's branch, whatever ready CR sits above it; --note - ... back on the nearest earlier CR handed back ready`), line 5291 (`[x] 8.`), line 5000 (`[x] 9.`); tests B, B2, B3, A.
6. Printed base where the worktree sits (Q2, Q4): scenario line 4393 (`[x] 6. ... still prints base origin/main once the CR below it is ready with a PR`), line 6627 (`[x] 4. ... handoff b ... default branch and the base: line naming a`).
7. `base:` line (section 2, Q6): `_record_alone` in facts.py; test rows dependency, release, start-on-between, start-on-chosen-past, unaffected, start-on-ended pass (claim 2 covers test_stack_base.py in full).
8. Scope: `git diff --stat` vs base touches only stacks.py, facts.py, records.py, concepts.md, driver.md, foreman.md, test_stack_base.py, scenario/run_scenario.py, scenario/README.md: matches spec sections 1-4, 6, 7; no hooks/ or types/ change.
9. Cards: diff of concepts.md (Stack, Dependencies), foreman.md, driver.md carries the spec's text.

PR body (work/pr-body.md draft, not yet at its final form), judged against the diff:
- Summary, Deliverables, Changes, Blast radius match the diff; no delivered change unmentioned.
- Test plan still has `<sha7>` placeholders and the Known gaps bullet "The independent verification has not run yet at this head" is stale once this verdict is in: the Driver must fill the SHAs (e5d656e) and drop that bullet. Not a failure of the change.
- Known gaps' third bullet (merge message to the Foreman owed, dependents of batch-30 print their dependency's branch) matches spec Decisions 6-8; kept.
- Review box: `$CHANTIER log CR-455` has `r2 approved at 311ccf4d..., committed as 6cff375f` and `r3 inspector approved; committed; just check and eval-dry-run pass` (03:48:23Z) with no SHA. The box `Review: approved at <sha7>` must cite 6cff375 (r2) or the r3 commit; for e5d656e the r3 note carries no SHA, so the Driver should add a note naming e5d656e (or the r3 commit it approved) before the box cites it.
- Internal references: "CR-455 take-draft; stacked after CR-442 ... and CR-438" sits in the folded details under Internal references, allowed. PR base is CR-442's branch; CR-438 not in the base chain (spec says "where it can"): not claimed as delivered.
- No images in the body.

before/after: not a UI change; before/after is the failing-then-passing test run of claim 3 (before = base 311ccf4d, after = e5d656ee). No other evidence pair owed.

VERIFIED

Description pass at e5d656ee3f7fc487796817c7075ed5fbc11e0275 (posted body, `gh pr view 421 --repo gsemet/chantier --json body`):
- Sections in template order, fold with blank lines, nothing after `</details>`, no images, no STALE mark, no placeholders: clean.
- Test plan names e5d656e on every item; the stale "verification not run" gap is gone. Known gaps: UNVERIFIED none, matches verify.md; the owed merge message matches spec Decisions 6-8.
- Review box: `$CHANTIER log CR-455` note "r3 inspector approved the one-line scenario change, reviewed on 6cff375f, committed as e5d656e" names e5d656e: proves the box.
- Summary, Deliverables, Changes match the diff vs the base (stacks.py, facts.py, records.py, three cards, test_stack_base.py, scenario steps and README); CR names only under Internal references; "stack driver" is a product term of the cards this change edits.

VERIFIED
