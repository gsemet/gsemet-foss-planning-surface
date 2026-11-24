# Web board: menu, detail overlay, multi-project home, History

Web board: remove the Kanban page, rename and reorder the menu, hide the detail page's Grill button, dim the page behind a detail, and give the multi-project home an activity feed, a list of open PRs and a History page.

From the user, 2026-11-24, looking at the web board (clients/web/). Seven changes, to be grilled before specifying:

1. Remove the Kanban page: it is of no use.
2. Rename the menu's "Inbox": it confuses with the inbox folder. The user proposes "Notifications".
3. Move "Help" to the very bottom of the menu, after "Configuration".
4. Hide the Grill button of the detail page for now: it does not work. (Hidden, not removed: the board's Griller stays in the server.)
5. When a detail page is open, grey out the rest of the page; a click on the greyed part closes the detail.
6. On the main home page (multi-project): show an activity feed across all projects, and a list of the open PRs (to review and to merge).
7. Add a History page at the root, to follow all projects.

Notes: a change under `clients/web/` reads its `DESIGN.md` first and keeps it true (AGENTS.md). Open points for the grill: what "Notifications" holds beyond the rename; what the open-PR list reads (the forge hub's data, which already covers a running batch's PRs only); what the feed and the History page show and keep; whether the Grill button's hiding is a flag or a removal.
