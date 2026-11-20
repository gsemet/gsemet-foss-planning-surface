Head: 867cabc5acbb90f9c76fb6ffcc8f0c00a7d8f337

All claims judged at 867cabc5 (git diff origin/main...HEAD read in full; two files changed).

1. Template "A highlight": order heading, at most two sentences, picture; whole-change case "heading and picture, with no text". `grep -n "then a picture\|under it" skills/chantier/references/release-template.md` prints nothing (rc=1). PASS.
2. Template "Visible evidence": four crop points present (part where change happens, every source; same region and scale in joined image; Driver crops with project's means, names no tool, checks crop; uncroppable stays whole, noted, no other image). PASS.
3. `grep -n -i "why it matters\|usage or call example\|two-column" docs/release-process.md` prints nothing (rc=1). Item 3 links template#a-highlight and #writing-rules; introduction states the split; "Visuals" has the crop sentence linking #visible-evidence; diff touches only intro, item 3, Visuals. PASS. (Intro lists "release folder, structure, links, anonymisation, batch" rather than the spec's list; declared in the PR's Autonomous decisions, accurate to the sections kept.)
4. Agreement: no sentence of release-process.md asks a highlight for anything; it defers to the template. PASS.
5. `gh pr checks 387`: just check on macos, ubuntu, windows pass; eval-dry-run pass; scenario (ubuntu-latest) pass, at head 867cabc. PASS.
6. PR description: renders (sections, details fold), Summary/Deliverables/Changes match the diff, no images, Known gaps names the first-release gap, Review box matches `chantier log` note "approved at 4ed0d56, committed as 867cabc5". PASS.
7. Evidence: text-only, no visual change; no before/after captured.

VERIFIED

## Description pass at 867cabc5acbb90f9c76fb6ffcc8f0c00a7d8f337

Command: `gh pr view 387 --repo gsemet/chantier --json body` read against `git diff origin/main...HEAD` (two files) and the audit of pr-template.md.
- Sections in order, Known gaps visible after Autonomous decisions, one `<details>` fold with blank lines after `</summary>` and before `</details>`, nothing after it, Internal references last: PASS.
- No CR, batch or role name outside Internal references; no issue line in the spec, so no Issues References: PASS.
- Summary, Deliverables, Changes, Impacts match the diff (template reorder and four crop points; release-process intro, item 3, Visuals sentence): PASS.
- Proofs name 867cabc; Review box matches the log note "approved at 4ed0d56, committed as 867cabc5": PASS.
- Known gaps names the one unproven point; no images attached: PASS.
- Minor, not failing: the answers file records points settled by the Chief of Staff without the user; the body's Autonomous decisions lists one and Deliverables "Choices" covers the rest.

VERIFIED
