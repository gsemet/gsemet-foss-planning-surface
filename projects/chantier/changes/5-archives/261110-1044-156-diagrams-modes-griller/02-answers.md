# Answers: diagrams-modes-griller

## Interactions with the other CRs (2026-11-10, the Chief of Staff, on the user's word "tu peux le mettre en dépendance des autres")

- `multi-session-chief-of-staff` (P1, carries the former `skill-entry-points`) creates the
  Griller role, the `/chantier:griller` skill and the two steering modes' wording; its intent
  listed "README and docs diagrams". This CR takes the SVG diagrams over: the multi-session
  spec-writer was told to leave `docs/*.svg` and the README's images out of its scope.
  `depends.json`: after `multi-session-chief-of-staff`, so the diagrams draw what that CR ships.
- `claude-code-config` and `pr-details-fold` touch no SVG: no dependency.
- `landing-page` and `docs-sphinx-rtd` (P2) reuse the diagrams later: no dependency.

## Grill (2026-11-10)

- **Priority:** P1 (recommended), right after `multi-session-chief-of-staff` in the same batch.
- **README:** both variants of the simple diagram, one under the other, **direct first, then Foreman** (the user chose this over the recommended Foreman first), each with one line saying when to pick it (direct: works in remote, grill in a Griller session; Foreman: nested session, at the desktop, natural interaction with the Chief of Staff).
- **Griller on the other diagrams:** wherever the Chief of Staff appears (both how-it-works, the CR lifecycle simple and detailed, the CR folder lifecycle), marked optional; not the batch lifecycle nor the batch pace. (Recommended.)

## Go (2026-11-10)

> Oui tu peux tout lancer

- Grilled enough, after the full restatement: specification by the spec-writer. The same word is the go for the batch of the four specified P1s (multi-session-chief-of-staff, claude-code-config, pr-details-fold, diagrams-modes-griller).

- **When it joins the batch** (2026-11-10): "La CR spécifié ne pourra être mise que lorsque toutes les autres CR seront traitées." The batch opens with the three other CRs; this one joins with `order add` once they are all handled and the batch is paused (a direct batch takes no CR while it runs).

## Scope widened: README, docs and the introduction (2026-11-10, after batch-09 paused)

User's words: "on va griller un peu diagrams-modes-griller, il y en a une autre sur le readme non ? on va merger et mettre a plomb le README, la doc et ce que dis chantier a l'intro."

- The inbox item `release-template-deliverables` is merged into this CR (its request is
  `intake/request-readme-intro.md`; the inbox folder went to `5-trash/`). This CR now also:
  points `release-template.md` at the PRs' Deliverables section, and sets the README, the docs and
  the Chief of Staff's first-turn introduction (`references/session-start.md` section 4) straight,
  keeping the important messages.
- The specification (`03-change-spec.md`) was written for the diagrams alone; it is rewritten
  after this grill. It no longer joins batch-09 as specified: the grill comes first.
- Messages the user wants, in their words:
  - "quand on explique le CR, il faut dire c'est un niveau d'abstraction supplémentaire au issues
    d'un tracker (jira, github, gitlab,...) qui permet d'accepter et prioritiser des petites
    requetes hors tracker" — a CR is one more level of abstraction over a tracker's issues (Jira,
    GitHub, GitLab…): it lets small requests outside the tracker be accepted and prioritised.
  - "tracker = vision strategique, demandes externes, planification long terme" — the tracker
    holds the strategic vision, external requests and long-term planning.
  - "Planning aera (in project .agents/changes) ou externe (le agentic planning)" — the planning
    area is either in the project (`.agents/changes/`) or external (the agentic planning surface).
- The user's planning surface was renamed https://github.com/gsemet/gsemet-foss-planning-surface
  and holds several empty projects to show the structure (`projects/<name>/project.md`,
  `checkout.yml`, `changes/1-inbox … 6-trash`). Also recorded in the P1 `planning-repo`, whose
  answers still name the old URL.

## Grill of the widened scope (2026-11-10)

- **External planning area:** "Ne pas en parler" (not the recommended "bientôt"). The README
  describes only the in-project planning area (`.agents/changes/`); the external surface is not
  mentioned. The P1 `planning-repo` adds it to the README when it ships (noted there).
- **Where the CR/tracker explanation goes:** "Section Change Requests" (not the recommended top
  of the README): it replaces the current paragraph "A Change Request is an idea, a bug…".
- **Messages the introduction keeps** (README and the Chief of Staff's first turn), all four:
  CR and tracker; one person to talk to (the Chief of Staff, nothing starts without the user's
  go, the user merges); direct or Foreman (the two modes and when a CR may join a running
  batch); zero configuration (`AGENTS.md` is the only configuration, everything is Markdown and
  JSON in `.agents/changes/`).

- **Grilled enough** (2026-11-10, after the full restatement): "oui lances". The spec-writer
  rewrites `03-change-spec.md` for the widened scope.

## The specification's open questions, and the README phrase (2026-11-10)

- **Review of the drawings:** in the PR, from PNG renders (recommended); the Griller's emoji (🔥 proposed) and the split box's band label are settled there. No prototype step first.
- **batch-lifecycle.svg's direct line:** "grill in another session of yours" becomes "grill in a Griller session", no box drawn, also in its `<desc>` and `batch-lifecycle-texts.md`: implementation wording, not asked (the user's rule: detail is the agents'); the recommendation stands.
- **A simple phrase in the README on the modes' difference.** User's words: "une fois le batch lancé en mode direct, on ne peut rajouter une CR spécifié ou non que lorsque toutes les autres CR seront traitées et que le batch sera passé en pause. C'est le genre de phase simple à faire apparaître dans le readme pour expliquer la différence entre mode direct et foreman." So the README, with the two simple diagrams, says in plain words: once a batch runs in direct mode, a CR (specified or not) joins only when all the others are handled and the batch is paused; in Foreman mode a CR may join while it runs (`order add`).
