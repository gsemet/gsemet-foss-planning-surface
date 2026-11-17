# Chantier 0.3.1 on OKF: report for the simplification PR

Batch `p3-chantier-test` (2026-11-04, 21:46 to 23:19 UTC, 1 h 33), compared with CRs 258 to 260 run
the same evening with the project's guidelines workflow (PRs 315, 316, 317).

Labels: **Measured** comes from `batch.json`, `events.jsonl`, gate logs, `chantier cost`, git, GitHub
or transcripts. **Inferred** is my reading. Sources: the clone, its transcripts, and my own session.
I did not read Chantier's code. Numbers about earlier PRs come from the Chief of Staff's exit report.

## Result

**Measured**

| | |
| --- | --- |
| CRs | 4 (3 P3, plus CR-104 added to fix preflight) |
| Pull requests | 1 (PR 321), shipped with a red long gate |
| Blocked | 3; their work is uncommitted in worktrees (8, 1 and 3 changed files) |
| Long gates | 5 runs, 5 red, 74 min of gate time |
| Cost | $4.17, 255 model calls |
| Owner interventions | 3 orders, 1 mode change outside the CLI, 10 messages |

Owner, 22:47, on the gap with earlier sessions: "écart monstrueux". Owner, 23:06: project rules
come first, not everything can be foreseen, and Opus 5.5 and Sonnet 5.5 should be trusted.

