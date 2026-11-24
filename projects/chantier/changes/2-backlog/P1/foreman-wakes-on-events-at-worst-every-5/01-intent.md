# Foreman wakes on events, at worst every 55 minutes

From the Markdown Studio batch-07 retro (2026-11-22) and the owner's word: with the surface
server and the watchers, the Foreman should wake on the batch's events (a merge, a red CI, a wait
met) that a watcher of its own carries, instead of having the Chief of Staff relay them, and on
its timer only as a safety net, at worst once every 55 minutes (under the 1-hour prompt cache).

Intent: give the Foreman its own watcher on the batch's forge events, move the Claude Code
steering wake's shipped default to 55 minutes, and rewrite the AGENTS.md rule that makes the
watcher the Chief of Staff's alone.
Short name: `foreman-wake`
