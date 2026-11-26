"""Rewrites the head of work/verify.md for the third pass; the carried sections stay."""
import pathlib
import sys

note = pathlib.Path(__file__).resolve().parents[1] / "verify.md"
text = note.read_text(encoding="utf-8")


def between(source, start, end, new):
    first = source.index(start)
    last = source.index(end)
    return source[:first] + new + source[last:]


def swap(source, old, new):
    if source.count(old) != 1:
        sys.exit("not exactly one match: " + old)
    return source.replace(old, new)


head = """- Third pass at the same head (no code change). It judges only what changed in the posted description
  since the second pass, and the sections "Human decisions" and "Autonomous decisions" as wholes. Every
  other claim is carried from `5a8a593`: same head, same sentence.
- `git rev-parse HEAD`: `5a8a59398692a0d497ad88c18e5f142de1411638`; `git status --porcelain --branch`:
  the branch line only. `gh pr view 532 --repo <repo> --json state,isDraft,headRefOid,baseRefName,updatedAt,body`:
  `OPEN`, draft `true`, base `main`, head `5a8a593`, `updatedAt 2026-11-26T09:12:36Z`. `gh pr checks 532`
  and `gh run list --commit <H>`: unchanged (`45773633868 pull_request success`, `45774743144
  workflow_dispatch success attempt 3`, no newer run).
- Changes since the second pass: `gh pr view 532 --json body --jq .body > verifier/posted-body-3.md`, then
  `git diff --no-index -U0 verifier/posted-body.md verifier/posted-body-3.md`: two bullets added under
  "Autonomous decisions", the two G1 and G2 bullets removed from "Human decisions", nothing else
  (`2 insertions(+), 2 deletions(-)`). `work/pr-body.md` equals the posted body but for the last newline.
- Judged: the partial delivery (trust and security group; mode switch and gate left, `02-answers.md`
  items 5 to 7).

## Verdict: NOT VERIFIED

The two moved bullets hold and G1 and G2 are resolved. One bullet of "Human decisions" still credits an
agent's rule to the user (H3). It overturns one line of the second pass (S8) on the same evidence rule
as G1 and G2. Editing and posting the description fixes it; no code change.

Placeholders: `<worktree>` the change's worktree at the head, `<base>` the detached worktree of the
base, `<scripts>` `work/verifier/`, `<B>` the base SHA, `<H>` the head SHA, `<repo>` the GitHub
repository of pull request 532, `<504>` the folder `4-batch/3-done/504-strs-path-validation`.

## Failed claim

The rule applied: `references/pr-template.md` lines 102 to 111: "Human decisions" holds "the impactful
decisions the user took during the grill"; "Autonomous decisions" holds "each decision an agent took
without the user".

### H3. Human decisions: "The delivery may stop after any complete group; the coverage-mode switch lands last." - NOT VERIFIED (first half)

SHA `<H>`.
- The permission to stop is the Chief of Staff's: `02-answers.md` line 4, `acceptance-Q2 (Chief of
  Staff): Delivery in this CR is as large as the Driver can make it in 3 rounds; if the Driver reports
  that it cannot finish, the Chief of Staff splits it per e2e group ... The mode switch and the D11 gate
  land last.` `03-change-spec.md` lines 212 to 215 list the same under `acceptance-Q2`.
- No record gives it to the owner: a search of the surface's `changes/` for `complete (e2e )?group|after
  any group|stop after (a|any|each)` finds it only in copies of this description and in the earlier
  `verify.md` (one other hit is an unrelated archived task note).
- The owner's recorded words on delivery: `<504>/02-answers.md` Q10 and Q34, "one CR for everything";
  Q36, the split in two, is the Chief of Staff's. On 2026-11-26 (`02-answers.md` item 5, ask A-28,
  `events.jsonl` line 2953, which gives the split per group as what the spec says) the owner chose where
  the rest goes; item 7 and the inbox item's `02-answers.md` line 4 move it to a later batch. These
  support the follow-up changes and "the switch last", not a permission to stop.
- The second pass (S8) accepted the bullet on items 5 and 7 while noting that item 2, "same wording", is
  the Chief of Staff's: those items do not carry its first half.

Fix: remove that bullet from "Human decisions". Nothing has to be added: "the switch last" is in the
section's last bullet (the owner's), and stopping at one group is the first "Autonomous decisions"
bullet.

## Third pass: what holds

### T1. Autonomous decisions, "one shard per requirement group and one shared window per test file, with no raised timeout ..." - VERIFIED

SHA `<H>`. Agent's decision: `<504>/02-answers.md` line 73, Q37 (Chief of Staff), "several launches each
with its own budget below the 15 min launch deadline, the job sharded by group ... no raised timeouts".
In the code: `ci.yml` line 327 `group: [trust-security]` (the one group with files, `git ls-tree`);
`acceptanceRunner.ts` lines 219 to 225 launch each file once, each launcher under its own `watchLaunch`
(`acceptanceRunner.ts` line 87, `spawnedWindow.ts` line 61); `launchWatchdog.ts` line 78 defaults to
`launchDeadlineMs()`, and `hangWatchdog.ts` line 29 `LAUNCH_DEADLINE_MS = 15 * 60_000`, a file the diff
does not touch. `git diff -U0 -G"[Tt]imeout|...|BUDGET" <B> <H> -- test/shared test/integration .github
scripts`: the added limits belong to the new job and the new files (`timeout-minutes: 5` and `3`, polls
of 20 s and 60 s); no existing limit is changed.

### T2. Autonomous decisions, "The dropped and wrong scenario markers of the earlier change are repaired here for the trust and security group only ..." - VERIFIED

SHA `<H>`. `git diff -U0 -G"@(tests|accepts)_req" --output=<scripts>/markers-diff.log <B> <H> -- test src
scripts sphinx requirements/guidelines`, searched for changed marker lines outside `TRUST`: only
`SwRS-MDOKFSTUDIO-CORE-076` lines, which follow that requirement's edit for the new job (V5, S6). The
repairs themselves are the trust tables (V7). "Only" agrees with the first Known gaps bullet.

### T3. Autonomous decisions as a whole - VERIFIED

Seven bullets: the first five carried (V11, S5, S3), the last two T1 and T2; the two decisions the second
pass found missing there are now listed.

### T4. Human decisions, the four other bullets - VERIFIED

Carried from `5a8a593` (S8): "one nominal acceptance test" (Q3, Q6), "coverage counts test markers"
(Q35), the three paths (item 6 and the inbox item), delivered later with the switch last (item 7 and the
inbox item). With H3 removed, the section holds only decisions recorded as the owner's.

"""

