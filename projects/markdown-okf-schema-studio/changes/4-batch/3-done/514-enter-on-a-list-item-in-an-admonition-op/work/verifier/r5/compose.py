import pathlib, re, sys

work = pathlib.Path(sys.argv[1])
previous = (work / "verify-f9dc2c6-second.md").read_text(encoding="utf-8")


def between(start, end):
    a = previous.index(start)
    return previous[a:previous.index(end)].rstrip("\n")


old_judged = between("### D1.", "### D4.")
carried = between("### Previous claim A", "### PR description form")
files = between("## Files that may be attached", "## Limits")

marker = "_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._"
new_marker = "_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim E0)._"
assert marker in carried
carried = carried.replace(marker, new_marker)
other = "_carried from f9dc2c6: same head; every bullet but the three of D1 to D3 is unchanged (claim D0). The observation at its end is replaced by D3._"
assert other in carried
carried = carried.replace(other, "_carried from f9dc2c6: same head; no Known gaps bullet changed since that pass (claim E0). The observation at its end is replaced by D3._")
links = "- `curl -sL` of the three description links (at f9dc2c6): 200, same sizes, byte-identical to the\n  worktree files."
assert links in carried
carried = carried.replace(links, links + "\n  (The description's links as judged then; the posted ones are judged in E3.)")
pieces = re.split(r"(?m)^(### D\d\..*)$", old_judged)
old_judged = ""
for title, text in zip(pieces[1::2], pieces[2::2]):
    old_judged += title + "\n\n_carried from f9dc2c6: same head, and the bullet it judges is unchanged (claim E0)._\n" + text.rstrip("\n") + "\n\n"
files = files.replace("Clip of the branch (already linked by the description at f9dc2c6):",
                      "Clip of the branch (the description now carries the GIF as an upload and links the other two, E3):")

