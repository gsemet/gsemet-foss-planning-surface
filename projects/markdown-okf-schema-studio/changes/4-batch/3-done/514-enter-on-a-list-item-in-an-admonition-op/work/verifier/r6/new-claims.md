# CR-514 verification

Head: f9dc2c630b852635e8bffcd0b00b42cc886b293c

Base of every "before": `5f0746d79ca28e564841daa19288075aa7823776` (`origin/main`). Sixth
verification, a short pass on the posted description of pull request 540 alone. The previous
verdict at this head is kept as `verify-f9dc2c6-third.md` (NOT VERIFIED on its claim E6 only: the
screenshot proof named no SHA). The code did not change since; the description did. Verdict at the
end: VERIFIED.

Placeholders: `<work>` the folder of this file; `<wt>` the CR worktree; `<r2>` to `<r6>` = the
folders `verifier/r2` to `verifier/r6`; `<node>` =
`fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run from `<wt>`; `<chantier>` the
CLI of the brief with `--batch batch-09`; the other placeholders of the carried claims are `<base>` =
a detached base worktree used by the first verdict (since removed) and `<repro>` =
`verifier/repro`.

## Judged in this pass

### F1. The posted body is `pr-body.md`; since the last pass only the named parts changed: VERIFIED (f9dc2c6)

- Command: `gh pr view 540 --json number,headRefOid,baseRefName,baseRefOid,isDraft,state,title,body,updatedAt`
  (saved as `r6/pr-540-f9dc2c6-sixth.json`), `python -I <r6>/desc.py <work>` (against
  `r5/pr-540-f9dc2c6-closing.json`; log `r6/desc-diff-f9dc2c6.log`)
- Output: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c`, base `5f0746d...`, draft, OPEN, same
  title, updated `2026-11-26T19:55:27Z` (the same at the end of this pass); old 16727 characters,
  new 16957; `posted equals pr-body.md (trailing newline ignored): True`. Hunks: the screenshot
  sentence in Impacts; the clip paragraph; the GIF link; the Local gates item ("unit and contract
  tests" to "tests" after "5503 unit"); one blank line at the end. Nothing else.

### F2. The screenshot proof names its SHAs, and they hold (failed before as E6): VERIFIED (f9dc2c6)

Posted: "Screenshots from the visual test harness: before at `5f0746d` (carried from `cd3b8e6`: the
same tree), after at `f9dc2c6`."

- Command: `git rev-parse 'cd3b8e6^{tree}' '5f0746d^{tree}'` (log `r6/shas-f9dc2c6.log`);
  `gh api repos/gsemet/markdown-okf-schema-studio/commits/cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f --jq '.sha + " " + .commit.tree.sha'`
- Output: `e6f6894de333c24969709306715c4f3c06d06418` twice; the forge answers
  `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f e6f6894de333c24969709306715c4f3c06d06418`.
- Command: `evidence/before-after.md`; `r3/visual-capture-f9dc2c6.log` (carried from f9dc2c6: same
  head); the downloads of F5
- Output: before captured on `cd3b8e6`, the tree of the base; after: the five scenarios captured at
  `f9dc2c6`, `"status": "passed", "scenario_count": 5, "screenshot_count": 5`, byte-identical to the
  `after-*.png`. The six posted uploads are byte-identical to the evidence pairs, each in the column
  the table names.

### F3. The clip paragraph names the commits the take predates, and the walk at the head: VERIFIED (f9dc2c6)

Posted: "... the extension built from this change before its last three commits (`b09dc7d` to
`f9dc2c6`); the filmed walk opens the same lines at `f9dc2c6`".

- Command: `git log --reverse --format='%h %ci %s' 5f0746d..f9dc2c6`, the same with
  `-- docs/demo-video/clips/keyboard-navigation` (log `r6/shas-f9dc2c6.log`);
  `git diff --stat 9023d10a f9dc2c6 -- docs/demo-video/clips/keyboard-navigation`, the commit dates
  of `9023d10a`, `a2ebb0e3`, `739f9e3e`, the dates of the take's logs (log `r6/take-f9dc2c6.log`)
- Output: four commits, the last three `b09dc7d0`, `8539f1cc`, `f9dc2c63`; only the first,
  `5a686ab0`, touches the clip. VSIX packaged `12:38`, take `12:41`, committed in `9023d10a` at
  `13:20`; the originals of the later commits are from `14:23`, `16:31` and (head) `19:59`; the clip
  folder of `9023d10a` and of the head differ by 0 lines.
