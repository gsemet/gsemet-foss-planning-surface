# Verification, CR-232

Head: 8285c96fcbaf2a01117d18f7ae0db0d69717100a

Result: VERIFIED

- `just check` at the head: passes (ruff, mypy strict, lock, 63 pytest, release notes).
- `just eval-dry-run`: 8 of 8 cases as expected, `ticket-summary-setup` included (171 s).
- `dry_run.py --case ticket-summary-setup --keep`: passes. Kept `ws.run.json` has campaign `ticket-summary`, `crs: []`, `issue.title` `[eval 1 2026-11-14 ticket-summary] Dark theme for the reading list`, and `issue.body` the kit's `issue.md`. Kept `settings.local.json` has exactly the four rules (`gh issue comment *`, `gh issue artifact create *`, Bash and PowerShell), no merge rule.
- Forge: 4 read-only calls, no `issue` call and no write.
- Spec sections 1 to 6: the texts match; the CAMPAIGNS entry matches; `issue` and `chat` lines present, no `merge`, `batch` or `CRs placed` line (the empty list is left out, as the PR body says); the docstring, runbook (3 steps, "setup places no frozen CR") and README (five campaigns, setup step 2 sentence, three table rows) match.
- Structure test: the spec names `test_structure.py`, but the test lives in `test_cli_units.py` at this head. It is updated as specified and passes.
- PR body (`work/pr-body.md`) matches the diff. Its `<sha7>` placeholders are still to be filled by the caller.
- Evidence: `work/verifier/evidence/` (eval-dry-run.txt, keep.txt, ws.run.json, settings.local.json).
- No real eval, no scenario, the main checkout untouched.

## Posted description check

Head: 8285c96fcbaf2a01117d18f7ae0db0d69717100a

Result: VERIFIED

- Body of PR 172 follows the template: sections and fold in order, no internal reference outside Internal references, every Test plan item names `8285c96`.
- Claims match the diff (7 files) and the earlier verification; `dry_run.py` is 909 lines (865 or 866 before), as the Known gaps say.
- `gh pr checks 172`: all five checks pass at the head, as the CI line says.

## Restack check

Head: acd7b405bbef89bcbb8b5ba8ec051b3634634925

Result: VERIFIED

Claims touched (the base brought changes to evals/kit/setup.py, dry_run.py, evals/README.md, the CLI and justfile; the CR's own files are the same 7), judged again at acd7b40 with HOME, USERPROFILE and CLAUDE_CONFIG_DIR on scratch folders:

- `just check`: exit 0, mypy strict clean on 77 files, `uv lock --check` ok, 63 passed, release notes ok.
- `just eval-dry-run`: exit 0, "dry run: 8 of 8 cases as expected", including `ok ticket-summary-setup: setup passes, no CR placed, record has the issue ... Dark theme for the reading list, the issue and chat lines, no merge or batch line, 4 allow rules, 4 read-only forge calls, no write`.
- `dry_run.py --case ticket-summary-setup --keep`: exit 0, "1 of 1 cases as expected".
- Spec sections 1 to 6 (texts, CAMPAIGNS entry, `issue_lines`, allow rules, runbook, README, structure test): the diff `febd917..acd7b40` shows the same setup.py, dry_run.py and test changes judged at 8285c96; carried from 8285c96 for the wording of the docs (same patch; the stack move only touched cards in the CR's own range).
- Review box: Driver's note "r1 approved at e54e299, committed as 8285c96" backs the pre-restack approval the body cites.
- PR 172 body: matches the 7-file diff; Known gaps lists the 909-line file and the campaign not run; the two unchecked boxes at acd7b40 are this verification and CI (scenario was pending when checked; check, eval-dry-run on three hosts pass).
