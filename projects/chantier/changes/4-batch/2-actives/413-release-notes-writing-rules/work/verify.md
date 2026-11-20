Head: a86aca24c205b0c8f8ede36715b5497b5a0ef177

Claims, all judged at a86aca24.

1. Diff touches only release-template.md (and pr-template untouched).
   `git diff --stat <base>..HEAD` -> 1 file: skills/chantier/references/release-template.md, 28 insertions, 8 deletions.
2. Structure (title, one verbs line, 2-4 highlights, smaller one-liners, folded fixes/details): lines 19-25 of release-template.md.
3. Writing rules (maintainer to colleague, short sentences, plain verbs, "you", no ticket/internal/implementation): "Writing rules" section, grep lines 33-36.
4. Highlight rules: heading, picture, at most two sentences (line 40); side-by-side before/after built from Verifier's, text does not describe before (41-43); no text when picture shows all (44); setting named "the setting `full.name`" with default and where to enable (45-46).
5. Never-use list: line 35 ("Before:"/"Now:", invented scene, punchy fragment, praise words, closing "why it matters").
6. Coverage: lines 27-28, each changelog line once.
7. Visible evidence side-by-side image: line 49-51.
8. PR #378 head = a86aca24c205b0c8f8ede36715b5497b5a0ef177 (gh pr view). Description: sections consistent with the diff; Known gaps (docs/release-process.md lines 47-51 still ask for usage example, doc link, why-it-matters) checked true by sed; no images; no role names beyond a CR reference in Internal references.
Test plan SHA boxes not judged (Driver fills).

VERIFIED

## Description pass at a86aca24c205b0c8f8ede36715b5497b5a0ef177
- Command: `gh pr view 378 --json body`, `git diff HEAD~1`, `chantier log 413`, `gh pr checks 378`.
- Summary, Deliverables table, Changes match the diff (release-template.md only; "The notes", "Writing rules", "A highlight", "Visible evidence"). Known gap on docs/release-process.md lines 47-51 confirmed (still asks usage example, doc link, why-it-matters).
- Review box: log notes "r1 approved at 2d07ac0c, committed as a86aca24" matches. CI: five checks pass. No images. No role names.
VERIFIED
