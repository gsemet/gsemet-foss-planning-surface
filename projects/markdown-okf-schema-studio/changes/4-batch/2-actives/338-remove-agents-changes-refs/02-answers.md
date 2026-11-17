# Answers

Short name: `agents-changes-refs`

## 2026-11-17: triage

1. agents-changes-refs-Q1: **Add to batch-05?** Owner, on « La CR `.agents/changes` : on
   l'ajoute à ce lot ? Et le générateur `just orchestrator`, on le garde ou on le supprime ? »:
   « 4. ok ». Added to batch-05, automatable (the Driver works from the request alone).
   The generator question got no explicit keep/remove answer: the Driver brings it back as a
   question before removing `just orchestrator` and `scripts/generate_orchestrator.py`.
2. agents-changes-refs-Q2: **Keep or remove the `just orchestrator` generator?** Owner,
   2026-11-17: « Remove it ». Remove the `orchestrator` recipe from the justfile and
   `scripts/generate_orchestrator.py` in this CR's PR (chantier keeps the batch state now).

## 2026-11-17: answer to the blocked hand-back

3. agents-changes-refs-Q3: **Long gate red on Windows on the pre-existing tableBreakout test.**
   Asked: waive CR-338's long gate (CR-339 already fixes that test), or hold CR-338 until CR-339
   merges. Owner: « Passer outre ». Long gate waived for this CR; its follow-up is CR-339, no new
   CR.
