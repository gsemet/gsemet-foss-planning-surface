# Timing and retry settings in the configuration, per model family and host

Filed 2026-11-16 from the user's words (French, translated): put in the configuration, like the
models, the settings that tune the loops' waits and the like. The most important is the prompt
cache's TTL, which can differ by model family and by coding agent (host): Claude models have a
5-minute TTL in subagents; in sessions it seems to be 30 minutes or 1 hour, hard to tell. So the
configuration needs a way to say "wake the Foreman every X"; the same for the retry maximums, and
so on. Show them all in the configuration (the web board's Configuration page), each overridable
by the configuration.

Relates to CR-299 (configuration in layers, shipped defaults), CR-300 (a model per role on each
host) and CR-301 (the board's Configuration page). Priority: P1, the user's word.
