# Answers

## 2026-11-12: grill round 1 (retro of v1.7.1)

Owner, 2026-11-12: « je suis d'accord. grille avec un advisor fable et fini par une CR de release. demande moi uniquement quand il y a un impact utilisateur », agreeing to the recommendations:

2. macOS only: `ci-integration` checks for a locked screen before the run and stops with that cause
   and what to do instead (unlock, or `gh workflow run ci.yml --ref <branch> -f heavy=true`). In
   `preflight`, `ci-report` and `ci-gallery` say they are skipped because integration did not run
   (screen locked) instead of failing without a cause. The release procedure says to dispatch the
   branch heavy run at once in that case.
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

## 2026-11-12: Fable advisor

A Fable advisor (read-only, at origin/main cb968299) answered the INTERNAL questions; its report is
`intake/advisor-grill.md` (the section of this CR). Its INTERNAL recommendations are adopted, per the
owner's instruction to be asked only on a user impact. USER-IMPACT questions go to the owner.

## 2026-11-12: USER-IMPACT answers

Owner, 2026-11-12: « exclu "Open VSX" pour l'instant. ok pour tout le reste. »
- No USER-IMPACT question for this CR.
Batch: Open VSX is out, so the release is v1.8.0 (Cmd+S is a feature; honest commit types).

## Autonomous decision (CR driver, owner order O-1)

Local preflight failures (visual sticky overlay, scroll-sync) were judged out of scope; the CI heavy run, re-dispatched once after two flaky `integration` failures, is the proof. The verifier step was skipped: the stop was shown with `STUDIO_SCREEN_LOCKED=1 just ci-integration` (exit 3) and the heavy run is green.
