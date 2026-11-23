# Slim the startup cards of the Chief of Staff, Foreman and Driver

Short name: `slim-cards`. Owner's words of 2026-11-23, relayed from markdown-okf-schema-studio.

The Chief of Staff, Foreman and Driver cards are still very large (`chief-of-staff.md` 200 KB read whole by one action, `foreman.md` 83 KB, `driver.md` 134 KB). Each is cut by moment of need, each piece an action of `startup-manifest.json` read when the situation arrives, so the right instruction comes at the right moment by the right means and nothing is lost. The three roles are in this one CR, in that order, after `slim-session-start`. Each role's start reading is measured before and after, aiming at about half, the figures said in the PR. Proof: a table naming each moved rule with its action, a test that every rule is reached by an action of the manifest, and a Fable advisor reading each role's split.
