# Verify CR-445 board-history

Head: 12e6f7bc0874291f3baa8210175b414d47145e87

## Claims (all judged at 12e6f7b)

1. Spec Evidence items 1-8 (local day, week/month limits, totals, older records, running batch, index reuse, protocol refusals, close keys): VERIFIED.
   Command (worktree, `skills/chantier/scripts/cli`): `uv run --no-sync --project <worktree> pytest tests/test_board_history.py tests/test_board_history_client.py tests/test_order_drop_to.py tests/test_board_design.py -q`
   Output: `100 passed in 22.01s`.
2. Item 9, shipped client files: VERIFIED. `git diff <base>...HEAD -- .../js/views/registry.js` shows `+import * as history from './history.js';` and
   `+  { id: 'history', icon: 'history', word: 'nav.history', module: history },` right after the `prs` entry, before `costs`;
   `ls js/i18n` lists `en-history.js` and `fr-history.js`; `index.html` line 36 links `css/views/history.css`;
   `tests/test_board_history_client.py` and `tests/test_board_design.py` are in the run of claim 1 (pass). Biome/just check: gate log below.
3. Gates at the head: gate log `work/gates/20261122-040514.log`, first line `gate CR-445 branch chantier/batch-30/cr-445-web-board-history-page-what-was-done-per head 12e6f7bc0874291f3baa8210175b414d47145e87`, line 32 `result: pass at 12e6f7bc0874291f3baa8210175b414d47145e87` (includes the scenario's close check). Worktree clean at HEAD (`git status --short` empty).
4. Scenario's close check: VERIFIED by the gate pass above (scenario/run_scenario.py changed in the diff, 16 lines).
5. PR description (work/pr-body.md): clean, sections and fold present, mermaid block, no images (so no username or home folder shown). Summary, Deliverables and Changes match the diff stat (history_page.py, cr_times.py, history.py, close_archive.py, protocol, topics, ops, router, registry, icons, en/fr-history, history.css, DESIGN.md, docs, tzdata in pyproject/uv.lock, tests). The look of the page is marked **UNVERIFIED** and appears in Known gaps ("No screenshot of the page from a real browser yet"): consistent. Test-plan boxes are unchecked placeholders for the Driver; no Review box SHA is claimed yet, so not judged.
6. Screenshots (day, week, month, empty, EN and FR) and the narrow screen: NOT CAPTURED (no browser or screen tool, and a served board needs a background process, refused to a Verifier). The look of the page is therefore UNVERIFIED, already marked so in the description and its Known gaps; this does not alone change the verdict.
7. Live read of the real surface (project `chantier`, read-only, in process: `history_page.answer` with `Repo.find(project="chantier", readonly=True)`, zone Europe/Paris, run from the surface folder):
   month 2026-11-01: `merged 132, dropped 0, opened 145, releases 0, cost_usd 517.9103, cost_partial True`, 7 days, `undated 197, unreadable 0` (197 matches the spec's count on disk); first call 3.136 s, second 2.55 s.
   day 2026-11-21: merged 16, opened 22, cost 85.1098; day 2026-01-05: all zero, 0 days (an empty period).
   Timing note: `reads.state_of` alone costs 2.216 s in this cold process (no server cache) and `index_of` 2.036 s, so the index itself is ~0.3 s on top of the state read the board pays for every page; the second call is not faster here because the state read dominates. The over-HTTP `curl` first/second-call figures the spec asks for are NOT measured; the "no visible wait" claim is UNVERIFIED.

## Verdict

VERIFIED for the server, protocol, close keys, client files and gates at 12e6f7b. Not proven: the page's look in a browser and the HTTP timings; both are named UNVERIFIED (pr-body Known gaps carries the screenshot; the HTTP timing is not claimed in the description).

VERIFIED

## Description pass (posted body of PR 419, judged at 12e6f7bc0874291f3baa8210175b414d47145e87)

Command: `gh pr view 419 -R gsemet/chantier --json body,headRefOid` (headRefOid = 12e6f7bc0874291f3baa8210175b414d47145e87); `gh pr view 419 --json isDraft,baseRefName,statusCheckRollup` (draft, base CR-441 branch, 5 checks SUCCESS).
- Renders: sections, mermaid, fold present; no image (no username or home folder).
- Summary, Deliverables, Changes match the diff and claims 1-7 above; no role name outside a product term.
- Test plan SHAs honest: check and scenario at 12e6f7b (gate log 20261122-040514, pass); eval-dry-run at 86544ac, `git diff --stat 86544ac 12e6f7b` touches only scenario/README.md and scenario/run_scenario.py, as stated; Review box matches driver notes (r1+r2 at 819b848, r3 at 86544ac committed as 12e6f7bc); Verified and CI green at 12e6f7b match the log notes and the checks.
- Known gaps: carries the UNVERIFIED screenshot and the month timing (3.1 s, 2.55 s, 2.2 s in state_of, same as claim 7); base-is-CR-441 draft note true.
VERIFIED
