# Answers: boot mode by surface, README rework and the board's docs

Grill of 2026-11-12. The user's word that day: "fait toutes les P1 et P2 en terminant sur la
release. pour la plupart je ne pourrais pas te repondre, utilise un advisor Fable. demande moi
uniquement quand il y a un impact utilisateur". The advisor answers in the user's place; the
questions with user impact are under "Open for the user", each with a recommendation, not decided.

## The mode

- Q: How is "remote" told from "local"? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): by the host's own signal only, the Remote Control notice in the conversation (`hosts/claude-code.md`, "Surfaces and options"); no notice means local. It is the one signal proved in use, and a missing notice fails safe: Foreman mode is chosen, and where no Foreman can start the existing rule of the plan applies.
- Q: When is the surface read: at the invocation, or when a batch starts? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): at the plan of each batch, and the introduction says which mode the session would use now. The known path to a remote Chief of Staff is "start locally, then turn on Remote Control"; a mode frozen at the invocation would make that session a Foreman one, the opposite of the request.
- Q: Does a forced argument hold for the whole session? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes, `foreman` or `direct` holds for every batch of the session until the user's word changes it; the user's word ("you are in direct mode", "use a Foreman") keeps working with or without an argument. This is today's rule for `direct`, extended to `foreman`.
- Q: What does a forced `foreman` do where no Foreman can start (Remote Control with no Foreman to reuse, a terminal)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): it is refused at the plan with the reason and what the user can do (say "direct", or start from the desktop); under Remote Control with a Foreman to reuse, it reuses it. The project's rule is no fallback: a forced mode is never swapped silently.
- Q: Is `direct` still allowed locally? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes, unchanged. Small batches and the `real-direct` eval rely on it.
- Q: Does a running batch change mode when the user changes surface (goes to the phone, comes back)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no. A batch keeps the steering it was opened with; "Switching to Foreman mode" stays the user's word, and a Foreman batch does not become direct. A Foreman batch followed from the phone already works (orders to the Foreman).
- Q: How is the argument read when a request follows it (`/chantier:chief-of-staff direct Run the campaign …`)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): the first word alone, when it is exactly `foreman` or `direct`; anything else is the user's request and forces nothing. The eval runbooks already use this form.
- Q: What about a cloud session and Copilot? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): unchanged. A cloud session has no main checkout and stops at the start checks; on Copilot the no-argument mode follows what the host's reference already says (an SDK host starts a Foreman, an agent session is direct), and how Copilot passes `foreman` or `direct` stays marked unproved. The request names Remote Control only.
- Q: Does the CLI learn the surface or the aliases? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no. The CLI knows no role and no host signal; `open --direct` and `preflight --direct` stay the only switches, set by the Chief of Staff.
- Q: Do the eval runbooks change? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): `real-foreman` and `full` start with `foreman` forced, `real-direct` keeps `direct`. An eval must not depend on whether Remote Control happens to be on.

## The README and the docs

