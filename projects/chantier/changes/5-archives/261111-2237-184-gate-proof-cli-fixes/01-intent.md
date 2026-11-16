# Intent: gate-proof-cli-fixes

Make the long gate's proof bind to one exact commit that anyone can read, make `handback ready`
refuse anything but that commit pushed, make the budget a real bound on new rounds as driver.md
already says, and give the user a CLI way to bring a trashed CR back to the inbox.

Source: batch-11 retro (`.agents/changes/4-batch/retro.md`), folding the inbox items
gate-log-commit, driver-budget-refusal and undrop-cr.

Findings from the grill:
- The gate already records a head in its event (commands.py:1720-1724) and `handback ready`
  already refuses without a passed gate at the recorded head (commands.py:1504-1513). The gaps are
  that the log file carries no commit, and how the head is read.
- Short SHAs are compared by string equality: `gate` and `verdict` record `git rev-parse --short
  HEAD` (commands.py:1720, 1754) while `ship` records `head[:7]` (commands.py:1782). Git
  abbreviates past 7 characters in large repositories, so `handback ready` would be refused
  forever there (found by reading, not exercised).
