Head: 1f209e139e616a8748817a49951cbf3d9627ad2d

NOT VERIFIED

Move judged: 3df0c86..124a348 -> 316f283..1f209e1 (restack). Previous judgment: verifier/verify-124a348.md.
The code claims hold. Only the posted description of PR #523 fails (claims D1 and D2); both are body-only fixes.
Worktree clean, `git ls-remote origin` of the branch = 1f209e1. Logs: work/scratch/artifacts-45706313890/.

## Failed (description, judged at 1f209e1)

D1. Known gaps does not match the heavy run at the head. FAIL.
- `gh run view 45706313890 --json status,conclusion,attempt,jobs`: attempt 2, completed, failure; integration, report, checks failure.
- Attempt 1 (`--attempt 1`): integration, report, checks failure.
- integration-a1.log: `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms deadline ... last heartbeat step: diff-preview-scroll`.
- integration-a2.log: `STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not return within 10000 ms (frame )` (not a launch timeout).
- report-a2.log: `FAILED integration: integration manifest status is failed`.
- The body names only the first attempt's integration failure. It names neither the second failure nor the `report` / `checks` jobs
  (the same omission of `report` failed the first description pass at 124a348).
- Not shown to be the CR's: `STEP done: open-at-line (22126 ms)` in attempt 1 at the same SHA. The cause of the attempt 2 timeout was not diagnosed further.
- Suggested bullet: "The heavy run 45706313890 at 1f209e1 failed on both attempts in `integration` (and so in `report` and `checks`):
  attempt 1 on a trusted-suite launch timeout (`diff-preview-scroll`), attempt 2 on a `locator.count` timeout at `open-at-line`,
  a step that passed in attempt 1."

D2. The picture proof names no SHA. FAIL.
- pr-body.md Deliverables: "pictures taken before the restack onto the current base; the chart code is unchanged since": a reason, no SHA
  (card: each proof names the head or `carried from <sha7>`).
- The pictures were captured at 4404b98 (verify-4404b98.md; verify-124a348.md claim 6). Suggested: "taken at 4404b98, carried to 1f209e1: ...".
  The reason itself is true (claim 6 below). The ship check's warning on an old SHA does not remove the card's rule.

## Judged again at 1f209e1

1. Move. `git diff 3df0c86 124a348 -- . <exclude the advanced-renderings-tour and export-html clip folders> | git patch-id --stable`
   and the same for 316f283..1f209e1: both `9c565923d92e3bb0dbd27106c720fb46676174df`. `git range-diff` differs only by the four clip files
   dropped and commit 124a348 skipped. PASS.
2. Unit and chart page tests (base brought widthMode.ts and tests). PR run 45706072543 static log: `tests 5288, pass 5242, fail 0, skipped 46`,
   `tests 35/pass 35`, `tests 107/pass 107`, `ci-static: passed`. That job has no Chromium for the chart page tests (they show as skipped), so run here:
   `node --import ./scripts/register-myst-patches.mjs --test` on chartCsp, chartTooltip, chartViewCache, vegaChart, chartError, exportSnapshot
   (out/test/page): `tests 64, pass 64, fail 0, skipped 0`. PASS.
3. `git grep -n "myst-vega-image" 1f209e13`: no output, exit 1. PASS.
4. Clips left in the base. `git ls-tree docs/demo-video/clips/`: no advanced-renderings-tour. `git grep -niE "vega|chart" 1f209e13 -- docs/demo-video/clips/export-html`:
   only "flowchart" hits and the stage's `flowchart LR`; no chart selector. `git diff --stat 316f283e 1f209e13 -- docs/demo-video`: theme-switch only.
   The spec's takes for the two moved clips are not delivered by this head, on purpose (patch in conflict-resolver/clip-hunks-for-later.patch);
   the body says so under Autonomous decisions. Not judged failed. PASS.
5. Requirements and changelog. static log: `1227 requirements, 0 errors, 26 warnings`; `git diff 316f283e 1f209e13 -- CHANGELOG.md requirements/tiers/log.md`:
   one CR-503 line under Unreleased (PR #523) and one CR-503 log entry above CR-502's. PASS.
6. "The chart code is unchanged since": `git diff --stat 124a348 1f209e13 -- src` lists only src/page/modules/widthMode.ts, a base change on
   code block breakout. PASS.
7. Real window. integration-a1.log (attempt 1, checkout 1f209e1): `PASS real-input screenshot: diagrams/r01-live-chart-hover`. Attempt 2 stopped before that step. PASS.
8. PR run: `gh pr checks 523`: static, static-windows, visual, viewer-graph, checks, report pass (run 45706072543, head 1f209e1). PASS.
9. Local gate: Driver note of `chantier log CR-503`, "just preflight (static stage, Windows) passed at 1f209e1" (not re-run, per the brief). PASS.
10. Review box: Driver note "move 124a348..1f209e1 (restack) inspector approved at 1f209e1". PASS. ("approved before the restack" would be clearer with its SHA.)
11. Description, rest: `gh pr view 523` body equals work/pr-body.md; draft, open, mergeable, base cr-502 branch (#520 head 316f283); the 40 changed files
    match Changes; no role name outside Autonomous decisions / Internal references that fails. PASS.

## Carried

- Picture content, byte identity of the uploaded images, no username or home path: carried from 124a348: the move changes no chart code and no image.
- theme-switch take: carried from 124a348 (taken at 4404b98): its two files and the CR's src are unchanged; the base's clip-kit change only lowers the
  length bound to 12 s (check.mjs, storyboard.mjs) and the clip is 10.9 s; widthMode.ts touches code block breakout only.
- Tests fail on the previous code; Summary, Deliverables diagram, Impacts, Blast radius; CSSOM style gap: carried from 124a348: patch unchanged.
- Main's heavy run 45580228461 failure: carried from 124a348 (`gh run view` here: head 4a47151, integration failure).
- export-html take (verify-124a348.md claim 5): dropped, not carried; the head no longer changes that clip.

No before/after capture again: the move touched no pair.
