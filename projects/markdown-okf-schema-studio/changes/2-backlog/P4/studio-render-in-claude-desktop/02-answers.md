# Decisions

## 2026-10-31 — target

- The target is **Claude desktop's file pane**, not VS Code. The VS Code variant ("open `.md` in the
  Studio custom editor by default") was grilled first by mistake; its answers are kept below in case
  it becomes its own backlog item. They do not apply to this item.
- Development goes through the project's Chief Of Staff session ("Projet: Markdown OKF-Schema
  Studio [CoS]") once the user triggers it. Not before.

## 2026-10-31 — integration, not re-implementation

- No re-implementation of the renderer: Studio itself, integrated as in VS Code (its page in a
  panel, with its host bridge). If Claude desktop cannot host it, the item is **blocked**.
- Trigger: a click on a `.md` in the conversation or in Claude desktop's file browser.
- File the extension-point request with Anthropic in parallel (draft in `01-intent.md`; the user
  sends it).
- Packaging once unblocked: in the repository's Claude plugin, built from the same `src/`.
- Verified against the 2.1.309 mod API: no file-open event, no webview/HTML element. Status:
  blocked.

## VS Code variant (on hold, not this item)

- Option: documentation + commands "Use Studio as default" / "Restore text editor", then a fallback
  to the text editor for `git:`, `untitled:` and diff sides, in two PRs.
- Scope of the written association: a quick pick, user scope first.
- Restricted Mode: open Studio read-only.
- No "Always open in Studio?" prompt after the first Open With.
- Requirement: extend SwRS-MDOKFSTUDIO-LIFE-018 itself (no new SwRS).
- "Restore" removes only Studio's `*.md` entry.
- Diff views: not decided (the question was interrupted by the change of target).
