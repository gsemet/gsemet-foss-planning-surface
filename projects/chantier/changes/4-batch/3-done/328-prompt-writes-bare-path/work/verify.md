Head: 906c73fce8b17126c46b0fdaa62e84025b435258

Claims, all judged at 906c73f:
1. handoff (worktree CLI) prints `scratch:` right after `folder:` (absolute, forward slashes, bare) and
   `worker writes line (...)` + `  writes: C:/.../batch-24-CR-328; C:/.../328-prompt-writes-bare-path`:
   bare, absolute, worktree first. Command: `chantier handoff CR-328 --batch batch-24 | grep ...`. PASS.
2. Driver skeleton has one column-0 writes line: proved by test_driver_prompt.py (take is already
   taken here, prints nothing live). PASS via tests.
3. `git check-ignore -v changes/x/work/scratch/f.txt` in a throwaway repo under work/scratch with
   `**/work/scratch/` -> `.gitignore:1:**/work/scratch/ changes/x/work/scratch/f.txt`, rc=0. PASS.
   (Deviation `**/` accepted; IGNORED holds that entry, files.py diff.)
4. Cards diff vs spec 5/6 (concepts template bare + prose, driver Children/checklist/lines 559/capture,
   verifier ground rules/capture, claude-code guard sentence): match. PASS.
5. `pytest test_driver_prompt.py test_cli_runs.py -q` -> 22 passed. PASS.
Not run: scratch isolation probe and scenario (CI scenario ubuntu green per Driver, not re-run).
Scratch folder removed.

VERIFIED

## Description pass

Head: 906c73fce8b17126c46b0fdaa62e84025b435258

Judged at 906c73f with `gh pr view 287 --json body` against `git diff origin/main...HEAD` and pr-template.md.
- Sections in order, fold in place, Internal references last and the only place naming CR-328: PASS.
- Summary, Deliverables, Changes match the diff (facts.py scratch line and worker writes line, files.py `**/work/scratch/`, cards, tests, scenario): PASS.
- Review box `bbabea5`: log has "r1 approved at 33a2305, committed as bbabea5": PASS.
- CI at head: check x3, scenario ubuntu, eval-dry-run all SUCCESS (gh statusCheckRollup): PASS.
- Known gaps names the work/gates/ anchoring flaw; no UNVERIFIED claims; no images: PASS.

VERIFIED
