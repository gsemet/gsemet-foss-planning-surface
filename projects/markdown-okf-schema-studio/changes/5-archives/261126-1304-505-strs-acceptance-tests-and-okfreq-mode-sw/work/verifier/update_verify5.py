"""Add the fifth (description-only) pass to work/verify.md, keeping the rest."""

from pathlib import Path

NOTE = Path(__file__).resolve().parent.parent / "verify.md"

FIFTH = """## Fifth pass (description only, same head): VERIFIED

Judges the one edit of the posted description since the fourth pass and the description as posted; every
other claim is carried from `5a8a593` (same head, same sentence). `<H>` is
`5a8a59398692a0d497ad88c18e5f142de1411638`, `<B>` is `3478f0992688c7a354d11106145793fc83590506`.

### D1. State - VERIFIED

SHA `<H>`. `git -C <worktree> rev-parse HEAD`: `5a8a59398692a0d497ad88c18e5f142de1411638`;
`git -C <worktree> status --porcelain --branch`: the branch line only. `gh pr view 532 --repo
gsemet/markdown-okf-schema-studio --json state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`,
draft `true`, base `main`, head `5a8a593`, `updatedAt 2026-11-26T09:19:30Z`, title `ci: accept trust and
security use case paths in a real VS Code`.

### D2. The only change of the description is the checked "Verified" item - VERIFIED

SHA `<H>`. `gh pr view 532 --repo <repo> --json body --jq .body > verifier/posted-body-5.md`, then
`git diff --no-index -U0 verifier/posted-body-4.md verifier/posted-body-5.md`: one hunk,
`@@ -210 +210 @@`,
`-- [ ] Verified at `5a8a593`: pending`
`+- [x] Verified at `5a8a593`: the delivered change and the claims of this description were checked
against that commit`.
`git diff --no-index -U0 pr-body.md verifier/posted-body-5.md`: one added empty last line, nothing else.

### D3. "Verified at `5a8a593`: the delivered change and the claims of this description were checked against that commit" - VERIFIED

SHA `<H>`. `$CHANTIER log 505`: `2026-11-26T09:19:08Z driver verdict result=VERIFIED
head=5a8a59398692a0d497ad88c18e5f142de1411638 base=3478f0992688c7a354d11106145793fc83590506`, the last
verdict before the body was posted (`09:19:32Z driver note closing: body posted at 5a8a593`). The delivered change
and the description's claims are the ones this note judges at `<H>` (P1 to P3, T1 to T4, S1 to S8, V1 to
V15); the older run it cites is named there as an earlier commit's.

### D4. The other items that cite a proof of the head - VERIFIED

SHA `<H>`.
- Review box "approved at `5a8a593` (carried from `18c63e5`)": same log, `06:52:32Z driver note r5
  approved at 0feab1d, committed as 18c63e5e85283af68e1e79dd78aad3f3d6782e13`; the carry is V14.
- CI box: `gh pr checks 532`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`
  `pass`, the other jobs `skipping`; `gh run list --commit <H>`: `45774743144 workflow_dispatch success
  attempt 3`, `45773633868 pull_request success attempt 1`, no other run.
- Changes, "CI and release guidelines, `AGENTS.md` and `CONTRIBUTING.md`" and "No file under `src/`":
  `git -C <worktree> diff --stat=200 <B> <H>`: `ci.guidelines.md`, `release-process.guidelines.md`,
  `AGENTS.md`, `CONTRIBUTING.md`, `docs/how-we-ship.md`, `project.guidelines.md` listed, no `src/` path;
  `120 files changed`.

### D5. The posted description is clean - VERIFIED

SHA `<H>`. Read of `verifier/posted-body-5.md`: headings Summary, Deliverables, Changes, Impacts (the
order of `.github/PULL_REQUEST_TEMPLATE.md`), Blast radius, Autonomous decisions, Known gaps, then one
`<details>` fold (lines 187 to 217, blank line inside each end) with Human decisions, Test plan, Internal
references. A search for `!\\[|<img|STALE|UNVERIFIED|pending|<drive>:\\Users|/home/|<user name>|
.agents/changes|4-batch|CR-[0-9]+|<details>|</details>|<summary>|^## ` finds only the headings, the fold
lines and `CR-505` on line 215, under Internal references: no image, no stale or unproven mark, no
pending item, no user name or home folder. A case-insensitive search for the agent role names, `batch`,
`round` and `grill`: no match. Known gaps: no `UNVERIFIED` mark needs a bullet; the section is the one
earlier passes judged (D2).

### Remarks of the fifth pass (not failures)

- R8. `pull-request.guidelines.md` lists "scenario ids" among the internal references. The ids in this
  body are those of the repository's own requirements bundle, whose markers are the subject of the
  change (not plan or backlog ids), and merged pull request 524 names them the same way (`gh pr view
  524`): read as product terms, as the earlier passes did.
- R9. `verifier/evidence/before-after.md`, pair 9, still gives the `08:54:30Z` version as the posted
  "after"; the description judged now is the `09:19:30Z` one (D1, D2). No pair was captured again.
- Files written by this pass, all under `work/`: `verify.md`, `verifier/posted-body-5.md`,
  `verifier/update_verify5.py`. No CI run started or re-run, no tracked file changed, no commit, push or
  pull request edit.

"""

text = NOTE.read_text(encoding="utf-8")

anchor = "## Verdict: VERIFIED\n"
assert text.count(anchor) == 1, "verdict heading not found once"
text = text.replace(anchor, anchor + "\n" + FIFTH + "## Fourth pass\n", 1)

start = text.index("## The pending item of the Test plan\n")
end = text.index("The table F1 to F7", start)
text = (
    text[:start]
    + "## The \"Verified\" item of the Test plan\n\n"
    + "Left unchecked up to the fourth pass; checked in the posted description now, judged in D3.\n\n"
    + text[end:]
)

assert "Head: 5a8a59398692a0d497ad88c18e5f142de1411638\n" in text
NOTE.write_text(text, encoding="utf-8", newline="\n")
print("verify.md updated")