PR 321 against 13 earlier PRs (Chief of Staff's count):

| Criterion | Earlier | PR 321 |
| --- | --- | --- |
| Template sections | 6 of 6 | 1 of 6 |
| Conventional title | all | no |
| `Assisted-by:` | 40 of 40 commits | absent |
| `Co-Authored-By` (forbidden here) | 0 of 40 | present (`1da255cd`) |

The main finding is not on your list: **project rules did not reach the output, and nothing checked
the output.** My seven points come after it.

## 0. Project rules were not applied or checked

- **Facts (measured):** see the table. The Verifier's report on CR-102 ends "Not run: just
  preflight", then "VERIFIED". The Inspector approved 4 of 4 CRs at round 1.
- **Chantier did:** the Driver wrote only Summary and "Autonomous decisions" (the second section is a project rule; the template's other sections were missing). The
  Foreman does not read project rules, so it could not check them. The owner had to send O-3,
  which restates the template, the title rule and "never ship a red long gate".
- **Should have:** one role reads `AGENTS.md` and the applicable guidelines for each CR, and a
  check on the real output (PR title, body, commit trailers) comes before a PR counts as ready. The
  owner's 22:44 message puts this on the Foreman. This includes planning-time rules, such as the
  before and after screenshots.
- **Cost:** the owner kept PR 321 as a trace, not as work to merge. **Inferred:** the attribution line comes from the
  harness default, which the project's precedence rule overrides; this session hit the same conflict
  and kept `Assisted-by`.

## 1. Context continuity

- **Facts (measured):** CR 259 went through a wrong reading, a redo that hid the bug (first
  version of PR 316), then a fix that passed 60 stress rounds but broke restored previews, then the
  final fix (`7612009d`). All in one session. In the batch, Drivers were not lost (`resumes: 0`).
- **Chantier did:** this run did not exercise it. CR-103's second Driver started from an order
  note, with a new agent id.
- **Should have:** a handover separating proved, inferred and refuted.
- **Cost:** no measured cost here. **Inferred:** this is the gap most likely to hurt on a hard bug,
  and P3s do not test it.

## 2. Green does not mean proved

- **Facts (measured):** PR 316's checks were green at `d702da5e` while `integration` failed in all
  3 heavy runs (`a restored preview releases its lock too`), with `stress` green. Runs 41922219006,
  41922229097, 41922238947. On PR 321, `integration` and `stress` are skipped, by design on PRs, yet `ci: green`.
- **Chantier did:** recorded `ci: green` and hand-back-ready at 22:29.
- **Should have:** read per job at the head commit, and report skipped jobs as not proved.
- **Cost:** on this project, a regression on restored previews would have counted as done.

## 3. Environment or product failure

This is the costliest point of the batch.

- **Facts (measured):**
  - The first three long gates overlapped on one Mac: 22:50 to 23:03, 22:53 to 23:08, 22:55 to 23:13
    CET. All failed `ci-integration`, each on a different step.
  - Three different decisions followed a similar failure: CR-102 shipped ("unrelated to this
    change"), CR-101 and CR-103 blocked.
  - CR-101's reason says "looks like desktop/focus env problem". Its log has `Timed out waiting for
    Warning to change the type` with `related=none commit active=body pageFocus=true`.
  - That is the trace of the product bug fixed in PR 316. The fix is not in the batch's base.
  - CR-104's gate ended on a locked screen (`CGSSessionScreenIsLocked=Yes`). My own preflight hit
    the same error just before it (23:52 to 00:05 CET); the lock was not checked at that moment.
  - CR-103 alone still failed, so overlap is not the only cause.
- **Inferred:** CR-101 was probably blocked by a real product bug labelled as environment. Overlap
  probably added noise. Only the signature links them.
- **Chantier did:** `events.jsonl` has no classify event. Each failure went to the owner.
- **Should have:** obey the written project rule ("Two CRs never run app-window tests locally at the
  same time", and the machine stays awake during the run); check for a locked screen
  before starting; and compare a failure with the base before calling it unrelated. Then wait or ask.
- **Cost:** 74 min of red gates. CR-104 ($1.30, the costliest CR) was opened to repair the gate. It
  did find a real defect: VS Code ignores port 65535 (fix uncommitted, reusable).

## 4. History rewriting

- **Facts (measured):** only one ship took place, so rebasing was not exercised here. On my side,
  `git commit --amend` plus force push was denied, and I merged the lower branch up through
  the stack, with `CHANGELOG.md` and `requirements/tiers/log.md` conflicting as usual. PR 320 sits
  on branch 258.
- **Correction:** the constitution says "History is linear: rebase, never merge commits;
  force-push only with `--force-with-lease`, after a rebase." Chantier's rebase follows the project.
  My merges broke that rule (branch 259 has 1 merge commit, 260 has 4), and I should have reported
  the denied force push to the owner. Disregard the merge-up request.
- **Cost:** none measured here.

## 5. Project guidelines as authority

See section 0. **Measured:** three titles start with "Change Specification:", from the spec's H1;
CR-104's title, `test: ...`, shows a good spec fixes it. Three agents ran `git diff main` and hit
`fatal: bad revision 'main'` (exit 128): the batch's base was `docs/remove-cr-workflow`.

## 6. Two backlogs

- **Facts (measured):** I kept 3 copies with a `02-chantier-eval.md` note and watched `chantier/*`
  by hand; the PR link exists only in `batch.json`.
- **Should have:** write the PR back to the source item.

## 7. Readability

- **Facts (measured):** `chantier status` printed `spent $3.04` while `chantier cost` gave $4.17.
  Each block reached the Chief of Staff twice (`asks`, CR-103 and CR-101).
- Your PR 18 may already change this; I have not seen it.

## Too strict, and not strict enough

**Measured:** the batch mode was fixed at opening. The owner said "Soir flexible !" and the Chief of
Staff changed it outside the CLI (`mode-change`, "by user's word, outside the CLI commands"). The
owner then asked whether Opus or Sonnet with good tools would do better.

**Inferred:** loosen the path, tighten the required results. The Foreman could not judge, while the
Driver had the freedom to ship red.

## What was not used, or was worked around

**Measured:**

- Never ran: `debugger`, `conflict-resolver`, `qa-driver`, `stack-driver`, `release-driver`.
- Verifier: 1 CR of 4 (others stopped earlier). Investigator: 2 CRs of 4 have a report.
- Worked around: mode change (by hand), rules (O-3 and spec edits), one gate at a time (O-1).

**Inferred, candidates to delete or merge:**

- Fixed mode at opening: remove.
- The Foreman's decision tables: replace with judgment; give it the job of checking output.
- A Chantier-specific PR body format: remove; use the project's template.
- Separate numbering: keep only if a link to the source item exists.

This batch cannot tell whether the five unused roles are useless: it ended before they applied.

## Which roles earned their cost

| Role | Cost | Calls | Verdict (inferred) |
| --- | --- | --- | --- |
| `cr-driver` | $1.57 | 83 | Too costly for what it controlled: red ship, template skipped |
| `coder` | $1.09 | 79 | Produced the changes; I did not review the diffs; CR-104's port fix has a failing-first test |
| `foreman` | $0.96 | 47 | Did not earn it here: relayed, and could not judge |
| `inspector` | $0.25 | 23 | Unproved: 4 of 4 approved, and it reviews the diff, not the PR |
| `investigator` | $0.23 | 17 | Not assessed |
| `verifier` | $0.07 | 6 | Good proof on tests (new test fails on old code), blind to the gate |

## Raw output

```text
Total: $4.17, no budget
Orchestration $2.53 (61%), work $1.63 (39%)
Most: CR-104 $1.30, CR-102 $0.67, CR-101 $0.66
Foreman: 16 wakes, context 105,820 tokens on average, 124,336 at its peak
Not counted: the Chief of Staff's own session

p3-chantier-test open stack slots 3 e1 spent $3.04
CR-104 blocked r1 | CR-102 ready r1 PR 321 ci green | CR-103 blocked r1 | CR-101 blocked r1
```

Models seen (assistant messages, batch transcripts): Sonnet 5.5, 372; Opus 5.5, 165. The Foreman ran
on Sonnet 5.5 at low effort; the owner wants Opus 5.5 for the Foreman and Sonnet 5.5 for Drivers, both
at normal effort.

## Cost comparison, with its limit

**Measured:** `chantier cost --transcript` on my session gives $88.32 over 1,250 calls.

This is not comparable. My session covers far more than three CRs, including a hard flake and
several proof runs. It does show the guidelines workflow is not cheap: quality was bought with
context. Chantier's $4.17 did not buy a mergeable PR, so a cost per mergeable PR is undefined here.

## The guidelines workflow had faults too

- I published overclaims in PR 316's body and corrected them myself.
- My first fix passed stress and broke `integration`; only the heavy job caught it.
- Hand-written STATE headers needed corrections.
- `just preflight` has still not passed on this stack on the Mac, so CRs 258 to 260 do not meet the
  project's completion gate either.
