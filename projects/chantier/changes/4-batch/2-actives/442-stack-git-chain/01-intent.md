# An ordered stack is checked as a git chain

Intent: in an ordered (stack) batch, each CR's branch is based on the previous CR's head, and chantier checks it, so a stack whose forge bases are linear but whose git branches are cut from main is caught at `ship`, not after restacks that void gates and verdicts. From Studio's batch-07 retro (see `intake/`). Not grilled yet.
