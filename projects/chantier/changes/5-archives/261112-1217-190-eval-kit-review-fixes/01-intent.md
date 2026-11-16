# Fix the eval kit's review findings before the first sandbox campaign

Follow-up of CR-188 eval-sandbox-app and CR-189 reproducible-evals (both merged, 2026-11-12). The
read-only fable review of the delivered kit (`evidence/00-fable-review.md`, read it whole) found
that `full` will not end clean and that the quick campaigns run with risks. The user's go for one
follow-up PR: "130 est mergé. Fait une PR en plus si besoin", in autonomy ("Fait en autonomie
maintenant plus de question"). The criteria stay those of CR-189's `02-answers.md`
(`.agents/changes/4-batch/3-done/189-reproducible-evals/02-answers.md`).

## What changes (decided by the Chief of Staff, under the user's autonomy)

1. **A1, the audit and the release PR.** `audit.py --sandbox` counts the merged release PR (and a
   fix's) as this batch's, from what the batch recorded (the `ship` events or the `merged:` note),
   and runs J5 on it; a correct `full` run no longer fails C12.
2. **A2, the reset's verification.** `sandbox.py reset` compares only `refs/heads/*` and
   `refs/tags/*` (GitHub keeps `refs/pull/*/head`), in its survey and its verification alike.
3. **A3, B4, B6: a named merge command.** The operator merges through one reviewed kit command,
   `sandbox.py merge <pr>`, never a raw `gh pr merge`: it works on the sandbox only, refuses a PR
   that is not open, whose title lacks the run's prefix, or whose checks are not all green at its
   head (the sandbox's `main` is unprotected, so the kit enforces it), and merges by rebase. The
   runbooks and `evals/README.md` use it and say why the operator merges (it plays the user; the
   Chief of Staff card's "never merge" is about the real user's PRs). `setup.py` writes the
   sandbox workspace's `.claude/settings.local.json` (ignored by the sandbox's git) with the allow
   rules a run needs that the user's own settings may lack: that merge command, the Release
   driver's tag push to the sandbox and `gh release create` on the sandbox, each as narrow as the
   rule form allows. Nothing else is allowed there.
4. **A4, `uv.lock` in the releases.** The two frozen release CRs (`release-v0-2-0`,
   `release-v0-3-0`) name `uv.lock` in their files and their steps (the bump changes it). The
   sandbox's own `RELEASING.md` stays as it is: changing it would change the base.
5. **Docs.** `evals/README.md` says batch 1 has 8 feature CRs plus the release (not 9), and that
   the merge command, not the forge, refuses a red PR. The quick runbooks get the 10-message-limit
   fallback that `full` has (B3). Every sandbox runbook says what the operator does on a `budget:`
   ask: one raise with `order budget`, recorded in the report as a finding; a second one drops the
   CR (B1). `full`'s runbook says a `ping` may be needed more than once and the report counts each
   (B2).

## Out of scope

The judge's strictness on contiguous text (B5, low); the base commit and the sandbox itself (no
reset, no push there); any change to the plugin, the cards or the CLI.
