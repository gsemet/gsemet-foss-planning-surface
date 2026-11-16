# Answers

Grill of 2026-11-06, with the user.

- **Detecting a Remote Control view:** no detection; the toggle's reply states the limit every time.
  The first answer was a throwaway probe of `e.origin.kind`. It could not load: the question that
  turns on the mods did not reach the Mac. The session's transcript then showed every message of the
  user as `promptSource: "sdk"`, the Mac's included, and no `bridge`, so `bridge` probably would not
  catch this case. That is an indication from the transcript, not a reading of `e.origin`.
- **The toggle from a Remote Control view:** it opens or closes the pane on the host as usual, and
  its reply says the pane is on the machine running the session.
- **`immediate: true`:** yes, in this CR; check that it holds on the Remote Control path.
- **README:** one sentence in the board's section, with a link to anthropics/claude-code#99217.
