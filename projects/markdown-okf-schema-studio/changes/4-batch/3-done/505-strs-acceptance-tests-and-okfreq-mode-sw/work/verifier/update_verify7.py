"""Record the second description pass at 9d7e788 in verify.md and before-after.md."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFY = HERE.parent / "verify.md"
PAIRS = HERE / "evidence" / "before-after.md"


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one match of: {old!r}")
    return text.replace(old, new)


NEW = """## Verdict: VERIFIED

Description-only pass at the same head, after F1 of the previous pass (kept below). The two Test plan
lines that failed are fixed and nothing else of the description changed. Every other claim is carried
from `9d7e788a` (same head, same sentence). `<head>`, `<base>`, `<W>`, `<S>`, `<repo>` as above.

### Q1. State - VERIFIED

SHA `<head>`. `git -C <W> rev-parse HEAD`: `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`; `git -C <W>
status --porcelain --branch`: the branch line only; `git -C <W> merge-base <head> <base>`:
`89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`. `gh pr view 532 --repo <repo> --json
state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`, draft `true`, base `main`, head
`<head>`, `updatedAt 2026-11-26T10:31:27Z`, title `ci: accept trust and security use case paths in a
real VS Code`.

### Q2. Only lines 206 and 207 of the description changed - VERIFIED

