When the user's Claude Code settings lack the allow rules chantier's agents need, the Chief of Staff asks the user whether to add them, instead of only showing the block.

The user (2026-11-13): "fait une revue générale de ces règles et dis-moi lesquelles on garde, lesquelles on peut enlever, puis tu les mets chez moi et tu t'arranges pour que quand l'utilisateur ne les a pas, le chief of staff pose la question de les rajouter".

What happened in batch-17: preflight's P10 warned "14 of 16 commands … are not allowed" at the batch's start; the warn was not put to the user as a question, so the Drivers' force pushes after each rebase (`git -C <worktree> push --force-with-lease …`) were refused by auto mode's classifier and went Driver → Foreman → Chief of Staff, and one Driver ran out while it waited.

The review (2026-11-13, agreed with the user):
- Keep: the five `git push` forms on `chantier/*`, `uv run --script *chantier.py *`, `gh pr create|edit|ready|checks|view`, `gh stack*` (gh-stack may be installed), the four `glab` MR/CI rules, `SendMessage`.
- Remove from the recommended set: `gh release create*` and `glab release create*`. A release is rare and irreversible; the release driver asks the user before it anyway (`release go`), so leaving it to the host's prompt costs nothing and keeps one more guard. P10 then checks 15 commands on GitHub. Changes `commands.py` (`_SAMPLES`), the "Allow rules" table and block of `hosts/claude-code.md`, the "release's publication" line of `chief-of-staff.md` ("Forge permissions"), and the structure test that compares them.

Open points for the grill:
- Who writes the rules on the user's yes. `AGENTS.md` says chantier writes only in the planning folder, and `hosts/claude-code.md` says "chantier never writes the user's settings: preflight's P10 compares, the user adds". Either the Chief of Staff writes `~/.claude/settings.json` on the user's yes (an exception to that rule, written in `AGENTS.md`; auto mode's classifier refused such an edit once on 2026-11-13, then accepted it at the user's explicit word), or it asks and, on the yes, gives the exact block and where to paste it.
- When: at the first turn of a session (where P10 already runs) and at each batch's preflight, once per session.
- Runs after CR-221 (python-inline-deps): it touches the CLI.
