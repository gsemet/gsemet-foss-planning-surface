# Excerpts: the Chief of Staff and the user, batch-27 (translated from French)

**User:** I merged, but the watcher did not work.

**Chief of Staff:** The hub did see the four merges (15:17:33 and 15:17:53), and the watcher ended
at about 15:18:13 with its four `forge saw merged` lines. Your message arrived about ten seconds
earlier: the watcher waits 20 s with no new event, so several merges wake the session once. I
verified the four merges on the forge, recorded `order merged` for each, relayed them to the
Foreman, and restarted the watcher with `--after 6`.

**Chief of Staff (woken by the watcher, nobody typing):** CR-364 is merged (15:28:38Z). The
watcher saw it, ended on its own and woke me at about 15:29:05, some 27 s later. Verified on the
forge, `order merged CR-364` recorded: batch-27 is complete, 7 merged, $14.48 of $60.

**User:** Make a release with no evals.
