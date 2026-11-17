# c5-1 Agents window cannot be driven by the harness (Gap, Medium, skill + environment)

Charter C5 (PR #223, Studio in the VS Code Agents window), VS Code 1.144.0.

What worked: `code --user-data-dir=<msq profile> --extensions-dir=<profile>/ext --agents <ws>` forwards to
the running isolated instance and opens the Agents window (`sessions.html`) on the same CDP port 
(2 page targets).

What blocked:
1. `qa.mjs connect()` picks `pages.find(/workbench/)`, so every `q` command targets the normal
   window; the Agents page (`.../vs/sessions/electron-browser/sessions.html`) is never reachable
   with `q` (no `--page` option). Raw playwright-core on the sessions page works (text, screenshot).
2. The Agents window shows a modal "Sign in to use Agents" (GitHub/Google/Apple/GHE) in the isolated
   profile. Signing in needs a real account OAuth flow; not done by the QA agent. Without it no
   session, no Open With, no folder switching can be exercised.
3. The Agents window listed a real project folder (agentic-coding-white-paper) in its Files pane,
   not the QA workspace passed on the command line (privacy note: do not use its shots as evidence).

Evidence: none. The shot of the sign-in modal was deleted: it showed private folder names. The modal reads "Sign in to use Agents".

Proposal: add `q --page sessions` target selection, and a pre-authenticated profile or a
documented manual sign-in step; until then #223/LIFE-143 session-switch behaviour stays untested.
Requirements: SwRS-MDOKFSTUDIO-LIFE-171, LIFE-143, TRUST-001 (Agents window parts), none automated end to end.
