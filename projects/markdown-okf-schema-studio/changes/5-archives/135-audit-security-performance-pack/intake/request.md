# 135 — Audit pack: security, performance and maintainability (2026-10-27 audit)

Type: fix · Priority: P1 · From: [audit report](../work/backlog-audit-performance-security-maintainability/report.md) (section 5, proposed CRs 3–28; CRs 1 and 2 shipped as CRs 132 and 133)

## Intent (user)

After CRs 132 and 133 (audit CRs 1 and 2), the user asked for the next audit items with several
drivers working in parallel, delivered as **one single PR with everything**: "fais travailler
plusieurs drivers en parallèle pour optimiser le dev mais livre qu'une seule PR avec tout",
then "en incluant tous les 28 points".

## Scope

| Task | Audit | Subject |
| --- | --- | --- |
| [T1](../work/tasks/T1-myst-tightness.md) | P-02, CR 9 | Patch `computeBlockTightness` of `markdown-it-myst` |
| [T2](../work/tasks/T2-plantuml-jar-profile.md) | S-03, CR 3 | PlantUML JAR: security profile and limits |
| [T3](../work/tasks/T3-sidecar-symlink.md) | S-04, CR 4 | Comments sidecar write is symlink-safe |
| [T4](../work/tasks/T4-sanitizer-hardening.md) | S-05, S-08, S-09, P-09, CR 5 | Sanitizer hardening |
| [T5](../work/tasks/T5-single-parse5-pass.md) | P-03, CR 10 | One parse5 pass per page build |
| [T6](../work/tasks/T6-visibility-shared-render.md) | P-01 (part), P-06 (part), CR 11 | Render only visible previews, once per document |
| [T7](../work/tasks/T7-drop-retain-context.md) | P-05, CR 12 | Drop `retainContextWhenHidden` |
| [T8](../work/tasks/T8-restricted-settings-capabilities.md) | S-06, S-07, CR 6 | Restricted-mode settings and page-callable capabilities |
| [T9](../work/tasks/T9-supply-chain-ci.md) | S-10, CR 7 | Supply-chain CI |
| [T10](../work/tasks/T10-vsix-contents.md) | P-13, S-10, CR 8 | VSIX contents |
| [T11](../work/tasks/T11-content-addressed-caches.md) | P-04, P-12 (part), CR 14 | Content-addressed caches for per-block work |
| [T12](../work/tasks/T12-plantuml-jar-cache.md) | P-10, CR 15 | PlantUML JAR cache and concurrency |
| [T13](../work/tasks/T13-event-fan-out.md) | P-06, CR 17 | Event fan-out |
| [T14](../work/tasks/T14-stable-morph-keys.md) | P-07, P-08, CR 16 | Stable morph keys and incremental page init |
| [T15](../work/tasks/T15-page-plantuml-queue.md) | P-11, CR 18 | Page PlantUML queue drops superseded runs |
| [T16](../work/tasks/T16-frontmatter-once.md) | P-12, CR 19 | Front matter parsed once per revision |
| [T17](../work/tasks/T17-bundle-trims.md) | P-13, CR 20 | Bundle trims |
| [T18](../work/tasks/T18-render-worker.md) | P-01, CR 13 | Worker-thread renderer with cancellation and adaptive debounce |
| [T19](../work/tasks/T19-logger-port.md) | N-01, CR 21 | Logger port and `fireAndForget` |
| [T20](../work/tasks/T20-shared-syntax-primitives.md) | M-04, CR 22 | Shared syntax primitives |
| [T21](../work/tasks/T21-postinstall-patch.md) | N-03, CR 25 | De-risk the postinstall patch |
| [T22](../work/tasks/T22-lifecycle-typing-nits.md) | N-04, N-05, CR 27 | Lifecycle and typing nits |
| [T23](../work/tasks/T23-split-realinput-tests.md) | N-02, CR 24 | Split `realInput.test.ts` and the near-limit tests |
| [T24](../work/tasks/T24-boundaries-debt.md) | M-01, M-02, CR 23 | Retire the session to node-services debt and break the `fileLinks` cycle |
| [T25](../work/tasks/T25-unused-exports-sphinx.md) | N-06, CR 28 | Unused-exports check and the Sphinx build decision |
| [T26](../work/tasks/T26-split-large-modules.md) | M-03, CR 26 | Split the 700+ line modules |

## Autonomous decisions

- Decided by the main session on 2026-10-27; list these in the PR body under "Autonomous decisions".
- Every remaining audit CR (3–28) is one task, T1–T26, integrated in task order.
- One CR, one branch `change-requests/135-audit-security-performance-pack`, one PR. Each task is built in parallel by its own
  driver on a local task branch, then integrated in task order T1 → T26, **one Conventional Commit
  per task** in the PR (26 commits, each one green on its own), so the PR can be reviewed per
  topic and merged with rebase.
- Task branches stay local (never pushed); only the integration branch is pushed.
- PR body: the class of input each security change refuses, never a ready-to-use exploit path.
  Performance claims come with before/after numbers from the repository's bench scripts.
- T1–T7 start from origin/main (already created). T8–T26 start from the integration branch tip
  when they start, to keep conflicts small; T18, T24 and T26 wait for the tasks their scope names.
- Each task has its own round limit (3). A blocked task is left out of the PR, recorded in
  `STATE.md` and in the PR body ("Not included"), and the others continue.
- The audit folder stays in the P3 backlog until the PR merges; then it is archived with the CR.
