# Before / after

No screenshot captured. Pair: the Configuration page, Models tab, base 33a2305 vs head 5041a0c.
Why: the board is a server and the Verifier may not run a background shell, so the page could not be served and opened at the same time.
To reproduce: `chantier board` against a scratch planning folder, open Configuration, Models tab; with the head, each role shows a grey description under its name.