text = between(text, "- Second pass at the same head", "## Changed sentences that hold", head)
text = swap(text, "## Changed sentences that hold\n", "## Sentences judged by the second pass (carried)\n")
text = swap(
    text,
    '- "May stop after any complete group; the switch lands last": items 5 ("The owner chose it": one\n'
    "  follow-up per group, switch last) and 7; item 2, same wording, is the Chief of Staff's.\n",
    '- "May stop after any complete group; the switch lands last": overturned by the third pass, see H3.\n',
)
text = swap(text, "### S8. Human decisions, the five other bullets - VERIFIED",
            "### S8. Human decisions, the five other bullets - VERIFIED but one line (H3)")
text = swap(
    text,
    "(Fourth: S5; fifth: S3. The decisions the section lacks: G1, G2.)",
    "(Fourth: S5; fifth: S3; sixth and seventh: T1, T2.)",
)
text = swap(
    text,
    "verdict, then a description pass). Not a failure. This pass ends NOT VERIFIED, so it stays unchecked.",
    "verdict, then a description pass). Not a failure. This pass ends NOT VERIFIED, so it stays unchecked.\n"
    "\nThe table F1 to F7 of the second pass is folded into this note: F1 to F5 hold (S1 to S6), F6 and F7\n"
    "(Human decisions, posted body) fail now only on H3.",
)
text = swap(
    text,
    "## Notes on this pass\n",
    "- R6. Owner answers Q28 (real VS Code is the acceptance bench) and Q30/Q30b (each scenario tested or\n"
    "  removed) are not bullets of \"Human decisions\"; Summary and Changes state both outcomes, and the\n"
    "  template leaves the choice of the shaping decisions to the writer: not a failure.\n"
    "- R7. The one re-run of the failed CI jobs, taken without the user, is stated in Known gaps and the\n"
    "  Test plan, not under \"Autonomous decisions\" (it is no investigation, round or conflict decision).\n"
    "\n## Notes on the third pass\n\n"
    "- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit.\n"
    "- Files written, all under `work/`: `verify.md`, `verifier/posted-body-3.md`,\n"
    "  `verifier/markers-diff.log`, `verifier/update_verify3.py`. One `git diff` call had its `--output`\n"
    "  after `--` and printed to the console instead; one had an invalid pattern; both were run again.\n"
    "\n## Notes on the second pass\n",
)
note.write_text(text, encoding="utf-8", newline="\n")
print("ok")
