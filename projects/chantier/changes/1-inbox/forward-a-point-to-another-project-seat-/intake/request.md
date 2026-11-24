# Forward a point to another project: seat, inbox or forge ticket


## Problem

The Chief of Staff card ("The chantier route", in chief-of-staff.md) sends every point for another project to a forge issue. Inside one planning surface that is the wrong route: in batch-09 the Chief of Staff drafted six GitHub issues for chantier points, while chantier lives in the same surface. The owner's rule has three cases:

- outside the surface: a ticket on the forge;
- inside the same surface, when the target project's session is found: send to it directly;
- otherwise: the target's inbox in the surface (a git file).

## Proposed fix

1. One cross-project route in the card, three cases tried in order:
   - same surface, a live Chief of Staff seat for the target: message it; it files the item with `file` and answers the slug. A live Foreman alone is not a target: use the inbox.
   - same surface, no seat: an inbox item through the CLI (`file --project <target>`, then commit and push), never a hand-written folder.
   - outside the surface: a forge issue, with the current steps (draft, privacy check, the owner's yes per issue).
2. The decision in the CLI: `$CHANTIER forward <point-file> --to <project>` prints the route that applies ("send to seat <id>", "filed 1-inbox/<slug>", or "issue draft at <path>"). It needs `seat --project <target>` to show the target's Chief of Staff seat.
3. Rules per route:
   - inside the surface, the owner's word on the retro point is enough, with no per-point yes; the forge keeps its per-issue yes;
   - the privacy check follows the target's visibility (public surface or public repository), not the route;
   - the duplicate check reads the target's inbox and backlog inside the surface, its open issues outside.
4. A record: a `forwarded: <project> <slug | issue link>` line on the retro point (the card says "No record" today).
5. A tag check: the retro-critic checks each point's [chantier] or [project] tag against where the cited file or command lives. In batch-09 a point on a script of the project's own repository was tagged [chantier].

The owner approved this design on 2026-11-24 ("bonne idee") and said they will make the CR.

From the markdown-okf-schema-studio batch-09 retro (2026-11-24), chantier 0.15.1.
