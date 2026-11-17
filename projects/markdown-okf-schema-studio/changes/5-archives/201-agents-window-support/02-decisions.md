# Decisions

| # | Question | Decision | By, date |
| --- | --- | --- | --- |
| D1 | Integrate as a Copilot canvas? | No. Studio is a custom editor, and the Agents window hosts custom editors once the extension is enabled. | user, 2026-10-29 |
| D2 | Scope before planning | Spike first in a real VS Code host, then plan. Done: [03-spike-report.md](03-spike-report.md). | user, 2026-10-29 |
| D3 | Read-only page when the file is not in a workspace folder | Fix it in this item: a preview becomes editable when the session worktree mounts. | user, 2026-10-29 |
| D4 | Where the item lives | `02-backlog/P1/agents-window-support/`; CR number and branch are assigned when it is picked (lifecycle step 3). | user, 2026-10-29 |

## Open questions for the grill (lifecycle step 2)

Each comes with the recommended answer.

1. When a workspace folder is removed (agent session switch), should a preview of a file in that
   folder close (today, LIFE-143) or stay open read-only?
   Recommended: stay open read-only in every window, and become editable again when a folder that
   holds the file is added. A closed tab is lost work for the reader, and the Agents window removes
   the folder on every session switch. LIFE-143 is `proposed`, so no owner agreement is needed.
   Its "dispose the watchers and Problems entries" part stays.
2. Raise `engines.vscode`?
   Recommended: no. Older hosts ignore an unknown `capabilities` key, and the Agents window exists
   only in recent builds.
3. Automated proof in the real Agents window?
   Recommended: no CI job. The window shows a sign-in overlay without a GitHub account, and the
   behaviour is host-agnostic once the extension is enabled. Unit tests cover the folder changes,
   a manifest test covers the declaration, and the spike scripts stay as manual evidence.
