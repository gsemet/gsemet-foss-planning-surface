# Answers

No grill held: the user delegated tonight's spec questions to a Fable advisor ("plus de question", 2026-11-21).

getting-started-Q1 (2026-11-21, Fable advisor): **Where the guide lives: a new page `docs/getting-started-surface.md` (A).** One walk in one place; `docs/planning-modes.md`'s "Setting one up" becomes a link, and the page is not tied to one host.
getting-started-Q2 (2026-11-21, Fable advisor): **Part 2 with the guide, in this one CR (A).** The request is one item and says the guide shows the three sources; a guide shipped first would be rewritten.
getting-started-Q3 (2026-11-21, Fable advisor): **Where the branch is stated: the surface root's `chantier.yaml`, `surface: branch: <name>`, refused in any other `chantier.yaml` (A).** The CLI already reads and checks that file and reads no `AGENTS.md` line.
getting-started-Q4 (2026-11-21, Fable advisor): **When sources disagree: the first set wins, in the order stated, `origin/HEAD`, upstream (A).** The statement is the user's own explicit word for this surface; the message names the source used.
getting-started-Q5 (2026-11-21, Fable advisor): **The tracked branch: only when the checked-out branch's upstream is on `origin` and has the same name as the local branch (B).** Under A a local `plan` tracking `origin/main` leaves two candidate names, a guess CR-404 forbids; the guide's `git push -u origin <branch>` gives exactly the accepted case.
getting-started-Q6 (2026-11-21, Fable advisor): **Preflight's P11 follows the same resolution and names its source (A).** One function: P11 and the writer cannot disagree about the surface's branch.
Destination (2026-11-21, Fable advisor): waits; specified and filed in `2-backlog/P3` for a batch after batch-30. The page quotes behaviour batch-30 has not merged (CR-436's plugin-mode rule), part 2 changes how the writer picks the branch while that writer publishes batch-30's surface from live code, and the user marked it "later".

Spec final (2026-11-21, the Chief of Staff): v2, getting-started-Q1..Q6 applied (Fable advisor); destination 2-backlog/P3, for a batch after batch-30.

# Decision (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is cancelled: it is kept for reference in `work/spec-before-rework.md`, and is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32. Replaces the earlier destination.
