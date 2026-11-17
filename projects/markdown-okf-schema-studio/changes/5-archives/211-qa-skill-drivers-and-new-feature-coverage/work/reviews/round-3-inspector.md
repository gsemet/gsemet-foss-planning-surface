# CR 211 — Inspector review, round 3 (final)

Worktree: `markdown-okf-schema-studio-wt-211` (base `b9118506`). Scope: `git diff` plus the
untracked files under `.agents/skills/markdown-studio-exploratory-qa-claude/`.

## Verdict: APPROVE

All round-2 findings are fixed. The major one was finding 1, the noop-sweep way back. It now
expands the collapsed toolbar, waits for an enabled Back button with a real size, and checks the
document id after each click and at the top of each target. If Back fails, it aborts the whole
sweep, still writes the report, and exits non-zero. Items 1–7, the "Done when" list and the two
owner replay fixes (`synth/admon.md`, c2-1) are in place. Round 3 added no blocking regression.
The findings below are all minor or nits.

## Round-2 findings: status

| # | Status | Note |
| --- | --- | --- |
| 1a | Fixed | `goBack()` (`noop-sweep.mjs:98-119`): if `[data-sphinx-preview-toolbar-collapse][aria-expanded="false"]` exists, it clicks the button through `box()` and waits 600 ms. It then polls up to 12 × 250 ms for Back: present, `!disabled` (it is a real `<button>`, `historyControls.ts:21,41`), and a non-zero rect. It clicks only when `box()` returns `w > 0 && h > 0`, so there is no stray click at the frame origin. It then polls `DOC_ID` up to 20 × 250 ms and re-enters edit mode only on success. The coordinates are right: `box()` adds `BASE`, the frame offset (`qa.mjs:246-247`), the same as `page.mouse.click` expects |
| 1b | Fixed | `abort()` sets `aborted` and `report.aborted`. `break` leaves the target loop, and `if (aborted) break` stops the outer loop, so later kinds do not run. The report JSON is still written (`:186-191`). Then `SWEEP ABORTED` is printed and the script throws, so `qa.mjs:465` exits with 1 |
| 1c | Fixed | `DOC_ID` is compared at the top of each target, after `settle()` (`:131-134`). `docId` is read once, before the loop (`:90`), so the first check cannot misfire. `runtime.ts:93` always sets the attribute. If both the attribute and the fallback were absent, `docId` and every later read would all be `""`, so the comparison stays equal and does not misfire |
| 1 docs | Fixed | `SKILL.md:134-139`, `harness-pitfalls.md:~88-92` and the script header now say "stops the whole sweep", aborted and non-zero |
| 2 | Fixed | Rule 2 runs only when `on_default_branch(rev)` (`new-features.py:70-82`): `origin/HEAD`, then `origin/main`, then `origin/master`, via `merge-base --is-ancestor`. It returns False when no ref resolves, which is fail-safe: the rule is turned off and more rows are kept, with a comment explaining why. Rule 3 now needs the exact `"<title> (#N)"` subject |
| 3 | Fixed | A failed optional action prints `optional step skipped` and is not counted or pushed to the results (`engine.mjs:368-374`). A non-optional failure still increments `failed`, records the result, takes a shot and stops. The summary `passed`/`failed` and the exit code are consistent. `scenario-format.md:38-39` documents it |
| 4 | Fixed | The header and SKILL.md say "skipped only when every candidate point is on a link" |
| 5–6 | Fixed | The wording is fixed. The remaining lines over 100 characters are frontmatter, table rows, code-block lines, or return-format templates |
| 7 | Fixed | No `__pycache__` in the worktree |

## Findings (non-blocking)

