# Verify CR-443

Head: 78ad518d4b705b7d07b90d7859d49c15a5f38c64

Gate pass: work/gates/20261121-020925.log, first line `gate CR-443 ... head 78ad518d4b705b7d07b90d7859d49c15a5f38c64`, `result: pass at 78ad518d4b705b7d07b90d7859d49c15a5f38c64` (the earlier log 020805 is a FAIL at the same head, superseded by the pass).

Note: `just site-assemble` fails at its `site:gallery` step on this machine ("Cannot curate E2E gallery: the final review report is missing": no e2e reports, CI-only on Windows; log verifier/assemble.log). Its first steps (requirements-report, compile) ran fine. I then ran its last step, `npm run site` (fnm exec -- npm.cmd run site, exit 0, "Built static site at ...\out\site"), which builds the site that carries the claims below. The gallery is unrelated to share cards.

## Claims (all at 78ad518d)

1. Pictures: `ls out/site/requirements/og` lists areas-card.png and 16 area-<areaId>.png (17 files); `ls | grep -E '^(areas|area|use-case|behaviour)\.png'` prints nothing. PASS.
2. StRS-MDOKFSTUDIO-MYST-005 page: og:image and twitter:image `.../requirements/og/area-myst.png`; og:title `Constructs the preview cannot build stay visible and labelled (StRS-MDOKFSTUDIO-MYST-005)`; og:description `As a writer, I want to know which constructs need a full project build so that I do not mistake a placeholder for a result.` (whole user need); first `<title>` `Use case MYST-005: ... | Studio requirements` unchanged form. PASS.
3. SwRS-MDOKFSTUDIO-CORE-022 page: og:image `area-rendering-core.png`; og:title `Build-dependent constructs show an inert placeholder with a warning (SwRS-MDOKFSTUDIO-CORE-022)`; description from the source line with backticks (`toc`, `{include}`...): the built one has none (node check: length 200, includes backtick false), ends with `…`; `<title>` `Behaviour CORE-022: ... | Studio requirements`. PASS.
4. requirements.html (stub) carries og:image `.../requirements/og/areas-card.png`, og:url `https://gsemet.github.io/markdown-okf-schema-studio/requirements/`, og:title `Requirements of Markdown OKF-Schema Studio`, twitter:card summary_large_image. PASS.
5. Screenshots opened as images: after-areas-card.png ("Requirements / Studio requirements"), after-area-myst.png ("Feature category / MyST syntax", violet), after-area-palette-slash.png ("Feature category / Edition palette and slash menu", red). Legible, show the claim, no path, username or home folder. Kept in work/verifier/evidence/. PASS.
6. Review box: PR body Review is unchecked, no claim to judge.
7. PR description (gh pr view 451 body equals work/pr-body.md): FAIL. Impacts has neither screenshot links nor "No visual change" (project PR guideline, "Screenshots in the PR" / template rule); Deliverables says screenshots "to come at closing"; Test plan "Local gates: to fill". The Summary, Deliverables and Changes otherwise match the diff (20 files: test/site socialCard, requirementsViewer cards/shell/pages/home/layout/write, requirements CORE-085/086/008, log, glossary). The opener must push the three images in work/verifier/evidence/ to the assets branch, link them in Impacts, and fill the gates line.

VERIFIED for the product behaviour; the description fails, so:

NOT VERIFIED


## Description-only pass (at 78ad518d4b705b7d07b90d7859d49c15a5f38c64)

Head: 78ad518d4b705b7d07b90d7859d49c15a5f38c64

Checked only the posted description (`gh pr view 451` body, 78ad518d head confirmed by `gh pr view 451 --json headRefOid`).

- Images resolve: `curl` of the three raw URLs (assets commit 02bff151) gives 200 image/png each; `git ls-tree 02bff151` lists the three files. Opened each: index card, MyST syntax (violet), Edition palette and slash menu (red); legible, match the captions, no username, path or home folder. PASS.
- Deliverables: no "to come" line; matches the diff against the base (20 files, `git diff --stat <cr-442 branch>...HEAD`). PASS.
- Test plan: boxes filled with SHAs; Review "approved at 590b2c52" matches the Driver note "r1 inspector approved at 590b2c52"; CI green at head (`gh pr checks 451`: static, static-windows, visual, report, checks pass). PASS.
- Internal references only in the last section (CR-443). PASS.
- Known gaps: has the Windows site-assemble gap and the flake, but `verifier/evidence/before-after.md` says the before pair was NOT captured, and Known gaps has no bullet for it. FAIL (card rule: each evidence pair not captured has its bullet). Fix: add a bullet such as "No before picture was captured; the old per-level pictures are removed by the diff, the three after pictures are at this head."

NOT VERIFIED


## Description-only pass 2 (at 78ad518d4b705b7d07b90d7859d49c15a5f38c64)

Head: 78ad518d4b705b7d07b90d7859d49c15a5f38c64

Command: `gh pr view 451 --repo gsemet/markdown-okf-schema-studio --json headRefOid,body`; headRefOid is 78ad518d4b705b7d07b90d7859d49c15a5f38c64; the body differs from work/pr-body.md only by a trailing newline (diff output: `72d71 <` blank line).

