A session whose chantier CLI cannot start must stop at once, in every mode and every role.

Seen 2026-11-17 (owner's screenshot): a session wrote "chantier's CLI won't start here and its packages can't be fetched, so I'm proceeding without it" and went on reading an XState v6 post. Owner: « non si le CLI ne peut pas être lancé il faut arrêter tout de suite ».

Today the stop rule ("role initialization stops; no upgrade, repair, substitute, or alternative route") covers only the dev mode's `uv sync` failure. The plugin mode (`uvx --from <plugin root>`) and any later CLI failure (a fetch refused, a sandbox without network, a cloud session) have no such rule, and the general "a tool a role lacks is not a stop: work without it" lines read as permission to go on.

Make it one rule in the startup core of every role (skills/*/SKILL.md and the references they load): if `$CHANTIER` cannot run, in either mode, the session reports the exact error and stops; it does no work as that role, takes no seat, writes nothing in the planning folder, and never goes on "without it". Exclude the CLI explicitly from the "work without a missing tool" lines.
