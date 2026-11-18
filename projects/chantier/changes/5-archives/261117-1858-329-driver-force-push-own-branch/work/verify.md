# Verify CR-329

Head: c103c074890eeadf718f0162c66f54dc75708a4b

All claims judged at c103c07.

1. Scripts untouched. `git diff origin/main -- skills/chantier/scripts/ | wc -l` -> `0`. VERIFIED.
2. Only 3 cards change. `git diff --stat origin/main` -> chief-of-staff.md (6), driver.md (3), hosts/claude-code.md (21). VERIFIED.
3. driver.md changes no push command. `git diff origin/main -U0 -- driver.md` adds only the sentence "`<branch>` is your own CR's branch ... never another CR's (the stack driver restacks ...)" after "(a rebase)". VERIFIED.
4. Greps. `git grep "Destructive or Unwanted Actions"` -> claude-code.md:248 (Mark, batch-23, still "refused 4 times"), :396 (labels bullet, batch-23); the first Auto-mode bullet (diff lines 389-394) reads "In batch-23 (CR-318), the classifier refused ... unproved, not documented" (wraps the label out of the grep line; it names batch-23, CR-318 and the refusal; the label itself is quoted in row 248). `git grep "except batch-23, CR-318"` -> claude-code.md:411. `git grep "own CR's branch"` -> driver.md:270, claude-code.md:247 and :248. VERIFIED.
5. Other Area 2/4 edits present per diff: Every batch row, trial sub-bullet ("for the steering session; for a Driver, see batch-23 above"), alert line, CoS "On the yes" and step 3. VERIFIED. (Minor: the "Every batch" Mark text is in the row's Mark cell per diff line 352; accepted.)
6. Matcher check. `uv run --no-sync --project . python -c "...rule_matches..."` printed `True True`. VERIFIED.
7. `just check` at c103c07: 443 passed, release-notes ok, lint clean. VERIFIED.
8. PR #286 description (head c103c07 confirmed by `gh pr view`): renders, quotes the refusal verbatim and the matcher command with `True True`; Summary/Deliverables/Changes match the diff; no images; Known gaps "None" with no UNVERIFIED claim. Test-plan boxes keep `<sha7>` placeholders for Review/Verified/CI (to fill by the Driver at handback). VERIFIED.
9. CI: scenario green at the head per the prompt (not re-run by me).

VERIFIED

10. Description-only pass at c103c07 (posted body re-read via gh pr view 286): renders, matches the diff, Known gaps "None" with no UNVERIFIED claim, no images, SHA placeholders now filled with c103c07; Review box backed by log note "approved at a111e18..., committed as c103c07"; CI note 5 jobs pass at c103c07. Claims 1-8 carried from c103c07 (head unchanged). VERIFIED.

VERIFIED
