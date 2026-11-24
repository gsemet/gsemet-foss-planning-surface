# Role cards still too big for a Driver's context

Role cards are still too big for a Driver's context (from the Markdown Studio batch-08 retro, 2026-11-22).

Owner's word: the cards are still too big. Check first that it still holds on current main: chantier changed a lot since.

What happened (Markdown Studio release v1.12.0, plugin 0.14.0 label, main around 687a4723): one release needed three release-drivers. The first reached about 129k tokens in about 4 minutes, mostly reading driver.md in large ranges, the project's release guideline (about 21k characters) and PNG captures, then handed back `blocked context:` as the card says. The second waited with Monitor + sleep and was cut by the host with no `chantier handback` event. The third polled in the foreground with sleep loops and finished.

Leads: smaller per-role cards (or sections read on demand), the Release driver section pointing to the typed `pipeline` wait for a long heavy run on main, waiting only with a background shell (Monitor is not proven to keep a subagent alive), and reading a project guideline by section.