- Command: `r3/clip-f9dc2c6.log` (carried from f9dc2c6: same head;
  `<node> <repro>/gesture.js` on `stage/release-plan.md`)
- Output: `enter on "the VSIX" opens <p> lines 8-8`, editor `"  - the VSIX\n"`; "Build the packages"
  7-7: the lines of the filmed walk.

### F4. The GIF is the file at the pull request's head; the MP4 and WebM links too: VERIFIED (f9dc2c6)

- Command: `python -I <r6>/images.py <work> <wt>` (log `r6/images-f9dc2c6.log`);
  `curl -sIL <the GIF link>`; `git cat-file -p f9dc2c6:<the GIF path>`
- Output: `.../raw/f9dc2c630b85.../keyboard-navigation.gif`: 302 to `media.githubusercontent.com`,
  then `200`, `Content-Type: image/gif`, 1696690 B, sha256 `e6775d0b4ccb...`, the LFS object id
  committed at the head and the worktree file; the repository is `PUBLIC`. MP4 200, 543383 B, and
  WebM 200, 368400 B, both at the head and the same as the worktree files.
- Rule: `feature-clip-process.guidelines.md`: "The pull request of a clip shows the GIF inline in
  its body, from the file committed at the PR's head, and links the MP4 and the WebM by their raw
  URLs at the same head": followed.

### F5. It renders, and its images resolve and match: VERIFIED (f9dc2c6)

- Command: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/540 -H "Accept: application/vnd.github.html+json" --jq .body_html`
  (saved as `r6/pr-540-body.html`, signed tokens removed), then F4's `images.py`
- Output: headings `Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions,
  Known gaps, Test plan, Internal references`; the Deliverables table 9 rows of 3 cells; the
  screenshot table 4 rows of 3 cells with 2 images in each of its 3 body rows; 7 images; 6 checked
  boxes. The 7 image links answer 200 without credentials; six PNGs byte-identical to
  `evidence/{before,after}-{alert-body-click,admonition-body-click,admonition-keyboard-enter}.png`
  (the before images of two pairs equal the unchanged title images, as expected), the seventh the
  committed GIF.
- User name and home folder: carried from f9dc2c6: the bytes are those of the images opened in the
  earlier passes (the six PNGs, and sampled frames of the GIF): none shows either.

### F6. The Local gates item: VERIFIED (f9dc2c6)

- Command: first line and result lines of `work/gates/prepush-f9dc2c6-preflight.log` (extract
  `r6/gate-f9dc2c6.log`); `<chantier> handoff CR-514`
- Output: `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d79ca28e564841daa19288075aa7823776: just preflight`;
  unit `tests 5503 pass 5495 fail 0 skipped 8`; the contract target `tests 0`, so all 5503 are unit
  tests; security `tests 116 pass 116`; clip kit `tests 56 pass 56`;
  `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`;
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
  `exit 0`. The handoff's "before push at f9dc2c6" note says the same.

### F7. Each proof names its SHA; no stale mark, role as a doer or local path: VERIFIED (f9dc2c6)

- Command: `desc.py` (log `r6/desc-diff-f9dc2c6.log`, which holds the whole body, numbered)
- Output: Impacts: the screenshots name `5f0746d`, `cd3b8e6` and `f9dc2c6` (line 74-75), the clip
  names `b09dc7d` to `f9dc2c6` and links at the head (lines 87-92); each of the six Test plan items
  names `f9dc2c6` (lines 206-237). `STALE: False UNVERIFIED: False unchecked boxes: 0 checked: 6`;
  role words: none; local paths: `lines matched: 0`. The only internal reference is under Internal
  references. No Known gaps bullet changed; the section is not "None".

### F8. Head, pull request and CI: VERIFIED (f9dc2c6)

- Command: `git rev-parse HEAD`, `git status --short | wc -l`,
  `git ls-remote origin refs/heads/main <branch>`, `gh pr checks 540`
- Output: `f9dc2c630b852635e8bffcd0b00b42cc886b293c`, `0`; remote main `5f0746d...`, branch
  `f9dc2c6...`; `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`,
  `visual-2` pass; `acceptance`, `gallery`, `integration`, `pages`, `release`, `release-check`,
  `stress`, `tag-release`, `toc-loop` skipping.

## Observations, not counted

- Hosting of the screenshots. `.agents/guidelines/pull-request.guidelines.md` ("Screenshots in the
  PR") asks for raw links to a `-assets` side branch; the body uses uploaded attachments (what the
  card's `pr-template.md` asks). The project's guidelines rank above the card, so this is a conflict
  to report. It is none of the description's failure cases, and the uploads are byte-identical to
  the evidence.

