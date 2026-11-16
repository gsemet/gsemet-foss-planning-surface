## Summary

The eval kit's review found that a correct `full` campaign would not end clean and that the quick campaigns carry avoidable risks. This PR fixes what it found, so the first paid campaign measures chantier and not the kit: the audit counts the merged release PR, `reset --yes` survives GitHub's permanent `refs/pull/*`, the operator merges through one reviewed command, the release PRs no longer go red on a stale `uv.lock`, and the docs say what the code does.

## Deliverables

- The audit (`evals/kit/audit.py`) gains `batch_prs(data, events)`: every PR link the batch recorded for each CR (its `ship` events, its `merged:` note, its current PR). J5 runs on each link; a PR closed without a merge is not required green; the strays check and the release-merges check use all links.
- The reset (`evals/kit/sandbox.py`) compares only `refs/heads/*` and `refs/tags/*` through `parse_refs` and `ref_problems`; setup's precondition uses the same rule.
- A new command, `sandbox.py merge <pr> [--workspace <dir>]`, sandbox only. It refuses a PR that is not open, whose title lacks the run's prefix, or whose checks are not all green at its head (`merge_refusal`, `checks_green`, shared with the audit); otherwise it merges by rebase with `--match-head-commit`.
- `setup.py` writes the workspace's ignored `.claude/settings.local.json` (Claude campaigns only) holding the merge command and, per release, the exact tag push and `gh release create` rules (`merge_command`, `allow_rules`).
- Both frozen release CRs now name `uv.lock` in their changes and files.
- The README and the four sandbox runbooks say how the operator merges and why, what to do on a `budget:` ask, and the 10-message fallback for the quick campaigns.

Evidence at 179304b (scratch scripts outside the repository, canned data only, nothing written on the sandbox).

Audit on a made-up batch whose release PR #12 was merged (its CR's PR link cleared by the CLI), before (d72df44's `audit.py`) and after:

```text
--- before
FAIL every PR of this run's prefix merged since the batch opened is a PR of this batch: ['#12']
--- after
PASS CR-2 PR 12: title starts with the prefix, no auto-merge, checks green at its head, merged ...
PASS every PR of this run's prefix merged since the batch opened is a PR of this batch
PASS each merge of the release or a fix is recorded with `order merged --epoch` (1 recorded for 1 merges)
batch_prs = {"CR-1": [".../pull/11"], "CR-2": [".../pull/12"]}
```

A release attempt closed red (#12) then merged green (#13): J5 passes for both.

Reset's refs, on a local bare repository holding `refs/pull/1/head`:

```text
parse_refs -> {'refs/heads/main': 'aaa', 'refs/tags/v0.2.0': 'ddd'}   (HEAD, refs/pull/*, peeled tags dropped)
remote_refs(bare) == {main: base}: True ; ref_problems -> []
d72df44 whole-map comparison: reports refs/pull/1/head
```

Merge command: the six refusals (merged, closed, no prefix, failed check, pending check, no check) refuse with exit 2 and run no `gh pr merge`; the open, prefixed, green PR makes exactly one call, `pr merge <n> --repo gsemet/chantier-eval-sandbox --rebase --match-head-commit <sha>`. `merge abc` exits 1; another repository's link, a missing run record and a record naming another repository exit 2. `setup.py full` writes 14 rules (the merge pair, then per release the tag push in four forms and two `gh release create` rules), `setup.py real-foreman` 2; the file is UTF-8 without BOM and not listed by `git status`.

`uv.lock`: after setting `0.2.0`, `uv run --locked pytest -q` fails; after `uv lock` it passes (28) and `git status` lists `uv.lock`.

Not run: the host's acceptance of the new allow rules, the merge command on a real PR, and `reset --yes` against real `refs/pull/*`; the first paid campaign proves them.

## Blast radius

Grade: 1. Everything is under `evals/` (the eval kit and its docs); no plugin, card, CLI, hook or scenario file changes. A plain `git revert` restores the previous kit.

## Autonomous decisions

- `merge` reads the prefix from `<workspace>.run.json` (workspace = `--workspace` or the current folder), accepts a number or the sandbox PR link, and uses `--match-head-commit` so the head merged is the head checked; it deletes no branch.
- Refusals are the three named plus "sandbox only" and the missing run record; a draft or another base is left to `gh`, whose error is passed on (exit 4).
- "All green" is the audit's existing rule (`SUCCESS` only), now one shared function.
- Allow rules are exact where the command is fixed and use `*` only where an argument varies; quick campaigns get only the merge rule; Copilot gets no file.
- A release attempt's PR closed without a merge is not required green by J5.
- The budget raise is the opening budget x 1.5, once per batch; a later `budget:` ask drops the CR.
- The quick-campaign 10-message fallback goes in `real-foreman`; `real-direct` only says how to report a refused send.
- Each `ping` in `full` is a counted human step.
- No new structure test: the evidence runs the new functions directly.
- Two wording fixes to keep the text true: `full`'s intro mentions a possible `ping`, and the README no longer says nothing else changes the sandbox (`merge` does).

<details>
<summary>Details</summary>

## Changes

- `evals/kit/audit.py`: `batch_prs`, J5 per link, C12 strays and release merges per link, release PR column.
- `evals/kit/sandbox.py`: `parse_refs`, `ref_problems`, `remote_refs(url)`, `verify`, `checks_green`, `merge_refusal`, `cmd_merge`, `merge` sub-parser.
- `evals/kit/setup.py`: `survey` via `ref_problems`, `merge_command`, `allow_rules`, settings file, summary lines.
- `evals/kit/sandbox-crs/release-v0-{2,3}-0/03-change-spec.md`: `uv.lock`.
- `evals/README.md` and the `full`, `real-foreman`, `real-direct`, `copilot` runbooks.

## Impacts

No visual change. Operators merge sandbox PRs with the new command; the first paid campaign proves the host's acceptance of the new allow rules.

## Test plan

- [x] No new tests by design (structure tests only); the new functions are run directly as evidence
- [x] Local gates at `179304b`: `just check` passed
- [x] Evidence at `179304b`: audit before/after, refs, merge command, allow rules, `uv.lock` (above)
- [x] Review: approved at `d72df44` plus the uncommitted diff, committed as `179304b`
- [x] Verified at `179304b`
- [x] CI green at `179304b`

## Internal references

- CR-190 eval-kit-review-fixes (batch-13); specification, review and the Verifier's evidence in its folder (`work/verifier/`).

</details>
