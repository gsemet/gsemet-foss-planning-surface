# Answers

## 2026-11-14: release again after the fixes

Owner, 2026-11-14: « oui je pense qu'il faut tout corriger et retenter une release ». Earlier, the
owner's overnight word: « tu peux faire 2 releases tout seul, 1.9.0 et eventuellement 1 fix
1.9.1 »; grant O-11 (releases=2, fixes=on, budget $45), one release used by v1.9.0.

Decided by the Chief of Staff:

- Version 1.9.1 (patch): the three CRs are fixes, with no user-visible feature.
- Same procedure as v1.9.0 (release guideline): branch heavy run green on the exact head, the
  owner merges the version PR by rebase (the harness refuses the Foreman's merge), watch both
  registries 10 to 15 minutes.
- Success criterion: the version push's Open VSX step is green with no recovery dispatch. If it
  fails again, one recovery dispatch of `release.yml` with the tag, as for v1.9.0, and it is
  reported as a failure of the fix.
- No hero image (no visual change); the announcement thread is drafted, never posted.

## 2026-11-17: discarded, already done

Owner, 2026-11-17: « 334 est deja faite je crois. reverifie ce qui est deja fait et discard ».

Checked by the Chief of Staff: v1.9.1 published on 2026-11-14 (work/04-report.md), success criterion met.
