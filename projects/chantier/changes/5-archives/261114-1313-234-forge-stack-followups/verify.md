# Verify CR-234

Head: 7742cc9d96cc6134971eca1f99f18a6477954775
Verdict: NOT VERIFIED (round 2, delta after the rebase onto main 4d9075f)

The move: 756a387 (on the CR-221/CR-237 stack, base 2d9a2aa) rebased onto main 4d9075f.
`git range-diff 2d9a2aa..756a387 4d9075f..7742cc9`: the CR's patch changes only in
`commands/permissions.py` (main dropped the `gh-release`/`glab-release` samples and the rules
reading in `_sample_groups`, signature now `_sample_groups(remote)`) and in `hosts/claude-code.md`
(the P10 paragraph no longer names "the publication"). `git diff --stat 756a387 7742cc9` on
`commands/facts.py`, `commands/forge_stack.py`, `commands/delivery.py`, `scenario/fake_gh.py`:
empty. The base changed almost every file of the CLI, so the code claims are judged again.

Claims, each at 7742cc9 unless carried:

1. P10 detection via `gh extension list` (Area 1). Diff `4d9075f..7742cc9`: `_gh_names_stack`
   runs `[gh, "extension", "list"]` with `check=False`, `timeout=GH_LIST_TIMEOUT` (10),
   utf-8/replace; no gh, OSError, timeout or non-zero reads as no; folder test removed.
   `Select-String ... -Pattern "XDG_DATA_HOME|LOCALAPPDATA"` over `src/chantier/*.py` and
   `src/chantier/commands/*.py`: no match. Probe:
   `uv run --locked --project <worktree> python -c "...print(_gh_names_stack(), sorted(g), n)"`
   -> `True ['always', 'dev', 'gh-stack', 'github'] 14` (`gh extension list` here:
   `gh stack	github/gh-stack	v0.3.0`). Real run `chantier preflight` at the worktree:
   `P10 warn 1 of 15 commands ...` (14 samples + SendMessage, gh-stack counted). Scenario steps
   present in the diff (`run_scenario.py` +566..584); CI `just scenario` at 7742cc9 was pending at
   this pass (not seen green). VERIFIED for the code.
2. P10 count explained (Area 2). `hosts/claude-code.md` +124..128 and the `gh stack*` row
   ("only when `gh extension list` names `gh-stack`"); comment "P10 counts these commands, not
   rules." above `SAMPLES`. The paragraph drops "the publication" because main removed that group
   (consistent with the code at head). VERIFIED.
3. rebuild exits 4 (Area 3). `commands/forge_stack.py`: `UNSTACK_TRIES = 5`, the `else` raises
   `ChantierError(..., EXIT_EXTERNAL)` with `stack #<n> is still open after 5 unstack tries (the
   forge reads it back with #.. | open, with no PR)`; docstring added. File unchanged since 756a387.
   Scenario step 3b in the diff. Carried from 756a387 for the run (transcript cited there):
   the file and `fake_gh.py` did not change. VERIFIED.
4. Stale-SHA scan (Area 4). `commands/delivery.py` `_stale_token`: pattern
   `\b(?=[0-9a-f]{0,39}[a-f])[0-9a-f]{7,40}\b`, docstring updated. File unchanged since 756a387.
   Scenario step in the diff. VERIFIED (run carried from 756a387).
5. Area 5 evidence. Carried from 756a387: evidence on `_stack_base`, which neither the patch nor
   the range-diff touches (`work/coder/area5-old-stack-base.log` 698/700 with the two FAIL lines,
   `area5-current.log` 700/700).
6. Fast gate. `just check` in the worktree at 7742cc9: ruff format/check pass, mypy "Success: no
   issues found in 86 source files", `uv lock --check` ok, pytest `63 passed`, release-notes ok.
   CI at 7742cc9: `just check` ubuntu pass, windows pass; macOS, scenario, eval-dry-run pending.
   Long local gate: none at 7742cc9, waived by the user (driver note 2026-11-14T11:50:09Z).