head = """# CR-514 verification

Head: f9dc2c630b852635e8bffcd0b00b42cc886b293c

Base of every "before": `5f0746d79ca28e564841daa19288075aa7823776` (`origin/main`). Fifth
verification, the closing pass on the posted description of pull request 540 alone. The previous
verdict at this head is kept as `verify-f9dc2c6-second.md` (VERIFIED). The code did not change since;
the description did. Verdict at the end: NOT VERIFIED, on claim E6 only (the screenshot proof names no
SHA). Every other claim holds.

Placeholders: `<work>` the folder of this file; `<wt>` the CR worktree; `<r3>`, `<r4>`, `<r5>` = the
folders `verifier/r3`, `verifier/r4`, `verifier/r5`; `<node>` =
`fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run from `<wt>`; `<chantier>` the
CLI of the brief with `--batch batch-09`; the other placeholders of the carried claims are `<base>` =
a detached base worktree used by the first verdict (since removed), `<repro>` and `<r2>` =
`verifier/repro` and `verifier/r2`.

## Judged in this pass

### E6. Each proof of the description names its SHA: NOT VERIFIED (f9dc2c6)

- Command: `python -I <r5>/shas.py <work>` (log `r5/shas-f9dc2c6.log`)
- Output: no line of the Impacts section (body lines 67-91) names a SHA in its text or in an image's
  alt text. The screenshot table (lines 77-81) and its sentence "Screenshots from the visual test
  harness, before and after the change." name neither the base nor the head; the six images are
  uploads, so their links name none either. `5f0746d` is nowhere in the body. The six Test plan items
  do name `f9dc2c6`.
- Rule: `help verifier-description`: the description fails when "a proof does not name its SHA: the
  head, or `carried from <sha7>` with its reason". `references/pr-template.md`: "Each proof names its
  SHA (seven characters): the Test plan items and the screenshot captions (before at the base's SHA,
  after at the head's)". The project's template and `pull-request.guidelines.md` say nothing about
  SHAs (`grep -i` for `sha`: no such rule for a PR body), so the card fills there.
- What the evidence supports (`evidence/before-after.md`; `git rev-parse cd3b8e6a^{tree} 5f0746d^{tree}`
  gives `e6f6894de333c24969709306715c4f3c06d06418` twice): before at the base `5f0746d` (captured on
  `cd3b8e6`, the same tree), after at `f9dc2c6` (captured there, byte-identical). One sentence above
  the table is enough, for example: "Screenshots from the visual test harness: before at `5f0746d`
  (carried from `cd3b8e6`: the same tree), after at `f9dc2c6`."

### E0. The posted body is `pr-body.md`; since the last pass only the named parts changed: VERIFIED (f9dc2c6)

- Command: `gh pr view 540 --json number,headRefOid,baseRefName,isDraft,state,title,body,updatedAt`
  (saved as `r5/pr-540-f9dc2c6-closing.json`), `python -I <r5>/desc.py <work>` (against
  `verifier/pr-540-f9dc2c6-second.json`; log `r5/desc-diff-f9dc2c6.log`); `git rev-parse HEAD`
- Output: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c` on both, draft, OPEN, base `main`, same
  title, updated `2026-11-26T19:46:10Z` (the same at the end of this pass); old 14542 characters, new
  16727; `posted equals pr-body.md (trailing newline ignored): True`. Hunks: the Deliverables sentence
  on the screenshots and clip; the screenshot sentence and table in Impacts; the GIF link and its alt
  text; and the Test plan, checked with its figures (the diff log lists every hunk).

### E1. It renders, and its images resolve and match: VERIFIED (f9dc2c6)

- Command: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/540 -H "Accept: application/vnd.github.html+json" --jq .body_html`
  (saved as `r5/pr-540-body.html`, signed image tokens removed), then
  `python -I <r5>/images.py <work> <wt>` (log `r5/images-f9dc2c6.log`)
- Output: headings `Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions,
  Known gaps, Test plan, Internal references`; the Deliverables table 9 rows of 3 cells; the
  screenshot table 4 rows of 3 cells with one image in each Before and After cell; 7 images; 6 checked
  boxes. The 7 attachment links download without credentials (200); six are byte-identical to
  `evidence/{before,after}-{alert-body-click,admonition-body-click,admonition-keyboard-enter}.png` in
  the order and column the table names, the seventh to the committed GIF.
- Opened: the six PNGs of `evidence/`. Each shows what its alt text says (before: `Lines 5-8`,
  `Lines 5-9`, `Lines 3-8` open; after: `Line 8`, `Line 8`, `Line 6`). No user name or home folder.
  The GIF's bytes are the file whose sampled frames were opened before (`<r3>/gif/`), looked at again
  in this pass: no user name or home folder.

### E2. The new sentences in Deliverables and Impacts: content VERIFIED (f9dc2c6)

- "Screenshots before and after the change, and the re-filmed clip, are under Impacts": E1.
- "A click on the title of an admonition or alert opens all of it, before and after":
  `images-f9dc2c6.log`: `alert-title-click before == after: True`,
  `admonition-title-click before == after: True`; the two scenarios' images show the whole box open
  (carried section "Files that may be attached").
- The table's three gestures are the three evidence pairs of `evidence/before-after.md`.

### E3. The clip links: VERIFIED (f9dc2c6)

- Command: as E1.
- Output: GIF upload 200, 1696690 B, byte-identical to
  `docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif` at the head and to
  `work/attach/keyboard-navigation.gif`; the MP4 (543383 B) and WebM (368400 B) raw links at
  `f9dc2c6...` answer 200, byte-identical to the worktree files. The clip paragraph's text is unchanged.

### E4. The six Test plan items: VERIFIED (f9dc2c6)

- Tests. Command: `git diff --name-status 5f0746d f9dc2c6 -- test` (log `r5/testplan-f9dc2c6.log`);
  result lines of `<r3>/tests-head-f9dc2c6.log` and `<r3>/tests-base-f9dc2c6tests.log` (carried from
  f9dc2c6: same head). Output: the changed or added unit and page test files are the nine run;
  `tests 284 pass 284 fail 0`; with the previous source `pass 177 fail 107`.
- Requirements. Output of the same log: 13 SwRS files changed. Gate log lines 5987-5990:
  `0 indexes would change`, `0 requirement OKF projections would change`, `0 files would change`.
- Changelog. Same log: one bullet added under Unreleased, ending `(CR-514 enter-admonition, PR #540)`.
- Local gates. `work/gates/prepush-f9dc2c6-preflight.log`: line 1
  `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d79ca28e564841daa19288075aa7823776: just preflight`;
  unit `tests 5503 pass 5495 fail 0 skipped 8`; contract target `tests 0`; security 116/116;
  clip kit 56/56; `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`; `exit 0`;
  `tree checked`.
- Review. `<chantier> handoff CR-514`: `r6 inspector approved at 8539f1cc...` and
  `r6 approved at 8539f1cc..., committed as f9dc2c630b852635e8bffcd0b00b42cc886b293c`.
- CI. `gh pr checks 540`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`,
  `visual-2` pass; `acceptance`, `gallery`, `integration`, `pages`, `release`, `release-check`,
  `stress`, `tag-release`, `toc-loop` skipping.

### E5. No stale mark, no role as a doer, no gap left out: VERIFIED (f9dc2c6)

- Command: `desc.py` (same log)
- Output: `STALE: False UNVERIFIED: False unchecked boxes: 0 checked: 6`; no line matches a role
  word; the "local path" matches are `https://` links only. The only internal reference is under
  Internal references. No Known gaps bullet changed; the section is not "None";
  `evidence/before-after.md` has no pair left uncaptured.

## Observations, not counted

- Hosting of the images. `docs/demo-video/guidelines/feature-clip-process.guidelines.md` asks for
  "the GIF inline in its body, from the file committed at the PR's head", and
  `.agents/guidelines/pull-request.guidelines.md` ("Screenshots in the PR") for raw links to a
  `-assets` side branch. The body now uses uploaded attachments (what `pr-template.md` asks); the
  project's guidelines rank above the card, so this is a conflict to report. The uploads are
  byte-identical to the files, and the previous GIF link (raw, at the head) served the file.
- The clip paragraph names the head only through its MP4 and WebM links. The take predates the later
  fixes (its walk opens the same lines at the head, carried below); saying so with the head in the same
  edit as E6 would leave no proof without a SHA.
- "5503 unit and contract tests": the contract target ran 0 tests, so all 5503 are unit tests.

## Carried claims: the three bullets of the previous pass

"""

middle = """## Carried claims: code, tests, evidence

"""

limits = """## Limits

- No real VS Code window, no new take, no macOS or Linux run of mine; integration, acceptance and
  stress did not run in CI for this pull request.
- Browser behaviour is covered by the visual harness and DOM-level page tests; the chord, formula
  and Known gaps claims were judged through the real renderer, page helpers and `PreviewManager`.
- The clip was viewed as sampled frames, not frame by frame.
- This pass judged the description: no test, build, capture or probe of the code was run again.

NOT VERIFIED
"""

text = head + old_judged + middle + carried + "\n\n" + files + "\n\n" + limits
with open(work / "verify.md", "w", encoding="utf-8", newline="\n") as out:
    out.write(text)
print("written", len(text), "characters,", text.count("\n"), "lines")
