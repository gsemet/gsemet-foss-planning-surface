# Board: one fingerprint walk per project per pass

From the code audit of 2026-11-21 (priority 3, measured): while a board page is open, the server walks each project's planning folder several times per 2-second pass (0.65 to 1 s of work per pass). Intent: one walk per project per pass, so an open page costs a fraction of that, with no change seen to come later than today.
