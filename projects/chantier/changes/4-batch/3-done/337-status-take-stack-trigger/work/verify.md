# Verify CR-337

Head: 99ed572723c72d0e4bc5ae91051cdfbbb906ae10

All claims judged at 99ed572723c72d0e4bc5ae91051cdfbbb906ae10 (worktree `git rev-parse HEAD`, clean).

1. Behaviour on a scratch batch (CLI run from the worktree, scratch project `work/scratch/p`, own git repo, `open --mode stack` of two CRs; the record's `status`/`pr`/`stacked`/`stack_agent` fields set by hand in the scratch record, `status` run each time; scratch removed afterwards).
   - one CR ready with a PR: `status | grep -c "stack: take stack now"` -> 0
   - two CRs ready with a PR: `stack: take stack now: CR-101, CR-102 ready with a PR, no stack made yet (`take stack --epoch <n>`)` (exactly one line, exact text of the spec)
   - `stack_agent` set: count -> 0
   - one CR `stacked`: count -> 0
   - the stacked CR merged, the other ready: count -> 0 (retro-Q1)
   The real `stack` / `agents set stack` / merge path is proved by the scenario step 13 (claim 4), not by hand edits.
2. Unit tests: `uv run --no-sync --project . python -m pytest skills/chantier/scripts/cli/tests/test_stack_due.py skills/chantier/scripts/cli/tests/test_code_targets.py -q` -> `18 passed in 1.66s`. `batch_status.py` is 380 lines (limit 400). The test file covers every case the spec lists.
3. Diff read against the spec: `stack_due`/`stack_line` in `stacks.py` match section 1 (mode, running, stack_agent, any `stacked` in all crs, deps ready, FORMING); `batch_status.py` only imports and appends `*stack_line(d)` after the CR rows (before `_order_lines`); `foreman.md` first-take bullet names the line as the trigger, same turn, rule stays the reference; mode switch clause added; scenario step 13 adds the checks (line present naming CRs in order, absent with a stack driver, back after `-`, absent after `stack`, absent after the recorded merge) and the README item has its `(test: ...)` tag. Nothing else touched. The merge check sits after the first recorded merge (PR body says so).
4. CI at the head (`gh pr checks 297`): just check macos/ubuntu/windows pass; just eval-dry-run ubuntu pass; just scenario (ubuntu-latest) pass (3m49s).
5. PR description (work/pr-body.md): renders (sections, fold, mermaid), Summary/Deliverables/Changes match the diff (six files, none missing or unmentioned), no image, Known gaps "None" is consistent (no UNVERIFIED claim, no evidence pair uncaptured; no screenshot owed), no role name outside Internal references. Open boxes (Review, Verified, CI) are the Driver's to tick.

Not run by me: `just scenario` locally (CI ubuntu covers it); the Review box note (`$CHANTIER log`) is not yet in the description as approved.

VERIFIED

## Description pass (head 99ed572723c72d0e4bc5ae91051cdfbbb906ae10)

Head: 99ed572723c72d0e4bc5ae91051cdfbbb906ae10

Command: `gh pr view 297 --json body -q .body` and `git diff --stat main...HEAD` (six files).
- Renders: sections, fold, mermaid block, no image: pass.
- Summary, Deliverables, Changes match the diff (stacks.py, batch_status.py, foreman.md, scenario x2, test_stack_due.py): pass.
- Known gaps "None": no UNVERIFIED claim, no uncaptured pair, no STALE: pass.
- Review box "approved at 99ed572": `chantier log 337` note "r1 approved at a65a8d3d, committed as 99ed5727": pass.
- Role names only under Internal references: pass.

VERIFIED
