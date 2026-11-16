# Retro of batch-13

## 2026-11-12: CR-188 eval-sandbox-app, CR-189 reproducible-evals, CR-190 eval-kit-review-fixes

- Four blockers of the `full` campaign (release PR counted as a stray merge, reset verify on `refs/pull/*`, a raw `gh pr merge` the host may refuse, `uv.lock` missing from the release CRs) were found by the end review after CR-189 merged, not by its Inspector or Verifier, which judged each piece alone: an eval-kit CR's specification asks for an end-to-end dry run of the campaign (setup, a staged run, audit) as Verifier evidence, and the independent review runs before the merge, not after.
- CR-189 needed a third round (r2 FIX-REQUIRED: the audit read the release tag from the workspace instead of its origin) and its r2 checkpoint commit "wip(evals)" stayed in the merged history: a Driver gives a checkpoint commit a real message before `ship`, or folds it into the round's commit.
- The fable review's 17 calls are not priced, so the batch's cost is a floor and the shares and the orchestration ratio read not measured: add `claude-fable-5-2` under `prices:` in `chantier.yaml`, or have the CLI's built-in table carry it.
- The steering session's `gh ... --jq '<expr with spaces>'` broke several times under PowerShell quoting, and `order add --epoch` was refused (only `order merged` and `order add --fix-for` take it): the steering session prints `--json` plainly on PowerShell and passes `--epoch` only where the card lists it.
- Nothing was proved on the host by this batch: the new allow rules of `setup.py`, `sandbox.py merge` on a real PR, and `reset --yes` with real `refs/pull/*` wait for the first paid campaign, which runs `setup.py` from the main checkout (its merge rule embeds the checkout's path).
