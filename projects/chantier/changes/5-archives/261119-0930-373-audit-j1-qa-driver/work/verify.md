# Verify CR-373

Head: 1b58d39aa0c56c35d0a9434ce3845f4293f8dd48

All claims judged at 1b58d39.

1. `uv run --locked python evals/kit/dry_run.py --case audit-qa-prompt` -> `ok audit-qa-prompt: ...` ; `dry run: 1 of 1 cases as expected` (own, form, role, card, branch, outside, direct all behave per the spec table; the case fails with a message if any variant diverges).
2. `just eval-dry-run` -> exit 0, `dry run: 18 of 18 cases as expected`, `audit-qa-prompt` ok. Log: work/verifier/evidence/eval-dry-run.log.
3. Mutation proof (throwaway copy under work/scratch, removed): (a) QA_PROMPT recognition disabled -> `FAIL audit-qa-prompt: ... (own) / ['- FAIL [J1] ... starts with a `chantier <role>` prompt']`, 0 of 1; (b) `lawful_worktree` back to verifier only -> `FAIL audit-qa-prompt: ... (own) / ['- FAIL [J3] ... creates no worktree but its detached one of the default branch']`, 0 of 1. Logs: work/verifier/evidence/mutation-no-qa-recognition.log, mutation-no-j3-relax.log.
4. Diff (`git diff origin/main...HEAD`): item 1 (QA_PROMPT, `PROMPT.match or QA_PROMPT.match`, docstring), item 2 (`lawful_worktree` accepts qa-driver; `in_folder` and the OWN_FILES exception; PASS label), item 2b (`load_agents` excludes role qa-driver from `outside`; docstring), item 3 (`case_audit_qa_prompt`, CASES, FUNCTIONS, docstring; reads agents/qa-driver.md; finally restores batch.json), item 4 (evals/README.md row) all present; no card, CLI, agent or scorecard change (3 files changed).
5. PR description (work/pr-body.md): Summary, Deliverables, Changes match the diff; Known gaps "None" is consistent (no UNVERIFIED claim); no images; the Review box `approved at 1b58d39` matches the Driver note `r1 approved at 3a9afc2c, committed as 1b58d39a` (`chantier log CR-373`). Verified/CI boxes are filled by the Driver after this pass.

VERIFIED

## Description pass at 1b58d39aa0c56c35d0a9434ce3845f4293f8dd48 (posted PR 338)

Command: `gh pr view 338 -R gsemet/chantier --json body`, `git diff origin/main...HEAD` (3 files), `gh pr checks 338 -R gsemet/chantier` (5 of 5 pass).
Posted body follows the template; Summary, Deliverables and Changes match the diff (audit.py, dry_run.py, README row); each proof names `1b58d39`; Known gaps "None" is consistent; no images; boxes checked are backed (checks pass, earlier verdict VERIFIED at this head, review note carried above).

VERIFIED
