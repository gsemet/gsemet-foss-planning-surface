# Verify CR-240

Head: 2952a02dc543577705ff2b0a5e18a92f58fff96f

Verdict: VERIFIED

## Commands and results (at the head)

- `just check` in the worktree: ruff format/check ok, mypy --strict "no issues in 84 source files", `uv lock --check` ok, pytest 63 passed, release-notes ok. Exit 0.
- `preflight` runs with HOME, USERPROFILE and CLAUDE_CONFIG_DIR on scratch folders (empty settings). The CLI takes `--project`, not `--batch`, for preflight. P7/P8 FAIL come from running in a linked worktree (environmental); P10 lines are what matters and P10 is warn-only.
  - `preflight`: one line `P10 warn every batch: 14 of 14 commands ... not allowed ...; the host's auto-mode classifier judges each command at run time, and in a remote session (Remote Control) nobody may be there to answer its prompt: every batch may stop at the first one; the rules are in hosts/claude-code.md, "Capabilities and their commands"; not checked here: a stack, a release on its own, fixes on a grant (checked at the go when the batch uses them)`.
  - `preflight --mode stack`: the base line, then `P10 warn a stack: 1 of 1 commands ... gh stack view (add Bash(gh stack*), PowerShell(gh stack*)); <classifier/Remote Control text>: a stack may stop at the first one; ... not checked here: a release on its own, fixes on a grant`.
  - `preflight --autonomous-releases 1 --grant-fixes`: base line, then `P10 warn a release on its own: 3 of 3 commands ...: gh pr merge 12 --rebase (add Bash(gh pr merge*) ...); git push origin v1.2.3 (add Bash(git push origin v*) ...); gh release create v1.2.3 --verify-tag ... (add Bash(gh release create*) ...)`, then `P10 warn fixes on a grant: 1 of 1 commands ...: gh pr merge 12 --rebase (add Bash(gh pr merge*) ...) ...; not checked here: a stack`.
  - Exit 2 in this worktree only because of P7/P8; the P10 lines never fail (covered by the pytest P10 test, which passes).
- Trials (run from the Verifier's session, not the Chief of Staff's): `git push --force-with-lease -u origin chantier/preflight-trial --dry-run` -> "src refspec ... does not match any" (host let it run, command's own error = pass); `git push origin v0.0.0-preflight-trial --dry-run` -> same; `gh pr view --json number` -> `{"number":186}`; `gh stack view` -> "not part of a stack" (ran). `git ls-remote origin refs/heads/chantier/preflight-trial refs/tags/v0.0.0-preflight-trial` -> empty; `git status --short` -> clean. The `git -C <main checkout> push` and `gh release create`/merge trials were not run (no harmless form, or the Chief of Staff's own session).
- Forge probes on gsemet/chantier: `gh api repos/gsemet/chantier/stacks -X GET -F per_page=1` -> 200, one stack (closed, PRs 139-156), so the stacks API exists; `gh api repos/gsemet/chantier/rules/branches/main` -> `[]` (no ruleset rule); `gh repo view --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed` -> `{"mergeCommitAllowed":false,"rebaseMergeAllowed":true,"squashMergeAllowed":false}` (rebase only: matches the project's "merge by rebase").

## Claims checked against the diff

- Section 2 (SAMPLES with capability, RECOMMENDED_ALLOW from batch/stack, GRANT_ALLOW, per-capability counts): present; table-vs-SAMPLES test passes.
- Section 3 (three options named as `open`, one P10 line per checked capability, warn-only, no trial and no probe in the CLI): present.
- Section 4 (host table, base-set paragraph, "Auto mode" limits, remote-session sentence), 5 (trials), 6 (probes 4 and 5, GitLab items), 7 (per-capability question, release "auto" flow, project's own procedure), 8 (refusal notes, retro line), 9 (Copilot), 10 (session-start, init, driver, tutorial) and 11 (test and scenario assertions): present in the diff.
- Files: permissions.py 301 lines, preflight.py 279 lines (limit 400).

## Deviations and notes

- Spec section 3 asks for "one more line" `P10 ok not checked here`; the head appends the text to the last P10 line (the 10-line report cap). The PR body discloses it (Autonomous decisions). Accepted, not a failed claim.
- PR body example block shows "2 of 4 commands" for the release capability; the real output is "3 of 3". The block is illustrative only; the UNVERIFIED line can be replaced with the outputs above (use the actual numbers).
- Unproved still (as the PR's Known gaps say): a real session run of the Chief of Staff's trials, the release question and the `brief.md` "Permission trials" record; GitLab probes; Copilot trials. No pane change, so no screenshot is due.
- The scenario was not run (waived by the user).

## Description pass (posted body, head 2952a02)

Commands: `gh pr view 186 --json body,headRefOid` -> head 2952a02dc543577705ff2b0a5e18a92f58fff96f; `gh pr checks 186` -> just check (macos, ubuntu, windows), eval-dry-run, scenario all pass; `git diff --stat main...HEAD` -> 13 files; `git grep GRANT_ALLOW|autonomous-releases|grant-fixes|"Capabilities and their commands" HEAD` -> names exist (permissions.py:132, preflight.py:269/276, claude-code.md).

Audit (pr-template.md):
1. Sections and order: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, then Details (Changes, Human decisions, Impacts, Test plan, Internal references). No `issue:` line in the spec, no Issues References: ok. Human decisions present, and 02-answers.md holds decisions: ok.
2. Fold: one details block after Known gaps, blank lines after summary and before `</details>`, nothing after: ok.
3. Internal references: none outside the last section (grep for CR-, batch, Round, Verifier, Inspector, Driver outside it: only "inspector approved" in the Test plan Review item, a proof line, not the doer of the change). "Chief of Staff" appears as a product term of a card the diff changes: allowed.
4. Deliverables: table, P10 output sketch, choices; names exist in the diff: ok.
5. Changes and Impacts match the 13-file diff: ok.
6. Blast radius: Grade 2 with explanation and rollback: ok.
7. Autonomous decisions match the notes (appended text, bare rules column, subsection placement): ok.
8. Human decisions vs 02-answers.md (answers 2, 4, 5 and the waiver): all shaping decisions present, none invented: ok.
10. Known gaps: no UNVERIFIED claims in the body; the gaps match the notes and verify.md (no real session, GitLab/Copilot unproved, no long gate): ok.

Claims vs verify.md: P10 counts (14 of 14; 1 of 1; 3 of 3; 1 of 1) match verify.md lines 11-13; trials and probes (200, `[]`, rebase only) match line 15-16; the earlier "2 of 4" example is gone; Test plan SHAs (2952a02; review 3a96b35 carried, matches STATUS notes; CI all pass at 2952a02 confirmed by gh pr checks) hold. The "Local gates" box is unchecked with the waiver recorded in the notes: consistent.

Minor, not failing: the body's Deliverables sample shows the P10 text elided with "...", illustrative.

Verdict (description): VERIFIED
