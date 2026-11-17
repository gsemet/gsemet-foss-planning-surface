# CR 201: Studio in the VS Code Agents window

Intent: [01-intent.md](../01-intent.md). Spike evidence: [03-spike-report.md](../work/03-spike-report.md).
Plan: [04-implementation-plan.md](../work/04-implementation-plan.md).

## User decisions (2026-10-29)

- Scope: full plan, T1 to T4 (manifest declaration, editable on mount, keep the tab read-only on
  unmount, docs). User: "full".
- Grill question 1 (02-decisions.md): accepted the recommendation. A removed workspace folder keeps
  the Studio tab open read-only, in every window, and a later added folder makes it editable again.
- Grill question 2: no `engines.vscode` bump (recommended answer, not challenged).
- Grill question 3: no CI job in the real Agents window; unit and manifest tests plus manual spike
  replay (recommended answer, not challenged).
- Approved requirements touched: none (TRUST-001 and LIFE-143 are `proposed`).
- Rounds: default limit 3.
- Push and open the PR on GitHub following the project PR format (user request).
