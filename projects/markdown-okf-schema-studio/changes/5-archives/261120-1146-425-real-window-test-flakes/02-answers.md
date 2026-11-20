Short name: `rw-flakes`

# Answers (owner, 2026-11-20, Chief of Staff grill)

- Scope: fix the root cause of all three real-window flakes in this CR: paste-url (diagnosis in CR-350 work/diagnosis.md: obsolete stored-mode wait), checkbox-toggle, preview-editing issue-highlight (stepSchemaOrderAndBadge locator timeout). (owner chose: 'Les trois tests')
- If a cause stays unfound: keep the test, no automatic retry, no quarantine; document a Known issue with the written analysis. (owner chose: 'Garder et documenter')

- Spec open questions, decided by the Chief of Staff under the owner's standing autonomy grant: (1) no extra file under docs/: a short Known issue in the SwRS, the full analysis in the CR folder and summarized in the PR body; (2) the reportStaleEdit debug log stays out unless the Driver needs it to prove a cause.
