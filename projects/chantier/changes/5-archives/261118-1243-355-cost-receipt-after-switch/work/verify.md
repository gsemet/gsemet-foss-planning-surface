# Verify CR-355

Head: 21a23678d6878597f880db41f1b5f165f4494b7f

Base: bdd27e0f. PR https://github.com/gsemet/chantier/pull/322.

## Evidence 1: switched batch, text and receipt agree (21a23678)

Command (head): `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_cost_switch.py skills/chantier/scripts/cli/tests/test_cost_receipt.py skills/chantier/scripts/cli/tests/test_cost_reading.py -q`
Output: `26 passed in 2.37s`.
Test reads the code: direct record after claims chief, foreman, chief; calls at +2 and +12 outside; asserts the receipt steering is not None, `(2 calls)` in the text line, calls equal, dollars equal as printed.
Fails on the base: base worktree (detached at bdd27e0f, in scratch, removed after) with the two new test files copied in, run with `PYTHONPATH=<base>/skills/chantier/scripts/cli/src` (import path checked: it resolved to the base's `src`):
`pytest tests/test_cost_switch.py -q` -> `E assert (None is not None)`, `1 failed`.

## Evidence 2: one rule on prepared reads (21a23678)

Same head run above (parametrized over direct and foreman, 4 reads: held, held with inside, only untimed with inside, nothing outside): passed; it compares `chief_outside(read)` to `chief_line(...)` text for each, both shipped functions.
On the base (same command with both files): `9 failed, 7 passed`; all 8 parametrized cases fail with `TypeError: chief_outside() missing 1 required positional argument: 'read'` (the signature changed, the base cannot take the new call). Note: that failure is a call-signature failure, not a value mismatch; the behavioural gap on the base is shown by Evidence 1 (value mismatch). Diff of the code confirms the removed `d.steering == "direct"` test and the added untimed case.

## Evidence 3: scenario (21a23678)

Diff read: `c-out` at `at(-30)` seeded; the check demands exactly one `outside the budget` line with `(1 calls)`; a probe runs `chantier.board.costs.compute` and compares calls and dollars with the line. Own and Foreman row checks `(2 calls,` and `(1 calls,` kept. Proof it runs: `gh pr checks 322`: `just scenario (ubuntu-latest) pass 2m51s` at head 21a23678 (headRefOid confirmed by `gh pr view 322`). No local gate pass exists at this head; not owed to this verdict (the long gate is the pipeline's job).

## Evidence 4: existing checks green (21a23678)

`test_cost_reading.py` and the other tests of `test_cost_receipt.py` are in the 26 passed above. CI: `just check` pass on ubuntu, macos, windows; `just eval-dry-run` pass.

## Evidence 5: docs grep (21a23678)

Command: `grep -rn "steering in a Foreman batch" docs skills scenario` -> no output, exit 1. Docs diff shows the new wording in `docs/web-board.md` line 94.

## PR description (as posted, 21a23678)

`gh pr view 322 --json body` equals `work/pr-body.md` apart from one trailing blank line. Renders (sections, fold). Summary, Deliverables and Changes match the diff (sessions.py, receipt.py, receipt.js comment, docs, three test/scenario files). No images. Known gaps "None": no UNVERIFIED claim, no failed accepted claim. Test plan boxes still open for Verified and CI are the Driver's to tick. No role name outside Internal references. Review box `Review: approved at 21a2367`: `chantier log` has the Driver note "r1 approved at bdd27e0f, committed as 21a23678", which is the committed-as SHA the box cites: accepted.

## Verdict

VERIFIED at 21a23678d6878597f880db41f1b5f165f4494b7f.

## Description pass at 21a23678d6878597f880db41f1b5f165f4494b7f

Head: 21a23678d6878597f880db41f1b5f165f4494b7f

- Description (gh pr view 322 --json body), judged at 21a2367: renders (sections, table, fenced block, fold), no images; Summary, Deliverables and Changes match `git diff --stat origin/main...HEAD` (7 files: sessions.py, receipt.py, receipt.js, web-board.md, test_cost_receipt.py, test_cost_switch.py, run_scenario.py).
- Review box: `$CHANTIER log CR-355` has "r1 approved at bdd27e0f, committed as 21a23678", matching the box.
- Test plan boxes cite 21a2367; Verified and CI notes in the log. Known gaps "None": no UNVERIFIED claim, no evidence pair uncaptured. Role names are product terms of the cost code.

VERIFIED
