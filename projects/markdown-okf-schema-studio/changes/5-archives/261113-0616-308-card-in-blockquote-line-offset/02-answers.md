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
- No USER-IMPACT question for this CR.
Batch: Open VSX is out, so the release is v1.8.0 (Cmd+S is a feature; honest commit types).
- Scope narrowed per the advisor: the offset reproduces for a quoted {grid} whose body starts with a blank '>' line (rawBody fallback in src/core/render/mystGridToctree.ts:90-101).

## Autonomous decisions (owner order O-1, 2026-11-12)

- A quoted backtick-fenced card with a blank first body line was also one line early on main (the specification listed it as correct). The same prefix-stripping fix covers it, so it is fixed here with its own test row.
- A grid inside a list item with a blank first line is also one line early but needs a different change: left out, filed in `.agents/changes/1-inbox/grid-in-list-item-line-offset/`.
- Local long gate is `just check && just requirements-lint` (a preflight needs an unlocked screen); the branch heavy run is the proof for the real-window jobs.
