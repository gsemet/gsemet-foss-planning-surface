The planning surface (https://github.com/gsemet/gsemet-foss-planning-surface) launches chantier's board and sync with no agent.

The user (2026-11-13): "le script de synchro (dossier scripts) sera remplacé par des commandes chantier, il faudra un moyen de lancer le backend directement sans nécessairement avoir de chief of staff (fonctionnement hors agent)".

Decided with CR-237 (root-pyproject-launch): one launch method, `uvx --from <source> chantier`; a launch with no agent uses `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier`, the version pinned where that launch lives.

So, in the surface's repository (not chantier's):
- `just board`: runs `chantier board` at the pinned version, with the surface as its planning folder;
- `just sync`: runs chantier's sync commands at the same pinned version, in place of `scripts/ai-autosync-git.py` and `.agents/autosync.toml`;
- one place holds the pinned version, bumped by hand or by a recipe;
- optionally, an autostart (a scheduled task, a service) so the board and the sync run with no session open.

Runs after CR-237, CR-222 (visualization-backend) and CR-227 (surface-autosync); it goes with the read-only audit `surface-transition-audit` (inbox), which lists what breaks first. The change lands in the surface's repository.
