# Spec-writers and slots set from the board's configuration

On 2026-11-18 the Chief of Staff ran about seven spec-writers at once, with no limit but its own
judgment, while batch-28 ran with 4 slots set once at `open`. The user wants both numbers in the
project's configuration, editable from the web board's Configuration page, and a change to them
to reach the Chief of Staff at once.

Wanted:
- A configuration key for the most spec-writers the Chief of Staff (or a Griller) runs at once,
  default 4, read by the cards before a spec-writer starts.
- The batch slots in the configuration too (the default `open` uses), editable from the same page.
- A change made on the Configuration page writes an event the watcher reads, so the Chief of Staff
  wakes and acts on it (for the slots of a running batch: `order slots`; for the spec-writers:
  start more, or let the running ones end before starting a new one).

Source: the user, 2026-11-18: « Alors mets ça aussi en configuration, max parallel spec-writer.
Default: 4. Il faudrait que ces slots et max spec-writer soient configurables dans la page config
et qu'un événement soit déclenché pour réveiller le watcher sur cet événement. »
Short name: `config-spec-writers-slots`
