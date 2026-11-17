# Conflicts, CR-318 rebase onto CR-317 head 0bd9d9c

- skills/chantier/references/chief-of-staff.md, "Resume" bullet (~line 1364), commit b9daeff.
  Choice: kept the base (CR-317) sentence that a Driver with a cleared id and a replaced Foreman are never a close blocker (listed apart, no --stopped), then appended CR-318 direct-batch sentences (Chief of Staff restarts a Driver stopped from outside with no question; clears the recorded id the same turn when it stops one and does not restart it). Dropped CR-318 old sentence "The old Foreman session ... close --stopped", obsolete.
- No BOM (file starts "# C" as before). Rebase continued: e0e60c8.
- Fast gate: `just check` -> lint ok, 402 passed in 17.01s, release-notes ok. PASS.
