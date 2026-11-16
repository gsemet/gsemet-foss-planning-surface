# A planning surface stays in sync through its own autosync

## What is wrong

With an external planning surface, the Chief of Staff commits and pushes the surface by hand
after each step that changes it and at each hand-back (`chief-of-staff.md`, "With a planning
surface"). That costs turns, is easy to forget, and leaves the surface behind while a batch runs:
the Foreman, a Griller and the Chief of Staff all write in it.

A surface may already ship its own autosync. The user's surface `gsemet-foss-planning-surface`
does: `scripts/ai-autosync-git.py` with `.agents/guidelines/autosync.guidelines.md`, named first in
its `AGENTS.md`.

How that autosync works:
- every agent session in the checkout joins one group (`join . --owner-pid <host pid>`, detached);
- a file lock in `.git/ai-autosync/` elects one leader, which commits after 10 s of quiet (30 s at
  most), fetches, scans for secrets with Gitleaks, pushes LFS objects and pushes;
- when upstream moved, it never rebases on its own: it disables the group with a `blocked:`
  reason, and an agent integrates and runs `start . --enable-only`;
- staged changes or a found secret need the user's approval (`approve . <incident>`), never an
  agent's;
- `start`, `stop` and `sync` apply to the whole group; `status` prints the control state, the
  leader and the participants as JSON.

## The solution (the user's choice, 2026-11-13: "option A")

chantier does not own an autosync: the surface does, and chantier uses it.

1. **Cards.** When the surface's rules name an autosync (its `AGENTS.md` or what it links), every
   chantier session that runs in the surface joins its group at session start, by the surface's
   own guideline: the Chief of Staff, the Foreman, a Griller. Drivers work in the code's worktrees
   and do not join. A Griller working in a surface worktree joins nothing (already in
   `griller.md`). While the group is enabled, the session does not commit or push the surface by
   hand.
2. **A `blocked:` group.** The Chief of Staff handles it: upstream moved → integrate (no discarded
   change, never a force push), then `start . --enable-only`; an approval needed → show the user
   the incident and wait for their word, never approve for them. The Foreman that meets it tells
   the Chief of Staff.
3. **Read-only checks in the CLI.** The CLI still runs no git that changes anything and has no
   dependency:
   - `preflight`: a surface whose rules name an autosync but whose group has no live participant
     (or is `blocked:`) is a warning that names it;
   - `status`: one line with the autosync state when the surface has one, read from
     `.git/ai-autosync/status.json` and `control.json`.
4. The user says "start autosync" / "stop autosync": the Chief of Staff runs the surface's own
   commands; chantier adds no command of its own.

## Out of scope

- An autosync for the project's code repository.
- Porting the autosync into chantier's CLI, or a CLI command that wraps it (no dependency, no git
  write: `AGENTS.md`).
- A surface with no autosync keeps today's rule (commit and push after each step).
