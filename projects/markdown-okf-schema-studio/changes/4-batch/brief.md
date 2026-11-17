# batch-05

- Mode: parallel. Slots: 4. Budget: none. Host: claude. Steering: direct.
- CRs, in order:
  - CR-336: Nothing protects the engines.vscode ^1.95.0 minimum: the lock file resolves @types/vscode to 1.140.0, so a change could use a newer API without any check failing. Add a just check step that type-checks src/ against @types/vscode 1.95. Found by the cursor-compatibility spec-writer, 2026-11-14. (4-batch/1-pending/336-check-against-minimum-vscode-types)
  - CR-337: Stress flake: the incoming-changes scenario timed out once in frame.waitForFunction (30 s) in round 2 of a scoped stress run on CR-328's branch (PR #402). The step was not touched by that CR. Seen once; find the run, the condition it waited for, and whether it repeats. (4-batch/1-pending/337-stress-incoming-changes-wait-timeout)
- Project instructions: AGENTS.md; the surface's: AGENTS.md.
- Team (who runs which role): no chantier.yaml, the plugin's agents and models (`chantier:<role>`,
  each with its file's model; escalation: opus). No extra review step in AGENTS.md.
- Autonomous decisions: both CRs are automatable on the owner's word (2026-11-17, "Yes, run
  them"; recorded in each CR's 02-answers.md): the Driver works from the request alone, with no
  reviewed specification. CR-337 may end with a documented "not reproduced" and no code change if
  the investigation shows no fix is warranted; it says so in its PR or its hand-back.
- Questions to bring back: any change of scope (a CR-336 check that needs a new dependency or a
  CI job change beyond `just check`; a CR-337 fix outside the incoming-changes scenario).
- Long gate: `just preflight` (AGENTS.md "Completion gate"; on Windows, the static stage only, CI
  runs the others).

## Permission trials

- P10, every batch: "the commands its agents run are allowed by your settings".
- every batch: `git -C C:/Users/gaeta/Projets/markdown-okf-schema-studio push --force-with-lease -u origin chantier/preflight-trial --dry-run` -> ran (git: src refspec does not match any)
- every batch: `gh pr view --json number` -> ran (no pull requests found for branch "main")
