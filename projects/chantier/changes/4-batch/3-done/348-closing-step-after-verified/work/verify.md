# Verify CR-348

Head: 4d58060d4811a571da9d98309a830d0459836fa3

Verdict: VERIFIED

Claims (all judged at 4d58060d):

1. CI green at the head. Command: `gh pr checks 313`. Output: `just check` macos, ubuntu, windows pass; `just eval-dry-run (ubuntu-latest)` pass; `just scenario (ubuntu-latest)` pass (3m41s). The scenario job runs the new check (handback `context: closing:` prints "for the closing step", no "out of context" or "asks the Chief of Staff"; take with `resume: closing` keeps the round) and the card-string check. Cited from CI, not rerun locally.
2. driver.md names the trigger, note, hand-back, reads, exception and no-loop rule. Command: `git diff origin/main -- skills/chantier/references/driver.md`. Output: CR-driver paragraph holds the pushed-head `VERIFIED` trigger, the `closing: VERIFIED at ...` note, `handback <cr> blocked context: closing: ...`, "always happens, whatever the context size", matrix probe and `ship` carry excluded; the Context bullet gets the exception on both clauses; "A Driver started again" gains the `resume: closing` sub-bullet (reads, no spec/investigation/r<n>/diff, `next:` order, no re-hand-off); "Your end" lists `context: closing: ...` twice; Startup core gets the one line.
3. foreman.md names the take-back and counting exclusion. Command: `git diff origin/main -- skills/chantier/references/foreman.md`. Output: the `blocked context:` bullet's parenthesis gains the closing case; `take <cr> --note "resume: closing" --epoch <n>` path, no round, no ask, before queued CRs; "the closing step" naming; second-`context:` ask excludes `closing:`. "A silent end" is untouched, as the spec says.
4. CLI changes only the printed line. Command: `git diff origin/main -- .../driver_checks.py`. Output: 6 added lines, a `context: closing` branch before the `context:` branch returning `[line, "<cr> verified; the Foreman restarts a fresh Driver for the closing step, with no ask to the Chief of Staff"]`. `git diff --stat` shows only the four expected files (no tests/, docs/, agents/, evals/kit/).
5. Scenario check as spec step 8, with the extended card check (`resume: closing`, `context: closing:` in driver.md; `resume: closing` in foreman.md): read in `git diff origin/main -- scenario/run_scenario.py`.
6. Review box: `Review: approved at ef9f977 (committed as 4d58060)` matches the log notes "r1 body re-inspection approved at ef9f9779..." and "r1 approved at ef9f9779, committed as 4d58060d" (`chantier log CR-348`).
7. PR body (work/pr-body.md, and the body as posted on the forge for PR 313, base main, draft): Summary, Deliverables (mermaid diagram, three bullets), Changes and Human decisions match the diff; nothing claimed is missing and nothing delivered is unmentioned; no images, so no username or home folder shown. Left for the closing step by design: the Test plan boxes `Verified at <sha7>` and `CI green at <sha7>`, and the Known gaps bullet "The long gate is not yet shown green at this head" (CI scenario is now green at 4d58060; the closing Driver must update it, and the Windows `chantier gate` rule of AGENTS.md applies if this CR is on top of the stack). The description pass runs after the closing, on the posted final body.

Not run: no local `just scenario` (cited from CI, claim 1). No before/after evidence: no visual change.

## Description pass at 4d58060d4811a571da9d98309a830d0459836fa3

Command: `gh pr view 313 --json body,headRefOid` (headRefOid 4d58060d4811a571da9d98309a830d0459836fa3); `git diff --stat main...HEAD`; `gh pr checks 313`; `chantier log 348`.
Output: Summary, Deliverables, Changes match the four changed files (driver.md, foreman.md, driver_checks.py, run_scenario.py); renders (mermaid, details fold); no images. Every SHA in the Test plan is 4d58060 (Review ef9f977 committed as 4d58060 matches the log notes "r1 approved at ef9f9779, committed as 4d58060d"); CI checks x3, scenario, eval-dry-run all pass. Known gaps names the long gate as CI-only, matching the `ship` off-list. Role names are product terms of a change to those roles. Description: VERIFIED.
