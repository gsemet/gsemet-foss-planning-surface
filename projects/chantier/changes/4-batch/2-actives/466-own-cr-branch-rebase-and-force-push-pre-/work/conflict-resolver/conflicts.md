# Conflicts, CR-466 rebase onto b4cb7066
- concepts.md rule 8 push item: kept CR-465's "rebase only, never --rebase-merges, no merge/Update branch" and CR-466's pre-authorized force-with-lease on own chantier/* branches plus "never --exec/-x".
- conflict-resolver.md "Your part": kept CR-465's no-merge/--rebase-merges sentence plus CR-466's "(never git rebase --exec or -x)".
- driver.md "Means: rebase and push": kept CR-465's "Rebase only (rule 8)" and CR-466's wording and `Rewrites:` scope sentence; tightened wording (9+ bytes) so cr-driver startup bytes fit 36000.
- Fast gate: `just check` -> 2288 passed, 20 skipped, release-notes ok.
