# Verify CR-342

Head: 8ae64cb96fc9d71c1a341c2aa864ef9952ee3ddb

All claims judged at 8ae64cb96fc9d71c1a341c2aa864ef9952ee3ddb (`git rev-parse HEAD` in the worktree).

1. `just mod` passes (8ae64cb). Command `just mod` in the worktree: `claude plugin validate .` accepts the hook and lists
   `$.session.id (via readSessionId)` among the calls, no error; plugin tests end `78 pass, 0 fail, Ran 78 tests across 1 file`.
2. `just check` passes (8ae64cb). Command `just check`: `506 passed in 22.82s`, `release-notes: ... ok`.
3. Matching fields (8ae64cb). `hooks/register.tsx` `SEAT_IDS`, `BATCH_IDS`, `BATCH_LISTS` cover seat `session`/`transcript` and batch
   `foreman`, `foreman_transcript`, `chief_transcript`, `foreman_transcripts`, `chief_transcripts`; `idsIn` ignores non-strings and non-string lists;
   exact `includes`. `just mod` output: seven `(pass) the session id in seat session / seat transcript / batch foreman / foreman_transcript /
   foreman_transcripts / chief_transcript / chief_transcripts keeps only that project, with no line`; `(pass) two projects that name the session are both drawn, with no line`.
4. Surface-only choice (8ae64cb). `choose` returns `bases` unchanged when every base has `name === null` (in-project); `findRoot` reads no id then.
   `(pass) a session in the project itself reads no seat and draws no line`; `(pass) a planning surface shows one section per project` (no match: both and the line);
   `(pass) a session id that cannot be read shows every project, with the error`.
5. 15 s check and mtime (8ae64cb). `rechoose` runs from `check` when not forced, `idsOf` re-reads only on a changed mtime, no `git rev-parse` there.
   `(pass) a seat written after opening is followed by the next check, which reads no file that did not change`;
   `(pass) a periodic check keeps the seated project alone from the id held in the site atom`.
6. No-seat line placement (8ae64cb). `unseated` is drawn under `Bar()` in the board view and in `Alone(..., true)` for fatal/missing, not on a CR page. Source read in the diff (`git diff HEAD~1 -- hooks/register.tsx`);
   tests above include the single-project `Alone` case (`just mod` all 78 pass).
7. Site atom and types (8ae64cb). `grep -n "site-" hooks/register.tsx`: `shape: 'site-4'`, value `{root, bases, error, unseated, sid}`; `types/index.d.ts` matches. Deviation from the spec: the spec says `site-3` and no `sid`; the code adds `sid` and
   tags `site-4`, disclosed in the PR's Autonomous decisions (kept across a plugin reload). Judged acceptable: it satisfies "a shape change changes the tag" and the behaviour; flagged for the Driver.
8. Header comment and `docs/boards.md` (8ae64cb): both updated per the diff (`git diff HEAD~1 -- docs hooks`), "What it is" and "How to read it".
9. Review box: `chantier log CR-342` has `driver note note=r3 approved at ade7512b (worktree), committed as 8ae64cb9 after rebase`; the PR says `approved at 8ae64cb`: matches.
10. PR description (8ae64cb): `gh pr view 304 --json body` equals work/pr-body.md (a trailing blank line only); Summary, Deliverables and Changes match the diff; no image attached; Known gaps names "No screenshot of the pane from a real session"; no internal role names. The `Verified at <sha7>` and `CI green at <sha7>` boxes are for the Driver to fill. `headRefOid` = 8ae64cb96fc9d71c1a341c2aa864ef9952ee3ddb.
11. CI green at the head: reported by the Driver's note (five jobs); not re-run here.

Not provable here, per the brief: real-session screenshot (known gap, not failed).

VERIFIED

## Description pass at 8ae64cb96fc9d71c1a341c2aa864ef9952ee3ddb

Command: gh pr view 304 --json body, checked against git show HEAD (4 files: docs/boards.md, hooks/register.tsx, hooks/register.test.tsx, types/index.d.ts) and pr-template audit. Sections and fold in order, no internal reference outside the last section, Changes/Deliverables match the diff, SHA 8ae64cb right, Review box matches log note "committed as 8ae64cb9", gh pr checks 304 all pass, Known gap present. Minor: the types entry also gains `bases` (not named). Result: VERIFIED.

VERIFIED