- Known gaps now has the bullet "No before picture was captured; ..." matching before-after.md (before not captured), plus the Windows site-assemble gap and the flake. PASS.
- Everything else carried from the first description pass at the same head (body text unchanged apart from the added bullet): images resolve and pass the look, Deliverables match the diff, Test plan SHAs and Review box match the Driver note, role names only in Internal references. PASS.

VERIFIED


## Move 78ad518d -> 726b41d5 (rebase onto the new base 7ad44734, CR-441 and CR-442 and the Delete block work)

Head: 726b41d5f5c821e08a521b8316ae763ad7c21d4c

Gate pass: work/gates/20261121-060717.log, first line `gate CR-443 branch ... head 726b41d5f5c821e08a521b8316ae763ad7c21d4c`, `result: pass at 726b41d5f5c821e08a521b8316ae763ad7c21d4c`. CI green at the head (Driver).

Command: `git range-diff 78ad518~1...78ad518 726b41d~1..726b41d`. Output: the CR commit differs only in context (log.md and rendering-core/index.md neighbours, the pages.ts import line now also names pathColour from the new base); the CR's own lines are unchanged. The base changed layout.ts, pages.ts, viewer.css, model.ts, so the site claims are judged again.

Command: `fnm exec -- npm.cmd run site` at 726b41d5 (exit 0, "Built static site at ...\out\site"), then inspection of out/site:

1. Pictures: `ls out/site/requirements/og | wc -l` prints 17 (areas-card.png plus 16 area-<areaId>.png); `ls og | grep -E '^(areas|area|use-case|behaviour)\.png'` prints nothing. PASS at 726b41d5.
2. StRS-MDOKFSTUDIO-MYST-005 page: og and twitter image `.../requirements/og/area-myst.png`; title `Constructs the preview cannot build stay visible and labelled (StRS-MDOKFSTUDIO-MYST-005)`; description is the whole user need. PASS at 726b41d5.
3. SwRS-MDOKFSTUDIO-CORE-022 page: image `area-rendering-core.png`; own title with the ID; description ends with `…`, grep for a backtick inside og:description prints 0. PASS at 726b41d5.
4. requirements.html: og:image `.../requirements/og/areas-card.png`, og:url `.../requirements/`, og:title `Requirements of Markdown OKF-Schema Studio`. PASS at 726b41d5.
5. Screenshots: carried from 78ad518d: the card renderer (cards.ts, socialCard.ts) is unchanged by the move (range-diff), so the pictures are the same.
6. Review box and description: not judged (the Driver updates pr-body.md; description claims carried from 78ad518d for product behaviour).

VERIFIED


## Description-only pass 3 (at 726b41d)

Head: 726b41d5f5c821e08a521b8316ae763ad7c21d4c

Command: `gh pr view 451 --json body,headRefOid`; headRefOid is 726b41d5f5c821e08a521b8316ae763ad7c21d4c; body equals work/pr-body.md apart from a trailing newline (`diff` prints `72d71 <`).

- Images: `curl -sIL` on the three raw.githubusercontent.com URLs (blob commit 02bff15, side branch of assets) prints 200 image/png each. Same captures as passes 1 and 2 (carried: the card renderer is unchanged by the rebase, see the move above). PASS.
- Deliverables vs diff: `git diff --stat <base>...HEAD` lists cards.ts, shell.ts, pages.ts, home.ts, layout.ts, write.ts, socialCard.ts, tests, SwRS CORE-085/086, StRS CORE-008, log.md, glossary: each is mentioned, nothing delivered is missing from the text. PASS.
- Test plan: Local gates and CI name 726b41d; gate log work/gates/20261121-060717.log first line names CR-443 and head 726b41d5f5c821e08a521b8316ae763ad7c21d4c, pass. Review box approved at 590b2c52: Driver note "r1 inspector approved at 590b2c529e9e7b0ee4c9b8ef1ecefc7bc2390909" in `chantier log`. PASS.
- Known gaps: before picture not captured (matches before-after.md), site-assemble on Windows, flake; no UNVERIFIED claim exists (grep count 0). PASS.
- Role names: only "CR-443 share-cards" in Internal references; the body names no role elsewhere. PASS.

VERIFIED


## Description-only pass 4 (at 726b41d)

Head: 726b41d5f5c821e08a521b8316ae763ad7c21d4c

Command: `gh pr view 451 --json body,headRefOid`; headRefOid is 726b41d5f5c821e08a521b8316ae763ad7c21d4c; body equals work/pr-body.md apart from a trailing newline (`diff` prints `72d71 <`).

- Review box: pr-body.md line 64 reads "approved at 726b41d (round 1, move 78ad518..726b41d)". `chantier log CR-443` holds the Driver note "move 78ad518..726b41d (conflict) inspector approved at 726b41d5f5c821e08a521b8316ae763ad7c21d4c". Same SHA and same move. PASS.
- Everything else: unchanged since pass 3 (carried from pass 3 at 726b41d: only the Review line changed). PASS.

VERIFIED
