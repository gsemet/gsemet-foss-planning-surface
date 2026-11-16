A CR's CI runs while its local long gate runs, so a failure on a system the local gate does not cover is seen early, in any project.

Generic form (the user, 2026-11-14: "ça peut rentrer dans chantier lui-même pour que les utilisateurs n'aient pas ces problèmes"): chantier cannot know each project's checks, but it knows the order of a Driver's steps. Today a Driver runs the local long gate first, then pushes, then reads CI; a CI matrix covering other systems (Linux, macOS when the user works on Windows) reports its failure only after the gate, costing a round and an hour.

What happened (batch-17, chantier's own repository): CR-221 had a mypy error invisible on Windows (a Windows-only constant), CR-222 a socket never `listen()`ed (Windows retries, Linux refuses at once); each CI red came after a 35-minute local gate and cost one or two more rounds.

Wanted:
- the Driver pushes the round's commit (draft PR) as soon as the Inspector approves it, and runs the local long gate while CI runs; a red CI job stops the gate (`gate --stop`) and goes to the Debugger at once;
- the Driver reads the CI matrix and names, in the PR's Known gaps, the systems only CI covers;
- for chantier's own repository (a project item, not a chantier rule): `just check` also runs mypy with `--platform linux` and `--platform darwin`.
## After the critic's review (Fable, 2026-11-14)

Renamed from gate-cross-platform-mypy: the mypy half is chantier's own repository's item. The generic change contradicts rules it must rewrite: `driver.md:112` ("the long gate… before any PR"), `driver.md:168`, and the push refusal "no long gate passed" (`driver.md:293`). It spends CI minutes: the project chooses it (`chantier.yaml`), off by default.