Short name: `evals-rework`

# Answers

Decided by the Chief of Staff (technical, not asked):

- The claims files move to `evals/results/claims/`, apart from the run reports.
- The README names the campaigns in one table. Every other place points to that table instead of
  listing the campaigns again.
- Each host-specific step of the README names its host: Claude Desktop or the Copilot app.
- The published release notes (v0.9.0, v0.10.0) keep the old names.

Grilled with the user, 2026-11-15:

1. evals-rework-Q1: **Old reports.** Every report is renamed date first, under the campaign it
   really ran. For example, `claude-full-2026-11-04-ask-only.md` becomes
   `2026-11-03-22-17-claude-planted-ask-only.md`, and the `real-*` reports of 11-05 become
   `claude-real-foreman` reports. The README's "Past reports keep their names" paragraph goes.
2. evals-rework-Q2: **Time zone.** UTC, the zone of the times written inside the reports. The
   README says so.
3. evals-rework-Q3: **The ticket summary.** The GitHub ticket-summary rule stays in
   `chief-of-staff.md`, marked unproved with no trial planned. The `ticket-summary` kit goes with
   the campaign: `evals/kit/ticket-summary/`, its setup case, its dry-run case and its check in
   `test_cli_units.py`.
4. evals-rework-Q4: **claude-full before a release.** `claude-full` runs before a minor or major
   release; a patch release needs only the quick campaigns. This changes the README,
   `CONTRIBUTING.md` and `docs/release-process.md`.
5. evals-rework-Q5: **How far the Copilot campaigns go.** `copilot-real-foreman` and
   `copilot-real-direct` each get:
   - their runbook, their setup entry and prompt line, and their dry-run case;
   - the Copilot prerequisites in the README.

   The audit checks what every host shares: the run, the judge and the cost. The
   Copilot-specific checks are written after the user's first real run, from its logs, and the
   runbooks say so. The old `copilot` campaign goes.
6. evals-rework-Q6: **Grilled enough?** Yes: specify. The user approved the full restatement on
   2026-11-16. Done means `just check` and `just eval-dry-run` pass, and no old campaign name is
   left anywhere except the published release notes.

The specification's open questions are facts, not behaviour. The Chief of Staff settled them on
2026-11-16:

7. **Time of the ask-only report.** `2026-11-04-19-11-claude-planted-ask-only.md`, read from its
   transcripts. Q1's example used the time of another report by mistake.
8. **Reports that give no start time.** The time is read from the run's records: the batch's
   `open` in the transcripts. When no record gives it for sure, the name uses the time of the
   commit that added the report, and the PR says so.
9. **The `-smoke` qualifier** stays after the campaign: `...-claude-planted-smoke.md`.

Spec critic: yes. The CR changes the release rule (when `claude-full` runs) and a card
(`chief-of-staff.md`, the ticket summary's trial). A wrong specification would weaken the checks
made before a release.

# Decision (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is cancelled: it is kept for reference in `work/spec-before-rework.md`, and is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32.
