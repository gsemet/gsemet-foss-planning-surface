# Verify CR-377

Head: 8a88c5568cd1ea8138438ec80cbd79b71e82eba3

All claims judged at 8a88c5568cd1ea8138438ec80cbd79b71e82eba3.

1. No change under src/, hooks/, types/, agents/: `git diff HEAD~1 --name-only | grep -E "src/|hooks/|types/|agents/"` printed nothing (rc=1). Files: scenario/README.md, scenario/run_scenario.py, and the chief-of-staff, driver, foreman cards.
2. Spec 1 (chief-of-staff Releases paragraph, placed after the "auto" paragraph, before `draft <path>`): present in the diff, covers the ask, For-you line, no `order approve`, relay note, Foreman/direct mode, steering-session note, what follows, never-relay. Coherent with the existing text.
3. Spec 2 (foreman release bullet): present, take-back with the note, `agents set <cr> -`, `order done`, not a new attempt, working-Driver message.
4. Spec 3a/3b (driver): both added sentences and the new bullet "publication done by someone else" present: no `release start`, never rerun the command, `gh release view`, found/not-found routes; 3c unchanged (the diff touches no "Release driver: the end").
5. Spec 4: run_scenario.py steps 1-5 present (note, blocked handback, blocked check with batch not paused, `order note` accepted with "is blocked", `fm.turn()` with started/status/attempts/orders checks, then the existing `release published`). README sentence added before the kept `(unit: release)` marker.
6. Scenario unit: `just scenario --unit release` run at this head: `ok  release (github): 143/143 checks, 256.0 s`; CI scenario job is green as well.
7. PR description (`gh pr view 340`, headRefOid = the head): renders (sections, mermaid, fold); Summary, Deliverables and Changes match the diff; Known gaps names the two unproved items; no image; the role names are product terms of the change.
8. Review box "approved at 8a88c55": `log CR-377` shows "r1 approved at 1b58d39, committed as 8a88c556", which matches (committed as).

VERIFIED
