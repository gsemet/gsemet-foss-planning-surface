# Release 1.10.0: retro

The publication path ran green end to end: no re-run, no recovery dispatch, both registries served
at the first poll. What cost time or nearly did:

- [project] `CONTRIBUTING.md` "How to Release" step 3 amends the version commit with `-s`, which
  contradicts the release guideline (no `Signed-off-by` on the version commit); an agent following
  CONTRIBUTING.md alone adds the trailer: drop `-s` from that command in a docs fix CR, so the two
  documents give the same command.
- [chantier] The release spanned two Drivers: the first handed back at the version PR and a second
  was started after the owner's merge, re-reading the startup core, the cards and the release
  guideline (about 45k tokens before the first useful command) to watch a run that needs no
  decision: let `handoff` of a release CR print the procedure's remaining steps and their commands,
  so a resumed Release Driver reads only the steps after the merge.
- [chantier] The version push's CI takes about 17 minutes, past the Driver's 10-minute lease, and
  the release run is a separate dispatch found only once CI ends: name in the Release driver
  section that the post-merge watch is one `lease hold -- gh run watch <run>` per run (version push,
  then the dispatched release run), so no Driver polls or lets its lease lapse.
- [chantier] CI artifacts and downloads under `work/` (outside `work/scratch/`) make paths too long
  for the surface writer on Windows; the rule lived only in the steering session's take note: put
  it in the Driver card's "Means: context and your folder".
