# TUI: resize three columns with the mouse and keep the widths

Asked by the owner, 2026-11-27, to the Chief of Staff, for the batch being opened. Verbatim: « fait un batch stack et rajoute la CR du TUI qui elargie les colonnes je ne sais pas ou elle est », then, with a screenshot of `chantier live`:

> les 3 colonnes a redimensionner en screenshot
>
> * gauche: 50% plus large
> * dans la zone principale
>    * project: x2
>    * who: x1.5
> *
>
> la CR etait de rajouter de pouvoir redimensionner les 3 colonnes principale avec la souris et de garder la taille dans un json (utilise la lib platformdirs pour connaitre le dossier user config)

The screenshot is not attached (it shows the home folder). It frames in red three columns whose texts are cut: the left column (the Projects and Agents boxes), and the Project and Who columns of the Flow table. No earlier change request for this was found in the planning surface, so this one is new.

## Wanted

1. Wider default widths: the left column 50 % wider, the Flow's Project column twice as wide, its Who column 1.5 times as wide. Today: `LEFT_W = 28` in `clients/tui/parts.py`; `PROJECT_W = 10` (12 with several boards) and `WHO_W = 10` in `clients/tui/screen.py`.
2. The user resizes these three columns with the mouse.
3. The sizes are kept in a JSON file in the user's configuration folder, found with the `platformdirs` library (a new dependency).

Chief of Staff's reading, to confirm by the owner: the three columns are the three framed in the screenshot. The last bullet of the owner's list is empty.

## To settle in the specification

- `AGENTS.md` says that `live` writes nothing, and lists every place chantier writes: this change alters that rule and updates it.
- `profiles.json` already lives in `config_dir()` (`clients/profiles.py`: `$CHANTIER_CONFIG_HOME`, else `%APPDATA%/chantier` on Windows, else `$XDG_CONFIG_HOME/chantier`, else `~/.config/chantier`). The default folder of `platformdirs` can differ from it: one folder or two, and whether `CHANTIER_CONFIG_HOME` still applies.
- `RIGHT_W = 44` and the left column shows from 100 terminal columns (`NARROW`): with a wider left column the Flow gets very little room on a narrow terminal. Say what gives way.
- `blessed` 1.53.0, already a dependency, exposes mouse support (`Terminal.does_mouse`, `mouse_enabled`); it was not tried in a Windows terminal. Prove it; no fallback.
- The keys keep working as today.

Proof: tests of the widths and of the JSON file's read and write; a screenshot of the real terminal showing no home folder.