1. **minor**: `scripts/noop-sweep.mjs:131,155`: a failed `DOC_ID` read is treated as a navigation.
   Both checks use `wv(DOC_ID).catch(() => "")`. A one-off `wv` error (for example, the frame is
   briefly unavailable during a re-render) therefore looks like "document changed". `goBack()` then
   finds Back disabled because there is no history, so it **aborts the whole sweep**. Before round
   3, the same error only added one line to the per-target errors. It is fail-loud, not
   fail-silent, so it does not block. **Fix:** on a read error or an empty result when `docId` is
   not empty, wait 250 ms and read again once before calling `goBack()`.
2. **nit**: `scripts/new-features.py:138-154`: rule 2 can still drop a PR in one narrow case. If
   the revision is a commit of a feature branch that was later merged into the default branch with
   a merge commit, it is an ancestor of `origin/main`, but PRs merged into main *between* its
   committer time and that merge are not in it. Campaigns normally test the default branch HEAD,
   so this is acceptable. A stricter check would be "rev is on the first-parent chain"
   (`git rev-list --first-parent origin/main | grep rev`).
3. **nit**: `scripts/noop-sweep.mjs:105-108`: after a recovery, the toolbar stays expanded for the
   rest of the sweep. Block clicks are safe (`PICK_POINT` rejects points covered by the toolbar).
   Cell and field clicks use a fixed point without a hit test, but they come after
   `scrollIntoView({block: 'center'})`, so the risk is low. A one-line note in the pitfalls entry
   would be enough.
4. **nit**: `scripts/engine.mjs:378`: `!keepGoing && !step.optional`. The `!step.optional` part
   can no longer be false there, because optional steps `continue` earlier. Harmless.

## Gates (re-run by the Inspector)

| Gate | Result |
| --- | --- |
| `bash -n scripts/setup-workspace.sh` | OK |
| `PYTHONPYCACHEPREFIX=/private/tmp/claude-502/cr211-driver/pycache python3 -m py_compile` on all skill `.py` | OK |
| `node --check` on all 9 skill `.mjs`/`.js` files | all OK |
| JSON parse of `scenarios/*.json` (22) and `assets/synth/*.json` | all OK |
| Relative links in skill `.md` (outside `assets/`) | all resolve. The one hit, `harness-pitfalls.md:83`, is `[Chapter N](…)` inside a code span: a false positive |
| `git status`: changes only under the skill folder | yes |
| `__pycache__` in the worktree | none |
| noop-sweep live run | Not run (VS Code not allowed); reviewed from the source |

## Dry-run outputs (verbatim)

`python3 scripts/coverage-map.py --campaign /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/04-archives/210-qa-campaign-2026-10-31`
(rc 0, from the Baseline line on):

```text
## Baseline: b9118506 from /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/04-archives/210-qa-campaign-2026-10-31 (--campaign)
## Changes since b9118506 (0 commits)
product sources: unchanged
areas without product changes (lower priority unless never explored): A1 A2 A3 A4 A5 B1 B2 B3 B4 B6 C1 C2 C3 C4 D1 D2 D3 D4 D5 D6 D7 E1 E2 E3 E4 E5 F1 F2 F3
```

`python3 scripts/new-features.py --campaign <same>` (rc 0):

```text
<!-- baseline: 2026-10-30, revision b9118506, source: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/04-archives/210-qa-campaign-2026-10-31 (--campaign) -->
<!-- already in b9118506: #236 (merge commit is an ancestor); #234 (merge commit is an ancestor); #233 (merge commit is an ancestor); #232 (merge commit is an ancestor); #231 (merge commit is an ancestor); #230 (merge commit is an ancestor); #228 (merged before the revision was committed) -->

### New-feature coverage (0 PR(s) merged since 2026-10-30)

| PR | Feature | Charter | Result |
| --- | --- | --- | --- |
| (none) | | | |

Charter: charter ID, or `automated: <test>`. Result: PASS / finding IDs / not run.
A user-facing PR left at TODO is a gap: list it under Limits; status cannot be `completed`.
```

Campaign 210 still gives 0 rows. `b9118506` is on `origin/main` (`origin/HEAD -> origin/main`),
so rule 2 stays on and still drops #228.

The Inspector added no file to the worktree.
