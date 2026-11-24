# Verify CR-471 (round 1)

Head: a96fd75ac3445a4e0926464c35a698ee8048f446

Base: 3c29dd7c7aa6dc44961dc8f1588ab6fa4b2371b4 (= origin/main).

Verdict: VERIFIED at 3be21b3 (round 4 below); fa40185 was NOT VERIFIED (round 3, a broken newline literal, fixed) (round 2, see the end; round 1 claims 4 and 5 are superseded there)

## Claims judged at 4a1b125

1. Full test suite at the head (worktree sources via PYTHONPATH, cards read from the worktree):
   `uv run --no-sync --project <main> python -B -m pytest -q -p no:cacheprovider -n 4 skills/chantier/scripts/cli/tests -x`
   output: all dots, 100%, exit code 0. PASS. Test file sizes (`wc -l`): test_startup_manifest.py 395,
   test_role_cards_split.py 180, test_start_reading.py 91, test_plugin_files.py 399 (unchanged). PASS.
2. Links: a script over every `*.md` checking each `](x.md#anchor)` against the target's headings:
   only 3 hits, all external URLs mis-parsed (release notes, evals/README). No broken anchor into
   `chief-of-staff.md`, `foreman.md`, `driver.md` or any piece. PASS.
3. Text moved, not lost (line and word multisets of base `chief-of-staff.md`, `foreman.md`,
   `driver.md` vs the three entry cards plus the new pieces; `work/scratch/lines.log`, `words.py`):
   words lost beyond link rewrites are only the "Deferred:" / "Concepts:" / "Specification" /
   "A Driver started again" opening bullets, which the specification lets become lines of the
   list of moments. PASS for the three cards.
4. "No rule is added, none dropped; a duplicate found is said in the PR, not merged away"
   (specification, section 1). FAIL. `git diff --word-diff HEAD~1 HEAD` on
   `skills/chief-of-staff/SKILL.md`, `skills/griller/SKILL.md`, `skills/status/SKILL.md`,
   `skills/chantier/SKILL.md`, `startup-core.md`, `session-start.md` shows text reworded and cut that
   the specification does not touch (it asks only for link updates there and the Q11 sentence):
   - the CoS skill description's "With no argument the session's batches follow the surface (Foreman at
     the desktop, direct under Remote Control ...)";
   - the `$CHANTIER` paragraph of four SKILLs: "never a Foreman, a Driver or a worker" (syncs), "runs no uv sync"
     (reload), "chantier writes only to the planning folder ..." line, "the question is ..." and other clauses;
   - `startup-core.md`: ', never "without it"';
   - `session-start.md` "5. Reload": its first sentence replaced.
   `work/coder/r1.md` ("Duplicates removed") and the PR body ("Five duplicate sentences removed") confirm
   it was done to fit the 12,544-byte manifest limit. The specification says that a cut that cannot fit is
   redone with shorter action lines, else handed back blocked with the figures; it does not allow
   shaving other text.
5. PR description draft (`work/pr-body.md`) against the specification's Evidence section. FAIL:
   - the three moved-rule tables are not in Deliverables (they are in `work/tables.md`);
   - "no rule lost" contradicts claim 4; Known gaps does not name the duplicates removed;
   - the figures give base and after only, not today's `main` figures too, and no boot/reload bytes per role;
   - Test plan boxes are unticked, the long gate is pending (expected, running).
6. Start readings (PR body table, from `test_start_reading.py`, passing at the head): CoS 0.47, Foreman 0.30,
   Stack 0.49, QA 0.67, Release 0.53 of base; CR Driver 1.08 (grew 25,134 to 27,122), the one role
   that did not reach "about half": declared in Known gaps with its reason. Carried as stated, not a failure.

