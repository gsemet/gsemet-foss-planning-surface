# The watcher starts on its own with a running batch

On 2026-11-18 the Chief of Staff opened batch-28 and did not start the watcher, though its card
says to start it "once the batch runs (Starting a batch, after `open`)". The user noticed it. When
started by hand, it was given a `--batch` flag that `watch` does not take, and it failed. The rule
lives only in a long card section; nothing in the CLI's output at the moment that matters names
the step.

Wanted: the watcher's start does not depend on the Chief of Staff remembering a card paragraph.
At each moment the card names (after `open`, when a paused batch runs again, at a session start or
a reload with a running batch, after a switch to direct mode), the CLI's own output names the
exact command to start in the background when no watcher of this project runs, and the cards make
that line a step the Chief of Staff does at once.

Source: the user, 2026-11-18: « Ah il faut un déclencheur automatique du watcher. Il faut le
spécifier ? »
Short name: `watcher-autostart`
