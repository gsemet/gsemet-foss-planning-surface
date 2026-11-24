## 2026-11-24 — batch-09 (CR-467 to CR-479, release v1.12.1)

- [chantier] `asks`, `stack`, `note` and `order done` disagree on `--epoch`; a refused `note --epoch` exits 2 silently: dropped by the critic: the only source is the CoS's account, no event or note shows it, and nothing lost reached the user.
- [chantier] A conflict-resolver pushed a branch itself against its card (CR-479): dropped: no work note or event shows it, one unproven occurrence with no cost.
- [chantier] (release) The release procedure says the tag is a main-checkout step but CI's tag-release job creates it: dropped: it happened once and cost nothing ("no just tag needed").
- [project] (release) The version push heavy run takes about 17 minutes with integration last: dropped: its own author says there is nothing to fix.
- [chantier] The watcher ends after 2 h without an event and the board stops with it: merged into the serve/junction point (same result for the user, same component).
