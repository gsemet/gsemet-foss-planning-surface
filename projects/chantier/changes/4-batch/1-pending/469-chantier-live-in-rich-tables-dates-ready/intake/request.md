# chantier live in Rich: tables, dates, Ready and Agents boxes

Filed on the owner's words of 2026-11-23, relayed by the Chief of Staff of okf-schema. To grill later with the owner, not now.

The owner's words (French), after running `chantier live`: "il est en ASCII. Fait une nouvelle CR pour Chantier: je le voudrais en rich avec de jolis tables. Les lignes des evenements sont comme ca: `14:27:23 chantier   driver     note CR-296 worktree created at 5eb0c1e (origin/main); investigator starts`. Il faut rajouter la date a cote de l'heure. Rajoute aussi un hotkey pour switcher ces dates en temps depuis l'evenement (46s = 46 secondes apres, utilise une formulation claire "2 min", "1h", ... arrondi, pas la peine d'etre tres precis). Niveau organisation de la page: haut a gauche: aujourd'hui "Projects", c'est ok. En bas rajoute "Agents" (aujourd'hui il semble dans les Projects), a mettre dans sa propre boite; par contre la valeur aujourd'hui c'est `none` alors que c'est les agents actifs a afficher, verifie qu'il n'y ait pas de bug. Zone principale: Flow, ok. Droite: 2 blocs: Tasks, et au-dessus "Ready", la liste des PR ou MR pretes a revoir ou a merger; si possible afficher l'etat de chacune (en reprenant le code couleur de la board) et un lien cliquable si c'est possible."

In short: rework the terminal client `chantier live` (`clients/tui/`) with the Rich library: real tables and boxes instead of the drawn ASCII frames, and a new layout.

Wanted:

- **Rich rendering.** Tables with proper columns and colours; `--once` keeps printing a plain-text screen for tests and bug reports.
- **Flow, the date.** Each event line shows its date next to its time (the lines now show the time only, so an event of another day looks like today's).
- **Flow, a hotkey.** One key switches the time column between the clock (date and time) and the time since the event, in a plain rounded form: "46 s", "2 min", "1 h", "3 days"; no need to be precise.
- **Layout.** Top left: Projects, as today. Below it: Agents, in its own box (today it sits inside the Projects box). Centre: Flow, as today. Right: two boxes, Ready above (the PRs or MRs ready for review or to merge, each with its state in the board's colour code and a clickable link where the terminal can make one, e.g. an OSC 8 hyperlink), Tasks below.

To check at the grill (observed 2026-11-23 on a surface with several projects):

- **Agents says `none` while a batch runs.** At 12:26 local, `live --once` showed `Agents none` with chantier's batch-20 running; `preflight` P14 reported "batch-20 running, steering direct, 0 Drivers", so `none` may be right (no Driver at that moment) and not a bug. The grill settles what "Agents" must list (Drivers, workers, the Foreman, the Chief of Staff's session) and checks it against a batch that has live Drivers.
- **Event times look ahead of the clock.** The header said `11:26:25 UTC` (12:26 local) while the last Flow lines read 16:20 and 15:xx. Either the events are of another day (the date to add would show it) or the Flow's times are not in the header's zone; check which, and show the zone or convert.
- **The Ready box's source.** The board's PRs page already reads the forge for the running batch's PRs; the server's API must give the TUI that list and the state colours, with no `gh` or `glab` call in the client (a forge-neutral API, one client of the server's published API, `docs/server-api.md`).
- Rich is a new dependency of the CLI: check the `uv`/`uvx` launch and the package's dependency rules.