Not run: the long gate (running, per the brief); `just check` as a whole (its tests were run, claim 1).
No Fable reading (the Chief of Staff's, section 5). No before/after evidence (no UI; the figures are the proof).

## Round 2 at 4a1b1253682ae97457fe4505ebbb416d9cd25b94 (same head, updated PR body)

Claims 1 to 3 and 6 carried from round 1: same head, no commit since.

4b. The reworded startup text is the user's decision: `STATUS.md` line 43 of the CR folder records
    "user chose option 3 (A-9): free about 900 bytes in the CoS startup reading (the CHANTIER paragraph of
    skills/chief-of-staff/SKILL.md and startup-core.md, other roles' skills if needed), no rule lost, the
    12,544 limit stays, no second manifest". `grep -n "A-9" STATUS.md` shows it. Judged: no rule dropped,
    read at the head (`git diff --word-diff HEAD~1 HEAD` on the six files, then `grep`/`sed` of the targets):
    - the no-argument mode sentence: `session-start.md` still says "Say which mode ... forced, Remote Control, a host that cannot start a Foreman, or the desktop";
    - "chantier writes only ...": `session-start.md` "Zero configuration" holds it, archive in the PR included;
    - reload "no uv sync": `session-start.md` "5. Reload" Does still says "no order, `take`, heartbeat, Driver, message or `uv sync`";
    - the old reload-reads-only sentence: the manifest's `reload` action lists `startup-core.md`, `role-core.md`, the manifest and `session-start.md#5. Reload`, and `startup-core.md` says to read every reading the action lists;
    - ', never "without it"': covered by "The CLI is never a tool a role works without";
    - "never a Foreman, a Driver or a worker" (sync): implied by "only the steering session syncs" (a note, not a lost rule);
    - the Windows folder sentence in `startup-core.md`: same meaning.
    PASS.
5b. PR body (`work/pr-body.md`, 25,501 bytes): holds the figures, boot and reload per role, manifest size, the
    three moved-rule tables, Human decisions, and Autonomous decisions names the five shortened texts. The CR Driver
    growth is in Known gaps. PASS. Open: Test plan boxes unticked and the long gate pending (the Driver's to tick).

## Round 3 at fa40185c93e83f5f22864d8a0aefc12828c61ca9

The move is one commit, `scenario/run_scenario.py` only (`git diff 4a1b1253 HEAD`, 5 insertions, 2 deletions).
The two `check` calls and their assertions are untouched. But the new lines hold a raw line break inside the
string literal: `sed -n 6520,6528p scenario/run_scenario.py | cat -A` shows `foreman = "$` then `".join(...)`.
`python -c "import ast; ast.parse(open('scenario/run_scenario.py',encoding='utf8').read())"` gives:
`SyntaxError: unterminated string literal (detected at line 6523)`. The scenario cannot run: FAIL.
Claims 1 to 3, 4b, 5b, 6 are carried from 4a1b125: only that file changed and no test or card reads it
(claim 1's test suite does not import the scenario, so it is not proof of this commit; re-run `just check` after the fix).

## Round 4 at 3be21b3e390c29d3b823b31c9b175442d26c6552

`git diff 4a1b1253 HEAD` is `scenario/run_scenario.py` only (3 insertions, 2 deletions): the two card reads
now join `foreman*.md` and `*driver*.md` with "
"; both `check` calls and their assertions are unchanged.
`python -c "import ast; ast.parse(open('scenario/run_scenario.py',encoding='utf8').read())"` prints `parse ok`.
I ran the 15 asserted phrases of the two checks against the joined cards at the head: all True
(`True True True True True` and nine more `True`). PASS.
Claims 1 to 3, 4b, 5b and 6 carried from 4a1b125: the cards, tests and manifest did not change since.

## Round 5 at a96fd75ac3445a4e0926464c35a698ee8048f446 (fix round 1, Fable readings)

Move: 33 files (`git diff --stat 3be21b3 HEAD`): cards, manifest, moved_rules.tsv, test_start_reading.py.
1. Full test suite at the head: `PYTHONPATH=skills/chantier/scripts/cli/src uv run --no-sync --project <main> python -B -m pytest -q -p no:cacheprovider -n 4 skills/chantier/scripts/cli/tests`
   output: `2405 passed, 20 skipped in 184.34s`; `git status --short` clean. PASS (includes manifest limit, split and moved-rule tests).
2. Text moved, not lost (word multiset of removed vs added lines of `git diff 3be21b3 HEAD -- skills/chantier/references`, manifest and tsv excluded):
   137 words net removed, nearly all pointer words (below, above, chief-of-staff.md, Your means, While) replaced by action names; the content words
   in the list (Half-done irreversible, contributors, critic:) were found with `git grep` at HEAD in driver.md, chief-of-staff-grill.md, chief-of-staff-batch-end.md. PASS.
3. PR description: `gh pr view 450` body equals `work/pr-body.md` (only a trailing blank line differs); it names a96fd75; Summary, figures, fix-round growth and Known gaps
   (dropped CoS sentence, critic rule, readings not re-run) match `work/r1.md`. PASS.
4. Long gate at a96fd75: `work/gates/20261124-122353.log` first line `gate CR-471 ... head a96fd75ac3445a4e0926464c35a698ee8048f446`; still running at this verdict, not judged here (the Driver cites its end). A pass existed at 3be21b3.
Claims 4b, 5b of earlier rounds carried (same reasoning); claim 6 superseded by the PR body's figures, consistent with r1.md.

VERIFIED at a96fd75.
