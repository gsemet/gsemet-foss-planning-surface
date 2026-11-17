# Verify CR-342

Head: db9e4560fd957edc0fc8bb1311376949727fcc7a

VERIFIED

Judged at db9e4560 unless stated. Move b971dda..db9e456: clean rebase onto main (9bae4f9a) plus one docs commit.

1. Long gate: carried from b971dda (itself carried from 05550d0): the patch is unchanged, `git range-diff 72eb59fc..b971dda origin/main..HEAD` prints `1: b971dda8 = 1: 9a8c2664 feat(render): show a use case diagram on the requirements site` then `-: -------- > 2: db9e4560 docs: state how GitHub draws a use case diagram` (the only new patch). Base commit of the CR's feat patch moved (CR-340 and CR-341 merged), the patch itself is identical.
2. Review box: carried from b971dda: code patch identical (claim 1); the new commit is docs only, one sentence.
3. Site tests at db9e4560: `fnm exec -- npm.cmd run compile` (tsc, no error) then `node --test out/test/site/requirementsViewer/*.test.js`: tests 31, pass 31, fail 0, skipped 0.
4. `just requirements-lint` at db9e4560: exit 0, `0 files would change`, `main paths: 78 StRS checked, 536 SwRS citations, all valid`. `just requirements-report`: carried from b971dda: no requirement file changed except the guideline sentence (`git diff b971dda HEAD --stat`: 1 file, project.guidelines.md, 6 insertions, 4 deletions).
5. PR scenario, steps 2 to 5 (local site, GitHub, CI, branch cleanup): carried from b971dda: code unchanged; the move touched no site code.
6. Guideline sentence (`git diff b971dda HEAD`): now says "checked on a GitHub branch preview, GitHub draws a sequence, a flowchart and a state diagram fence natively", own theme not the site's cream colours, newer Mermaid than `^12.2.0`, iframe with pan, zoom and copy buttons, layout and text match, no label cut, renderers can still differ. Matches step 3 of b971dda (own theme, newer Mermaid, overlay buttons, iframe, same layout and text, no cut). The statement "checked on a branch preview" has no date; acceptable.
7. PR description at db9e4560: `gh pr view 412 --json headRefOid,isDraft` gives head db9e4560fd957edc0fc8bb1311376949727fcc7a, draft. `diff` of the posted body against work/pr-body.md (CR stripped) differs only by one trailing blank line. Its text on GitHub rendering (line 34) matches the guideline; Known gaps lists the screenshots not attached and the CI gallery tweak. Review and CI boxes open, honest for a draft. No STALE mark.
