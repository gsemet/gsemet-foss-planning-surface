# Verify CR-297 description (PR 248)

Head: 943fcb4868aafcb4d22c37cc96cb3dff0f25c2f6

Description-only pass: `gh pr view 248 --repo gsemet/chantier --json body,headRefOid` (headRefOid = the head above), against `git diff origin/main` and work/verify.md (code unchanged since, carried from 943fcb4).

1. Summary roles/models (Sonnet 5.5 driver, Luna investigator, Sol coder and inspector, Terra verifier, debugger, conflict resolver; `model-policy: required`): the `model:` and `model-policy:` lines of `com.github.copilot/agents/*.md` match. OK.
2. Deliverables table: `git diff origin/main` on the agents shows exactly the four lines (coder Luna->Sol, verifier Sol->Terra, debugger and conflict-resolver Luna->Terra). OK.
3. models.py row `gpt-6.1-terra`: one added line in the diff. OK. Refusal text: verify.md item 4. OK.
4. `evals/kit/copilot_models.py` and its sample output (5 shown + "other nine" = 14 agents): verify.md item 5 (carried from 943fcb4, same head). OK.
5. Docs list (docs/agents-and-models.md, docs/hosts.md, hosts/copilot.md, evals/copilot/RUNBOOK.md) and Changes section: the 11 files of `git diff --stat origin/main...HEAD` are all mentioned (incl. test_plugin_files.py); none unmentioned, none claimed and absent. OK.
6. Test plan: `just check` 262 passed (verify.md item 6); Review `approved at 943fcb4` backed by the Driver notes "r2 approved at cb7690a, committed as 943fcb4" (`chantier log 297`); CI "all 5 pass at 943fcb4" note in the log; Verified at 943fcb4 (log verdict VERIFIED at that head). OK.
7. Known gaps: two bullets (no real Copilot session; events.jsonl shape checked on the fake only), which match the unobserved claims. No UNVERIFIED or STALE mark. OK.
8. Render: sections, table, fenced block and `<details>` fold are well formed; no images. Role names appear as the product's own subject (change to those roles), not as doer; "Internal references" holds only CR/follow-up. OK.

VERIFIED
