# The board's toggle says when a Remote Control view will not show it

The user, on a Mac following a Windows session through Remote Control: "je vois bien le message de
chantier. fait une CR pour dire au toggle du board que l'utilisateur est sur une session remote, et
que les mod ne suivent pas. recherche sur internet si c'est le cas et s'il y a un bug ouvert dessus".

What happened: `/chantier-board` typed from the Mac ran and replied "CR board opened.", and no pane
appeared on the Mac. Closing and reopening gave the same. The reply is true on the host and misleading
in the view the user reads.

What the research found:

- It is documented: in "Where mods run", Remote Control runs a mod's hooks "in the session on your
  machine", and what it draws appears "in the terminal on your machine".
  https://code.claude.com/docs/en/plugins/mods/overview.md
- The same page says a mod that draws can fall back to "a command's text reply where nothing draws".
- The Remote Control page's limitations do not mention mods.
  https://code.claude.com/docs/en/remote-control
- Open issues in anthropics/claude-code: 99217 (our symptom: the command runs from the viewer,
  `$.session.surfaces()` returns `["terminal"]`, `$.ui.open` says `isPlaced: true`, the pane draws on
  the host only, no `session.attach`, `$.ui.status` does not reach the viewers), 105772, 106948,
  101313, 103763.

What a mod can read: `isPlaced` and `surfaces()` cannot tell (99217). `command.run`'s input carries
`origin`, whose `{ kind: 'bridge' }` is "the user's message through the Remote Control bridge (a
phone or web client)". Not proved yet on a session the desktop app hosts.
