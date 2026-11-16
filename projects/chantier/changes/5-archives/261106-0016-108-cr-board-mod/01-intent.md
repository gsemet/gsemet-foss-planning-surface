# CR board mod

The user wants to see the state of the change requests without leaving the conversation, in a
read-only pane beside the chat, when working with chantier in Claude Code. It must do better than
the board of chantier's predecessor, a generated Markdown table: that one showed a raw HTML
comment, said nothing about what waits for the user, let the backlog drown the page, had no landed
or dropped CRs, no budget or cost, and no detail on a CR.

The request came from that predecessor, so two names in it do not exist here: `STATE.md` is
`STATUS.md`, and `just orchestrator` is the CLI, which writes the `STATUS` files. `/chantier` is
already the Chief of Staff's skill, so it cannot also close the pane. `3-requests/STATUS.json`
holds only open batches and the backlog, so the CLI must extend it for landed and dropped CRs.

The work has two parts: the index in the CLI, and a mod shipped in the plugin.
