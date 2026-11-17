# Answers

## 2026-11-12: grill round 1 (retro of v1.7.1)

Owner, 2026-11-12: « je suis d'accord. grille avec un advisor fable et fini par une CR de release. demande moi uniquement quand il y a un impact utilisateur », agreeing to the recommendations:

1. Grouping: one CR for the three release-process fixes (this one); release-marketplace-check-of-record
   and release-step8-empty-issue-list are abandoned and folded in here.
3. The changelog line is required by the documents (lifecycle guideline and a checkbox in the PR
   template), not by a CI check.
4. Triage: automatable, short specification the owner does not review.
- Priority P1, in the next batch, which ends with a release CR.
- Other questions: a Fable advisor answers them; the owner is asked only on a user impact.

## 2026-11-12: delivery of the batch

Owner, 2026-11-12: « tu livreras une stack prete a mergée avec le PR de release en dernier ».
Open: this conflicts with the release-process guideline (the version commit is never stacked on
top of development; the stack lands first, then the heavy run on `main` HEAD, then the version PR).
The conflict was reported to the owner.

Owner, 2026-11-12, on the conflict: « Yes, and update the guide ». The release PR is the top of the
stack; before it turns ready, the heavy run is dispatched on the stack's top branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`); the owner merges the whole stack by
rebase in order; the version push on `main` stays the final gate and makes the tag.
This CR also updates the release-process guideline (and CONTRIBUTING.md "How to Release" if it
says the same) to allow this way: the version PR may top a ready stack when the branch heavy run of
that top is green; the 1.3.0/1.3.1 rationale stays, met by the branch heavy run.

## 2026-11-12: Fable advisor

A Fable advisor (read-only, at origin/main cb968299) answered the INTERNAL questions; its report is
`intake/advisor-grill.md` (the section of this CR). Its INTERNAL recommendations are adopted, per the
owner's instruction to be asked only on a user impact. USER-IMPACT questions go to the owner.

## 2026-11-12: USER-IMPACT answers

Owner, 2026-11-12: « exclu "Open VSX" pour l'instant. ok pour tout le reste. »
- No USER-IMPACT question for this CR.
Batch: Open VSX is out, so the release is v1.8.0 (Cmd+S is a feature; honest commit types).
- Open VSX is out of the batch: this CR does not touch the Open VSX parts of the release guideline.

## 2026-11-12: spec-writer's readings

The Chief of Staff accepts the spec-writer's three readings (no user impact, per the owner's rule to be
asked only on a user impact): `ci.guidelines.md` rule 14 and the lifecycle guideline's release
sections change too; every other merge is held from the branch heavy run until publication; the
bottom of the stack is based on the current `origin/main` HEAD.
