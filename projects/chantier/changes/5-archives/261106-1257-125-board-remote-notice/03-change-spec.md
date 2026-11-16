# The board's toggle says where the pane is

## Problem

`/chantier-board` typed from a Remote Control view runs and replies "CR board opened.", and nothing
appears in that view: a mod draws on the machine running the session only. The reply is true on the
host and misleading in the view. A mod cannot tell which of the two the user reads from: `isPlaced`
and `$.session.surfaces()` answer as if the pane were placed (anthropics/claude-code#99217).

Typed during a turn, the command does not run: it reaches the session as text.

## Change

- In `hooks/register.tsx`, the toggle's reply on opening becomes, every time and with no detection:
  "CR board opened on the machine running this session; a Remote Control view does not show it."
- The replies "CR board closed." and "The CR board could not be placed here." stay.
- The toggle opens and closes the pane as it does today, wherever the command came from.
- `$.command.register` gets `immediate: true`, so that the toggle also runs during a turn. Its
  `command.run` hook assumes nothing of the turn's state.
- `hooks/register.test.tsx` follows the new reply.
- The README's section "The CR board (Claude Code)" gets one sentence: the pane shows on the machine
  running the session, not in a Remote Control view, with a link to
  https://github.com/anthropics/claude-code/issues/99217.

## Out of scope

Showing the board's content in a Remote Control view, as text or otherwise. Any detection of the
view. The pane that the `chantier` skill opens by itself says nothing: only the command replies.

## Done when

- The reply and the registration are as above, and the test passes.
- `just check` passes.
- Not provable by an agent, left to the user: from a Remote Control view, the reply reads as above,
  and the command runs during a turn.
