# Foreman wakes on events, at worst every 55 minutes

Foreman wakes on events, not on a timer (from the Markdown Studio batch-07 retro, 2026-11-22).

Owner's word: this changes soon. With the notification server and the watchers, the Foreman should no longer need to wake on a timer; at worst once every 55 minutes (to stay under the 1-hour cache TTL). Check whether it still holds when picked up.

Evidence: in batch-07 orchestration was half the spend ($118 of $236); the Foreman woke 336 times on its timer at about 180k tokens of context on average (267k peak). On main 687a4723 the steering wake defaults to 30 minutes, up to 60 (hosts/claude-code.md "Heartbeat"); the event watcher serves only the Chief of Staff in direct mode.
