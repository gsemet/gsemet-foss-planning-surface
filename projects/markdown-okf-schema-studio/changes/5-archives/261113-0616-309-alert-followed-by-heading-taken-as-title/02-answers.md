# Answers

## 2026-11-12: picked for the next batch

Owner, 2026-11-12: « je suis d'accord. grille avec un advisor fable et fini par une CR de release. demande moi uniquement quand il y a un impact utilisateur », agreeing to add this item to the batch after the v1.7.1 retro items.
Priority P1. Open questions: a Fable advisor answers them; the owner is asked only on a user impact.

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
- Match GitHub for > [!NOTE] alerts: default title (or the text after the marker, which stays), and a heading on the first line stays a heading in the body.
- Same for a lone bold first line (> **Bold**), through takeAdmonitionTitle.
- MyST :::{note} admonitions and Quarto callouts keep the title shortcut (MYST-005, MYST-001).
Batch: Open VSX is out, so the release is v1.8.0 (Cmd+S is a feature; honest commit types).

## 2026-11-12: autonomous decision (Driver, owner away, order O-1)

The spec's `[TOC]` row ("lists Top, not Inside") does not hold: `[TOC]` lists headings inside any admonition, MyST ones included. Decision: the test asserts the heading stays inside the `.admonition` aside (excluded from the TOC column and sticky band) instead; behaviour of `[TOC]` is not changed in this CR.