SHA `<head>`. `gh pr view 532 --repo <repo> --json body --jq .body > <S>/posted-body-7.md`, then `git
diff --no-index -U0 <S>/posted-body-6.md <S>/posted-body-7.md`: one hunk, `@@ -206,2 +206,2 @@`, the
two Test plan lines of runs 45766254331 and 45774743144. In them "at an earlier commit" became "at
`9d7e788a` (carried from `0feab1d`: the run the limits were set from)", and ", on an earlier head of
this change" became ", at `9d7e788a` (carried from `5a8a593`)"; figures and links as before. `git diff
--no-index -U0 <work>/pr-body.md <S>/posted-body-7.md`: one added empty last line, nothing else.

### Q3. "The limits were set from the first measured run (45766254331), at `9d7e788a` (carried from `0feab1d`...): job 115 s, test step 77 s" - VERIFIED

At `<head>`, carried from `0feab1d`: a recorded measurement of a past run, which no later move changes.
- `gh run view 45766254331 --repo <repo> --json databaseId,headSha,event,conclusion,attempt`:
  `headSha 0feab1d914f39682507bf5c0d58adddd4174c395`, `workflow_dispatch`, `success`, attempt 2.
- `gh api repos/<repo>/actions/runs/45766254331/attempts/1/jobs`, job `acceptance (trust-security)`:
  `success`, `head_sha 0feab1d...`, job `06:09:35` to `06:11:30` = 115 s, step `just ci-acceptance`
  `06:10:07` to `06:11:24` = 77 s.
- Limits at `<head>`: `ci.yml` job `acceptance` (line 314), line 322 `timeout-minutes: 5`, line 351
  `timeout-minutes: 3`. `$CHANTIER log CR-505`, `06:23:38Z ... round=5`: "set the acceptance job and
  step timeouts from the measured first shard (job 115 s, test step 77 s)".

### Q4. "Re-run of the shard alone (run 45774743144), at `9d7e788a` (carried from `5a8a593`): job 91 s, test step 55 s; ... attempt-3 ... kept attempt 3" - VERIFIED

At `<head>`, carried from `5a8a593`: `git -C <W> diff --stat 5a8a593 <head> -- .github scripts
justfile` prints nothing, so the workflow and the attempt selection the run exercised are those of the
head (the whole move: 12 files, `CONTRIBUTING.md` and files under `test/`).
- `gh run view 45774743144 ...`: `headSha 5a8a59398692a0d497ad88c18e5f142de1411638`,
  `workflow_dispatch`, `success`, attempt 3.
- `gh api repos/<repo>/actions/runs/45774743144/attempts/3/jobs`, job `acceptance (trust-security)`:
  `success`, job `08:04:50` to `08:06:21` = 91 s, step `08:05:21` to `08:06:16` = 55 s.
- `<work>/ci-45774743144-report-attempt3.log` line 418: `acceptance trust-security: kept attempt 3
  (e2e-acceptance-trust-security-attempt-3)`.

### Q5. Each proof of the description names its SHA - VERIFIED

SHA `<head>`. A search of `posted-body-7.md` for backticked hexadecimal ids: lines 180, 199 to 204,
206 to 209 and 211 name `9d7e788a`; the two ids outside the head's history, `0feab1d` (line 206) and
`5a8a593` (line 207), each follow `carried from`. Line 205 is a sub-item of "Evidence at `9d7e788a`"
and details the run of line 204 (N18). "Verified" (line 210) is unchecked and states no proof yet.

### Q6. The posted description is clean - VERIFIED

SHA `<head>`. `gh api repos/<repo>/pulls/532 -H "Accept: application/vnd.github.html+json"`, `body_html`
filtered on the two run numbers: two list items, each with its link, its code spans and balanced
parentheses. A case-insensitive search of `posted-body-7.md` for images, `STALE`, `UNVERIFIED`,
`pending`, home folder forms, the user name, "earlier head", "earlier commit", batch, round, grill,
change ids and planning paths finds only line 180 ("earlier head", a Known gaps sentence, R10) and line
215 (the change id, under "Internal references"). Sections and fold: unchanged (Q2, N24). F1 was fixed,
so Known gaps needs no bullet for it.

### Q7. Review and CI at the head - VERIFIED

SHA `<head>`. `$CHANTIER log CR-505`: `10:06:46Z driver note note=move 5a8a593..9d7e788 (restack)
inspector approved at 9d7e788a479dec70fd882d295bf0d5e78f4f6b98`. `gh pr checks 532`: `checks`,
`report`, `static`, `static-windows`, `viewer-graph`, `visual` pass, the others skipping; `gh run list
--commit <head>`: 45794286167 `workflow_dispatch success` and 45794229373 `pull_request success`, both
attempt 1, no other run.

### Carried claims

N1 to N18, N21 to N23 and the delivery table below: carried from `9d7e788a`: same head, and the
description sentences they judge are unchanged (Q2). N19 and N20 (figures) hold, their SHA form now
judged in Q3 and Q4.

### Remark and notes of this pass

- R15. When "Verified" is ticked, the item should name its commit, as the template does (`Verified at
  `9d7e788a``).
- R10 to R14, R1 and R8 below still stand.
- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit; no
  command refused. Files written, all under `work/`: `verify.md`, `verifier/posted-body-7.md`,
  `verifier/update_verify7.py`, `verifier/evidence/before-after.md` (pair 9, the "after" version).

## Previous pass at 9d7e788a (history): NOT VERIFIED on F1, resolved by Q3 and Q4
"""

text = VERIFY.read_text(encoding="utf-8")
text = replace_once(text, "## Verdict: NOT VERIFIED\n", NEW)
text = replace_once(
    text,
    "## F1. Description, Test plan: two proofs name no SHA - NOT VERIFIED",
    "## F1. Description, Test plan: two proofs name no SHA - was NOT VERIFIED (fixed: Q3, Q4)",
)
text = text.replace("(their SHA form fails, F1)", "(SHA form failed as F1; fixed: Q3, Q4)")
VERIFY.write_text(text, encoding="utf-8", newline="\n")

pairs = PAIRS.read_text(encoding="utf-8")
pairs = replace_once(
    pairs,
    "- After: the description posted at `9d7e788` (updated `2026-11-26T10:06:51Z`, `posted-body-6.md`);\n"
    "  judged in `work/verify.md`.\n",
    "- After: the description posted at `9d7e788` (updated `2026-11-26T10:31:27Z`, `posted-body-7.md`;\n"
    "  it differs from the `10:06:51Z` version, `posted-body-6.md`, in two Test plan lines); judged in\n"
    "  `work/verify.md`.\n",
)
PAIRS.write_text(pairs, encoding="utf-8", newline="\n")
print("updated")
