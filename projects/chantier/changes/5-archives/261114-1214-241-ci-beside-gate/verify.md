# Verify CR-241

Head: 5d4e83102343f07478cc389ccea5b340389c4655

Scratch projects (git repo plus bare origin; HOME, USERPROFILE and CLAUDE_CONFIG_DIR in scratch folders). Base = a worktree of origin/main (4d9075f); it differs from the PR's base only by other CRs.

- E3, output unchanged when off, at 5d4e831: `open`, `playbook`, `playbook --batch`, `take`, `handoff` with no chantier.yaml, base vs head, paths normalised. Compare-Object shows no difference (65 lines each). Files: evidence/E3-base-noyaml.txt, evidence/E3-head-noyaml.txt.
- Key on, at 5d4e831: evidence/E3-head-ciOn.txt has `ci: beside the long gate (chantier.yaml): push at the approved round, run the long gate while CI runs` in playbook, playbook --batch, take and handoff. brief.md holds `- CI beside the long gate: on (chantier.yaml).`. batch.json playbook = `{"file":"chantier.yaml","host":"claude","roles":{},"ci":{"beside_gate":true}}`.
- `beside_gate: false`: `playbook` prints no ci line (checked, at 5d4e831).
- Refusals at 5d4e831: `ci: true` gives `chantier.yaml:1: "ci" holds its keys: ...`; `colour: red` gives `ci: unknown key "colour": one of beside_gate`; `maybe` gives `"beside_gate" is true or false, found "maybe"`; `foo: 1` gives the top-level keys "roles", "prices", "board" and "ci". All "chantier.yaml is not valid".
- The previous code refuses the key (`unknown key "ci"`): evidence/E-base-ci-key.txt.
- E4, at 5d4e831: git diff of driver.md, chief-of-staff.md and concepts.md read. Every driver.md edit is qualified by the `ci: beside the long gate` line (Context, long gate bullet, ship, CI bullet, round sequence, `rebase: merged` path, force-push exception, Known gaps); chief-of-staff.md has step 2 and the routing row. No unqualified sentence changed. (rg is not installed in this environment; the diff was read.)
- E5, at 5d4e831: the CI bullet carries "Unproved; trial: a CR Driver of a batch with the line pushes at the approved round, runs its gate while CI runs, and on a red CI job stops its gate and starts a debugger before the gate ends."
- Not run: E1 CI and E2 `just scenario` (waived by the user for this batch). Section 17b cannot run alone (run_scenario.py takes only --forge, --keep, --verbose). Gap.
- The PR description was not judged (outside my brief).

VERIFIED
