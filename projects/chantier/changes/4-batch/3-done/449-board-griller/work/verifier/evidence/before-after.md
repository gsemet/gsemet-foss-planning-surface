# Before / after (CR-449, web client's Grill button and panel)

Before (base 5569703b28fc0dd9a3f33330f02ddd261c3d8071): no Grill button exists (the diff adds `js/panel/griller*.js`); not captured, no look-alike.
After (head fb80d194ac27eb8f6f85bf438e2719fd94bdf62a), Chrome 157 headless driven over the DevTools protocol, board on a scratch planning surface, the engine's griller_standin.py as the host (no real Claude):

- en-1-grill-button.png: the Grill button in the head of an inbox item's panel.
- en-2-panel-notice.png: the panel open before the first message (notice, shared note, HTTP note, Send and End).
- en-3-panel-turn.png: one turn round-tripped (typed text, the stand-in's answer, "Written: 02-answers.md").
- fr-1-grill-button.png: the button in French ("Griller").
- fr-2-panel-notice.png: the French panel and notice.

The stand-in's answer printed the scratch path; the page text was rewritten to made-up paths before each capture (home folder and username are not on screen). The machine name `battlestation` is shown by the notice; it is neither the username nor a path. Reproduce: start `chantier board` on a scratch surface with `griller.command` replaced by the stand-in, open `?v=kanban&lang=en`, click the card, then Grill.
