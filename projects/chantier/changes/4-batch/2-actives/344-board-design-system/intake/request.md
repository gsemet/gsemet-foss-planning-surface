# The board's design rules are written down once and every page follows them

Replaces `board-design-realign` (abandoned, 2026-11-17). The user: "I don't want to realign
EVERYTHING, discard it. I want to fix the horrors that were put in recently":

- the task cards are not consistent from one page to the next;
- the left border with a curve: it should be FORBIDDEN;
- the Triage and Kanban columns are not the same.

And: "the fact that the designer wanted to remove the ticket means the design rules and the
important features are not encoded in a markdown base." The user wants the design rules (and the
features that must not be lost, such as the Costs page's paper ticket) written in Markdown, so
that changing a design rule updates every page automatically, with the CSS refactored as much as
possible (tokens and shared components, pages only lay them out).

The UX QA of the abandoned CR (`intake/ux-qa.md` and its screenshots) is kept here as reference.