- Q: Is this one CR or two (the mode; the README and the board's docs)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): one, as the user filed it ("Met une CR"). The README's new "How chantier works" opening describes the new entry, so the two halves would conflict if run apart.
- Q: Are the user's English openings for "Planning modes" and "Batch modes" taken word for word? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): their content and order, in the README's plain English (grammar fixed, "Change Request" and "batch" as the README spells them). The user dictated a draft, not a final text.
- Q: Does the "Releases" example promise that chantier publishes to a marketplace or posts a thread? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no. It is written as an example of a project's own procedure that the Release Driver follows with the tools the session has, each irreversible step on the user's approval; "about ten minutes" for the VS Code marketplace is given as an order of size. The README must not claim a capability chantier does not ship.
- Q: Where do "What is chantier?" and "Repository layout" land in `CONTRIBUTING.md`? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): under "How the project is built", moved as they are, with their links fixed. The user asked for a move, not a rewrite; CR-195's "stays in the README" is reversed on the user's later word.
- Q: Does the README still say somewhere what the moved "What is chantier?" alone said (the CR's files, the grill, the spec-writer)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes, through the new "Planning modes" opening (intent, then Change Specification) and the tutorial link; nothing else is copied back. The user's opening covers it, and the move is the point.
- Q: Is the board's richer page a new page or `docs/boards.md`? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): `docs/boards.md`, enriched; the remote board keeps its section there. The README's "More" list and the cards already link that page.
- Q: Which screenshots go on the board's page, and where do the files live? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): the five board screenshots, in the order of a batch, copied under `docs/` beside the diagrams; the intake keeps its originals untouched. The user said each screenshot sent is for this documentation.
- Q: Does the page explain the two oddities the screenshots show? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes: "waiting for you" in the header counts the unread asks too, and the batch's cost moves when the steering session refreshes the status, not live. Both would otherwise read as bugs.
- Q: Does this CR wait for `board-refresh-button`, or the reverse? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): neither; no `depends.json`. Each documents the pane as it is at its merge, and the second to merge rebases its lines of `docs/boards.md`.
- Q: Do the diagrams change? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): only the entry named in the two simple diagrams and their `-texts.md` (no argument locally or `foreman`; no argument under Remote Control or `direct`). They are the target the docs follow and would otherwise contradict the README.
- Q: Is `direct-mode-session.png` published as sent? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes, whole. The user sent it to show the whole window (transcript, Background tasks, board); it shows nothing private beyond the public eval sandbox's name.
- Q: Which gates? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): `just check` and `just scenario` (the cards change); not `just mod` (nothing under `hooks/` or `types/`). This is `AGENTS.md`.

## Open for the user

1. **No argument where a Foreman cannot start, and the router.** Today, with no argument in a
   terminal, VS Code or under Remote Control, the plan *proposes* direct mode and waits for a yes;
   and `/chantier:chantier` asks three roles (Chief of Staff, Chief of Staff in direct mode,
   Griller).
   Recommended: no argument means "the mode this surface can run": Foreman at the desktop app's
   keyboard, direct under Remote Control and on every host that cannot start a Foreman (terminal,
   VS Code, a Copilot agent session). The plan says the mode and why in one line, with no separate
   question (the go is the yes). The router asks two roles only (Chief of Staff, Griller) and the
   mode follows the surface. Reason: one rule for every entry, one question fewer at each start;
   `foreman` and `direct` remain for whoever wants to force.
2. **The README's order and its pictures.** Recommended order: the bullets; How chantier works
   (opening on the one boot skill, then the two modes); Planning modes; Batch modes; Change
   Requests lifecycle; Detailed lifecycle; Releases; **The CR board** (new: `board-mod-batch.png`
   and the link to `docs/boards.md`); Install; Use; More; Develop.
   `direct-mode-session.png` goes in "How chantier works", under the direct-mode paragraph, with
   the line on the Griller session (the intake's summary says "Batch modes", but that section is
   about parallel, series and stack). `status-report-done.png` goes in the docs (the tutorial's
   status step and `docs/costs.md`), not in the README, which keeps two screenshots.

- Q: (open 1) No argument where a Foreman cannot start, and the router? — User (2026-11-12, "proposition validee"): the advisor's recommendation. No argument means the mode this surface can run: Foreman at the desktop keyboard, direct under Remote Control and on every host that cannot start a Foreman (terminal, VS Code, Copilot agent session). The plan says the mode and why in one line, no separate question; the go is the yes. The router asks two roles only (Chief of Staff, Griller).
- Q: (open 2) The README's order and pictures? — User (2026-11-12, "boot-mode-by-surface : ok"): the advisor's recommendation. Order: bullets; How chantier works (opening on the one boot skill); Planning modes; Batch modes; CR lifecycle; Detailed lifecycle; Releases; new "The CR board" (board-mod-batch.png and a link to docs/boards.md); Install; Use; More; Develop. direct-mode-session.png under the direct-mode paragraph of How chantier works, with the Griller line. status-report-done.png in the docs (the tutorial's status step and docs/costs.md), not the README. "What is chantier?" and "Repository layout" move to CONTRIBUTING's "How the project is built".
- Q: Copilot: which mode? — User (2026-11-12): Copilot can run a Foreman or direct; no eval yet, so no difference from Claude Code on this point: the spec's rule stands (a host that can start a session runs Foreman, else direct), to be validated later by an eval; no CR for it.