7. PR description on the forge (`gh pr view 175`, headRefOid 7742cc9). FAILS:
   - Deliverables: "reads `P10 warn 2 of 16 commands`: the 16 samples are ... 1 for
     `gh release create` (the project's rules name it)". At 7742cc9 the `gh-release` group no
     longer exists and the real run reads `P10 warn 1 of 15`. Inconsistent with what the PR
     delivers at head.
   - Test plan: "Verified at `21f5677`" and "CI green at `21f5677`": 21f5677 is not the head
     (7742cc9).
   - Proofs named "at the pre-restack head" (Deliverables line "the full gate passed at the
     pre-restack head", "`just scenario` at the pre-restack head", Local gates, Evidence, Review)
     name no SHA and give no `carried from <sha7>: <reason>`: each proof must name its SHA.
   - Review box "approved at the pre-restack head plus the diff committed as the pre-restack head"
     names no SHA, so no Driver note can be matched to it.
   - Known gaps does not say that no local long gate ran at the head (user waiver).

Verdict: NOT VERIFIED, on claim 7 (the description) only; the code claims 1 to 6 hold at 7742cc9.

## Description-only pass (rewritten body, head 7742cc9)

`gh pr view 175 --json headRefOid,body`: headRefOid 7742cc9d96cc6134971eca1f99f18a6477954775.

Fixed: Deliverables reads `P10 warn 1 of 15 commands` at 7742cc9 (matches my run); the Test plan
names 7742cc9; Known gaps names the waived local long gate; the Review box ("approved at e54e299
plus the diff committed as 756a387; carried to 7742cc9") matches the Driver's note
(`chantier log CR-234`: "r1 approved at e54e299, committed as 756a387"); Area 5's carry ("the code
it covers is unchanged by the rebase") holds: `git diff --stat 756a387 7742cc9 --
commands/facts.py` is empty. `just check` on the three OSes: CI at 7742cc9 lists check macOS,
ubuntu, windows pass (mypy runs inside `just check`).

Still fails: the Test plan's Local gates line says "`just scenario` pass on both forges at 756a387
(carried: scenario files unchanged by the rebase)". `git diff --stat 756a387 7742cc9 -- scenario/`
gives `scenario/run_scenario.py | 360` (355 insertions, 5 deletions, brought by main). The carry's
reason is false. Fix: give a true reason, or say that the scenario at 7742cc9 rests on CI's
`just scenario` (pending at this pass) and on the waiver in Known gaps.

Verdict: NOT VERIFIED (description, one item).
## Description-only pass 2 (head 7742cc9)

`gh pr view 175`: headRefOid 7742cc9d96cc6134971eca1f99f18a6477954775. The Local gates line now
reads "carried: this CR's own scenario steps are unchanged by the rebase; main added other steps
to `run_scenario.py`, so the scenario at 7742cc9 rests on GitHub CI", and the Deliverables carry
says the same. Proof: the changed lines of the CR's patch to `scenario/run_scenario.py`,
`git diff e54e299 756a387` vs `git diff 4d9075f 7742cc9`: 45 and 45 lines, `Compare-Object` finds 0
differences. All other items as in the previous pass (P10 1 of 15 at 7742cc9, Review box matched to
the Driver's note, waived gate in Known gaps, no STALE, no stale SHA). CI at 7742cc9: check
macOS/ubuntu/windows and eval-dry-run pass; `just scenario` pending (Known gaps covers it).

Verdict: VERIFIED at 7742cc9 (code claims 1 to 6 from round 2, description from this pass).
## Round 3 (head 9bd0412, rebase onto main 3fb9129, P10 per capability)

Head: 9bd0412d71a16a1ddc3ee4b60ce150edd23d94eb (`gh pr view 175` headRefOid matches; merge-base with
origin/main = 3fb9129).

`git range-diff 4d9075f..7742cc9 3fb9129..9bd0412`: the patch changes only in `permissions.py`
(`_sample_groups` is now main's `_forges`; the gh-stack test is `"github" in forges and
_gh_names_stack()`; comment kept above `SAMPLES`), the P10 scenario step (`preflight --mode stack`,
P10 lines joined), the card's P10 paragraph (per capability) and `scenario/README.md`.
`forge_stack.py`, `delivery.py`, `fake_gh.py` patches identical. `_stack_base` untouched
(`git diff 7742cc9 9bd0412 -- commands/facts.py`: only main's `ci_lines` import/use).

1. Area 1: no `XDG_DATA_HOME|LOCALAPPDATA` in `src/chantier/*.py`, `commands/*.py`. Probe:
   `_gh_names_stack()` True, `_forges('origin')` = any, dev, gh-stack, github; the only gh-stack
   sample is `gh stack view`, capability `stack`. VERIFIED.
2. Area 2: card paragraph says each P10 line counts its capability's commands, gh stack for a
   stack when `gh extension list` names it, SendMessage for every batch, Windows both forms, pre-0.9.0
   not comparable; `gh stack*` row reworded. Matches the code (batch: 13 samples + SendMessage = 14;
   stack: 1). VERIFIED.
3. Area 3 and 4: code as at 7742cc9 (UNSTACK_TRIES, EXIT_EXTERNAL, message, docstring; lookahead
   regex). VERIFIED (scenario run on CI).
4. Real preflight at the worktree (user settings): default mode
   `P10 warn every batch: 1 of 14 commands ...: uv run --locked --project /checkout chantier status`
   and "not checked here: a stack, ..."; `--mode stack`: same batch line plus
   `P10 ok   a stack: the commands its agents run are allowed by your settings`. With an empty home:
   `P10 warn a stack: 1 of 1 ...: gh stack view (add Bash(gh stack*), PowerShell(gh stack*))`.
   No `1 of 15` line exists any more.
5. `just check` in the worktree at 9bd0412: ruff ok, mypy 86 files ok, lock ok, pytest 63 passed,
   release-notes ok. CI at 9bd0412: check macOS/ubuntu/windows pass, eval-dry-run pass, scenario
   pending at this pass. Local long gate waived.
6. PR body (work/pr-body.md identical to the GitHub body): FAILS, every head reference names 7742cc9
   and two carries/counts are now false. Lines of work/pr-body.md:
   - 21: "scenario at 7742cc9 rests on CI" -> 9bd0412; and "carried: this CR's own steps unchanged"
     no longer holds for the P10 step (now `--mode stack`).
   - 30: "reads `P10 warn 1 of 15 commands` at 7742cc9" is false: at 9bd0412 the run reads
     `P10 warn every batch: 1 of 14 commands` and, with `--mode stack`, `P10 ok   a stack` (gh stack
     view allowed, found through `gh extension list`).
   - 48: "No local long gate at 7742cc9" -> 9bd0412.
   - 57: "the `gh-stack` group applies" -> the gh-stack forge (a stack's capability) applies (wording).
   - 70: "`just check` ... pass at 7742cc9" -> 9bd0412; the carry reason "this CR's own scenario
     steps are unchanged by the rebase" is false at 9bd0412 (the P10 step changed); say the scenario at
     9bd0412 rests on GitHub CI.
   - 71: Evidence "carried to 7742cc9" -> 9bd0412 (reason holds: `_stack_base` unchanged).
   - 72: Review "carried to 7742cc9 (...release groups)" -> name 9bd0412 and the second rebase's
     adaptation (permissions.py `_forges`, P10 step `--mode stack`, card paragraph, README).
   - 73, 74: "Verified at `7742cc9`", "CI green at `7742cc9`" -> 9bd0412.
   - 78 (pointer): `work/preflight-real-settings.log` still holds the 756a387 run (`2 of 16`); refresh
     it or say it is the 756a387 run.

Verdict: NOT VERIFIED (description only; code claims hold at 9bd0412).

## Description-only pass (head 9bd0412)

`gh pr view 175`: headRefOid 9bd0412d71a16a1ddc3ee4b60ce150edd23d94eb; the GitHub body equals
work/pr-body.md. Fixed from round 3: lines 21, 30 (`P10 warn every batch: 1 of 14`, `--mode stack`
`P10 ok   a stack`, matches my run), 48, 57, 71, 72 (adaptation stated as unreviewed), 73, 74, 78 (log
labelled as the 756a387 run). CI at 9bd0412: check macOS/ubuntu/windows and eval-dry-run pass;
scenario pending.

Still fails: line 70, "`just scenario` pass on both forges at 756a387 (carried for the CR's code,
unchanged since)". The CR's code is not unchanged since 756a387: the rebase onto 3fb9129 changed its
`permissions.py` patch (`_forges`) and its P10 scenario step (`--mode stack`, range-diff in round 3).
Only `forge_stack.py`, `delivery.py`, `fake_gh.py` and `_stack_base` are unchanged. Fix: carry the
756a387 scenario run only for those, and say `permissions.py` and the P10 step rest on GitHub CI at
9bd0412.

Verdict: NOT VERIFIED (description, one line).

## Description-only pass 2 (head 9bd0412)

`gh pr view 175`: headRefOid 9bd0412d71a16a1ddc3ee4b60ce150edd23d94eb; GitHub body equals
work/pr-body.md; no `7742cc9` left. Line 70 now carries the 756a387 scenario run only for
`forge_stack.py`, `delivery.py`, `fake_gh.py` and the `_stack_base` comparison, and says
`permissions.py` and the P10 step rest on GitHub CI at 9bd0412: true (range-diff, round 3). CI at
9bd0412 (run 43594155773): check macOS/ubuntu/windows, eval-dry-run and `just scenario` (11m11s) all
pass. Other items as in the previous pass.

Verdict: VERIFIED at 9bd0412 (code claims from round 3, description from this pass).
